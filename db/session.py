import settings

from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker
)

from typing import AsyncGenerator


# interaction with the database
# create an async engine to interact with the database
engine = create_async_engine(
    settings.PROD_DB_URL,
    future=True,
    echo=True
    )

# create a session to interact with the database
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)


async def get_db() -> AsyncGenerator:
    try:
        session: AsyncSession = AsyncSessionLocal()
        yield session
    finally:
        await session.close()
