import pandas as pd
import numpy as np
from loguru import logger


def make_all_methods_static(cls):
    """Decorator to make all methods in a class static."""
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            setattr(cls, attr_name, staticmethod(attr_value))
    return cls


@make_all_methods_static
class Postprocessor:

    """
    Postprocessor for handling and enhancing model output data.

    This class contains a series of static methods intended for
    postprocessing the output of predictive models. These methods
    apply heuristic rules to DataFrames containing room usage
    information and anomaly scores, handle cases where predictive
    models are missing, and combine original and scored data into
    enriched DataFrames.

    Methods
    -------
    heuristics(cls, room: pd.DataFrame) -> pd.DataFrame:
        Applies heuristic rules to modify the predicted data in a
        DataFrame representing room usage. It has the following rules:
        - Night Time Filtering: Filters out false positives during
        midnight to 6 AM.
        - Stand-Alone Instances: Removes isolated instances of "IN_USE"
          being 1.
        - Low CO2 Levels: Sets "IN_USE" to 0 if CO2 levels are low.
        The method also updates the "ANOMALY_SCORE" based on the modified
          "IN_USE" values.

    handle_missing_model(room_name: str, room: pd.DataFrame,
        models: list[str]) -> tuple[list[np.nan], list[np.nan]]:
        Returns null values for anomaly scores and predictions if the
        predictive model
        for a room is missing. It also logs a warning message about the
          missing model.

    combine_frames(original: dict[str, pd.DataFrame],
        scored: dict[str, pd.DataFrame],
        merge_cols: list = ["DATE", "TIME", "ID", "KOMMUNE", "SKOLE"])
        -> pd.DataFrame:
        Merges the original data and the scored data for each room into
          a single DataFrame.
        If a room does not have corresponding scored data, it will be filled
          with null values
        in the 'IN_USE' and 'ANOMALY_SCORE' columns.

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'DATETIME': pd.date_range(start='2022-01-01', periods=4,
      freq='15T'),
    ...     'ANOMALY_SCORE': [0.2, 0.8, 0.5, 0.7],
    ...     'IN_USE': [0, 1, 1, 0],
    ...     'CO2': [300, 400, 500, 200]
    ... })
    >>> processed_df = Postprocessor.heuristics(df)

    """

    @classmethod
    def heuristics(cls, room: pd.DataFrame) -> pd.DataFrame:
        """
        Apply heuristic rules to modify the predicted data in a room
          DataFrame.

        This class method applies a series of heuristic rules to a DataFrame
          containing
        predicted room usage and anomaly scores. The rules are applied in the
        following order:

        1. Night Time Filtering: If the time is between midnight and 6 AM and
          the
        anomaly score is less than or equal to 0.7, set "IN_USE" to 0.

        2. Stand-Alone Instances: If an instance of "IN_USE" being 1 is surrounded
        by instances of "IN_USE" being 0, set that isolated "IN_USE" to 0.

        3. Low CO2 Levels: If the CO2 level is less than or equal to 325, set
        "IN_USE" to 0.

        The anomaly score is then updated based on the modified "IN_USE" values.

        Parameters
        ----------
        cls : class
            The class to which this class method belongs.
        room : pd.DataFrame
            Input DataFrame containing at least the following columns:
            - "DATETIME": Timestamps for each 15-minute interval.
            - "ANOMALY_SCORE": Anomaly scores ranging from 0 to 1.
            - "IN_USE": Binary values indicating room usage (1 for in use,
              0 for not in use).
            - "CO2": CO2 levels.

        Returns
        -------
        pd.DataFrame
            Modified DataFrame after applying the heuristic rules.

        Examples
        --------
        >>> df = pd.DataFrame({
        ...     'DATETIME': pd.date_range(start='2022-01-01', periods=4,
        freq='15T'),
        ...     'ANOMALY_SCORE': [0.2, 0.8, 0.5, 0.7],
        ...     'IN_USE': [0, 1, 1, 0],
        ...     'CO2': [300, 400, 500, 200]
        ... })
        >>> Postprocessor.heuristics(df)
        """

        def apply_night_time_filter(df):
            """Filters out false positives during midnight to 6 AM."""
            hour = df["DATETIME"].dt.hour
            mask = (hour >= 0) & (hour < 6) & (df["ANOMALY_SCORE"] <= 0.7)
            df.loc[mask, "IN_USE"] = 0
            return df

        def apply_stand_alone_instances_filter(df):
            """Removes isolated instances of "IN_USE" being 1."""
            prev_IN_USE = df["IN_USE"].shift(1, fill_value=0)
            next_IN_USE = df["IN_USE"].shift(-1, fill_value=0)
            mask = (prev_IN_USE == 0) & (df["IN_USE"] == 1) & (next_IN_USE == 0)
            df.loc[mask, "IN_USE"] = 0
            return df

        def apply_low_co2_filter(df):
            """Sets "IN_USE" to 0 if CO2 levels are low."""
            mask = df["CO2"] <= 325
            df.loc[mask, "IN_USE"] = 0
            return df

        def update_anomaly_score(df):
            """Updates the anomaly score based on the modified
            "IN_USE" values."""
            mask = ((df["IN_USE"] == 1) & (df["ANOMALY_SCORE"] < 0.5)) | (
                (df["IN_USE"] == 0) & (df["ANOMALY_SCORE"] > 0.5)
            )
            df.loc[mask, "ANOMALY_SCORE"] = 1 - df.loc[mask, "ANOMALY_SCORE"]
            return df

        return (
            room.pipe(apply_night_time_filter)
            .pipe(apply_stand_alone_instances_filter)
            .pipe(apply_low_co2_filter)
            .pipe(update_anomaly_score)
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

        Args:
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
        return pd.concat(combined_frames, ignore_index=True)
