"""
Snowflake Database Connection Script

This module contains functions for establishing and managing connections
to a Snowflake database. It relies on the `snowflake.snowpark` package
to handle the actual database operations.
"""

from typing import Generator
from snowflake.snowpark import Session
from tilly.config import SNOWFLAKE_CREDENTIALS


def get_session() -> Generator[Session, None, None]:
    """
    Get a Snowflake Session for Database Interactions.

    This function yields a Snowflake session for interacting with the
    Snowflake database. The session is yielded as a generator and
    should be used within a 'with' context to ensure
    that resources are managed appropriately.

    Yields:
        Generator[Session, None, None]: A generator yielding a Snowflake
            session object. The session is automatically closed when exiting
            the 'with' context.

    Examples:
        ```python
        from your_module import MyTable  # Replace with actual table class

        with get_session() as session:
            # Perform database operations using the 'session' object
            # Replace 'MyTable' and 'column_name' with actual table and column
            result = session.query(MyTable).filter_by(column_name='value').all()

        # The session is automatically closed when the 'with' block is exited.
        ```
    """
    with Session.builder.configs(SNOWFLAKE_CREDENTIALS).create() as session:
        yield session
