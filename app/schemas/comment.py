"""
Comment Pydantic schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
    author_id: int


class CommentUpdate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)


class Comment(BaseModel):
    id: int
    content: str
    task_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
