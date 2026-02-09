from sqlmodel import Session, select
from sqlalchemy.orm import sessionmaker
from models.user import User, UserCreate
from auth.utils import hash_password, verify_password
from typing import Optional
from datetime import datetime

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get a user by email"""
    statement = select(User).where(User.email == email)
    # Use the SQLAlchemy way which is compatible with current setup
    result = session.execute(statement)
    user = result.scalar_one_or_none()
    return user

def create_user(session: Session, user_create: UserCreate, name: str) -> User:
    """Create a new user"""
    hashed_password = hash_password(user_create.password)

    # Set timestamps explicitly
    current_time = datetime.utcnow()

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

    if not verify_password(password, user.password_hash):
        return None

    return user