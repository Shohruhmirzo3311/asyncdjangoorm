import os

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from asyncdjangoorm.config.base import Base

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./asyncdjangoorm.db")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """
    Initialize the database: create all tables defined with Base.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)