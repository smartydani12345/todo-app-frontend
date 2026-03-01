"""Test script to debug auth issues"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"JWT_SECRET: {os.getenv('JWT_SECRET')[:10]}...")

from database.init_db import engine, create_db_and_tables, SessionLocal
from sqlmodel import Session, select
from models.user import User
from auth.utils import hash_password

# Create tables
print("\nCreating tables...")
create_db_and_tables()

# Test database connection
print("\nTesting database connection...")
try:
    with SessionLocal() as session:
        # Try to query users
        users = session.exec(select(User)).all()
        print(f"Found {len(users)} users")
        
        # Check User model fields
        print(f"\nUser model fields: {User.__fields__.keys() if hasattr(User, '__fields__') else 'N/A'}")
        
        # Try to create a new user
        print("\nCreating test user...")
        hashed_pw = hash_password("test123")
        new_user = User(
            name="Test User",
            email="debug@example.com",
            password_hash=hashed_pw
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print(f"Created user: {new_user.id}, {new_user.email}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
