from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Goal details
    category = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Timeline
    target_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Status
    status = Column(String(20), default='active', nullable=False)
    progress = Column(Integer, default=0)
    
    # Additional data
    extra_data = Column(JSONB, default={})
    
    __table_args__ = (
        CheckConstraint("category IN ('personal', 'work')", name='check_goal_category'),
        CheckConstraint("status IN ('active', 'completed', 'paused', 'abandoned')", name='check_goal_status'),
        CheckConstraint("progress >= 0 AND progress <= 100", name='check_goal_progress'),
    )
