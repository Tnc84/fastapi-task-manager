"""
Task management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_admin, resolve_include_deleted
from app.models.user import User
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/", response_model=List[Task])
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    db: Session = Depends(get_db),
    include_deleted: bool = Depends(resolve_include_deleted),
):
    """Get all tasks with pagination and optional project filter"""
    task_service = TaskService(db)
    return task_service.get_tasks(
        skip=skip,
        limit=limit,
        project_id=project_id,
        include_deleted=include_deleted,
    )


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    include_deleted: bool = Depends(resolve_include_deleted),
):
    """Get a specific task by ID"""
    task_service = TaskService(db)
    task = task_service.get_task(task_id, include_deleted=include_deleted)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    """Create a new task"""
    task_service = TaskService(db)
    return task_service.create_task(task)


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing task"""
    task_service = TaskService(db)
    task = task_service.update_task(task_id, task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Soft delete a task (admin only)"""
    task_service = TaskService(db)
    success = task_service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
