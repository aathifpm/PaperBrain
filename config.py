import os
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration settings for the RAG application."""
    
    # Embedding settings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION = 384
    
    # Chunking settings
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    
    # Search settings
    TOP_K_RESULTS = 5
    
    # LLM settings
    LLM_MODEL = "gemini-1.5-pro"
    MAX_TOKENS = 1000
    TEMPERATURE = 0.3
    
    # File upload settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = ['pdf', 'txt', 'docx']
    
    # UI settings
    PAGE_TITLE = "PaperBrain"
    PAGE_ICON = "📚"
    
    @classmethod
    def get_api_key(cls):
        """Get API key from environment."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Please set GOOGLE_API_KEY environment variable")
        return api_key