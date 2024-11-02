from fastapi import HTTPException,Depends,Request
from models.users_model import User
from models.login_model import refresh_token_request
from models.users_model import User
from utilities.login_utilities import create_access_token, create_refresh_token, verify_token, authenticate_user,save_refresh_token,is_token_revoked,revoke_refresh_token,pwd_context,OAuth2PasswordRequestForm,OAuth2_scheme


class LoginController:
    """Handles user authentication and token generation."""

    @staticmethod
    async def login_for_token(user :OAuth2PasswordRequestForm= Depends() ) -> dict:
        """
        Authenticates user credentials and generates access and refresh tokens and stores the refresh tokens into the database.

        Args:
            username (str): Username for authentication.
            password (str): Password for authentication.

        Returns:
            dict: Dictionary containing access and refresh tokens.

        Raises:
            HTTPException: Raises 422 for missing fields and 401 for invalid credentials.
        """
        if not user.username:
            raise HTTPException(status_code=422, detail="Please enter a username.")
        if not user.password:
            raise HTTPException(status_code=422, detail="Please enter a password.")
        
       
        user_data = await authenticate_user(user.username, user.password)

        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid Credentials")

        access_token = create_access_token(data={"sub": user.username})
        refresh_token = create_refresh_token(data={"sub": user.username})
        #stores the refresh_token into the database
        await save_refresh_token(user.username,refresh_token)

        return {"access_token": access_token, "refresh_token": refresh_token}


class RefreshTokenController:
    """Handles access token refresh using a valid refresh token."""

    @staticmethod
    async def refresh_access_token(refresh_token: str = Depends(OAuth2_scheme)) -> dict:
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
        payload = verify_token(refresh_tkn["refresh_token"])

        if not payload or await is_token_revoked(refresh_tkn["refresh_token"]):
            raise HTTPException(status_code=401, detail="Invalid or Expired refresh token")
        new_access_token =  create_access_token(data={"sub": payload["sub"]})

        return {"access_token": new_access_token}
    
class LogoutController:

    @staticmethod
    async def logout(refresh_token : str = Depends(OAuth2_scheme)):
        
        """
    Logs out the user by revoking the provided refresh token, preventing further use for obtaining new access tokens.

    This function handles the process of marking the provided refresh token as revoked in the database. It ensures
    that the token cannot be used again, effectively ending the user's session.

    Args:
        refresh_token (str): The refresh token provided by the user for revocation.

    Returns:
        dict: A response message indicating that the user was logged out successfully.

    Raises:
        HTTPException: If the revocation process fails, raises an HTTP exception with:
            - status_code 400: Indicates that the token could not be revoked successfully.
    """

        if await revoke_refresh_token(refresh_token):
            return {"detail":"User logged out successfully."}
        raise HTTPException(
            status_code=400,
            detail = "Failed to revoke the refresh token."
        )
class protected_users:
    @staticmethod
    async def protected_routes(request:Request):
        return {"message":"you have access to this protected route."}
