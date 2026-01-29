"""Task model for individual actions."""
from datetime import datetime
from typing import Optional
from enum import Enum

from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Index, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TaskStatus(str, Enum):
    """Task status enumeration."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    """Task priority enumeration."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskEnergyLevel(str, Enum):
    """Energy level required for task."""
    HIGH = "high"  # Complex, requires focus
    MEDIUM = "medium"  # Normal cognitive load
    LOW = "low"  # Easy, can do when tired


class Task(Base):
    """Task represents a single action item."""
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus),
        default=TaskStatus.TODO,
        nullable=False
    )
    priority: Mapped[Optional[TaskPriority]] = mapped_column(
        SQLEnum(TaskPriority),
        nullable=True
    )
    energy_level: Mapped[Optional[TaskEnergyLevel]] = mapped_column(
        SQLEnum(TaskEnergyLevel),
        nullable=True
    )
    
    # Time
    estimated_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    project: Mapped[Optional["Project"]] = relationship("Project", back_populates="tasks")
    
    __table_args__ = (
        Index("idx_tasks_user_status", "user_id", "status"),
        Index("idx_tasks_project", "project_id"),
        Index("idx_tasks_due_date", "due_date"),
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"
