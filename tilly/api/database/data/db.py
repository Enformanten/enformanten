from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import async_sessionmaker
from typing import AsyncGenerator

from api.config import SNOWFLAKE_CREDENTIALS


# Define your Snowflake connection parameters
SNOWFLAKE_URL = (
    "snowflake://{user}:{password}@{account}"
    "/{database}/{schema}?warehouse={warehouse}&role={role_name}"
).format(**SNOWFLAKE_CREDENTIALS)


# Create an async engine
engine = create_async_engine(SNOWFLAKE_URL, echo=True, future=True)
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
