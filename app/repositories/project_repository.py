"""
Project repository for database operations
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        return self.db.query(Project).offset(skip).limit(limit).all()

    def get_project(self, project_id: int) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def create_project(self, project: ProjectCreate) -> Project:
        payload = project.model_dump() if hasattr(project, "model_dump") else project.dict()
        payload["key"] = payload["key"].upper()
        db_project = Project(**payload)
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def update_project(self, project_id: int, project_update: ProjectUpdate) -> Optional[Project]:
        db_project = self.get_project(project_id)
        if not db_project:
            return None

        update_data = (
            project_update.model_dump(exclude_unset=True)
            if hasattr(project_update, "model_dump")
            else project_update.dict(exclude_unset=True)
        )
        if "key" in update_data and update_data["key"]:
            update_data["key"] = update_data["key"].upper()

        for field, value in update_data.items():
            setattr(db_project, field, value)

        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def delete_project(self, project_id: int) -> bool:
        db_project = self.get_project(project_id)
        if not db_project:
            return False
        self.db.delete(db_project)
        self.db.commit()
        return True
