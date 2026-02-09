from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})  # Added connect_args for SQLite

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    """Create database tables on startup"""
    from sqlmodel import SQLModel
    # Import all models to ensure they're registered with SQLModel metadata
    from models.user import User
    from database.models import Task
    SQLModel.metadata.create_all(bind=engine)