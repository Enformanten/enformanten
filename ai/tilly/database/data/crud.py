from loguru import logger
from sqlalchemy.orm import Session
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
from snowflake.connector import connect, SnowflakeConnection

from tilly.config import SCORED_TABLE_NAME, SNOWFLAKE_CREDENTIALS, OUTPUT_COLUMNS


def get_snowflake_conn() -> SnowflakeConnection:
    return connect(**SNOWFLAKE_CREDENTIALS)


def log_size(df) -> pd.DataFrame:
    logger.info(f"Retrieved {len(df)} rows | {df.SKOLE_ID.nunique()} rooms")
    return df


def retrieve_data(session: Session, table: object) -> dict[str, pd.DataFrame]:
    """retrieve all timeslots using sqlalchemy"""
    logger.debug(f"Retrieving data from {table.__tablename__}")

    query = session.query(table).statement  # .limit(5000)

    return {
        school_room: df
        for school_room, df in (
            pd.read_sql(query, session.bind)
            .pipe(log_size)
            .assign(SKOLE_ID=lambda d: d.SKOLE + "_" + d.ID)
            .rename(str, axis="columns")  # Fixes weird SA bug
            .groupby("SKOLE_ID")
        )
    }


def push_data(rooms: pd.DataFrame, table: object | str = SCORED_TABLE_NAME) -> None:
    logger.debug(f"Sending data to {table} ..")

    conn = get_snowflake_conn()
    response, *_ = write_pandas(conn=conn, df=rooms[OUTPUT_COLUMNS], table_name=table)
    conn.close()
    return response  # status