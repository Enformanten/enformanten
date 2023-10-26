"""Initial Users Module for Tilly

This module provides utilities for creating initial users in the Tilly
application. It makes use of FastAPI Users and SQLAlchemy for user creation
and database interaction.

Main Components:
    - get_async_session_context: An asynchronous context manager for getting an
        SQLAlchemy async session.
    
    - get_user_db_context: An asynchronous context manager for getting the
        SQLAlchemy user database instance.
    
    - get_user_manager_context: An asynchronous context manager for getting the
        UserManager instance.
    
    - create_user: An asynchronous function responsible for creating a new user.
        It takes in the email, password, and superuser status as 
        arguments. It also handles UserAlreadyExists exceptions and
        logs relevant information.
                   
    - create_initial_users: An asynchronous function that iterates through a list
        of user details and creates them.
        It catches and handles IntegrityError exceptions.

Logging:
    User creation events, as well as exceptions, are logged using the 
    loguru logger.

Example:
    >>> from tilly.users.initial_users import create_initial_users
    >>> await create_initial_users([
    >>>     {'email': 'admin@example.com', 'password': 'password', 
    >>>      'is_superuser': True},
    >>>     {'email': 'user@example.com', 'password': 'password'}
    >>> ])

"""


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
    """
    Asynchronously creates a new user.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.
        is_superuser (bool, optional): A flag that denotes if the user is a
            superuser. Defaults to False.

    Returns:
        None: Returns None but logs the user creation event.

    Exceptions:
        UserAlreadyExists: Logs an info-level message stating that the user
            already exists.

    Example:
        >>> await create_user('example@example.com', 'example_password',
        >>> is_superuser=True)
    """
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
    """
    Asynchronously creates initial users based on the provided list.

    Args:
        users (list, optional): A list of dictionaries containing user details
            like email, password, and is_superuser.
            Defaults to a list from the configuration.

    Returns:
        None: Returns None but logs the user creation events.

    Exceptions:
        IntegrityError: Catches and ignores the IntegrityError to ensure the
        rest of the users are still created.

    Example:
        >>> await create_initial_users([
        >>>     {'email': 'admin@example.com', 'password': 'password',
        >>>      'is_superuser': True},
        >>>     {'email': 'user@example.com', 'password': 'password'}
        >>> ])
    """
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
