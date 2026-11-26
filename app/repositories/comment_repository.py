"""
Comment repository
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_comments_for_task(self, task_id: int) -> List[Comment]:
        return (
            self.db.query(Comment)
            .filter(Comment.task_id == task_id)
            .order_by(Comment.created_at.asc())
            .all()
        )

    def get_comment(self, comment_id: int) -> Optional[Comment]:
        return self.db.query(Comment).filter(Comment.id == comment_id).first()

    def create_comment(self, task_id: int, comment: CommentCreate) -> Comment:
        payload = comment.model_dump() if hasattr(comment, "model_dump") else comment.dict()
        db_comment = Comment(task_id=task_id, **payload)
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment

    def update_comment(self, comment_id: int, comment_update: CommentUpdate) -> Optional[Comment]:
        db_comment = self.get_comment(comment_id)
        if not db_comment:
            return None
        payload = (
            comment_update.model_dump(exclude_unset=True)
            if hasattr(comment_update, "model_dump")
            else comment_update.dict(exclude_unset=True)
        )
        for field, value in payload.items():
            setattr(db_comment, field, value)
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment

    def delete_comment(self, comment_id: int) -> bool:
        db_comment = self.get_comment(comment_id)
        if not db_comment:
            return False
        self.db.delete(db_comment)
        self.db.commit()
        return True
