from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np


class UsageModel:
    @classmethod
    def fit_predict(cls, df, **kwargs) -> tuple:
        model_IF = IsolationForest(**kwargs)
        model_IF.fit(df)

        scores = model_IF.decision_function(df)
        predictions = model_IF.predict(df)
        return scores, predictions

    @classmethod
    def format_predictions(cls, preds: list) -> list:
        return [1 if pred == -1 else 0 for pred in preds]

    @classmethod
    def format_scores(cls, scores: list) -> list:
        """Normalize scores in range [-1, 1] to
        [0, 1] where 1 is most anomalous

        Args:
            scores (list): List of scores
        """
        return np.interp(scores, (min(scores), max(scores)), (0, 1))

    @classmethod
    def run_model(cls, data: pd.DataFrame, features: list, **kwargs) -> pd.DataFrame:
        """Run for every room in every school"""

        scores, predictions = cls.fit_predict(data[features], **kwargs)
        return data.assign(
            usage_score=1 - cls.format_scores(scores),
            in_use=cls.format_predictions(predictions),
        )
