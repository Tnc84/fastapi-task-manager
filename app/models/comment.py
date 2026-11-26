"""
Comment database model
"""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Comment(Base):
    """Comment on a task"""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments")
