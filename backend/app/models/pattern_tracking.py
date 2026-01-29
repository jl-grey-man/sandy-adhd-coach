"""Pattern tracking models."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class PatternCategory(Base):
    """A category of behavior pattern Sandy tracks (system or user-discovered)."""
    __tablename__ = "pattern_categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class PatternObservation(Base):
    """A single observation/data point for a pattern category."""
    __tablename__ = "pattern_observations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("pattern_categories.id", ondelete="CASCADE"), nullable=False, index=True)
    sub_pattern = Column(String(100), nullable=True, index=True)  # NEW: specific sub-pattern
    observation = Column(Text, nullable=False)
    context = Column(JSONB, default={}, nullable=False)
    observed_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)


class PatternHypothesis(Base):
    """A hypothesis about a pattern (what Sandy thinks might be true)."""
    __tablename__ = "pattern_hypotheses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("pattern_categories.id", ondelete="CASCADE"), nullable=False, index=True)
    sub_pattern = Column(String(100), nullable=True, index=True)  # NEW: specific sub-pattern
    hypothesis = Column(Text, nullable=False)
    confidence = Column(Integer, default=0, nullable=False, index=True)
    supporting_observations = Column(Integer, default=0, nullable=False)
    contradicting_observations = Column(Integer, default=0, nullable=False)
    last_updated = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(String(20), default='exploring', nullable=False)
    needs_exploration = Column(Boolean, default=False, nullable=False, index=True)
