from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://zencore_user:zencore_password@localhost:5432/zencore"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Railway specific settings
    port: int = 8000
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Email (placeholder)
    smtp_server: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Slack (placeholder)
    slack_webhook_url: Optional[str] = None
    
    class Config:
        env_file = ".env"


settings = Settings() 