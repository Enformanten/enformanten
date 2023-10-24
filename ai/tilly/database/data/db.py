"""
Snowflake Database Connection Script. 
This script provides functions to establish and manage
a connection to a Snowflake database.
"""

from typing import Generator
from snowflake.snowpark import Session

from tilly.config import SNOWFLAKE_CREDENTIALS


# # Create a synchronous engine
# engine = create_engine(
#     SNOWFLAKE_URL,
#     echo=DB_ECHO,
#     future=True,
#     connect_args={
#         'client_session_keep_alive': True,
#     }
# )

# engine = Session.builder.configs(SNOWFLAKE_CREDENTIALS)


def get_session() -> Generator[Session, None, None]:
    """
    Get a SQLAlchemy session for interacting with the Snowflake database.

    Yields:
        Generator[Session, None, None]: A generator yielding SQLAlchemy sessions.
            The session should be used within a 'with' context.

    Example:
    ```python
    with get_session() as session:
        # Perform database operations using the 'session' object
        result = session.query(MyTable).filter_by(column_name='value').all()
    # The session is automatically closed when the 'with' block is exited.
    ```
    """
    with Session.builder.configs(SNOWFLAKE_CREDENTIALS).create() as session:
        yield session
