from fastapi import HTTPException
from models.users_model import User
from models.login_model import refresh_token_request
from utilities.login_utilities import create_access_token, create_refresh_token, verify_token, authenticate_user


class LoginController:
    """Handles user authentication and token generation."""

    @staticmethod
    async def login_for_token(username: str, password: str) -> dict:
        """
        Authenticates user credentials and generates access and refresh tokens.

        Args:
            username (str): Username for authentication.
            password (str): Password for authentication.

        Returns:
            dict: Dictionary containing access and refresh tokens.

        Raises:
            HTTPException: Raises 422 for missing fields and 401 for invalid credentials.
        """
        if not username:
            raise HTTPException(status_code=422, detail="Please enter a username.")
        if not password:
            raise HTTPException(status_code=422, detail="Please enter a password.")
        
        user = User(username=username, password=password).model_dump()
        user_data = await authenticate_user(user["username"], user["password"])

        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid Credentials")

        access_token = await create_access_token(data={"sub": user["username"]})
        refresh_token = await create_refresh_token(data={"sub": user["username"]})

        return {"access_token": access_token, "refresh_token": refresh_token}


class RefreshTokenController:
    """Handles access token refresh using a valid refresh token."""

    @staticmethod
    async def refresh_access_token(refresh_token: str) -> dict:
        """
        Verifies refresh token and generates a new access token.

        Args:
            refresh_token (str): The user's refresh token for verification.

        Returns:
            dict: Dictionary containing the new access token.

        Raises:
            HTTPException: Raises 401 for invalid or expired refresh token.
        """
        refresh_tkn = refresh_token_request(refresh_token=refresh_token).model_dump()
        payload = await verify_token(refresh_tkn["refresh_token"])

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or Expired refresh token")
        new_access_token = await create_access_token(data={"sub": payload["sub"]})

        return {"access_token": new_access_token}