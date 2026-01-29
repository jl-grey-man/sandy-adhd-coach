"""
Document processing service for uploaded files and URLs.
Extracts text and stores in Pinecone for RAG.
"""
from pypdf import PdfReader
from docx import Document
import io
import requests
from bs4 import BeautifulSoup

from app.services.memory import get_memory_service


class DocumentService:
    def __init__(self):
        self.memory_service = get_memory_service()
    
    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extract text from PDF file"""
        pdf = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n\n"
        return text.strip()
    
    def extract_text_from_docx(self, file_bytes: bytes) -> str:
        """Extract text from Word document"""
        doc = Document(io.BytesIO(file_bytes))
        text = "\n\n".join([para.text for para in doc.paragraphs if para.text])
        return text.strip()
    
    def extract_text_from_txt(self, file_bytes: bytes) -> str:
        """Extract text from plain text file"""
        return file_bytes.decode('utf-8').strip()
    
    def extract_text_from_url(self, url: str) -> tuple[str, str]:
        """
        Extract text from URL (webpage, article, etc.)
        Returns: (text, title)
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title = title.get_text().strip() if title else url
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text, title
            
        except Exception as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")
    
    def process_document(
        self,
        file_bytes: bytes,
        filename: str,
        user_id: int,
        doc_type: str = "personal"  # "personal" or "research"
    ) -> dict:
        """
        Process uploaded document and store in Pinecone.
        
        Args:
            file_bytes: File content as bytes
            filename: Original filename
            user_id: User ID
            doc_type: Type of document ("personal" or "research")
        
        Returns:
            dict with status and extracted text info
        """
        # Extract text based on file type
        ext = filename.lower().split('.')[-1]
        
        try:
            if ext == 'pdf':
                text = self.extract_text_from_pdf(file_bytes)
            elif ext in ['docx', 'doc']:
                text = self.extract_text_from_docx(file_bytes)
            elif ext in ['txt', 'md']:
                text = self.extract_text_from_txt(file_bytes)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported file type: {ext}"
                }
            
            if not text or len(text) < 50:
                return {
                    "success": False,
                    "error": "Document appears to be empty or too short"
                }
            
            # Split into chunks (for long documents)
            chunk_size = 1000
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            
            # Store each chunk in Pinecone
            for i, chunk in enumerate(chunks):
                doc_id = f"doc_{user_id}_{filename}_{i}"
                
                # Create embedding
                embedding = self.memory_service.create_embedding(chunk)
                
                # Store in Pinecone with metadata
                self.memory_service.index.upsert(
                    vectors=[{
                        "id": doc_id,
                        "values": embedding,
                        "metadata": {
                            "user_id": user_id,
                            "doc_type": doc_type,
                            "filename": filename,
                            "chunk_index": i,
                            "text": chunk[:500],  # First 500 chars for reference
                            "full_text": chunk,
                        }
                    }]
                )
            
            return {
                "success": True,
                "chunks_stored": len(chunks),
                "total_chars": len(text),
                "doc_type": doc_type
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to process document: {str(e)}"
            }
    
    def process_url(
        self,
        url: str,
        user_id: int,
        doc_type: str = "research"
    ) -> dict:
        """
        Process URL content and store in Pinecone.
        
        Args:
            url: URL to fetch
            user_id: User ID
            doc_type: Type of document ("personal" or "research")
        
        Returns:
            dict with status and extracted text info
        """
        try:
            # Extract text from URL
            text, title = self.extract_text_from_url(url)
            
            if not text or len(text) < 100:
                return {
                    "success": False,
                    "error": "URL content appears to be empty or too short"
                }
            
            # Split into chunks
            chunk_size = 1000
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            
            # Store each chunk in Pinecone
            for i, chunk in enumerate(chunks):
                doc_id = f"url_{user_id}_{hash(url)}_{i}"
                
                # Create embedding
                embedding = self.memory_service.create_embedding(chunk)
                
                # Store in Pinecone with metadata
                self.memory_service.index.upsert(
                    vectors=[{
                        "id": doc_id,
                        "values": embedding,
                        "metadata": {
                            "user_id": user_id,
                            "doc_type": doc_type,
                            "source_url": url,
                            "title": title,
                            "chunk_index": i,
                            "text": chunk[:500],
                            "full_text": chunk,
                        }
                    }]
                )
            
            return {
                "success": True,
                "chunks_stored": len(chunks),
                "total_chars": len(text),
                "title": title,
                "doc_type": doc_type
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Singleton instance
_document_service = None

def get_document_service() -> DocumentService:
    """Get or create the document service singleton"""
    global _document_service
    if _document_service is None:
        _document_service = DocumentService()
    return _document_service
