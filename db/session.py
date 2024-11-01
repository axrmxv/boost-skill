import settings

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from typing import AsyncGenerator


# interaction with the database
# create an async engine to interact with the database
engine = create_async_engine(
    settings.PROD_DB_URL,
    future=True,
    echo=True
    )

# create a session to interact with the database
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
    )


async def get_db() -> AsyncGenerator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
