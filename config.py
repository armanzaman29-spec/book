from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Keys
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")

    # Application settings
    app_name: str = "RAG Chatbot API"
    app_version: str = "2.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Server settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", 8000))

    # Database settings
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", os.getenv("COLLECTION_NAME", "documents"))

    # Model settings
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    cohere_model: str = os.getenv("COHERE_MODEL", "embed-multilingual-v2.0")

    # RAG settings
    retrieval_top_k: int = int(os.getenv("RETRIEVAL_TOP_K", 5))
    max_tokens: int = int(os.getenv("MAX_TOKENS", 1000))
    temperature: float = float(os.getenv("TEMPERATURE", 0.7))

    # Caching settings
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", 3600))

    # Rate limiting
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", 3600))

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra environment variables

    def validate_required_keys(self):
        """Validate that all required API keys are present"""
        errors = []

        # At least one of OpenAI or Groq API keys should be provided
        if not self.openai_api_key and not self.groq_api_key:
            errors.append("Either OPENAI_API_KEY or GROQ_API_KEY is required")
        if not self.cohere_api_key:
            errors.append("COHERE_API_KEY is required")
        if not self.qdrant_url:
            errors.append("QDRANT_URL is required")
        if not self.qdrant_api_key:
            errors.append("QDRANT_API_KEY is required")

        if errors:
            raise ValueError(f"Missing required configuration: {', '.join(errors)}")

# Create a single instance of settings
settings = Settings()