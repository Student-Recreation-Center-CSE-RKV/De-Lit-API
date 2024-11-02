from fastapi import Request,HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from utilities.login_utilities import verify_token
from typing import Callable

class JWTMiddleware(BaseHTTPMiddleware):
    
    """
    Middleware for handling JWT authentication in FastAPI.

    This middleware intercepts incoming requests to extract and validate JWT
    tokens from the Authorization header. If the token is valid, the user 
    information from the token payload is attached to the request state for 
    access in downstream endpoints. If the token is missing or invalid, 
    an appropriate HTTP exception is raised.
    """
    async def dispatch(self, request: Request, call_next:Callable):

        """
        Processes the incoming request, extracting and validating the JWT token 
        from the Authorization header.

        Args:
            request (Request): The incoming HTTP request object.
            call_next (Callable): A function to call the next middleware or 
                                  endpoint in the request/response cycle.

        Returns:
            Response: The HTTP response returned from the next middleware or 
                       endpoint.

        Raises:
            HTTPException: Raises 403 if the authorization header is invalid 
                           or the token is invalid/expired.
            HTTPException: Raises 401 if the authorization header is missing.
        """
        public_routes = ["/login/protected"]

        if request.url.path not in public_routes:
            response = await call_next(request)
            return response
        # Retrieve the Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header:
            # Check if the header follows the "Bearer <token>" format
            try:
                scheme, token = auth_header.split()
                if scheme.lower() != "bearer":
                    raise ValueError("Invalid auth scheme")
            except ValueError:
                raise HTTPException(status_code=403, detail="Invalid authorization header")

            # Validate and decode the JWT token
            payload = verify_token(token)
            if payload is None:
                raise HTTPException(status_code=403, detail="Invalid or expired token")

            # Attach user info to request state for access in endpoints
            request.state.user = payload  # Save payload info for later use
        else:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        # Allow request to proceed
        response = await call_next(request)
        return response