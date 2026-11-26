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

    def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        project_id: Optional[int] = None,
        include_deleted: bool = False,
    ) -> List[Task]:
        return self.task_repository.get_tasks(
            skip=skip,
            limit=limit,
            project_id=project_id,
            include_deleted=include_deleted,
        )

    def get_task(self, task_id: int, include_deleted: bool = False) -> Optional[Task]:
        return self.task_repository.get_task(task_id, include_deleted=include_deleted)

    def get_tasks_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> List[Task]:
        return self.task_repository.get_tasks_by_user(
            user_id,
            skip=skip,
            limit=limit,
            include_deleted=include_deleted,
        )

    def _sync_completion_fields(self, payload: dict) -> dict:
        data = dict(payload)

        if "status" in data and data["status"] is not None:
            status = data["status"]
            data["is_completed"] = status == "done"
            return data

        if "is_completed" in data and data["is_completed"] is not None:
            data["status"] = "done" if data["is_completed"] else "todo"

        return data

    def create_task(self, task: TaskCreate) -> Task:
        payload = self._sync_completion_fields(task.model_dump())
        synced = TaskCreate(**payload)
        return self.task_repository.create_task(synced)

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        payload = self._sync_completion_fields(
            task_update.model_dump(exclude_unset=True)
        )
        synced = TaskUpdate(**payload)
        return self.task_repository.update_task(task_id, synced)

    def delete_task(self, task_id: int) -> bool:
        return self.task_repository.soft_delete_task(task_id)
