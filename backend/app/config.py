from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "postgresql://localhost/adhd_coach_dev"
    environment: str = "development"
    debug: bool = True
    port: int = 8000

    # JWT settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Together.ai settings
    together_api_key: str = ""
    
    # Pinecone settings
    pinecone_api_key: str = ""
    
    # OpenAI settings (for embeddings)
    openai_api_key: str = ""
    
    # Telegram settings
    telegram_bot_token: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
