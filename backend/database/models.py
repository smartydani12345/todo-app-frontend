from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from models.task import TaskBase  # Import the validated base

# Note: The User model has been moved to models/user.py
# This file now only contains the Task model

class Task(TaskBase, table=True):
    __tablename__ = "tasks"  # Explicit table name
    id: Optional[int] = Field(default=None, primary_key=True)  # Integer ID for database
    user_id: str = Field(sa_column_kwargs={"nullable": False})  # This comes from JWT token
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
