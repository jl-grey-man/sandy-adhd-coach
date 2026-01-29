from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class Checkin(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Check-in type
    type = Column(String(20), nullable=False)
    
    # Ratings (1-10 scale)
    overall_rating = Column(Integer)
    energy_rating = Column(Integer)
    focus_rating = Column(Integer)
    mood_rating = Column(Integer)
    stress_rating = Column(Integer)
    
    # Conversational responses
    responses = Column(JSONB, default=[])
    
    # AI analysis
    ai_analysis = Column(Text)
    insights = Column(JSONB, default={})
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        CheckConstraint("type IN ('daily', 'weekly', 'monthly')", name='check_checkin_type'),
        CheckConstraint("overall_rating >= 1 AND overall_rating <= 10", name='check_overall_rating'),
        CheckConstraint("energy_rating >= 1 AND energy_rating <= 10", name='check_energy_rating'),
        CheckConstraint("focus_rating >= 1 AND focus_rating <= 10", name='check_focus_rating'),
        CheckConstraint("mood_rating >= 1 AND mood_rating <= 10", name='check_mood_rating'),
        CheckConstraint("stress_rating >= 1 AND stress_rating <= 10", name='check_stress_rating'),
    )
