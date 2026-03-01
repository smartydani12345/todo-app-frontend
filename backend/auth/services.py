from sqlmodel import Session, select
from models.user import User, UserCreate
from auth.utils import hash_password, verify_password
from typing import Optional
from datetime import datetime, timezone

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get a user by email"""
    statement = select(User).where(User.email == email)
    result = session.execute(statement)
    user = result.scalar_one_or_none()
    return user

def create_user(session: Session, user_create: UserCreate, name: str) -> User:
    """Create a new user"""
    hashed_password = hash_password(user_create.password)
    current_time = utc_now()

    db_user = User(
        name=name,
        email=user_create.email,
        password_hash=hashed_password,
        created_at=current_time,
        updated_at=current_time
    )

    session.add(db_user)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(db_user)

    return db_user

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password"""
    user = get_user_by_email(session, email)
    if not user:
        return None

    # Try password_hash first (new users)
    if hasattr(user, 'password_hash') and user.password_hash:
        if verify_password(password, user.password_hash):
            return user
        return None

    # Fallback to password field (old users - plain text)
    if hasattr(user, 'password') and user.password:
        if password == user.password:
            # Upgrade to hashed password
            user.password_hash = hash_password(password)
            session.add(user)
            session.commit()
            return user
        return None

    return None
