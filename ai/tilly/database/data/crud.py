"""
Data-related CRUD operations. Everything that deals with IO
to the data pipelines of Enformanten.
"""

from loguru import logger
from sqlalchemy.orm import Session
import pandas as pd
from snowflake.connector.pandas_tools import pd_writer

from tilly.utils.logger import log_size
from tilly.config import SCORED_TABLE_NAME, OUTPUT_COLUMNS


def retrieve_data(session: Session, table: object) -> dict[str, pd.DataFrame]:
    """
    Retrieve all timeslot data from the given table
    using SQLAlchemy. The data is assigned a unique
    ID based on the school and room ID and is then
    grouped by this ID, resulting in a dictionary of
    DataFrames where each DataFrame corresponds to a
    room.

    Args:
        session (Session): The SQLAlchemy session to
            use.
        table (object): The SQLAlchemy table to
            retrieve data from.

    Returns:
        dict[str, pd.DataFrame]: A dictionary of
            DataFrames, where each DataFrame
            corresponds to a room.

    Example:
    ```python
    from sqlalchemy.orm import Session
    from your_module import YourTable  # SQLAlchemy
    import pandas as pd

    # Create an SQLAlchemy session
    # (you should initialize your session as needed)
    session = Session()

    # Replace 'YourTable' with the actual table you
    # want to retrieve data from
    data = retrieve_data(session, YourTable)

    # Access data for a specific room by its unique ID
    # (school ID + room ID)
    room_id = 'School123_Room456'
    room_data = data.get(room_id)

    if room_data is not None:
        # Now you can work with the DataFrame for the
        # specific room
        print(f"Data for room {room_id}:{room_data.head()}")
    ```
    """
    logger.debug(f"Retrieving data from {table.__tablename__}")

    # debug tools:
    query = session.query(table).statement
    # query = session.query(table).limit(1000).statement

    data = {
        school_room: df
        for school_room, df in (
            pd.read_sql(query, session.bind)
            .assign(SKOLE_ID=lambda d: d.SKOLE + "_" + d.ID)
            .pipe(log_size)
            .rename(str, axis="columns")
            .groupby("SKOLE_ID")
        )
    }
    return data


def push_data(
    rooms: pd.DataFrame, session: Session, table: object | str = SCORED_TABLE_NAME
) -> None:
    """
    Send data to a specified Snowflake table using the
    provided DataFrame.

    Args:
        rooms (pd.DataFrame): The DataFrame containing data
            to be sent to the Snowflake table.
        table (object | str): The target Snowflake table
            name or SQLAlchemy table object. Defaults to
            SCORED_TABLE_NAME if not specified.

    Returns:
        None: This function does not return a value.

    Example:
    ```python
    import pandas as pd
    from your_module import YourSnowflakeTable
    from your_module import SCORED_TABLE_NAME
    from your_module import get_snowflake_conn, write_pandas

    # Create or load the DataFrame 'rooms' with data to be
    pushed to the Snowflake table
    rooms = pd.DataFrame(...)  # preparation logic

    # Push the data to the Snowflake table using the default
    # table name (SCORED_TABLE_NAME)
    push_data(rooms)

    # Alternatively, specify a different table name
    # (replace 'YourSnowflakeTable' with your actual table)
    push_data(rooms, YourSnowflakeTable)
    ```
    """
    logger.debug(f"Sending data to {table} ..")

    rooms[OUTPUT_COLUMNS].to_sql(
        table,
        session.bind,
        method=pd_writer,
        if_exists="append",
        index=False,
    )
