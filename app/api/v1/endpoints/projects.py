"""
Project management endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter()


@router.get("/", response_model=List[Project])
def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return ProjectService(db).get_projects(skip=skip, limit=limit)


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = ProjectService(db).get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    return ProjectService(db).create_project(project)


@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = ProjectService(db).update_project(project_id, project_update)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    success = ProjectService(db).delete_project(project_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
