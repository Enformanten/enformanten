import pandas as pd
import numpy as np


def cast(df, map):
    return df.astype(map)


def merge_dt(df, date, time, name, sep=" "):
    return df.assign(
        **{
            name: lambda d: pd.to_datetime(
                d[date].astype(str) + sep + d[time].astype(str)
            )
        }
    )


def fill_na(df, cols, values, types):
    return df.assign(
        **{
            col: df[col].fillna(value).astype(_type)
            for col, value, _type in zip(cols, values, types)
        }
    )


def drop_inactive_ranges(df, range_length=5):
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


def add_date_range_group(df):
    TIMEdiff = df["DATETIME"].diff().dt.total_seconds() / 60
    df["DATE_RANGE_GROUP"] = TIMEdiff.ne(15).cumsum()
    return df


def acceleration_features(df):
    sorted_df = df.sort_values("DATETIME")
    sorted_df = add_date_range_group(sorted_df)  # Directly call the function here

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


def preprocess_for_modelling(df):
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
