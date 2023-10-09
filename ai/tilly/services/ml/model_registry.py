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
        """
        Singleton pattern implementation, ensuring only one instance exists.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ModelRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the ModelRegistry instance with an empty models dictionary.
        """
        self.models: Dict[str, Model] = {}

    def train(self, timeslots: dict[str, DataFrame]) -> None:
        """
        Train models on new timeslot data and store them in the registry.

        Args:
            timeslots (dict[str, DataFrame]): The timeslots data to train on, per room.
        """
        _preprocessed: dict[str, DataFrame] = self.preprocess(timeslots)
        room_results: dict[str, DataFrame] = self.fit_predict(_preprocessed)
        _postprocessed: dict[str, DataFrame] = self.postprocess(room_results)

        return _postprocessed

    def fit_predict(self, rooms: dict[str, DataFrame]) -> Dict[str, DataFrame]:
        """Train models on new room data and make predictions.

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
        """
        Make predictions using the pre-trained models in the registry.

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
