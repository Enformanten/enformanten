from loguru import logger
from sqlalchemy.orm import Session
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
from snowflake.connector import connect, SnowflakeConnection

from tilly.config import SCORED_TABLE_NAME, SNOWFLAKE_CREDENTIALS


def get_snowflake_conn() -> SnowflakeConnection:
    return connect(**SNOWFLAKE_CREDENTIALS)


def retrieve_data(session: Session, table: object) -> dict[str, pd.DataFrame]:
    """retrieve all timeslots using sqlalchemy"""
    logger.debug(f"Retrieving data from {table} ..")

    query = session.query(table).statement  # .limit(5000)

    dataf = (
        pd.read_sql(query, session.bind)
        .assign(SKOLE_ID=lambda d: d.SKOLE + "_" + d.ID)
        .rename(str, axis="columns")
    )
    logger.info(f"Retrieved {len(dataf)} rows | {dataf.SKOLE_ID.nunique()} rooms")
    return {school_room: df for school_room, df in dataf.groupby("SKOLE_ID")}


def push_data(rooms: pd.DataFrame, table: object | str = SCORED_TABLE_NAME) -> None:
    logger.debug(f"Sending data to {table} ..")

    output_cols = ["ID", "KOMMUNE", "DATE", "TIME", "ANOMALY_SCORE", "IN_USE"]

    conn = get_snowflake_conn()
    response, *_ = write_pandas(conn=conn, df=rooms[output_cols], table_name=table)
    conn.close()
    return response  # status
