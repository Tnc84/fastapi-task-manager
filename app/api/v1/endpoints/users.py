"""
User management endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_admin, resolve_include_deleted
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    include_deleted: bool = Depends(resolve_include_deleted),
):
    """Get all users with pagination"""
    user_service = UserService(db)
    return user_service.get_users(
        skip=skip,
        limit=limit,
        include_deleted=include_deleted,
    )


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    include_deleted: bool = Depends(resolve_include_deleted),
):
    """Get a specific user by ID"""
    user_service = UserService(db)
    user = user_service.get_user(user_id, include_deleted=include_deleted)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """Create a new user"""
    user_service = UserService(db)
    return user_service.create_user(user)


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing user"""
    user_service = UserService(db)
    user = user_service.update_user(user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    actor: UserModel = Depends(require_admin),
):
    """Soft delete a user (admin only)"""
    if actor.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admins cannot delete their own account",
        )

    user_service = UserService(db)
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
