from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from pandas import DataFrame
from loguru import logger

from tilly.database.data import crud
from tilly.database.data.models import UnscoredTimeslots
from tilly.database.data.db import get_session
from tilly.services.ml import ModelRegistry, get_current_registry, Transformer


def prediction_flow(session, model):
    """Runs the prediction flow

    Args:
        session (Session): SQLAlchemy session
        model (Model): Model
        rooms (dict[str, DataFrame]): Rooms

    Returns:
        dict[str, DataFrame]: Scored rooms
    """

    rooms: dict[str, DataFrame] = crud.retrieve_data(session, UnscoredTimeslots)
    scored_rooms: dict[str, DataFrame] = model.predict(rooms)
    combined_rooms: DataFrame = Transformer.combine_frames(rooms, scored_rooms)
    return crud.push_data(combined_rooms)


router = APIRouter()


@router.post("/predict/")
def predict(
    _: Request,
    session: Session = Depends(get_session),
    model_registry: ModelRegistry = Depends(get_current_registry),
):
    logger.debug("Predict endpoint called")
    if model_registry:
        status = prediction_flow(session, model_registry)
        response = f"Scoring sequence completed - Pushed: {status}"
    else:
        response = "No models available - please train first"

    return {"message": response}
