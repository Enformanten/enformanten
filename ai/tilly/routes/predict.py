from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from pandas import DataFrame
from loguru import logger

from tilly.database.data import crud
from tilly.database.data.models import UnscoredTimeslots, ScoredTimeslots
from tilly.database.data.db import get_session
from tilly.services.ml import ModelRegistry, get_current_registry, Transformer


def prediction_flow(session, model):
    """Runs the prediction flow

    Args:
        session (Session): Snowpark session
        model (Model): Model

    Returns:
        dict[str, DataFrame]: Scored rooms
    """

    rooms: dict[str, DataFrame] = crud.retrieve_data(
        session, UnscoredTimeslots.__tablename__
    )
    scored_rooms: dict[str, DataFrame] = model.predict(rooms)
    combined_rooms: DataFrame = Transformer.combine_frames(rooms, scored_rooms)
    crud.push_data(
        combined_rooms, table_name=ScoredTimeslots.__tablename__, session=session
    )


router = APIRouter()


@router.post("/predict/")
def predict(
    _: Request,
    session: Session = Depends(get_session),
    model_registry: ModelRegistry = Depends(get_current_registry),
):
    """Hello!"""
    logger.debug("Predict endpoint called")
    if model_registry:
        prediction_flow(session, model_registry)
        response = "Scoring sequence completed."
    else:
        response = "No models available - please train first"

    return {"message": response}
