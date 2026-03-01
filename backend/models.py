from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# Minimal Task model (Phase 2 compatible)
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(default="test-user")
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Minimal Conversation model (Phase 3)
class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(default="test-user")
    created_at: datetime = Field(default_factory=datetime.utcnow)
