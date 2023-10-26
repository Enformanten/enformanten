from pandas import DataFrame
from numpy import interp
from sklearn.ensemble import IsolationForest
from tilly.config import MODEL_PARAMS


class Model:
    def __init__(
        self, estimated_usage: str | float = "auto", model_params=MODEL_PARAMS
    ):
        """Initializes the Model instance with the given parameters.

        Args:
            estimated_usage (str | float, optional): The contamination factor for
                the IsolationForest model. Defaults to "auto".
            model_params (dict, optional): Additional parameters for the
                IsolationForest model. Defaults to MODEL_PARAMS.

        Returns:
            None
        """
        self.model = IsolationForest(
            contamination=estimated_usage,
            **model_params,
        )

    def fit(self, X: DataFrame) -> "Model":
        """Fits the model with the given features.

        Args:
            X (DataFrame): The feature matrix to train on.

        Returns:
            Model: The trained model instance.
        """
        self.model.fit(X)
        return self

    def predict(self, X: DataFrame) -> list[float]:
        """Predicts whether each data point is anomalous or not.

        Returns 1 if the point is an outlier, and 0 otherwise.

        Args:
            X (DataFrame): The feature matrix to predict on.

        Returns:
            list[float]: A list of prediction results.
        """
        y_hats = self.model.predict(X)
        return [1 if y_hat == -1 else 0 for y_hat in y_hats]

    def score(self, X: DataFrame) -> list[float]:
        """Calculates and returns the normalized anomaly scores for each data point.

        Args:
            X (DataFrame): The feature matrix to score.

        Returns:
            list[float]: A list of normalized anomaly scores.
        """
        y_hat = self.model.decision_function(X)
        return 1 - interp(y_hat, (min(y_hat), max(y_hat)), (0, 1))
