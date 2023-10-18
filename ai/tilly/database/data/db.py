"""
Snowflake Database Connection Script. 
This script provides functions to establish and manage
a connection to a Snowflake database using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Generator

from tilly.config import SNOWFLAKE_CREDENTIALS, DB_ECHO


# Define your Snowflake connection parameters
SNOWFLAKE_URL = (
    "snowflake://{user}:{password}@{account}"
    "/{database}/{schema}?warehouse={warehouse}&role={role}"
).format(**SNOWFLAKE_CREDENTIALS)

# Create a synchronous engine
engine = create_engine(
    SNOWFLAKE_URL,
    echo=DB_ECHO,
    future=True,
)


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
    with Session(engine) as session:
        yield session
