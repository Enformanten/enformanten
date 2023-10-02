import contextlib
from fastapi_users.exceptions import UserAlreadyExists
from sqlalchemy.exc import IntegrityError
from loguru import logger

from tilly.config import USERS
from tilly.database.users.crud import get_async_session
from tilly.users.auth import get_user_db, get_user_manager
from tilly.users.schemas import UserCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: str,
    password: str,
    is_superuser: bool = False,
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                        )
                    )
                    logger.info(f"User created {user}")
    except UserAlreadyExists:
        logger.info(f"User {email} already exists")


async def create_initial_users(users: list = USERS):
    for user in users:
        try:
            user = create_user(
                user.get("email"),
                user.get("password"),
                user.get("is_superuser", False),
            )
            await user
        except IntegrityError:
            pass