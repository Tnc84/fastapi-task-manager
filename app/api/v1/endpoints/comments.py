"""
Task comments endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.comment import Comment, CommentCreate, CommentUpdate
from app.services.comment_service import CommentService

router = APIRouter()


@router.get("/{task_id}/comments", response_model=List[Comment])
def get_task_comments(task_id: int, db: Session = Depends(get_db)):
    comments = CommentService(db).get_comments_for_task(task_id)
    if comments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return comments


@router.post(
    "/{task_id}/comments",
    response_model=Comment,
    status_code=status.HTTP_201_CREATED,
)
def create_task_comment(
    task_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
):
    created = CommentService(db).create_comment(task_id, comment)
    if created is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return created


@router.put("/{task_id}/comments/{comment_id}", response_model=Comment)
def update_task_comment(
    task_id: int,
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
):
    service = CommentService(db)
    comments = service.get_comments_for_task(task_id)
    if comments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updated = service.update_comment(comment_id, comment_update)
    if not updated or updated.task_id != task_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return updated


@router.delete("/{task_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_comment(task_id: int, comment_id: int, db: Session = Depends(get_db)):
    service = CommentService(db)
    comments = service.get_comments_for_task(task_id)
    if comments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    existing = next((c for c in comments if c.id == comment_id), None)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    service.delete_comment(comment_id)
