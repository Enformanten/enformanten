import pandas as pd
import numpy as np


class Preprocessor:
    """A class that contains all the preprocessing logic for the
    model input"""

    @classmethod
    def estimate_usage(
        cls, data: pd.DataFrame, usage_coeff=2.1, usage_min=0.1, usage_max=0.4
    ) -> float:
        """Estimates the usage of a given room from the union of
        - booked timeslots: Timeslots within a registered booking, and
        - Scheduled timeslots: TImeslots within the school schema.

        This is used as a prior for our anomaly detection model.

        Args:
            data (pd.DataFrame): Timeslots
            usage_coeff (float, optional): Usage coefficient. Defaults to 2.1.
                This is a heuristic measure used to scale the estimated usage
            usage_min (float, optional): Minimum usage. Defaults to 0.1.
                This is a heuristic lower bound for the net estimated usage of
                a room.
            usage_max (float, optional): Maximum usage. Defaults to 0.4.
                This is a heuristic upper bound for the net estimated usage of
                a room.
        """
        try:
            used_slots = (data["SKEMALAGT"] | data["BOOKET"].fillna(False)).sum()
            used_slots = max(used_slots, usage_min)
            return min(usage_coeff * used_slots / len(data), usage_max)
        except ZeroDivisionError:
            return "auto"

    ####################
    # Pipes
    ####################

    @classmethod
    def cast(cls, df, map):
        return df.astype(map)

    @classmethod
    def merge_dt(cls, df, date, time, name, sep=" "):
        return df.assign(
            **{
                name: lambda d: pd.to_datetime(
                    d[date].astype(str) + sep + d[time].astype(str)
                )
            }
        )

    @classmethod
    def drop_outliers(
        cls, df, bounds: dict[str, tuple[float | None, float | None]]
    ) -> pd.DataFrame:
        """Drop rows where values are outside the given bounds.

        Args:
            df (pd.DataFrame): DataFrame to filter
            named_bounds (dict[str, tuple[float | None, float | None]]): Dictionary
                of column names and their lower and upper bounds. If a bound is None,
                then it is not applied."""

        mask = np.ones(df.shape[0], dtype=bool)

        for col_name, (lo, hi) in bounds.items():
            if lo is not None and hi is not None:
                mask &= (df[col_name].values >= lo) & (df[col_name].values <= hi)
            elif lo is not None:
                mask &= df[col_name].values >= lo
            elif hi is not None:
                mask &= df[col_name].values <= hi
            else:
                raise ValueError(f"Bounds for {col_name} are both None")

        return df[mask]

    @classmethod
    def fill_na(cls, df, cols, values, types):
        """Fill missing values in the given columns with the given values
        and cast to the given types."""
        return df.assign(
            **{
                col: df[col].fillna(value).astype(_type)
                for col, value, _type in zip(cols, values, types)
            }
        )

    @classmethod
    def drop_inactive_ranges(cls, df, range_length=5):
        """Create a new DataFrame that groups by "ID" and
        apply the rolling window calculation. This identifies
        intervals of 5+ rows of identical values"""
        rolling_uniques = (
            df.groupby("ID")["CO2"]
            .rolling(window=range_length)
            .apply(lambda x: x.nunique())
        )
        # Reset index to align with the original DataFrame
        rolling_uniques = rolling_uniques.reset_index(level=0, drop=True)
        # Drop the identified rows
        return df.loc[rolling_uniques != 1]

    @classmethod
    def add_date_range_group(cls, df):
        TIMEdiff = df["DATETIME"].diff().dt.total_seconds() / 60
        df["DATE_RANGE_GROUP"] = TIMEdiff.ne(15).cumsum()
        return df

    @classmethod
    def acceleration_features(cls, df):
        sorted_df = df.sort_values("DATETIME")
        sorted_df = cls.add_date_range_group(
            sorted_df
        )  # Directly call the function here

        return sorted_df.reset_index(drop=True).assign(
            **{
                f"{col}_ACC": lambda d: d.groupby(["DATE_RANGE_GROUP"])[col]
                .ffill()
                .pct_change()
                .fillna(0)
                .replace([np.inf, -np.inf], 0)
                for col in ["CO2", "TEMP", "MOTION", "IAQ"]
            }
        )

    @classmethod
    def preprocess_for_modelling(cls, df):
        """Preprocess the data for modelling"""
        return df.assign(
            # AKTIVITET=lambda d: pd.factorize(d["TIDSPUNKT_TYPE"])[0],
            # DOW=lambda d: d["DATETIME].dt.dayofweek,
            # HOUR=lambda d: d["DATETIME].dt.hour,
            # DAY_TYPE=lambda d: pd.factorize(d["Type"])[0],
            Booket=lambda d: d["BOOKET"].fillna(0.0),
        ).drop(
            columns=[
                "TIDSPUNKT_TYPE",
                "TYPE",
                "DATE_RANGE_GROUP",
                "DAYNAME",
                "NAVN",
            ]
        )

    ####################
    # Featurize input
    # Uses the pipes above
    ####################

    @classmethod
    def featurize(cls, timeslots: pd.DataFrame) -> pd.DataFrame:
        """Feature engineering"""

        timeslots.columns = timeslots.columns.astype(str)

        return (
            timeslots.pipe(cls.merge_dt, date="DATE", time="TIME", name="DATETIME")
            .pipe(cls.cast, map={"BOOKET": bool, "SKEMALAGT": bool})
            .pipe(
                cls.drop_outliers,
                bounds={
                    "CO2": (0, 8000),
                    "TEMP": (-1, 50),
                },
            )
            .pipe(
                cls.fill_na,
                cols=["CO2", "TEMP", "MOTION", "IAQ"],
                values=[487, 20.0, 0.0, 0.03],
                types=[float, float, float, float],
            )
            .pipe(cls.drop_inactive_ranges, range_length=5)
            .pipe(cls.acceleration_features)
            .pipe(cls.preprocess_for_modelling)
        )
