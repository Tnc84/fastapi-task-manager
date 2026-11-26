"""
User repository for database operations
"""

from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class UserRepository:
    """User repository for database operations"""

    def __init__(self, db: Session):
        self.db = db

    def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> List[User]:
        """Get all users with pagination"""
        query = self.db.query(User)
        if not include_deleted:
            query = query.filter(User.deleted_at.is_(None))
        return query.offset(skip).limit(limit).all()

    def get_user(self, user_id: int, include_deleted: bool = False) -> Optional[User]:
        """Get user by ID"""
        query = self.db.query(User).filter(User.id == user_id)
        if not include_deleted:
            query = query.filter(User.deleted_at.is_(None))
        return query.first()

    def get_user_by_email(self, email: str, include_deleted: bool = False) -> Optional[User]:
        """Get user by email"""
        query = self.db.query(User).filter(User.email == email)
        if not include_deleted:
            query = query.filter(User.deleted_at.is_(None))
        return query.first()

    def create_user(self, user: UserCreate) -> User:
        """Create a new user"""
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update an existing user"""
        db_user = self.get_user(user_id)
        if not db_user:
            return None

        update_data = (
            user_update.model_dump(exclude_unset=True)
            if hasattr(user_update, "model_dump")
            else user_update.dict(exclude_unset=True)
        )
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def soft_delete_user(self, user_id: int) -> bool:
        """Soft delete a user"""
        db_user = self.get_user(user_id, include_deleted=False)
        if not db_user:
            return False

        db_user.deleted_at = datetime.now(timezone.utc)
        db_user.is_active = False
        self.db.commit()
        return True
