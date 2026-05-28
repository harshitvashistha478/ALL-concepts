from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://cyberhub:cyberhub123@localhost:5432/cyberhub_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    GROQ_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
