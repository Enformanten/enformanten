from fastapi import Depends, APIRouter, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pandas import DataFrame

from api.database.data import crud
from api.database.data.db import get_async_session
from api.services.ml.model import ModelRegistry, get_current_model


router = APIRouter()


def prediction_flow(session, model: ModelRegistry):
    """Wrapper function for the background task.
    Load unscored data, score it, and sends it back
    to the database."""
    _unscored_data: list[dict[str, DataFrame]] = crud.retrieve_unscored_timeslots(
        session
    )
    _scored_data: list[dict[str, DataFrame]] = model.predict(_unscored_data)
    crud.send_scored_timeslots(session, _scored_data)


@router.post("/predict/")
def predict(
    request: Request,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    model: ModelRegistry = Depends(get_current_model),
):
    if model:
        background_tasks.add_task(prediction_flow, session, model)
        msg = {"message": "Scoring sequence initialized"}
    else:
        msg = {"message": "No model available"}

    return msg
