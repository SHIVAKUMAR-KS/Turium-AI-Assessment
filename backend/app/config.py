"""
Configuration settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    openai_api_key: str
    # MongoDB connection settings
    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    mongodb_user: Optional[str] = None
    mongodb_password: Optional[str] = None
    mongodb_db: str = "knowledge_inbox"
    # Alternative: use full database URL
    mongodb_url: Optional[str] = None
    chroma_db_path: str = "data/chroma_db"
    chunk_size: int = 500
    chunk_overlap: int = 50
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-3.5-turbo"
    max_chunks_per_query: int = 5
    
    @property
    def get_mongodb_url(self) -> str:
        """Get MongoDB connection URL"""
        if self.mongodb_url:
            return self.mongodb_url
        if self.mongodb_user and self.mongodb_password:
            return f"mongodb://{self.mongodb_user}:{self.mongodb_password}@{self.mongodb_host}:{self.mongodb_port}/{self.mongodb_db}?authSource=admin"
        return f"mongodb://{self.mongodb_host}:{self.mongodb_port}/{self.mongodb_db}"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields from .env (like old postgres settings)
    )


settings = Settings()

