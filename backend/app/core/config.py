from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://cyberhub:cyberhub123@localhost:5432/cyberhub_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    GROQ_API_KEY: str = ""
    RESEARCHER_MODEL: str = "llama-3.1-8b-instant"
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
