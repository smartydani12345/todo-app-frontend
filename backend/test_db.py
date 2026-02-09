#!/usr/bin/env python3
"""Test script to verify database table creation"""

import os
from sqlmodel import SQLModel, create_engine, text
from database.init_db import create_db_and_tables
from database.models import Task
from models.user import User

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
print(f"Using database URL: {DATABASE_URL}")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Test connection and table creation
try:
    print("Creating database tables...")
    create_db_and_tables()
    print("Tables created successfully!")

    # Check if tables exist
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result.fetchall()]
        print(f"Existing tables: {tables}")

        if 'user' in tables:
            print("User table exists")
        else:
            print("User table does NOT exist")

        if 'task' in tables:
            print("Task table exists")
        else:
            print("Task table does NOT exist")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()