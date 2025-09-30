"""
Task service layer
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.repositories.task_repository import TaskRepository


class TaskService:
    """Task service for business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db)
    
    async def get_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks with pagination"""
        return await self.task_repository.get_tasks(skip=skip, limit=limit)
    
    async def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        return await self.task_repository.get_task(task_id)
    
    async def get_tasks_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get tasks by user ID"""
        return await self.task_repository.get_tasks_by_user(user_id, skip=skip, limit=limit)
    
    async def create_task(self, task: TaskCreate) -> Task:
        """Create a new task"""
        return await self.task_repository.create_task(task)
    
    async def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """Update an existing task"""
        return await self.task_repository.update_task(task_id, task_update)
    
    async def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        return await self.task_repository.delete_task(task_id)
