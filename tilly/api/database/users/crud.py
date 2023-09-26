import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tilly.api.config import USER_DATABASE_URL
from tilly.api.database.users.models import UserBase


executor = ThreadPoolExecutor()

engine = create_async_engine(USER_DATABASE_URL)
Session = sessionmaker(bind=engine.sync_engine)


@asynccontextmanager  # Hack since we rely on sqlalchemy 1.4.49..
async def custom_async_sessionmaker():
    loop = asyncio.get_event_loop()
    session = Session()
    try:
        yield session
    finally:
        await loop.run_in_executor(executor, session.close)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(UserBase.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with custom_async_sessionmaker() as session:
        yield session
