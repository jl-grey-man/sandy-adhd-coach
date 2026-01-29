"""
Long-term memory service using Pinecone vector database.
Stores and retrieves conversation embeddings for RAG.
"""
import time
from typing import List, Dict
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

from app.config import get_settings


class MemoryService:
    def __init__(self):
        settings = get_settings()
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index_name = "adhd-coach-memory"
        
        # Initialize OpenAI for embeddings
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        
        # Create index if it doesn't exist
        self._ensure_index_exists()
        
        # Connect to index
        self.index = self.pc.Index(self.index_name)
    
    def _ensure_index_exists(self):
        """Create Pinecone index if it doesn't exist"""
        existing_indexes = [idx.name for idx in self.pc.list_indexes()]
        
        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=1536,  # OpenAI embedding size
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
            # Wait for index to be ready
            time.sleep(10)
    
    def create_embedding(self, text: str) -> List[float]:
        """Create embedding vector from text using OpenAI"""
        response = self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    
    def store_conversation(
        self,
        conversation_id: int,
        user_id: int,
        user_message: str,
        ai_response: str,
        session_id: str = None
    ):
        """Store a conversation in Pinecone"""
        # Combine user message and AI response for context
        full_text = f"User: {user_message}\nAssistant: {ai_response}"
        
        # Create embedding
        embedding = self.create_embedding(full_text)
        
        # Store in Pinecone with metadata
        self.index.upsert(
            vectors=[{
                "id": f"conv_{conversation_id}",
                "values": embedding,
                "metadata": {
                    "user_id": user_id,
                    "session_id": session_id or "",
                    "user_message": user_message[:500],  # Truncate for storage
                    "ai_response": ai_response[:500],
                    "full_text": full_text[:1000],
                    "timestamp": int(time.time())
                }
            }]
        )
    
    def search_relevant_memories(
        self,
        query: str,
        user_id: int,
        top_k: int = 5,  # Increased from 3 to include documents
        exclude_session: str = None
    ) -> List[Dict]:
        """
        Search for relevant past conversations AND documents.
        
        Args:
            query: Current user message
            user_id: User ID to filter by
            top_k: Number of results to return
            exclude_session: Session ID to exclude (don't retrieve current session)
        
        Returns:
            List of relevant past conversations and document chunks
        """
        # Create embedding for query
        query_embedding = self.create_embedding(query)
        
        # Search Pinecone (includes both conversations and documents)
        results = self.index.query(
            vector=query_embedding,
            filter={
                "user_id": user_id,
                # Exclude current session if provided
                **({"session_id": {"$ne": exclude_session}} if exclude_session else {})
            },
            top_k=top_k,
            include_metadata=True
        )
        
        # Format results
        memories = []
        for match in results.matches:
            if match.score > 0.7:  # Only include relevant matches
                metadata = match.metadata
                
                # Check if it's a document chunk or conversation
                if metadata.get("doc_type"):
                    memories.append({
                        "score": match.score,
                        "type": "document",
                        "doc_type": metadata.get("doc_type"),
                        "filename": metadata.get("filename", ""),
                        "text": metadata.get("full_text", ""),
                    })
                else:
                    memories.append({
                        "score": match.score,
                        "type": "conversation",
                        "user_message": metadata.get("user_message", ""),
                        "ai_response": metadata.get("ai_response", ""),
                        "full_text": metadata.get("full_text", ""),
                        "timestamp": metadata.get("timestamp", 0)
                    })
        
        return memories


# Singleton instance
_memory_service = None

def get_memory_service() -> MemoryService:
    """Get or create the memory service singleton"""
    global _memory_service
    if _memory_service is None:
        _memory_service = MemoryService()
    return _memory_service
