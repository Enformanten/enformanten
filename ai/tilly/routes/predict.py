"""
Prediction Endpoint for Tilly Service

This module contains a FastAPI router for serving an endpoint that performs
predictions based on unscored timeslots. The data is processed, predicted,
and then stored back into the database as scored timeslots.
"""

from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from pandas import DataFrame
from loguru import logger

from tilly.database.data import crud
from tilly.database.data.models import UnscoredTimeslots, ScoredTimeslots
from tilly.database.data.db import get_session
from tilly.services.ml import ModelRegistry, get_current_registry, Transformer


def prediction_flow(session: Session, model: ModelRegistry) -> None:
    """
    Run the Prediction Workflow.

    This function orchestrates the steps for the prediction workflow, including
    data retrieval, prediction, and data storage.

    Args:
        session (Session): SQLAlchemy session to the Snowflake database.
        model (ModelRegistry): Machine Learning model for performing the predictions.

    Examples:
        ```python
        from tilly.database.data.db import get_session
        from tilly.services.ml import get_current_registry

        with get_session() as session:
            model_registry = get_current_registry()
            prediction_flow(session, model_registry)
        ```
    """
    rooms: dict[str, DataFrame] = crud.retrieve_data(
        session, UnscoredTimeslots.__tablename__
    )
    scored_rooms: dict[str, DataFrame] = model.predict(rooms)
    combined_rooms: DataFrame = Transformer.combine_frames(rooms, scored_rooms)
    crud.push_data(
        combined_rooms, table_name=ScoredTimeslots.__tablename__, session=session
    )


# Initialize FastAPI router
router = APIRouter()


@router.post("/predict/")
def predict(
    _: Request,
    session: Session = Depends(get_session),
    model_registry: ModelRegistry = Depends(get_current_registry),
):
    """
    Initiatie prediction of room-specific ML models for all rooms in data source.
    The endpoint triggers a process to retrieve the unscored rooms, scores them
    using the designated room-specific machine learning model, and stores the
    scored data back into the database.

    Calls the `prediction_flow` function as a async background task.

    **NOTE**: Authentication is required for this endpoint.

    Args:

        request: The FastAPI request object. This argument is currently not used.

        session (Session, optional): SQLAlchemy session. Defaults to a new
            session from `get_session`.

        model_registry (ModelRegistry, optional): ML model registry. Defaults to
            the current model from `get_current_registry`.

    Returns:

        dict: A message indicating the completion status of the scoring sequence.


    Examples:
        ```bash
        curl -X POST http://localhost:8000/predict/
        ```

    Output:
        ```json
        {
            "message": "Scoring sequence completed."
        }
        ```
    """
    logger.debug("Predict endpoint called")
    if model_registry:
        prediction_flow(session, model_registry)
        response = "Scoring sequence completed."
    else:
        response = "No models available - please train first"

    return {"message": response}
