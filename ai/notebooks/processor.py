import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter1d


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
    def add_missing_timeslots(cls, df: pd.DataFrame, freq: str = "15T") -> pd.DataFrame:
        """Adds the rows that are missing from the DataFrame, by merging
        it with a DataFrame containing all the timeslots."""

        static_values = (
            df.head(1)[["ID", "KOMMUNE", "SKOLE", "SKOLE_ID"]].squeeze().to_dict()
        )
        return (
            pd.DataFrame(
                {
                    "DATETIME": pd.date_range(
                        start=df["DATETIME"].min(), end=df["DATETIME"].max(), freq=freq
                    )
                }
            )
            .assign(**static_values)
            .merge(
                df, on=["DATETIME", "ID", "KOMMUNE", "SKOLE", "SKOLE_ID"], how="left"
            )
        )

    @classmethod
    def interpolate_missing_islands(
        cls,
        df: pd.DataFrame,
        *,
        target_col: str = "CO2",
        limit: int = 3,
        direction: str = "forward",
        method: str = "cubic",
        **kwargs,
    ) -> pd.DataFrame:
        """Interpolate missing values in a dataframe, but only for
        islands of missing values, ie. rows where there
        are no more than `limit` consecutive missing values
        in the `target_col` column."""

        return df.assign(
            CO2=lambda d: d[target_col].interpolate(
                method=method,
                limit=limit,
                limit_direction=direction,
                **kwargs,
            )
        )

    @classmethod
    def remove_stagnate_intervals(
        cls, df, target_col: str = "CO2", threshold=4
    ) -> pd.DataFrame:
        """Remove intervals where the CO2 value is the
        same for consecutive rows within time-contiguous blocks"""
        return (
            df.assign(
                time_diff=lambda d: d["DATETIME"].diff(),
                new_block=lambda d: (d["time_diff"] > pd.Timedelta(minutes=15))
                | (d[target_col] != d[target_col].shift(1)),
                block_id=lambda d: d["new_block"].cumsum(),
            )
            .assign(
                block_count=lambda d: d.groupby("block_id")["block_id"].transform(
                    "count"
                )
            )[lambda d: d["block_count"].lt(threshold)]
            .drop(["time_diff", "new_block", "block_id", "block_count"], axis=1)
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
    def calculate_kinematic_quantities(
        cls, df, metric, *, window, prefix=None
    ) -> pd.DataFrame:
        """Add the rolling velocity, acceleration and jerk for a given metric.
        The rolling quantities are calculated using the gradient of the metric and
        the given window size. The resulting null values are filled with zeros"""

        if prefix is None:
            prefix = metric

        return df.assign(
            **{
                # First order derivative of the metric
                f"{prefix}_velocity": lambda d: (
                    d[metric].rolling(window=window).apply(lambda x: np.gradient(x)[-1])
                ),
                # Second order derivative of the metric
                f"{prefix}_acceleration": lambda d: (
                    d[f"{prefix}_velocity"]
                    .rolling(window=window)
                    .apply(lambda x: np.gradient(x)[-1])
                ),
                # Third order derivative of the metric
                f"{prefix}_jerk": lambda d: (
                    d[f"{prefix}_acceleration"]
                    .rolling(window=window)
                    .apply(lambda x: np.gradient(x)[-1])
                ),
                # Log of the metric - Useful for identifying
                # natural diffusion of CO2 from the room
                f"{prefix}_log": lambda d: (d[metric].fillna(0)),
            }
        ).assign(
            **{
                f"{prefix}_velocity": lambda d: (d[f"{prefix}_velocity"].fillna(0)),
                f"{prefix}_acceleration": lambda d: (
                    d[f"{prefix}_acceleration"].fillna(0)
                ),
                f"{prefix}_jerk": lambda d: (d[f"{prefix}_jerk"].fillna(0)),
            }
        )

    @classmethod
    def apply_time_group_funcs(cls, df, funcs) -> pd.DataFrame:
        """Apply a list of functions to each time-contiguous
        block of data in the DataFrame"""

        dataf = (
            df
            # Calculate time_diff and identify new blocks of time
            .assign(time_diff=lambda d: d["DATETIME"].diff())
            .assign(new_block=lambda d: d["time_diff"] > pd.Timedelta(minutes=15))
            .assign(block_id=lambda d: d["new_block"].cumsum())
        )
        for func, kwargs in funcs:
            dataf = (
                dataf.groupby("block_id").apply(func, **kwargs).reset_index(drop=True)
            )
        return dataf.drop(columns=["block_id", "new_block", "time_diff"])

    @classmethod
    def gaussian_smooth(cls, df, metric, *, std_dev):
        """Apply a gaussian filter to a given metric"""
        return df.assign(
            **{
                f"{metric}_smoothed": lambda d: gaussian_filter1d(
                    d[metric], sigma=std_dev
                )
            }
        )

    @classmethod
    def add_time_features(cls, df, *, night_start=23, night_end=6):
        """Add time features to the DataFrame"""
        return df.assign(
            is_night=lambda d: (
                (d["DATETIME"].dt.hour >= night_start)
                & (d["DATETIME"].dt.hour <= night_end)
            ).astype(int),
        )
