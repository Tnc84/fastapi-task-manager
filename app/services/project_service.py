"""
Project service layer
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.project_repository = ProjectRepository(db)

    def get_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        return self.project_repository.get_projects(skip=skip, limit=limit)

    def get_project(self, project_id: int) -> Optional[Project]:
        return self.project_repository.get_project(project_id)

    def create_project(self, project: ProjectCreate) -> Project:
        return self.project_repository.create_project(project)

    def update_project(self, project_id: int, project_update: ProjectUpdate) -> Optional[Project]:
        return self.project_repository.update_project(project_id, project_update)

    def delete_project(self, project_id: int) -> bool:
        return self.project_repository.delete_project(project_id)
