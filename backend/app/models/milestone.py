"""Milestone model for project check-ins."""
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Milestone(Base):
    """Milestone represents auto-generated project check-ins."""
    __tablename__ = "milestones"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    
    check_in_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Response from user
    user_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    responded_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="milestones")
    
    __table_args__ = (
        Index("idx_milestones_project", "project_id"),
        Index("idx_milestones_check_in_date", "check_in_date"),
    )

    def __repr__(self) -> str:
        return f"<Milestone(id={self.id}, project_id={self.project_id}, date={self.check_in_date})>"
