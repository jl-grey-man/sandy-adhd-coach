from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class WheelCategory(Base):
    __tablename__ = "wheel_categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Category details
    name = Column(String(100), nullable=False)
    description = Column(Text)
    definition_of_10 = Column(Text)
    
    # Display order
    display_order = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_user_wheel_category'),
    )


class WheelScore(Base):
    __tablename__ = "wheel_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("wheel_categories.id", ondelete="CASCADE"), nullable=False)
    
    # Score
    score = Column(Integer, nullable=False)
    
    # Optional notes
    notes = Column(Text)
    
    # Timestamp
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        CheckConstraint("score >= 0 AND score <= 10", name='check_wheel_score'),
    )
