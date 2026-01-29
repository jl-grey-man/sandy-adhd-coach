from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Metric type
    metric_type = Column(String(50), nullable=False)
    
    # Value (flexible structure)
    value = Column(JSONB, nullable=False)
    
    # Timestamp
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())


class ConversationEmbedding(Base):
    __tablename__ = "conversation_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    
    # Pinecone reference
    pinecone_id = Column(String(100), nullable=False, unique=True)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
