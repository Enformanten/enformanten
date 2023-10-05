from pandas import DataFrame
from numpy import interp
from sklearn.ensemble import IsolationForest

from ai.tilly.config import MODEL_PARAMS


class Model:
    def __init__(
        self, estimated_usage: str | float = "auto", model_params=MODEL_PARAMS
    ):
        self.model = IsolationForest(
            contamination=estimated_usage,
            **model_params,
            # n_jobs=-1,
        )

    def fit(self, X: DataFrame) -> "Model":
        self.model.fit(X)
        return self

    def predict(self, X: DataFrame) -> list[float]:
        """Predicts whether a given room is anomalous or not.
        Returns 1 if anomalous, 0 if not.
        """
        y_hats = self.model.predict(X)
        return [1 if y_hat == -1 else 0 for y_hat in y_hats]

    def score(self, X: DataFrame) -> list[float]:
        """Calculates the anomaly scores for each room and
        returns the normalized scores.
        """
        y_hat = self.model.decision_function(X)
        return 1 - interp(y_hat, (min(y_hat), max(y_hat)), (0, 1))
