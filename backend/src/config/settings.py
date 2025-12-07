from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database settings
    neon_database_url: str = os.getenv("NEON_DATABASE_URL", "postgresql://user:password@localhost/dbname")

    # Gemini API settings
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model_name: str = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")
    embedding_model_name: str = os.getenv("EMBEDDING_MODEL_NAME", "embedding-001")

    # Qdrant settings
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_host: str = os.getenv("QDRANT_HOST", "localhost:6333")
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "textbook_chunks")

    # Application settings
    app_name: str = "Textbook RAG API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001,https://yourdomain.com")

    model_config = {"env_file": ".env"}

settings = Settings()