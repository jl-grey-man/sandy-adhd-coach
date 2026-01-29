"""Pattern categories - the "boxes" Sandy tracks about you."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class PatternCategory(Base):
    """A category of behavior pattern Sandy is learning about."""
    __tablename__ = "pattern_categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    understanding_level = Column(Integer, default=0, nullable=False)  # 0-100
    observations_count = Column(Integer, default=0, nullable=False)
    current_hypothesis = Column(Text, nullable=True)
    confidence = Column(Integer, default=0, nullable=False)  # 0-100
    evidence = Column(JSONB, default=[], nullable=False)
    last_observed = Column(DateTime, nullable=True)
    needs_exploration = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
