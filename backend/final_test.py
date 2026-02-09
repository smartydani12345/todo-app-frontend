#!/usr/bin/env python3
"""Final test to verify the corrected Task model works properly"""

import os
from sqlmodel import SQLModel, create_engine, Session, Field
from typing import Optional
from datetime import datetime

# Define the correct Task model with integer ID
class Task(SQLModel, table=True):
    __tablename__ = "task"  # Explicitly set table name
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = None
    tags: Optional[str] = None  # comma separated
    due_date: Optional[datetime] = None
    user_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Get database URL
DATABASE_URL = "sqlite:///./final_test.db"
print(f"Using database URL: {DATABASE_URL}")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create tables - this will use only our defined model
SQLModel.metadata.create_all(bind=engine)
print("Tables created successfully!")

# Test creating a task without specifying ID
with Session(engine) as session:
    new_task = Task(
        title="Final Test Task",
        description="Final Test Description",
        priority="high",
        user_id="test-user-id",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    print(f"Created task object: {new_task}")
    print(f"Task ID before commit: {new_task.id}")

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    print(f"Task ID after commit: {new_task.id}")
    print(f"Task created successfully: {new_task.title}")

print("Final test completed successfully!")