from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class ConversationStatus(str, Enum):
    active = "active"
    archived = "archived"
    deleted = "deleted"

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: Optional[str] = Field(default=None, max_length=200)
    language: str = Field(default="en", max_length=20)
    status: ConversationStatus = Field(default=ConversationStatus.active)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # Will be 'user' or 'assistant'
    content: str = Field(max_length=10000)
    language: str = Field(max_length=20)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tools_used: Optional[str] = Field(default=None)  # JSON string of tools used
    parent_message_id: Optional[int] = Field(default=None, foreign_key="messages.id")  # For threaded conversations