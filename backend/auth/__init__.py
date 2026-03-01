from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer

from models.user import UserCreate, UserResponse
from auth.services import create_user, authenticate_user, get_user_by_email
from auth.utils import create_access_token, verify_token
from database.session import get_session
import os

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


@router.post("/register")
async def register(
    request_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    """Register a new user and return JWT token"""
    name = request_data.get("name")
    email = request_data.get("email")
    password = request_data.get("password")
    
    if not name or not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name, email, and password are required"
        )

    user_create = UserCreate(name=name, email=email, password=password)

    existing_user = get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    db_user = create_user(session, user_create, name)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.id, "email": db_user.email, "name": db_user.name},
        expires_delta=access_token_expires
    )

    return {
        "user_id": db_user.id,
        "email": db_user.email,
        "name": db_user.name,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login")
async def login(
    request_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    """Login a user and return JWT token"""
    email = request_data.get("email")
    password = request_data.get("password")
    
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    user = authenticate_user(session, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name},
        expires_delta=access_token_expires
    )

    return {
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """Get current logged-in user info"""
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

    user = get_user_by_email(session, email)
    if user is None:
        raise credentials_exception

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at.isoformat()
    )
