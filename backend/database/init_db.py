from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine with appropriate settings
if 'neon' in DATABASE_URL or 'postgresql' in DATABASE_URL:
    engine = create_engine(DATABASE_URL, echo=False, connect_args={"sslmode": "require"})
else:
    engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

def get_session():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    """Create database tables on startup"""
    # Import all models to ensure they're registered with SQLModel metadata
    from models.user import User
    from database.models import Task
    from models.chat import Conversation, Message
    
    # Create all tables
    SQLModel.metadata.create_all(bind=engine)
    
    # Handle schema migration for User table (add password_hash column if missing)
    try:
        with engine.connect() as conn:
            if 'postgresql' in DATABASE_URL:
                # Check if password_hash column exists
                result = conn.execute(text("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = 'password_hash'
                """))
                if not result.fetchone():
                    # Add password_hash column
                    conn.execute(text("""
                        ALTER TABLE users ADD COLUMN password_hash VARCHAR
                    """))
                    # Copy password to password_hash if password column exists
                    result = conn.execute(text("""
                        SELECT column_name FROM information_schema.columns 
                        WHERE table_name = 'users' AND column_name = 'password'
                    """))
                    if result.fetchone():
                        conn.execute(text("""
                            UPDATE users SET password_hash = password WHERE password_hash IS NULL
                        """))
                    conn.commit()
    except Exception as e:
        print(f"Schema migration note: {e}")
