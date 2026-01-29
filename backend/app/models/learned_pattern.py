"""Learned patterns - what Sandy knows about you."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base


class LearnedPattern(Base):
    """Patterns Sandy has learned about the user."""
    __tablename__ = "learned_patterns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    pattern = Column(Text, nullable=False)
    evidence = Column(Text, nullable=True)
    confidence = Column(Integer, default=50, nullable=False)  # 0-100
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
