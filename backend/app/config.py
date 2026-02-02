from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "postgresql://localhost/adhd_coach_dev"
    environment: str = "development"
    debug: bool = False  # Set to True only when debugging SQL queries

    # Together.ai settings (for AI responses)
    together_api_key: str = ""

    # Pinecone settings (for memory/embeddings)
    pinecone_api_key: str = ""

    # OpenAI settings (for embeddings)
    openai_api_key: str = ""

    # Telegram settings (primary interface)
    telegram_bot_token: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
