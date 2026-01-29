"""Backburner model for ideas and future projects."""
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class BackburnerItem(Base):
    """Backburner item represents ideas or projects for later."""
    __tablename__ = "backburner_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Context for smart resurfacing
    context_tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=[])
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Why moved to backburner
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resurfaced_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    activated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # When moved to active
    
    __table_args__ = (
        Index("idx_backburner_user", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<BackburnerItem(id={self.id}, title={self.title})>"
