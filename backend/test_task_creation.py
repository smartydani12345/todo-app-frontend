#!/usr/bin/env python3
"""Test script to verify Task model creation works properly"""

import os
from sqlmodel import SQLModel, create_engine, Session
from database.models import Task
from database.session import get_session

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app_test.db")
print(f"Using database URL: {DATABASE_URL}")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create tables
SQLModel.metadata.create_all(bind=engine)
print("Tables created successfully!")

# Test creating a task without specifying ID
with Session(engine) as session:
    new_task = Task(
        title="Test Task",
        description="Test Description",
        priority="high",
        user_id="test-user-id",
    )

    print(f"Created task object: {new_task}")
    print(f"Task ID before commit: {new_task.id}")

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    print(f"Task ID after commit: {new_task.id}")
    print(f"Task created successfully: {new_task.title}")

print("Test completed successfully!")