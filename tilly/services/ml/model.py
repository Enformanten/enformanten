from loguru import logger
from sklearn.ensemble import IsolationForest
from threading import Lock
from typing import Dict
from pandas import DataFrame

import tilly.services.ml.helpers as h
from tilly.config import MODEL_PARAMS, FEATURES

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
        _preprocessed: dict[str, DataFrame] = self.preprocess(timeslots)
        try:
            logger.info("Training model...")

            room_results: dict[str, DataFrame] = self.fit_predict(_preprocessed)

            logger.info("Model trained.")

        except Exception as e:
            logger.error(f"An error occurred while training: {e}")

        return room_results

    def fit_predict(self, rooms: dict[str, DataFrame]) -> Dict[str, DataFrame]:
        output = {}
        # try:
        for name, timeslots in rooms.items():
            logger.info(f"Fitting model for room: {name}")

            # estimate usage coefficient
            usage_coeff = h.estimate_usage(timeslots)

            # fit model
            features = timeslots[FEATURES]
            model_IF = IsolationForest(contamination=usage_coeff, **MODEL_PARAMS)
            model_IF.fit(features)

            # save model to registry
            self.models[name] = model_IF

            # extract scores and predictions
            scores = model_IF.decision_function(features)
            preds = model_IF.predict(features)

            # add scores and predictions to output
            output[name] = timeslots.assign(
                anomaly_score=1 - h.format_scores(scores),
                IN_USE=h.format_predictions(preds),
            )

        # except Exception as e:
        #     logger.error(f"An error occurred in fit_predict: {e}")

        return output

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
        return {name: room.pipe(h.featurize) for name, room in timeslots.items()}

    def _predict(self, timeslots: list[list]) -> list[tuple[int, float]]:
        return timeslots

    def postprocess(self, predictions: dict[str, DataFrame]) -> dict[str, DataFrame]:
        """Postprocess the predictions."""
        return {name: room.pipe(h.heuristics) for name, room in predictions.items()}
