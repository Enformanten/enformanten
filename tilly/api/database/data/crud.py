from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session
import pandas as pd

import tilly.api.database.data.models as m


def retrieve_training_data(session: Session) -> dict[str, pd.DataFrame]:
    """retrieve all timeslots using sqlalchemy"""
    logger.debug("Getting all data from Timeslots table..")

    query = session.query(m.TrainingTimeslots).statement

    grouped = (
        pd.read_sql(query, session.bind)
        .assign(SKOLE_ID=lambda d: d.SKOLE + "_" + d.ID)
        .groupby("SKOLE_ID")
    )
    return {school_room: df for school_room, df in grouped}


def retrieve_unscored_timeslots(session: Session) -> dict[str, pd.DataFrame]:
    """retrieve all unscored timeslots using sqlalchemy"""
    logger.debug("Getting all data from 'unscored' table..")

    result = session.execute(select(m.UnscoredTimeslots))
    timeslots: list[dict] = [*map(dict, result.fetchall())]
    grouped = (
        pd.DataFrame.from_records(timeslots)
        .assign(SKOLE_ID=lambda d: d.SKOLE + "_" + d.ID)
        .groupby("SKOLE_ID")
    )
    return {school_room: df for school_room, df in grouped}


def send_scored_timeslots(
    session: Session, scored_data: dict[str, pd.DataFrame]
) -> None:
    logger.debug("Sending scored data back to database..")

    combined_df = pd.concat(scored_data.values(), ignore_index=True)
    scored_timeslots_list = combined_df.to_dict(orient="records")

    session.add_all(
        [
            m.ScoredTimeslots(**scored_timeslot)
            for scored_timeslot in scored_timeslots_list
        ]
    )

    # Commit the session to insert the records
    session.commit()
