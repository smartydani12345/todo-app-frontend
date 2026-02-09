from fastapi import Request, HTTPException, status
from .jwt import verify_token
from functools import wraps
import inspect

def require_auth(request: Request):
    """
    Middleware function to require authentication.
    Validates JWT token from Authorization header.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid"
        )

    token = auth_header.split(" ")[1]
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: no user_id found"
            )

        # Add user info to request state
        request.state.user = {
            "user_id": user_id,
            "email": payload.get("email", ""),
            "name": payload.get("name", "")
        }
        return request.state.user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}"
        )

def verify_user_isolation(user_id_from_token: str, user_id_from_request: str):
    """
    Verify that the authenticated user can only access their own resources.
    """
    if user_id_from_token != user_id_from_request:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access resources owned by other users"
        )