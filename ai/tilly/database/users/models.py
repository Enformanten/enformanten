"""
User Database Models Script

This script defines database models for user data using
fastapi-users and SQLAlchemy.

"""

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import declarative_base

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    """
    Base class for database models.

    Args:
        DeclarativeBase: Base class for declarative SQLAlchemy
        table definitions.
    """

    __abstract__ = True
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    Database model for user data.

    Args:
        SQLAlchemyBaseUserTableUUID: Base class for fastapi-users
            user table definitions.
        Base: Base class for database models.

    Example:
    ```python
    # Create a new User object
    new_user = User(
        email="example@example.com",
        hashed_password="hashed_password",
        is_active=True
    )
    ```
    """

    __tablename__ = "users"
    pass
