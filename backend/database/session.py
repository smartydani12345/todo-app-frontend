from sqlmodel import Session
from sqlalchemy.orm import sessionmaker
from .init_db import engine  # Import engine from init_db to avoid duplication
from typing import Generator

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()