"""
Task repository for database operations
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    """Task repository for database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks with pagination"""
        return self.db.query(Task).offset(skip).limit(limit).all()
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def get_tasks_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks by user ID"""
        return (
            self.db.query(Task)
            .filter(Task.owner_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_task(self, task: TaskCreate) -> Task:
        """Create a new task"""
        db_task = Task(**task.dict())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task
    
    def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """Update an existing task"""
        db_task = self.get_task(task_id)
        if not db_task:
            return None
        
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        
        self.db.commit()
        self.db.refresh(db_task)
        return db_task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        db_task = self.get_task(task_id)
        if not db_task:
            return False
        
        self.db.delete(db_task)
        self.db.commit()
        return True
