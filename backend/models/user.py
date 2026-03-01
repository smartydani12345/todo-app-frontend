from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime, timezone
from typing import Optional

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def generate_uuid() -> str:
    return str(uuid.uuid4())

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    # Chatbot-specific fields
    preferred_language: str = "en"
    voice_preference: str = "none"
    chatbot_enabled: bool = True

    def __init__(self, **kwargs):
        if 'id' not in kwargs or kwargs['id'] is None:
            kwargs['id'] = generate_uuid()
        if 'created_at' not in kwargs or kwargs['created_at'] is None:
            kwargs['created_at'] = utc_now()
        if 'updated_at' not in kwargs or kwargs['updated_at'] is None:
            kwargs['updated_at'] = utc_now()
        super().__init__(**kwargs)

class UserCreate(SQLModel):
    name: str
    email: str
    password: str

class UserResponse(SQLModel):
    id: str
    email: str
    name: str
    created_at: str

    class Config:
        from_attributes = True
