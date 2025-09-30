"""
API v1 router configuration
"""

from fastapi import APIRouter

from app.api.v1.endpoints import tasks, users

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
