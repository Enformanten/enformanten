"""
Module for data-related CRUD operations

This module contains functions that handle CRUD 
(Create, Read, Update, Delete)
operations related to the data pipelines of Enformanten.
"""

from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError
from tenacity import retry, retry_if_exception_type, stop_after_attempt
import pandas as pd

from tilly.utils.logger import log_size
from tilly.config import OUTPUT_COLUMNS
from tilly.database.data.db import refresh_session


def retrieve_data(session: Session, table_name: str) -> dict[str, pd.DataFrame]:
    """
    Retrieve Data from a Table and Group by School and Room IDs.

    This function retrieves data from a specified table and groups it by
        a unique identifier
    generated using the 'SKOLE' and 'ID' fields from the table. Each group
        of data is stored in a
    DataFrame, and these DataFrames are then stored in a dictionary.

    Args:
        session (Session): The SQLAlchemy session used to interact with
            the database.
        table_name (str): The name of the table from which to retrieve data.

    Returns:
        dict[str, pd.DataFrame]: A dictionary where each key is a unique
            identifier for a room, and the
        associated value is a DataFrame containing the data for that room.

    Examples:
        ```python
        from sqlalchemy.orm import Session
        import pandas as pd

        # Initialize SQLAlchemy session
        session = Session()

        # Example table name
        table_name = "YourTableName"

        # Retrieve and group data
        data = retrieve_data(session, table_name)

        # Access a specific room's data using its unique identifier
        room_id = "School123_Room456"
        room_data = data.get(room_id)

        if room_data is not None:
            logger.debug(f"Data for room {room_id}:\n{room_data.head()}")
        ```
    """
    logger.debug(f"Retrieving data from {table_name}")

    data = {
        school_room: df
        for school_room, df in (
            session.table(f'"{table_name}"')
            .to_pandas()
            .assign(SKOLE_ID=lambda d: d.SKOLE + "_" + d.ID)
            .pipe(log_size)
            .rename(str, axis="columns")
            .groupby("SKOLE_ID")
        )
    }
    return data


@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(ProgrammingError),
    retry_error_callback=refresh_session,
)
def push_data(rooms: pd.DataFrame, table_name: str, session: Session) -> None:
    """
    Push Data to a Snowflake Table.

    This function pushes a DataFrame to a specified Snowflake table.
    If the operation fails due to a ProgrammingError, the function
    will attempt to retry the operation with a new session.

    Args:
        rooms (pd.DataFrame): The DataFrame containing the data to push.
        table_name (str): The name of the Snowflake table to which data
            should be pushed.
        session (Session): The SQLAlchemy session used for the operation.

    Returns:
        None

    Examples:
        ```python
        import pandas as pd
        from sqlalchemy.orm import Session

        # Initialize SQLAlchemy session
        session = Session()

        # Example DataFrame
        # (See OUTPUT_COLUMNS constant in tilly.config for the
        # required column names)
        rooms = pd.DataFrame({
            'Column1': [1, 2, 3],
            'Column2': ['a', 'b', 'c'],
        })

        # Example table name
        table_name = "YourSnowflakeTable"

        # Push data to Snowflake table
        push_data(rooms, table_name, session)
        ```
    """
    try:
        logger.debug(f"Sending {rooms.shape[0]} rows to {table_name} ..")
        session.write_pandas(
            rooms[OUTPUT_COLUMNS],
            f'"{table_name}"',
            overwrite=False,
            quote_identifiers=False,
        )
    except ProgrammingError as e:
        logger.debug(f"{e} - Retrying with new session ..")
        session.close()  # Explicitly close the session then raise error for retry
        raise e
