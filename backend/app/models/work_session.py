from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.sql import func
from app.database import Base


class WorkSession(Base):
    __tablename__ = "work_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"))
    
    # Session timing
    started_at = Column(DateTime(timezone=True), nullable=False)
    ended_at = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)
    
    # Context at start
    energy_at_start = Column(Integer)
    focus_at_start = Column(Integer)
    strategy_used = Column(String(100))
    
    # Outcome
    completed = Column(Boolean, default=False)
    switched_task = Column(Boolean, default=False)
    reason_for_switching = Column(Text)
    effectiveness_rating = Column(Integer)
    
    __table_args__ = (
        CheckConstraint("energy_at_start >= 1 AND energy_at_start <= 10", name='check_session_energy'),
        CheckConstraint("focus_at_start >= 1 AND focus_at_start <= 10", name='check_session_focus'),
        CheckConstraint("effectiveness_rating >= 1 AND effectiveness_rating <= 10", name='check_session_effectiveness'),
    )
