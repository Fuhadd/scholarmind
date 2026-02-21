from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# The engine is the connection pool — create once, reuse forever
engine = create_async_engine(
    settings.database_url,
    echo=settings.app_env == "development",  # logs SQL in dev, silent in prod
    pool_size=10,
    max_overflow=20,
)

# Session factory — creates individual database sessions
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Base class all your SQLAlchemy models will inherit from
class Base(DeclarativeBase):
    pass


# Dependency injected into every route that needs DB access
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise