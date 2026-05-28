from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# Engine = the connection to PostgreSQL
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Session factory = creates DB sessions on demand
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

# Dependency: gives each API route its own DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
