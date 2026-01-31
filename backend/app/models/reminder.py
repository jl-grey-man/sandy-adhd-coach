"""Reminder model for notifications."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base


class Reminder(Base):
    """Reminders for notifications (not tasks)."""
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Telegram user ID directly
    
    # Content
    task = Column(Text, nullable=False)  # What to remind about (was 'message')
    context = Column(Text, nullable=True)  # Why this reminder was created
    
    # Timing (timezone-aware)
    reminder_time = Column(DateTime(timezone=True), nullable=False, index=True)  # was 'remind_at'
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Status
    is_sent = Column(Boolean, default=False, nullable=False, index=True)  # was 'sent'
    sent_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Reminder(id={self.id}, user={self.user_id}, task='{self.task[:30]}...', time={self.reminder_time})>"
