from loguru import logger
from sqlalchemy.orm import Session
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas


from tilly.config import SCORED_TABLE_NAME
from tilly.database.data.db import connect, SNOWFLAKE_CREDENTIALS, SnowflakeConnection


def get_snowflake_conn() -> SnowflakeConnection:
    return connect(**SNOWFLAKE_CREDENTIALS)


def retrieve_data(session: Session, table: object) -> dict[str, pd.DataFrame]:
    """retrieve all timeslots using sqlalchemy"""
    logger.debug(f"Retrieving data from {table} ..")

    query = session.query(table).statement

    dataf = pd.read_sql(query, session.bind).assign(
        SKOLE_ID=lambda d: d.SKOLE + "_" + d.ID
    )
    return {school_room: df for school_room, df in dataf.groupby("SKOLE_ID")}


def push_data(
    rooms: dict[str, pd.DataFrame], table: object | str = SCORED_TABLE_NAME
) -> None:
    logger.debug(f"Sending data to {table} ..")

    output_cols = ["ID", "KOMMUNE", "DATE", "TIME", "ANOMALY_SCORE", "IN_USE"]
    rooms_df = pd.concat(rooms.values(), ignore_index=True)[output_cols]

    conn = get_snowflake_conn()
    response, *_ = write_pandas(conn=conn, df=rooms_df, table_name=table)
    conn.close()

    return response  # status

    # session.add_all(
    #     [
    #         table(**room)
    #         for room in rooms_df.to_dict(orient="records")
    #     ]
    # )

    # Commit the session to insert the records
    # session.commit()
