from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"  # Use plural form for consistency

    id: str = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"nullable": False})
    email: str = Field(sa_column_kwargs={"unique": True, "index": True, "nullable": False})
    password_hash: str = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4())

class UserCreate(SQLModel):
    name: str
    email: str
    password: str

class UserResponse(SQLModel):
    id: str
    email: str
    created_at: str

    class Config:
        from_attributes = True