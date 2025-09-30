"""
Task Pydantic schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    """Base task schema"""
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    priority: str = "medium"
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    owner_id: int


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class Task(TaskBase):
    """Schema for task response"""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
