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
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return self.user_repository.get_users(skip=skip, limit=limit)
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.user_repository.get_user(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.user_repository.get_user_by_email(email)
    
    def create_user(self, user: UserCreate) -> User:
        """Create a new user"""
        return self.user_repository.create_user(user)
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update an existing user"""
        return self.user_repository.update_user(user_id, user_update)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        return self.user_repository.delete_user(user_id)
