import pandas as pd
import numpy as np

import tilly.services.ml.pipes.preprocessing as prep


def estimate_usage(
    data: pd.DataFrame, usage_coeff=2.1, usage_min=0.1, usage_max=0.4
) -> float:
    try:
        used_slots = (data["SKEMALAGT"] | data["BOOKET"].fillna(False)).sum()
        used_slots = max(used_slots, usage_min)
        return min(usage_coeff * used_slots / len(data), usage_max)
    except ZeroDivisionError:
        return "auto"


def featurize(timeslots: pd.DataFrame) -> pd.DataFrame:
    """Feature engineering"""

    timeslots.columns = timeslots.columns.astype(str)

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


def heuristics(timeslots: pd.DataFrame) -> pd.DataFrame:
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


def combine_frames(
    original: dict[str, pd.DataFrame],
    scored: dict[str, pd.DataFrame],
    merge_cols: list = ["DATE", "TIME", "ID", "KOMMUNE", "SKOLE"],
) -> pd.DataFrame:
    """
    Combines original and scored data into a single pd.DataFrame.

    The function takes two dictionaries, where the keys represent
    room identifiers and the values are Pandas DataFrames containing
    the original and scored data. It enriches the original data with
    the anomaly scores and 'IN_USE' indicators from the scored data.
    If a room does not have corresponding scored data, it will be
    filled with null values in the 'IN_USE' and 'ANOMALY_SCORE' columns.

    Parameters:
    - original (dict[str, pd.DataFrame]): A dictionary containing the
    original data.
      The keys are room identifiers, and the values are pd.DataFrames
    with the original data.
    - scored (dict[str, pd.DataFrame]): A dictionary containing the
    scored data.
      The keys are room identifiers, and the values are pd.DataFrames
    with the anomaly scores and 'IN_USE' indicators.
    - merge_cols (list): The list of column names to use for merging the
    original and scored data.

    Returns:
    - pd.DataFrame: A concatenated DataFrame containing all the enriched
    data.

    """
    combined_frames = []
    for key, orig_df in original.items():
        scored_df = scored.get(key, None)
        if scored_df is not None:
            # Merge based on multiple common columns
            combined_df = orig_df.merge(
                scored_df[["ANOMALY_SCORE", "IN_USE"] + merge_cols],
                how="left",
                on=merge_cols,
            )
        else:
            # If there's no corresponding scored pd.dataframe,
            # copy the original pd.dataframe and add null columns
            # for 'IN_USE' and 'ANOMALY_SCORE'
            combined_df = orig_df.copy()
            combined_df["ANOMALY_SCORE"] = None
            combined_df["IN_USE"] = None

        # Add an identifier for the original key (i.e., room name)
        combined_df["ROOM"] = key

        combined_frames.append(combined_df)

    # Concatenate all frames vertically
    final_combined = pd.concat(combined_frames, ignore_index=True)
    return final_combined
