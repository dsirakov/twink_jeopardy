"""Database session management and ORM base configuration."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+asyncpg://"),
    echo=False,
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Get async database session dependency.
    :return: Async database session
    """
    async with AsyncSessionLocal() as session:
        yield session
