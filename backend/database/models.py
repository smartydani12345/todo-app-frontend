from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import CheckConstraint
from models.task import TaskBase  # Import the validated base

# Note: The User model has been moved to models/user.py
# This file now contains all models for database operations

class Task(TaskBase, table=True):
    __tablename__ = "tasks"  # Explicit table name
    id: Optional[int] = Field(default=None, primary_key=True)  # Integer ID for database
    user_id: str = Field(sa_column_kwargs={"nullable": False})  # This comes from JWT token
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Import all models for Alembic to recognize them
# These imports are kept at the bottom to avoid circular imports
from models.user import User  # Import user model
from models.chat import Conversation, Message, ConversationStatus  # Import new chat models

__all__ = ["Task", "User", "Conversation", "Message", "ConversationStatus"]
