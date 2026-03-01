from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from models.chat import ConversationStatus


class ConversationCreate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=200)
    user_id: Optional[str] = None  # Will be set from authenticated user
    language: str = Field(default="en", max_length=20)  # Default language
    status: ConversationStatus = Field(default=ConversationStatus.active)


class ConversationUpdate(SQLModel):
    title: Optional[str] = None
    status: Optional[ConversationStatus] = None




class MessageCreate(SQLModel):
    conversation_id: int = Field(foreign_key="conversations.id")
    role: Optional[str] = None  # Will be set by the API (user or assistant)
    content: str = Field(max_length=10000)
    language: str = Field(default="en", max_length=20)
    tools_used: Optional[str] = Field(default=None)  # JSON string of tools used


class MessageUpdate(SQLModel):
    content: Optional[str] = None
    tools_used: Optional[str] = None
