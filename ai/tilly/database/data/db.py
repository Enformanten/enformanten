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


def refresh_session(retry_state):
    """Create a new Snowflake session if an error occurs.
    using tenacity's before_retry hook"""
    old_session = retry_state.kwargs.get("session")
    if old_session:
        old_session.close()  # Explicitly close the old session

    with get_session() as new_session:
        retry_state.kwargs["session"] = new_session
