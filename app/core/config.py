"""
Application configuration using Pydantic BaseSettings
"""

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
    DATABASE_URL: str = "sqlite:///./task_manager.db"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings - commented out to avoid parsing issues
    # BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    # @classmethod
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
    #     if isinstance(v, str):
    #         if v.startswith("["):
    #             # It's a JSON string, parse it
    #             import json
    #             return json.loads(v)
    #         else:
    #             # It's a comma-separated string
    #             return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, list):
    #         return v
    #     return v


settings = Settings()
