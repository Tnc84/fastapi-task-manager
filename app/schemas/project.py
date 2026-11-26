"""
Project Pydantic schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: Optional[str] = None
    key: str = Field(min_length=2, max_length=10)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    description: Optional[str] = None
    key: Optional[str] = Field(default=None, min_length=2, max_length=10)


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
