"""Pattern observations - evidence supporting or contradicting hypotheses."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class PatternObservation(Base):
    """An observation that provides evidence for a pattern category."""
    __tablename__ = "pattern_observations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("pattern_categories.id", ondelete="CASCADE"), nullable=False, index=True)
    observation_type = Column(String(50), nullable=False)  # 'supports', 'contradicts', 'neutral'
    observation_text = Column(Text, nullable=False)
    context = Column(JSONB, default={}, nullable=False)
    weight = Column(Integer, default=1, nullable=False)  # How strong is this evidence?
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
