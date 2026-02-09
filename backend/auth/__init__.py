from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlmodel import Session
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer

from models.user import UserCreate, UserResponse
from auth.services import create_user, authenticate_user, get_user_by_email
from auth.utils import create_access_token, verify_token
from database.session import get_session

router = APIRouter(prefix="/auth", tags=["auth"])

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register")
async def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    """Register a new user"""
    # Create user create object from form data
    user_create = UserCreate(name=name, email=email, password=password)

    # Check if user already exists
    existing_user = get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    db_user = create_user(session, user_create, name)

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.id, "email": db_user.email},
        expires_delta=access_token_expires
    )

    # Return user info and token
    user_response = UserResponse(
        id=db_user.id,
        email=db_user.email,
        created_at=db_user.created_at.isoformat()
    )

    return {"user": user_response, "access_token": access_token, "token_type": "bearer"}


@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    """Login a user"""
    user = authenticate_user(session, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


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

    # Get user from database
    user = get_user_by_email(session, email)
    if user is None:
        raise credentials_exception

    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at.isoformat()
    )