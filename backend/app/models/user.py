from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, Index, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
    preferences: Mapped[dict] = mapped_column(
        JSONB,
        default={
            "voice_enabled": True,
            "notification_enabled": True,
            "checkin_times": {"morning": "09:00", "evening": "20:00"},
        },
    )
    adhd_profile: Mapped[dict] = mapped_column(JSONB, default={})
    
    # Telegram integration
    telegram_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    telegram_username: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    morning_briefing_time: Mapped[str] = mapped_column(String(5), default="09:00")

    __table_args__ = (Index("idx_users_email", "email"),)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
