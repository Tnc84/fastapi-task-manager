"""
Shared FastAPI dependencies
"""

from typing import Optional
from fastapi import Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.services.user_service import UserService


def get_optional_actor_user(
    x_actor_user_id: int | None = Header(default=None, alias="X-Actor-User-Id"),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Resolve acting user when header is present."""
    if x_actor_user_id is None:
        return None

    user = UserService(db).get_user(x_actor_user_id, include_deleted=False)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acting user not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acting user is inactive",
        )
    return user


def get_actor_user(
    actor: Optional[User] = Depends(get_optional_actor_user),
) -> User:
    """Require acting user header."""
    if actor is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Actor-User-Id header",
        )
    return actor


def require_admin(actor: User = Depends(get_actor_user)) -> User:
    """Allow only admin (superuser) actors."""
    if not actor.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return actor


def resolve_include_deleted(
    include_deleted: bool = Query(False),
    actor: Optional[User] = Depends(get_optional_actor_user),
) -> bool:
    """Only admins may request soft-deleted records."""
    if not include_deleted:
        return False
    if actor is None or not actor.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view deleted records",
        )
    return True
