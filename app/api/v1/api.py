"""
API v1 router configuration
"""

from fastapi import APIRouter

from app.api.v1.endpoints import tasks, users, projects, comments

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(comments.router, prefix="/tasks", tags=["comments"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
