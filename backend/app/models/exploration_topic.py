"""Exploration topics - what Sandy needs to understand about you."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class ExplorationTopic(Base):
    """Topics Sandy should explore to understand you better."""
    __tablename__ = "exploration_topics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic = Column(String(100), nullable=False)
    understanding_score = Column(Integer, default=0, nullable=False, index=True)
    last_discussed = Column(DateTime, nullable=True)
    priority = Column(Integer, default=5, nullable=False)  # 1-10, how important
    key_insights = Column(JSONB, default={}, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
