from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool, AsyncAdaptedQueuePool

from common.config import settings, ModeEnum


async_engine = create_async_engine(
    url=settings["db_url_test"],
    echo=False,
    poolclass=NullPool
    if settings["mode"] == ModeEnum.test
    else AsyncAdaptedQueuePool,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
)


async def async_session() -> AsyncGenerator:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
