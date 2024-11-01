from fastapi import APIRouter, Form, Depends
from controller.login_controller import LoginController, RefreshTokenController
from utilities.utils import handle_exception
from fastapi.security import OAuth2PasswordBearer

# Initialize router
app = APIRouter()
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login", summary="Authenticate user and issue tokens")
@handle_exception
async def login_for_token(username: str = Form(...), password: str = Form(...)) -> dict:
    """
    API endpoint to authenticate user and issue JWT tokens.
    """
    return await LoginController.login_for_token(username, password)


@app.post("/refresh", summary="Refresh access token")
@handle_exception
async def refresh_access_token(refresh_token: str = Form(...)) -> dict:
    """
    API endpoint to refresh access token using a refresh token.
    """
    return await RefreshTokenController.refresh_access_token(refresh_token)
