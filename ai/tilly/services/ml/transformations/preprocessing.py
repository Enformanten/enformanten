import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter1d
from loguru import logger

from tilly.utils import log_pipeline


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
    @log_pipeline
    def merge_dt(cls, df, date, time, name, sep=" "):
        return df.assign(
            **{
                name: lambda d: pd.to_datetime(
                    d[date].astype(str) + sep + d[time].astype(str)
                )
            }
        )

    @classmethod
    @log_pipeline
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
    @log_pipeline
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

        try:
            return df.assign(
                CO2=lambda d: d[target_col].interpolate(
                    method=method,
                    limit=limit,
                    limit_direction=direction,
                    **kwargs,
                )
            )
        except ValueError:
            logger.warning(
                f"[{df.iloc[0]['SKOLE_ID']}] "
                + "Interpolation failed, falling back to linear"
            )
            return df.assign(
                CO2=lambda d: d[target_col].interpolate(
                    method="linear",
                    limit=limit,
                    limit_direction=direction,
                    **kwargs,
                )
            )

    @classmethod
    @log_pipeline
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
    @log_pipeline
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
    @log_pipeline
    def day_filter(cls, df: pd.DataFrame, *, min_ratio: float = 0.25) -> pd.DataFrame:
        """Filter out days with too few data points
        (days with less than min_ratio of the data points).
        This is done to avoid overfitting on days with too
        few data points,where the kinematic quantities are
        not calculated correctly.
        Min ratio is multiplied by 4*24 to get the number of
        data points required for a day (4*24 is the number of
        15 minute intervals in a day)

        Args:
            df (pd.DataFrame): DataFrame to filter
            min_ratio (float, optional): Minimum ratio of data points
                required for a day. Defaults to 0.25.

        Returns:
            df (pd.DataFrame): Filtered DataFrame
        """
        min_data_points_required = int(min_ratio * (4 * 24))
        return df.groupby("DATE").filter(lambda x: len(x) >= min_data_points_required)

    @classmethod
    def calculate_kinematic_quantities(
        cls, df, metric, *, window, prefix=None
    ) -> pd.DataFrame:
        """Add rolling velocity, acceleration, and jerk for a metric.
        The rolling quantities are calculated using the gradient of the
        metric and the given window size. Null values are filled with zeros."""

        if prefix is None:
            prefix = metric

        # Calculate the rolling window mean for the metric
        rolling_metric = df[metric].rolling(window=window).mean()

        # First order derivative (velocity)
        df[f"{prefix}_velocity"] = rolling_metric.diff()

        # Second order derivative (acceleration)
        df[f"{prefix}_acceleration"] = df[f"{prefix}_velocity"].diff()

        # Third order derivative (jerk)
        df[f"{prefix}_jerk"] = df[f"{prefix}_acceleration"].diff()

        # Log of the metric
        df[f"{prefix}_log"] = np.log(df[metric].fillna(1) + 1)

        # Fill NAs
        fill_cols = [f"{prefix}_velocity", f"{prefix}_acceleration", f"{prefix}_jerk"]
        df[fill_cols] = df[fill_cols].fillna(0)

        return df

    @classmethod
    def gaussian_smooth(cls, df, metric, *, std_dev=2):
        """Apply a gaussian filter to a given metric"""
        df[f"{metric}_smoothed"] = gaussian_filter1d(df[metric], sigma=std_dev)
        return df

    @classmethod
    @log_pipeline
    def apply_time_group_funcs(cls, df, funcs) -> pd.DataFrame:
        """Apply a list of functions to each time-contiguous
        block of data in the DataFrame"""

        # Calculate all the needed columns in one go
        df["time_diff"] = df["DATETIME"].diff()
        df["new_block"] = df["time_diff"] > pd.Timedelta(minutes=15)
        df["block_id"] = df["new_block"].cumsum()

        for func, kwargs in funcs:
            df = df.groupby("block_id").apply(func, **kwargs).reset_index(drop=True)
        df.drop(columns=["block_id", "new_block", "time_diff"], inplace=True)
        return df

    @classmethod
    @log_pipeline
    def add_time_features(cls, df, *, night_start=23, night_end=6):
        """Add time features to the DataFrame"""
        return df.assign(
            is_night=lambda d: (
                (d["DATETIME"].dt.hour >= night_start)
                & (d["DATETIME"].dt.hour <= night_end)
            ).astype(int),
        )

    @classmethod
    @log_pipeline
    def featurize(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Run the full preprocessing flow on a DataFrame"""
        return (
            df.pipe(cls.merge_dt, date="DATE", time="TIME", name="DATETIME")
            .pipe(cls.add_missing_timeslots)
            .pipe(cls.interpolate_missing_islands, target_col="CO2", limit=4)
            .pipe(cls.remove_stagnate_intervals, target_col="CO2", threshold=5)
            .dropna(subset=["CO2"])
            .pipe(cls.drop_outliers, bounds={"CO2": (1, 8000)})
            .pipe(cls.day_filter, min_ratio=0.25)
            .pipe(
                cls.apply_time_group_funcs,
                funcs=[
                    (cls.gaussian_smooth, dict(metric="CO2", std_dev=2)),
                    (
                        cls.calculate_kinematic_quantities,
                        dict(metric="CO2_smoothed", window=4, prefix="CO2"),
                    ),
                ],
            )
            .pipe(cls.add_time_features, night_start=22, night_end=6)
        )
