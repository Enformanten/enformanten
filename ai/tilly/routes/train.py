from fastapi import APIRouter, BackgroundTasks, Depends, Request
from loguru import logger
from sqlalchemy.orm import Session
from pandas import DataFrame

from tilly.database.data import crud
from tilly.database.data.models import TrainingTimeslots
from tilly.database.data.db import get_session
from tilly.services.ml.trainer import train_models
from tilly.services.dashboard import update_dashboard

router = APIRouter()


def training_flow(session):
    training_data: dict[str, DataFrame] = crud.retrieve_data(
        session, TrainingTimeslots.__tablename__
    )
    data_results: dict[str, DataFrame] = train_models(training_data)
    update_dashboard(data_results)


@router.post("/train")
def train(
    _: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    background_tasks.add_task(training_flow, session)
    logger.info("Training sequence initialized")
    return {"message": "Training sequence initialized"}
