"""
Database connection and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from api.config import settings
from models.database import Base


# Sync engine for initialization
sync_engine = create_engine(
    settings.database_url.replace("sqlite+aiosqlite", "sqlite"),
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Async engine for runtime
async_engine = create_async_engine(
    settings.database_url if "sqlite" in settings.database_url else f"postgresql+asyncpg://{settings.database_url}",
    echo=False
)

# Session factories
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

SessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False
)


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=sync_engine)


def get_db() -> Generator[Session, None, None]:
    """Get database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> Generator[AsyncSession, None, None]:
    """Get async database session dependency."""
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
