"""
Task database model
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Task(Base):
    """Task model"""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    status = Column(String, default="todo", index=True)  # todo, in_progress, done
    priority = Column(String, default="medium")  # low, medium, high
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True, index=True)

    owner = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
