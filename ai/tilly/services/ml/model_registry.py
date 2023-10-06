from threading import Lock
from typing import Dict
from tqdm import tqdm
from loguru import logger
from pandas import DataFrame

from tilly.services.ml.transformations import Transformer as T
from tilly.services.ml.model import Model
from tilly.config import FEATURES


####################
# Allows us to access and
# update the global model
####################

current_registry = None


def update_registry(new_registry):
    """Updates the global model."""
    global current_registry
    current_registry = new_registry


def get_current_registry():
    return current_registry


####################
# Model class
####################


class ModelRegistry:

    """A singleton class that represents the model registry.

    This class is the core of the machine learning service.
    It is responsible for training, fitting, and predicting
    each model in the registry, including triggering the
    pre- and post-processing steps.

    The model registry holds a dictionary of models (the
    in-memory registry of models) - Each model is specific
    to a room.
    - Once a model is trained, it is added to the
    registry, or overwritten if a prior model exists for the
    room.
    - When a batch prediction initialized, the model is loaded
    from the registry and used to make predictions.

    The __new__ method and the _lock = Lock() are part of
    implementing the Singleton pattern in a thread-safe way.
    The Singleton pattern ensures that a class has only one
    instance and provides a way to access that instance from
    anywhere in the application"""

    _instance = None
    _lock = Lock()

    def __new__(cls):
        """Singleton instance"""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ModelRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.models: Dict[str, Model] = {}

    def train(self, timeslots: dict[str, DataFrame]) -> None:
        """
        Fits the model to the given training data.

        Args:
            timeslots: A list of Timeslot instances.
        """
        _preprocessed: dict[str, DataFrame] = self.preprocess(timeslots)
        room_results: dict[str, DataFrame] = self.fit_predict(_preprocessed)
        _postprocessed: dict[str, DataFrame] = self.postprocess(room_results)

        return _postprocessed

    def fit_predict(self, rooms: dict[str, DataFrame]) -> Dict[str, DataFrame]:
        """Fits the model to the given training data, adds the model to the
        registry, and makes predictions on the input data.

        Args:
            rooms: A list of Timeslot instances in the format of
                {room_name: room_data}

        Returns:
            A dictionary mapping room names to their data w/ predictions added
                as columns.
        """

        output = {}
        with tqdm(total=len(rooms), desc="Initial") as pbar:
            for name, timeslots in rooms.items():
                pbar.set_postfix_str(f"Running fit_predict | Room: {name}")
                pbar.update(1)

                if not timeslots.empty:
                    features = timeslots[FEATURES]  # extract features
                    model = Model().fit(X=features)  # fit model
                    self.models[name] = model  # add model to registry

                    # make predictions
                    output[name]: DataFrame = self._predict(name, timeslots)

        return output

    def predict(self, rooms: dict[str, DataFrame]) -> dict[str, DataFrame]:
        """Runs an inference flow in which the rooms are
        first preprocessed, the predicted on and lastly postprocessed.
        """
        _preprocessed: dict[str, DataFrame] = self.preprocess(rooms)
        _predictions = {
            name: self._predict(name, room)
            for name, room in tqdm(_preprocessed.items())
            if not room.empty
        }
        return self.postprocess(_predictions)

    def _predict(self, name: str, room: DataFrame) -> DataFrame:
        """Make predictions on the input data."""

        # extract features
        features = room[FEATURES]

        # load model from registry
        if model := self.models.get(name):
            # extract scores and predictions
            scores: list[float] = model.score(features)
            preds: list[int] = model.predict(features)

        else:
            scores, preds = T.handle_missing_model(
                room_name=name, room=room, models=self.models.keys()
            )

        return room.assign(
            ANOMALY_SCORE=scores,
            IN_USE=preds,
        )

    def preprocess(self, timeslots: dict[str, DataFrame]) -> dict[str, DataFrame]:
        """Featurize the input data."""
        logger.info("Preprocessing data...")
        return {name: room.pipe(T.featurize) for name, room in tqdm(timeslots.items())}

    def postprocess(self, predictions: dict[str, DataFrame]) -> dict[str, DataFrame]:
        """Postprocess the predictions."""
        logger.info("Postprocessing data...")
        return {
            name: room.pipe(T.heuristics) for name, room in tqdm(predictions.items())
        }
