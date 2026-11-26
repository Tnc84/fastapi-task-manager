"""
Task repository for database operations
"""

from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    """Task repository for database operations"""

    def __init__(self, db: Session):
        self.db = db

    def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        project_id: int | None = None,
        include_deleted: bool = False,
    ) -> List[Task]:
        """Get tasks with pagination and optional project filter"""
        query = self.db.query(Task)
        if not include_deleted:
            query = query.filter(Task.deleted_at.is_(None))
        if project_id is not None:
            query = query.filter(Task.project_id == project_id)
        return query.offset(skip).limit(limit).all()

    def get_task(self, task_id: int, include_deleted: bool = False) -> Optional[Task]:
        """Get task by ID"""
        query = self.db.query(Task).filter(Task.id == task_id)
        if not include_deleted:
            query = query.filter(Task.deleted_at.is_(None))
        return query.first()

    def get_tasks_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> List[Task]:
        """Get tasks by user ID"""
        query = self.db.query(Task).filter(Task.owner_id == user_id)
        if not include_deleted:
            query = query.filter(Task.deleted_at.is_(None))
        return query.offset(skip).limit(limit).all()

    def create_task(self, task: TaskCreate) -> Task:
        """Create a new task"""
        payload = task.model_dump() if hasattr(task, "model_dump") else task.dict()
        db_task = Task(**payload)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """Update an existing task"""
        db_task = self.get_task(task_id)
        if not db_task:
            return None

        update_data = (
            task_update.model_dump(exclude_unset=True)
            if hasattr(task_update, "model_dump")
            else task_update.dict(exclude_unset=True)
        )
        for field, value in update_data.items():
            setattr(db_task, field, value)

        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def soft_delete_task(self, task_id: int) -> bool:
        """Soft delete a task"""
        db_task = self.get_task(task_id, include_deleted=False)
        if not db_task:
            return False

        db_task.deleted_at = datetime.now(timezone.utc)
        self.db.commit()
        return True
