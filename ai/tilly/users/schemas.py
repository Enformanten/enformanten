"""
This script defines the schema classes for user-related operations.
These schemas extend the base user schemas provided by the FastAPI Users
library. These classes are utilized by other modules for data validation
and serialization when handling user-related operations such as registration,
login, and updating user details.

The script contains the following classes:
    - UserRead: Schema for reading user details.
    - UserCreate: Schema for creating a new user.
    - UserUpdate: Schema for updating an existing user's details.
"""

import uuid
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """
    Schema for reading user details. Extends the BaseUser schema provided
    by FastAPI Users.

    Attributes:
        Inherits all attributes from schemas.BaseUser.

    Example:
        >>> read_user = UserRead(email="example@example.com",
        >>> id=uuid.UUID("some-uuid"))
    """

    pass


class UserCreate(schemas.BaseUserCreate):
    """
    Schema for creating a new user. Extends the BaseUserCreate schema provided
    by FastAPI Users.

    Attributes:
        Inherits all attributes from schemas.BaseUserCreate.

    Example:
        >>> create_user = UserCreate(email="example@example.com",
        >>> password="example_password")
    """

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """
    Schema for updating an existing user's details. Extends the
    BaseUserUpdate schema provided by FastAPI Users.

    Attributes:
        Inherits all attributes from schemas.BaseUserUpdate.

    Example:
        >>> update_user = UserUpdate(email="new_example@example.com")
    """

    pass
