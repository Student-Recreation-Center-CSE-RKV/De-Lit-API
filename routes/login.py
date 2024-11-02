from fastapi import APIRouter, Form, Depends,Request
from controller.login_controller import LoginController, RefreshTokenController,LogoutController,protected_users
from utilities.utils import handle_exception
from utilities.login_utilities import OAuth2_scheme,OAuth2PasswordRequestForm
from models.users_model import User

# Initialize router
app = APIRouter()


@app.post("/login", summary="Authenticate user and issue tokens")
@handle_exception
async def login_for_token(user:OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    API endpoint to authenticate user and issue JWT tokens.
    """
    return await LoginController.login_for_token(user)


@app.post("/refresh", summary="Refresh access token")
@handle_exception
async def refresh_access_token(refresh_token: str = Depends(OAuth2_scheme)) -> dict:
    """
    API endpoint to refresh access token using a refresh token.
    """
    return await RefreshTokenController.refresh_access_token(refresh_token)

@app.post("/logout",summary="Revokes the refresh token")
@handle_exception
async def logout(refresh_token : str = Depends(OAuth2_scheme)) -> dict :

    """
    API endpoint to revoke the refresh token
    """
    return await LogoutController.logout(refresh_token)


@app.get("/protected",summary = "Protected routes only for admins")
@handle_exception
async def protected_routes(request:Request):
    return await protected_users.protected_routes(request)
