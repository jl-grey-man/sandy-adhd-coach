"""Projects API router."""
import logging
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project, ProjectStatus
from app.models.task import Task, TaskStatus, TaskPriority, TaskEnergyLevel
from app.models.backburner import BackburnerItem

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/projects", tags=["projects"])


# Pydantic models for requests/responses
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    estimated_hours: Optional[int] = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    deadline: Optional[datetime]
    estimated_hours: Optional[int]
    task_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    priority: str = "medium"
    energy_level: str = "medium"
    estimated_minutes: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    energy_level: str
    project_id: Optional[int]
    estimated_minutes: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all projects for the current user."""
    query = db.query(Project).filter(Project.user_id == current_user.id)
    
    if status:
        query = query.filter(Project.status == status)
    
    projects = query.order_by(Project.created_at.desc()).all()
    
    # Add task count to each project
    result = []
    for project in projects:
        project_dict = ProjectResponse.from_orm(project).dict()
        project_dict['task_count'] = len(project.tasks)
        result.append(ProjectResponse(**project_dict))
    
    return result


@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new project."""
    project = Project(
        user_id=current_user.id,
        title=project_data.title,
        description=project_data.description,
        deadline=project_data.deadline,
        estimated_hours=project_data.estimated_hours,
        status=ProjectStatus.ACTIVE
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return ProjectResponse.from_orm(project)


@router.put("/{project_id}/backburner")
async def move_to_backburner(
    project_id: int,
    reason: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Move a project to backburner."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.status = ProjectStatus.BACKBURNER
    project.moved_to_backburner_at = datetime.utcnow()
    project.backburner_reason = reason
    
    db.commit()
    
    return {"status": "moved_to_backburner", "project_id": project_id}


@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all tasks for the current user."""
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    if project_id:
        query = query.filter(Task.project_id == project_id)
    
    if status:
        query = query.filter(Task.status == status)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    
    return [TaskResponse.from_orm(task) for task in tasks]


@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task."""
    task = Task(
        user_id=current_user.id,
        project_id=task_data.project_id,
        title=task_data.title,
        description=task_data.description,
        priority=TaskPriority(task_data.priority),
        energy_level=TaskEnergyLevel(task_data.energy_level),
        estimated_minutes=task_data.estimated_minutes,
        due_date=task_data.due_date,
        status=TaskStatus.TODO
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return TaskResponse.from_orm(task)
