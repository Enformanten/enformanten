"""
Asynchronous Database Connection and Session Script

This script defines an asynchronous database connection and session for user data.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from tilly.config import USER_DATABASE_URL
from tilly.database.users.models import Base

# Create an asynchronous database engine
engine = create_async_engine(
    USER_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    """
    Create the database and tables.

    Example:
    ```python
    # Create the database and tables asynchronously
    await create_db_and_tables()
    ```
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an asynchronous database session.

    Returns:
        AsyncSession: An asynchronous database session.

    Example:
    ```python
    async with get_async_session() as session:
        # Use the database session for asynchronous operations
        user = await session.get(User, user_id)
    ```
    """
    async with Session() as session:
        yield session
