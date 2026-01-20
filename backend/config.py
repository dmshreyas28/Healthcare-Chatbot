import os
from typing import Literal
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # LLM Configuration
    llm_provider: Literal["openai", "anthropic"] = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # OpenAI Models
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Anthropic Models
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    
    # RAG Configuration
    enable_rag: bool = os.getenv("ENABLE_RAG", "false").lower() == "true"
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "./chroma_db")
    
    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # CORS Configuration
    allowed_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000", "*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()