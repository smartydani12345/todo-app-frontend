from sqlmodel import SQLModel, Field
from typing import Optional, List
import uuid
from datetime import datetime
from pydantic import field_validator
import json

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", max_length=20)
    tags: Optional[str] = Field(default='[]', max_length=2000)  # Store as JSON string
    due_date: Optional[datetime] = Field(default=None)

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        if v not in ['high', 'medium', 'low']:
            raise ValueError('priority must be high, medium, or low')
        return v

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        if v is None or v == '':
            return '[]'  # Return empty array as string if None or empty
        # If it's a list, convert to JSON string
        if isinstance(v, list):
            if len(v) > 10:
                raise ValueError('Maximum 10 tags allowed')
            for tag in v:
                if len(tag) > 50:
                    raise ValueError('Each tag must be 50 characters or less')
            return json.dumps(v)
        # If it's already a string, validate it
        elif isinstance(v, str):
            if v.strip() == '':  # If string is just whitespace, return empty array
                return '[]'
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    if len(parsed) > 10:
                        raise ValueError('Maximum 10 tags allowed')
                    for tag in parsed:
                        if len(tag) > 50:
                            raise ValueError('Each tag must be 50 characters or less')
            except json.JSONDecodeError:
                # If it's not valid JSON, treat it as comma-separated tags
                tags_list = [tag.strip() for tag in v.split(',') if tag.strip()]
                if len(tags_list) > 10:
                    raise ValueError('Maximum 10 tags allowed')
                for tag in tags_list:
                    if len(tag) > 50:
                        raise ValueError('Each tag must be 50 characters or less')
                return json.dumps(tags_list)
            return v
        else:
            raise ValueError('Tags must be a list or JSON string')


class TaskCreate(TaskBase):
    title: str
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None  # Stored as JSON string
    due_date: Optional[datetime] = None

class TaskPublic(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime