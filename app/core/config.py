"""
Application configuration using Pydantic BaseSettings
"""

from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Ignore extra fields from .env file
    )
    
    # Project settings
    PROJECT_NAME: str = "Task Manager API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    # Default to PostgreSQL - override in .env file
    # For development: postgresql://postgres:postgres@localhost:5432/taskmanager
    # For SQLite fallback: sqlite:///./taskmanager.db
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/taskmanager"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:4200",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080"
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from various input formats"""
        if isinstance(v, str):
            if not v:
                # Empty string, return default list
                return [
                    "http://localhost:3000",
                    "http://localhost:4200",
                    "http://localhost:8080"
                ]
            if v.startswith("["):
                # It's a JSON string, parse it
                import json
                return json.loads(v)
            else:
                # It's a comma-separated string
                return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return v


settings = Settings()
