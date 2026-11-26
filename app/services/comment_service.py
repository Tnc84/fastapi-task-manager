"""
Comment service
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate
from app.repositories.comment_repository import CommentRepository
from app.repositories.task_repository import TaskRepository


class CommentService:
    def __init__(self, db: Session):
        self.db = db
        self.comment_repository = CommentRepository(db)
        self.task_repository = TaskRepository(db)

    def get_comments_for_task(self, task_id: int) -> Optional[List[Comment]]:
        if not self.task_repository.get_task(task_id):
            return None
        return self.comment_repository.get_comments_for_task(task_id)

    def create_comment(self, task_id: int, comment: CommentCreate) -> Optional[Comment]:
        if not self.task_repository.get_task(task_id):
            return None
        return self.comment_repository.create_comment(task_id, comment)

    def update_comment(self, comment_id: int, comment_update: CommentUpdate) -> Optional[Comment]:
        return self.comment_repository.update_comment(comment_id, comment_update)

    def delete_comment(self, comment_id: int) -> bool:
        return self.comment_repository.delete_comment(comment_id)
