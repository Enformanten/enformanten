from loguru import logger
from sklearn.ensemble import IsolationForest
from threading import Lock
from typing import Dict, List, Tuple
from pandas import DataFrame

from api.services.ml.helpers import featurize, estimate_usage
from api.config import MODEL_PARAMS, FEATURES

####################
# Keeps track of the current model
####################

current_model = None


def update_model(new_model):
    global current_model
    current_model = new_model


def get_current_model():
    return current_model


####################
# Model class
####################


class ModelRegistry:

    """A singleton class that represents the model. The
    __new__ method and the _lock = Lock() are part of
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
        self.models: Dict[str, IsolationForest] = {}

    def train(self, timeslots: dict[str, DataFrame]) -> None:
        """
        Fits the model to the given training data.

        Args:
            timeslots: A list of Timeslot instances.
        """
        try:
            logger.info("Training model...")

            _preprocessed: dict[str, DataFrame] = self.preprocess(timeslots)
            room_results: dict[str, DataFrame] = self.fit_predict(_preprocessed)

            logger.info("Model trained.")

        except Exception as e:
            logger.error(f"An error occurred while training: {e}")

        logger.info("Model trained.")
        return room_results

    def fit_predict(
        self, rooms: dict[str, DataFrame]
    ) -> Dict[str, Tuple[List[float], List[int]]]:
        try:
            for name, timeslots in rooms.items():
                usage_coeff = estimate_usage(timeslots)

                features = timeslots[FEATURES]
                model_IF = IsolationForest(contamination=usage_coeff, **MODEL_PARAMS)
                model_IF.fit(features)

                self.models[name] = model_IF

                timeslots.assign(anomaly_score=model_IF.decision_function(features))
                timeslots.assign(IN_USE=model_IF.predict(features))

        except Exception as e:
            logger.error(f"An error occurred in fit_predict: {e}")

        return rooms

    def predict(self, timeslots: dict[str, DataFrame]) -> dict[str, DataFrame]:
        """
        Makes a prediction on a single input instance.

        Args:
            X: A single input instance.

        Returns:
            A dictionary mapping class indices to predicted
            probabilities.
        """
        _preprocessed: dict[str, DataFrame] = self.preprocess(timeslots)
        _predictions: dict[str, DataFrame] = self._predict(_preprocessed)
        return self.postprocess(_predictions)

    def preprocess(self, timeslots: dict[str, DataFrame]) -> dict[str, DataFrame]:
        """Featurize the input data."""
        return {
            name: timeslots.pipe(featurize) for name, timeslots in timeslots.items()
        }

    def _predict(self, timeslots: list[list]) -> list[tuple[int, float]]:
        return timeslots

    def postprocess(self, predictions: dict[str, DataFrame]) -> dict[str, DataFrame]:
        return predictions
