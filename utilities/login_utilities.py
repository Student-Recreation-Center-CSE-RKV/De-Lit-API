from fastapi import HTTPException,status
from datetime import datetime , timedelta
from jose import jwt,JWTError,ExpiredSignatureError
from models.users_model import User
from models.login_model import token_revocation
from utilities.utils import client
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

my_db = client['Delit-test']
login_db = my_db.logins
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "DelitTest02606712"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_token(data : dict , expiry : timedelta):
    """
    Generates a JWT Token with an expiration.

    Args:
        data (dict): The payload data to encode in the token.
        expiry (timedelta): The duration after which the token will expire.

    Returns:
        str: The encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expiry
    to_encode.update({"exp":expire})
    return  jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


def create_access_token (data : dict):
    """Creates an AccessToken."""
    return  create_token(data,timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(data : dict):
    """Creates a RefreshToken"""

    return  create_token(data , timedelta(days = REFRESH_TOKEN_EXPIRE_DAYS))




def verify_token(token : str):
    "Decodes the token and verifies it and returns the payload if valid , else None"
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    

def verify_password(plain_password,hashed_password):
    """
    Verify a plain text password against a hashed password.

    This function compares the plain text password provided by the user
    with the hashed password stored in the database to determine if they
    match. It utilizes the passlib library's context to handle the 
    hashing algorithm and verification process.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password,
              False otherwise.
    """
    print(f"Verifying password: {plain_password} against hash: {hashed_password}")
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError as e:
        raise Exception("Hash could not be identified") from e


async def authenticate_user(username : str , password : str):
    
    """
    Authenticate a user by validating their credentials against the stored data.

    This function queries the database for the user's information using
    the provided username. If the user is found, it verifies the
    provided password against the stored hashed password. If both the
    username and password are valid, the user's data is returned.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The plain text password provided by the user.

    Returns:
        dict or None: Returns a dictionary containing the user's data
                      if authentication is successful, or None if
                      the username is not found or the password is incorrect.
    """
    user = await login_db.find_one({"username":username})
    if not user :
        raise HTTPException(
            status_code = 404,
            detail = "User not found."
        )
    user_data = User(**user).model_dump()
    if user and verify_password(password,user_data["password"]) :
        return user_data
    return None

async def save_refresh_token(username : str , refresh_token :str):

    """
    Saves a refresh token for a given user in the database.

    Args:
        username (str): The username associated with the refresh token.
        refresh_token (str): The refresh token to be saved.

    Returns:
        dict: The result of the database insertion, including the newly created token's ID.
    """

    #Create and instance of the token object
    save_token = token_revocation(
        username = username,
        token = refresh_token,
        expires_at = datetime.utcnow() + timedelta(days = REFRESH_TOKEN_EXPIRE_DAYS),
        revoked_status = False
    )
    
    save_token_data = save_token.model_dump()
    #Inserts the token into the database
    store_token = await login_db.insert_one(save_token_data)

    if not store_token.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to save the refresh token.")
    
    return {"status": "success", "token_id": str(store_token.inserted_id)}

async def is_token_revoked(refresh_token:str):

    """
    Checks whether a given refresh token has been revoked.

    Args:
        refresh_token (str): The refresh token to check.

    Returns:
        bool: True if the token is revoked, False otherwise.

    Raises:
        KeyError: If 'revoked_status' is not found in the retrieved token document.
        TypeError: If the token retrieval returns None (i.e., token not found in the database).
    """

    revoked_token = await login_db.find_one({"token":refresh_token})
    
    if revoked_token is None:
        raise TypeError("Token not found in the database.")

    if "revoked_status" not in revoked_token:
        raise KeyError("'revoked_status' key not found in the token document.")
    
    if revoked_token["revoked_status"] is True:
        return True
   
    return False

async def revoke_refresh_token(refresh_token):
     
     
    """
    Revokes a refresh token by updating its `revoked_status` to False in the database.

    Args:
        refresh_token (str): The refresh token to be revoked.

    Returns:
        bool: True if the token was successfully revoked, False otherwise.

    Raises:
        HTTPException: If the token cannot be found or the update fails.
    """
    revoke_token = await login_db.find_one({"token":refresh_token})

    if not revoke_token :
        raise HTTPException(
            status_code = 404,
            detail = "Token not found."
        )
    
    update_revoke_status = await login_db.update_one(
        {"token":refresh_token},
        {"$set":{"revoked_status":True}}
    )
    if update_revoke_status.modified_count == 0:
        raise HTTPException(
            status_code = 404,
            detail = "Failed to revoke the token."
        )
        
    return True
