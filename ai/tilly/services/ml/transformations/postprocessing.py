import pandas as pd
import numpy as np
from loguru import logger


def make_all_methods_static(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            setattr(cls, attr_name, staticmethod(attr_value))
    return cls


@make_all_methods_static
class Postprocessor:
    """A class that contains all the postprocessing logic for the
    model output"""

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

    def handle_missing_model(
        room_name: str, room: pd.DataFrame, models: list[str]
    ) -> tuple[list[np.nan], list[np.nan]]:
        """Returns null values for scores and predictions if a model is missing.
        Also, logs a warning message.

        Args:
            room_name (str): Room name
            room (pd.DataFrame): Room data
            models (dict[str, object]): Available models

        Returns:
            tuple[array[np.nan], array[np.nan]]: Scores and predictions
        """
        n_rows = room.shape[0]
        school = room_name.split("_")[0]

        logger.warning(
            f"Model for {room_name} ({school}) not found. Returning null values.\n"
            + f"Available models in registry for {school}:\n"
            + f"{[key for key in models if school in key]}"
        )
        return (np.full(n_rows, np.nan), np.full(n_rows, np.nan))

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
