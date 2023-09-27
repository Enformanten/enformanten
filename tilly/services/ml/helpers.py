from pandas import DataFrame
import numpy as np

import tilly.services.ml.pipes.preprocessing as prep


def estimate_usage(
    data: DataFrame, usage_coeff=2.1, usage_min=0.1, usage_max=0.2
) -> float:
    used_slots = (data["SKEMALAGT"] | data["BOOKET"].fillna(False)).sum()
    used_slots = max(used_slots, usage_min)
    return min(usage_coeff * used_slots / len(data), usage_max)


def featurize(timeslots: DataFrame) -> DataFrame:
    """Feature engineering"""
    return (
        timeslots.pipe(prep.merge_dt, date="DATE", time="TIME", name="DATETIME")
        .pipe(prep.cast, map={"BOOKET": bool, "SKEMALAGT": bool})
        .pipe(prep.drop_outliers, cols=["CO2", "TEMP"])
        .pipe(
            prep.fill_na,
            cols=["CO2", "TEMP", "MOTION", "IAQ"],
            values=[487, 20.0, 0.0, 0.03],
            types=[float, float, float, float],
        )
        .pipe(prep.drop_inactive_ranges, range_length=5)
        .pipe(prep.acceleration_features)
        .pipe(prep.preprocess_for_modelling)
    )


def heuristics(timeslots: DataFrame) -> DataFrame:
    """Add heuristic rules to predicted data"""
    return (
        timeslots.assign(
            IN_USE=lambda d: np.where(
                d["CO2"].lt(400),
                0,
                d["IN_USE"],
            ),
        )
        .assign(  # Remove anomalies when CO2 accelerates or CO2 is high
            IN_USE=lambda d: np.where(
                (d["CO2_ACC"].gt(0) & d["CO2"].gt(600)) | (d["CO2"].gt(1000)),
                1,
                d["IN_USE"],
            )
        )
        .assign(
            # If the prior rules change the IN_USE value, then
            # update the usage score to reflect this change
            ANOMALY_SCORE=lambda d: np.where(
                (d["IN_USE"].eq(1) & d["ANOMALY_SCORE"].lt(0.5))
                | (d["IN_USE"].eq(0) & d["ANOMALY_SCORE"].gt(0.5)),
                1 - d["ANOMALY_SCORE"],
                d["ANOMALY_SCORE"],
            )
        )
    )


def format_predictions(preds: list) -> list:
    return [1 if pred == -1 else 0 for pred in preds]


def format_scores(scores: list) -> list:
    """Normalize scores in range [-1, 1] to
    [0, 1] where 1 is most anomalous

    Args:
        scores (list): List of scores
    """
    return np.interp(scores, (min(scores), max(scores)), (0, 1))
