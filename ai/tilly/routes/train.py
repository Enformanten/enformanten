"""
Machine Learning Training Endpoint

This module contains a FastAPI router for initiating machine learning
model training. The actual training is performed by the `train_models`
function from the `tilly.services.ml.trainer` module and dashboard updates
are performed by `update_dashboard` from `tilly.services.dashboard`.
"""

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from loguru import logger
from sqlalchemy.orm import Session
from pandas import DataFrame

from tilly.database.data import crud
from tilly.database.data.models import TrainingTimeslots
from tilly.database.data.db import get_session
from tilly.services.ml.trainer import train_models
from tilly.services.dashboard import update_dashboard

# Initialize FastAPI router
router = APIRouter()


def training_flow(session):
    """
    Initiates the Training Sequence.

    This function retrieves training data, trains machine learning models,
    and updates the dashboard based on the new models.

    Args:
        session (Session): SQLAlchemy session for database interactions.
    """
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
    """
    Initiate Machine Learning Model Training.

    This endpoint initiates the machine learning model training sequence by
    adding the `training_flow` function to the background tasks.

    Args:
        _: Request: FastAPI Request object. Not used, but kept for FastAPI
            dependency injection.
        background_tasks: FastAPI BackgroundTasks for running functions in the
            background.
        session: SQLAlchemy Session object for database interactions
            (injected via FastAPI's dependency system).

    Returns:
        dict: A dictionary containing a message indicating that the training
            sequence has been initialized.

    Examples:
        ```bash
        curl -X POST http://localhost:8000/train
        ```

        This will initiate the training sequence and return:

        ```json
        {
            "message": "Training sequence initialized"
        }
        ```
    """
    background_tasks.add_task(training_flow, session)
    logger.info("Training sequence initialized")
    return {"message": "Training sequence initialized"}
