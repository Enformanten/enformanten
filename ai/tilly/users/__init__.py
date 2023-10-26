"""
The `users` module handles all user-related functionality including 
authentication, user management, and initial user setup for the 
Tilly application.

The module includes the following scripts:
    - `auth.py`: Contains utilities for user authentication, JWT strategy,
        and user management. Defines the `UserManager` class to handle 
        custom behavior during user registration and implements FastAPI 
        dependencies to get instances of user database and user manager.
    
    - `initial_users.py`: A script that populates the database with initial
        users based on configuration. Handles exceptions for duplicate users
        and other integrity errors.
    
    - `schemas.py`: Defines the schema classes that extend the FastAPI Users
        library schemas for reading, creating, and updating users.

Each of these scripts plays a crucial role in managing user-related operations
and ensures secure and consistent behavior throughout the application.

Example Usage:
    Import UserManager from auth to use in other modules for custom user behavior:
    >>> from users.auth import UserManager

    Import schemas to validate user-related data:
    >>> from users.schemas import UserCreate, UserRead
    
    Use `create_initial_users` function to populate initial users in the database:
    >>> from users.initial_users import create_initial_users
"""
