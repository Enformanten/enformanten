from fastapi import APIRouter, BackgroundTasks, Depends, Request
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from pandas import DataFrame

from api.database.data import crud
from api.database.data.db import get_async_session
from api.services.ml.trainer import train_models
from api.services.dashboard import update_dashboard

router = APIRouter()


def wrapper(session):
    training_data: list[dict[str, DataFrame]] = crud.retrieve_training_data(session)
    data_results: list[dict[str, DataFrame]] = train_models(training_data)
    update_dashboard(data_results)


@router.post("/train")
def train(
    request: Request,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
):
    background_tasks.add_task(wrapper, session)

    logger.info("Training sequence initialized")
    return {"message": "Training sequence initialized"}
