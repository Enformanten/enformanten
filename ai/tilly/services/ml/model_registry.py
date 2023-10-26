"""
Model Registry Module

This module manages the model registry for machine learning models in the
Tilly system. It contains utilities for training, predicting, and handling
models that are specific to each room.

The `ModelRegistry` is a singleton class that holds a dictionary of trained
models, ensuring only one instance exists across the application.

Modules:
    - update_registry: Function to update the global model registry.
    - get_current_registry: Function to fetch the current model registry.
    - ModelRegistry: Singleton class to manage room-specific models.
"""

from threading import Lock
from typing import Dict
from tqdm import tqdm
from loguru import logger
from pandas import DataFrame

from tilly.services.ml.transformations import Transformer as T
from tilly.config import FEATURES
from tilly.services.ml.model import Model


# Global Variables
####################
# Allows us to access and
# update the global model
####################

current_registry = None


def update_registry(new_registry):
    """Updates the global model registry.

    Args:
        new_registry: The new model registry to set as global.
    """
    global current_registry
    current_registry = new_registry


def get_current_registry():
    """Fetches the current model registry.

    Returns:
        The current model registry instance.
    """
    return current_registry


# ModelRegistry Class
####################


class ModelRegistry:
    """A singleton class representing the model registry.

    This class is responsible for training, fitting, predicting, and managing
    each model. It holds a dictionary of models that are specific to each room.

    Attributes:
        - models (Dict[str, Model]): A dictionary holding room-specific
            machine learning models.

    Methods:
        - train: Train models based on new timeslot data.
        - fit_predict: Train and predict on new room data.
        - predict: Make predictions using pre-trained models.
        - preprocess: Preprocesses the input data for each room.
        - postprocess: Postprocesses the predicted data for each room.
    """

    _instance = None
    _lock = Lock()

    def __new__(cls):
        """Ensures that only one instance of the class exists."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ModelRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initializes an empty model dictionary."""
        self.models: Dict[str, Model] = {}

    def train(self, timeslots: dict[str, DataFrame]) -> None:
        """Train models based on new timeslot data and store them in the registry.

        Args:
            timeslots (dict[str, DataFrame]): The timeslots data to train on,
                per room.
        """
        _preprocessed: dict[str, DataFrame] = self.preprocess(timeslots)
        room_results: dict[str, DataFrame] = self.fit_predict(_preprocessed)
        _postprocessed: dict[str, DataFrame] = self.postprocess(room_results)

        return _postprocessed

    def fit_predict(self, rooms: dict[str, DataFrame]) -> Dict[str, DataFrame]:
        """Train and predict on new room data.

        Args:
            rooms (dict[str, DataFrame]): Room data to fit and predict on.

        Returns:
            Dict[str, DataFrame]: The predicted DataFrame for each room.
        """

        output = {}
        with tqdm(total=len(rooms), desc="Initial") as pbar:
            for name, timeslots in rooms.items():
                pbar.set_postfix_str(f"Running fit_predict | Room: {name}")
                pbar.update(1)

                if not timeslots.empty:
                    features = timeslots[FEATURES]  # extract features
                    model = Model(estimated_usage=0.3).fit(X=features)  # fit model
                    self.models[name] = model  # add model to registry

                    # make predictions
                    output[name]: DataFrame = self._predict(name, timeslots)

        return output

    def predict(self, rooms: dict[str, DataFrame]) -> dict[str, DataFrame]:
        """Make predictions using pre-trained models in the registry.

        Args:
            rooms (dict[str, DataFrame]): Room data to predict on.

        Returns:
            dict[str, DataFrame]: The predicted DataFrame for each room.
        """
        _preprocessed: dict[str, DataFrame] = self.preprocess(rooms)
        _predictions = {
            name: self._predict(name, room)
            for name, room in tqdm(_preprocessed.items())
            if not room.empty
        }
        return self.postprocess(_predictions)

    def _predict(self, name: str, room: DataFrame) -> DataFrame:
        """
        Make predictions for a specific room using its corresponding
          model in the registry.

        Args:
            name (str): The name of the room.
            room (DataFrame): The room data to predict on.

        Returns:
            DataFrame: The predicted DataFrame for the room.
        """

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
        """
        Preprocesses the input timeslot data for each room.

        Args:
            timeslots (dict[str, DataFrame]): The timeslot data for each room.

        Returns:
            dict[str, DataFrame]: The preprocessed DataFrame for each room.
        """
        logger.info("Preprocessing data...")
        return {name: room.pipe(T.featurize) for name, room in tqdm(timeslots.items())}

    def postprocess(self, predictions: dict[str, DataFrame]) -> dict[str, DataFrame]:
        """Postprocesses the prediction results for each room.

        Args:
            predictions (dict[str, DataFrame]): The predicted DataFrame for each room.

        Returns:
            dict[str, DataFrame]: The postprocessed DataFrame for each room.
        """
        logger.info("Postprocessing data...")
        return {
            name: room.pipe(T.heuristics) for name, room in tqdm(predictions.items())
        }
