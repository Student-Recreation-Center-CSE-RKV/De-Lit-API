from fastapi import APIRouter,HTTPException,Form,Depends
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from models.users_model import User
from models.login_model import refresh_token_request
from utilities.utils import client,handle_exception
from utilities.login_utilities import create_access_token,create_refresh_token,verify_token,authenticate_user,login_db

app = APIRouter(tags=["Login"])
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login")
@handle_exception
async def login_for_token(username : str = Form(...),password : str = Form(...)):
     
    """
    Authenticates the user with the provided username and password, and issues JWT tokens upon successful authentication.

    This function checks the user's credentials against stored user data and, if valid, generates and returns an access token 
    and a refresh token for authenticated access to the API.

    Args:
        username (str): The username provided by the user, received from form data.
        password (str): The password provided by the user, received from form data.

    Returns:
        dict: A dictionary containing:
            - "access_token" (str): The JWT access token used for short-term authenticated access.
            - "refresh_token" (str): The JWT refresh token used to renew the access token after expiration.

    Raises:
        HTTPException: 
            - 422: If the username or password is empty or None, with a message prompting the user to enter valid values.
            - 401: If authentication fails, indicating invalid credentials.
    """
    if username == "" or username == None :
        raise HTTPException(
            status_code = 422,
            detail = "Please Enter username to create user."
        ) 
    
    if password == "" or password == None :
        raise HTTPException(
            status_code = 422,
            detail = "Please Enter Password to create user."
        )
    
    user = User(
        username = username,
        password = password
    )
    user = user.model_dump()
    user_data =await authenticate_user(user["username"],user["password"])
    if not user_data :
        raise HTTPException(
            status_code = 401,
            detail = "Invalid Credentials"
        )
    access_token =await  create_access_token(data = {"sub":user["username"]})
    refresh_token =await  create_refresh_token(data = {"sub":user["username"]})
    return {"access_token":access_token,
            "refresh_token":refresh_token}


@app.post("/refresh")
async def refresh_access_token(refresh_token : str = Form(...)):

    """
    Refreshes the access token using a valid refresh token.

    This function verifies the provided refresh token and, if valid, generates a new access token for the user. 
    If the refresh token is invalid or expired, an HTTP 401 Unauthorized exception is raised.

    Args:
        refresh_token (str): The refresh token required for generating a new access token. 
                             It is obtained from the OAuth2 dependency.

    Returns:
        dict: A dictionary containing the new access token.

    Raises:
        HTTPException: If the refresh token is invalid or expired, an HTTP 401 error is raised.

    """
    refresh_tkn = refresh_token_request(refresh_token=refresh_token)
    refresh_tkn = refresh_tkn.model_dump()

    
    payload =await verify_token(refresh_token)

    if not payload :
        raise HTTPException(
            status_code = 401,
            detail = "Invalid or Expired refresh token"
        )
    new_access_token = create_access_token(data = {"sub":payload["sub"]})

    return {"access_token":new_access_token}