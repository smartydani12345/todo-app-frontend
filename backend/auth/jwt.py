import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime, timedelta
from typing import Optional
import os
from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from database.session import get_session

# Get secret from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_for_dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

security = HTTPBearer()

def verify_token(token: str) -> dict:
    """Verify JWT token and return decoded payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> dict:
    """
    Dependency to get current user from JWT token.
    Returns user info from token (user_id).
    """
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Return user info from token (Better Auth manages users externally)
    return {
        "user_id": user_id,
        "email": payload.get("email", ""),
        "name": payload.get("name", "")
    }

def get_current_user_id(
    current_user: dict = Depends(get_current_user)
) -> str:
    """
    Dependency to get just the user ID from JWT token.
    """
    return current_user["user_id"]

def verify_user_access(
    user_id_from_token: str,
    user_id_from_request: str
) -> bool:
    """
    Verify that the user in the token matches the requested resource.
    This ensures user isolation.
    """
    return user_id_from_token == user_id_from_request