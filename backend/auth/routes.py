from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database.init_db import get_session
from database.models import User

router = APIRouter()

@router.post("/api/auth/register")
def register(name: str, email: str, password: str, session: Session = Depends(get_session)):
    # Check if user already exists
    user_exists = session.exec(select(User).where(User.email == email)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(name=name, email=email, password=password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"user_id": new_user.id}

@router.post("/api/auth/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    # Find user by email and password
    user = session.exec(select(User).where(User.email == email, User.password == password)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"user_id": user.id, "name": user.name}