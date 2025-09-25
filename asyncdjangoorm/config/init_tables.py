import importlib
import os
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from asyncdjangoorm.config.base import Base
from asyncdjangoorm.cli import get_db_url


def _normalize_db_url(db_url: str) -> str:
    """
    Normalize DB URL so async drivers are supported consistently.
    """
    url = make_url(db_url)

    if url.drivername.startswith("sqlite+aiosqlite"):
        url = url.set(drivername="sqlite+aiosqlite")
    elif url.drivername.startswith("postgresql+asyncpg"):
        url = url.set(drivername="postgresql+asyncpg")
    elif url.drivername.startswith("mysql+aiomysql"):
        url = url.set(drivername="mysql+aiomysql")

    return str(url)


# --- Load DATABASE_URL from project settings ---
try:
    settings = importlib.import_module("settings")
    DATABASE_URL = getattr(
        settings,
        "DATABASE_URL",
        os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./default.db"),
    )
except ModuleNotFoundError:
    # fallback if no project settings found
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./default.db")

# --- Engine and Session ---


engine = None
AsyncSessionLocal = None


def init_engine():
    """
    Initialize the engine and session factory based on current settings.
    """
    global engine, AsyncSessionLocal

    database_url = get_db_url()  # always fetch latest DB URL
    engine = create_async_engine(database_url, echo=False, future=True)

    AsyncSessionLocal = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )


async def init_db():
    """
    Initialize the database: create all tables defined with Base.
    """
    if engine is None:
        init_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
