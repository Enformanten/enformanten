from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from pandas import DataFrame
from loguru import logger

from tilly.database.data import crud
from tilly.database.data.models import UnscoredTimeslots
from tilly.database.data.db import get_session
from tilly.services.ml.model import ModelRegistry, get_current_model


router = APIRouter()


@router.post("/predict/")
def predict(
    request: Request,
    session: Session = Depends(get_session),
    model: ModelRegistry = Depends(get_current_model),
):
    logger.debug("Predict endpoint called")
    if model:
        rooms: dict[str, DataFrame] = crud.retrieve_data(session, UnscoredTimeslots)
        scored_rooms: dict[str, DataFrame] = model.predict(rooms)
        status: bool = crud.push_data(scored_rooms)

        msg = {"message": f"Scoring sequence completed - Status: {status}"}

    else:
        msg = {"message": "No models available - please train first"}

    return msg
