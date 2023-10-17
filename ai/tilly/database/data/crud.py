"""
Data-related CRUD operations. Everything that deals with IO
to the data pipelines of Enformanten.

Author: [Your Name]
Date: [Date]
"""

from loguru import logger
from sqlalchemy.orm import Session
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
from snowflake.connector import connect, SnowflakeConnection

from tilly.config import SCORED_TABLE_NAME, SNOWFLAKE_CREDENTIALS, OUTPUT_COLUMNS


def get_snowflake_conn() -> SnowflakeConnection:
    """
    Connect to Snowflake using the credentials in the config file.

    Returns:
        SnowflakeConnection: A connection to the Snowflake database.

    Example:
    ```python
    # Get a Snowflake connection
    conn = get_snowflake_conn()

    # Use the connection for database operations
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    ```
    """
    return connect(**SNOWFLAKE_CREDENTIALS)


def log_size(df) -> pd.DataFrame:
    """
    Pandas pipe function to log:
    - The size of the dataframe / number of retrieved rows.
    - The number of unique rooms in the dataframe.

    Args:
        df (pd.DataFrame): The dataframe to log.

    Returns:
        pd.DataFrame: The dataframe.

    Example:
    ```python
    # Apply the log_size function to a DataFrame
    df = df.pipe(log_size)
    ```
    """
    logger.info(f"Retrieved {len(df)} rows | {df.SKOLE_ID.nunique()} rooms")
    return df


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

    # query = session.query(table).statement
    # debug tools:
    # query = session.query(table).limit(5000).statement
    query = session.query(table).statement

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


def push_data(rooms: pd.DataFrame, table: object | str = SCORED_TABLE_NAME) -> None:
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

    conn = get_snowflake_conn()
    response, *_ = write_pandas(conn=conn, df=rooms[OUTPUT_COLUMNS], table_name=table)
    conn.close()
    return response
