"""User Authentication Module for Tilly

This module provides utilities for user authentication and session management 
using FastAPI and JWT (JSON Web Tokens). It uses SQLAlchemy to interact with the
user database.

Main Components:
    - get_user_db: An asynchronous function that yields the SQLAlchemyUserDatabase
        instance tied to the user model.
    
    - UserManager: A class inheriting from BaseUserManager and UUIDIDMixin tha
        provides additional functionalities like handling events after user
        registration. It uses a secret token for both password reset and email
        verification.
    
    - get_user_manager: An asynchronous function that yields an instance of
        UserManager. It depends on get_user_db.
    
    - get_jwt_strategy: A function that returns an instance of JWTStrategy, with
        the secret and lifetime set.
    
    - auth_backend: An instance of AuthenticationBackend, utilizing the JWT 
        strategy and bearer token transport.

    - fastapi_users: An instance of FastAPIUsers that is initialized with the
        UserManager and authentication backend. This is the core utility for 
        user operations like login, registration, and more.
    
    - current_active_user: A dependency that fetches the currently active user.

Logging:
    User-related events such as successful registration are logged using the 
    loguru logger.

Example:
    >>> from tilly.users.auth import fastapi_users, current_active_user
    >>> # Inside FastAPI route
    >>> @app.get("/secure-route", dependencies=[Depends(current_active_user)])
    >>> def secure_route():
    >>>     return {"message": "You have access to this route"}

"""

import uuid
from typing import Optional
from loguru import logger
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.orm import Session

from tilly.config import SECRET
from tilly.database.users.crud import get_async_session
from tilly.database.users.models import User


# to work with user table
async def get_user_db(session: Session = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


# basic class of fastapi-users where additional behaviour can be added
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


# jwt
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# can fetch different types of users
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
