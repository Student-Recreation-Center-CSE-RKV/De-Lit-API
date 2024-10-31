from fastapi import HTTPException,status
from datetime import datetime , timedelta
from jose import jwt,JWTError,ExpiredSignatureError
from models.users_model import User
from utilities.utils import client
from passlib.context import CryptContext

my_db = client['Delit-test']
login_db = my_db.logins
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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




async def verify_token(token : str):
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

    return pwd_context.verify(plain_password,hashed_password)


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
    user_data = User(**user).model_dump()
    if user and verify_password(password,user_data["password"]) :
        return user_data
    return None
