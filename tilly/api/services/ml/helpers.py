from pandas import DataFrame


def estimate_usage(
    data: DataFrame, usage_coeff=2.1, usage_min=0.1, usage_max=0.2
) -> float:
    used_slots = (data["SKEMALAGT"] | data["BOOKET"].fillna(False)).sum()
    used_slots = max(used_slots, usage_min)
    return min(usage_coeff * used_slots / len(data), usage_max)


def featurize(timeslots: DataFrame) -> DataFrame:
    """Feature engineering"""

    return (
        timeslots.pipe(drop_inactive_ranges, range_length=5)
        .pipe(acceleration_features)
        .pipe(preprocess_for_modelling)
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
    return df.loc[~rolling_uniques == 1]


def add_date_range_group(df):
    time_diff = df["DATETIME"].diff().dt.total_seconds() / 60
    df["DATE_RANGE_GROUP"] = time_diff.ne(15).cumsum()
    return df


def acceleration_features(df):
    return (
        df.sort_values("DATETIME")
        .apply(add_date_range_group)
        .reset_index(drop=True)
        .assign(
            **{
                f"{col}_ACC": lambda d: d.groupby(["DATE_RANGE_GROUP"])[col]
                .ffill()
                .pct_change()
                .fillna(0)
                for col in ["CO2", "TEMP", "MOTION", "IAQ"]
            }
        )
    )


def preprocess_for_modelling(df):
    return df.assign(
        # AKTIVITET=lambda d: pd.factorize(d["TIDSPUNKT_TYPE"])[0],
        # DOW=lambda d: d["DATETIME"].dt.dayofweek,
        # HOUR=lambda d: d["DATETIME"].dt.hour,
        # DAY_TYPE=lambda d: pd.factorize(d["TYPE"])[0],
        BOOKET=lambda d: d["BOOKET"].fillna(0.0),
    ).drop(
        columns=[
            "TIDSPUNKT_TYPE",
            "TYPE",
            "DATE_RANGE_GROUP",
            "DAYNAME",
            "NAVN",
        ]
    )
