"""Project model for task and project management."""
from datetime import datetime
from typing import Optional
from enum import Enum

from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Index, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ProjectStatus(str, Enum):
    """Project status enumeration."""
    ACTIVE = "active"
    BACKBURNER = "backburner"
    DONE = "done"
    ARCHIVED = "archived"


class Project(Base):
    """Project represents a multi-step work stream."""
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(
        SQLEnum(ProjectStatus), 
        default=ProjectStatus.ACTIVE,
        nullable=False
    )
    
    # Time tracking
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    estimated_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    actual_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    moved_to_backburner_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    backburner_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    milestones: Mapped[list["Milestone"]] = relationship("Milestone", back_populates="project", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_projects_user_status", "user_id", "status"),
        Index("idx_projects_deadline", "deadline"),
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, title={self.title}, status={self.status})>"
