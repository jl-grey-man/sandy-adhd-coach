from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChatContext(BaseModel):
    energy: Optional[int] = None
    current_task: Optional[str] = None


class ChatMessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None  # Frontend-generated session ID
    context: Optional[ChatContext] = None


class ChatMessageResponse(BaseModel):
    conversation_id: int
    ai_response: str
    suggestions: list[str]
    created_at: datetime
