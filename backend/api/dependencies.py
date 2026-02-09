from fastapi import Depends, HTTPException, status, Header
from sqlmodel import Session

from auth.utils import verify_token
from auth.services import get_user_by_email
from database.session import get_session
from models.user import UserResponse


def get_current_user(authorization: str = Header(None), session: Session = Depends(get_session)) -> UserResponse:
    """Get current authenticated user from token"""
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract token from "Bearer <token>" format
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[7:]  # Remove "Bearer " prefix

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("email")
    if email is None:
        raise credentials_exception

    # Get user from database
    user = get_user_by_email(session, email)
    if user is None:
        raise credentials_exception

    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )


# Alternative approach - extract user ID directly
def get_current_user_id(authorization: str = Header(None), session: Session = Depends(get_session)) -> str:
    """Get current authenticated user ID from token"""
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract token from "Bearer <token>" format
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[7:]  # Remove "Bearer " prefix

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")  # "sub" is the subject (user ID) in JWT
    if user_id is None:
        raise credentials_exception

    return user_id