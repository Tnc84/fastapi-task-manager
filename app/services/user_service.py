"""
User service layer
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user_repository import UserRepository


class UserService:
    """User service for business logic"""

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> List[User]:
        return self.user_repository.get_users(
            skip=skip,
            limit=limit,
            include_deleted=include_deleted,
        )

    def get_user(self, user_id: int, include_deleted: bool = False) -> Optional[User]:
        return self.user_repository.get_user(user_id, include_deleted=include_deleted)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.get_user_by_email(email)

    def create_user(self, user: UserCreate) -> User:
        return self.user_repository.create_user(user)

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        return self.user_repository.update_user(user_id, user_update)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repository.soft_delete_user(user_id)
