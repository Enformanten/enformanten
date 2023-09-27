import pandas as pd


def filter_values(df, col, values):
    return df[lambda d: d[col].isin(values)]


def drop_inactive_ranges(df, range_length=5):
    # Identify intervals of 5+ rows of identical values
    to_drop = df.groupby("ID")["CO2"].transform(
        lambda x: x.rolling(range_length).apply(lambda d: d.nunique() == 1)
    )
    cdataf = df.drop(index=to_drop[lambda d: d.eq(1.0)].index)
    print(
        f"Turns {df.shape[0]} rows into {cdataf.shape[0]} rows "
        + "- Dropping {(df.shape[0] - cdataf.shape[0])/1000}K rows"
    )
    return cdataf


def add_date_range_group(grp):
    grp["Date_RANGE_GROUP"] = grp["DATETIME"].transform(
        lambda x: (x.diff().dt.total_seconds() / 60).ne(15).cumsum()
    )
    return grp


def acceleration_features(df):
    return (
        df.sort_values("DATETIME")
        .groupby("ID")
        .apply(add_date_range_group)
        .reset_index(drop=True)
        .assign(
            CO2_ACC=lambda d: d.groupby(["ID", "Date_RANGE_GROUP"])["CO2"]
            .ffill()
            .pct_change()
            .fillna(0),
            TEMP_ACC=lambda d: d.groupby(["ID", "Date_RANGE_GROUP"])["TEMP"]
            .ffill()
            .pct_change()
            .fillna(0),
            MOTION_ACC=lambda d: d.groupby(["ID", "Date_RANGE_GROUP"])["MOTION"]
            .ffill()
            .pct_change()
            .fillna(0),
            IAQ_ACC=lambda d: d.groupby(["ID", "Date_RANGE_GROUP"])["IAQ"]
            .ffill()
            .pct_change()
            .fillna(0),
        )
    )


def preprocess_for_modelling(df):
    return df.assign(
        AKTIVITET=lambda d: pd.factorize(d["TIDSPUNKT_TYPE"])[0],
        DOW=lambda d: d["DATETIME"].dt.dayofweek,
        HOUR=lambda d: d["DATETIME"].dt.hour,
        DAY_TYPE=lambda d: pd.factorize(d["Type"])[0],
        Booket=lambda d: d["Booket"].fillna(0.0),
    ).drop(
        columns=[
            "Date",
            "TIDSPUNKT_TYPE",
            "TYPE",
            "Date_RANGE_GROUP",
            "Dayname",
            "TIME",
            "SKOLE",
            "KOMMUNE",
            "Navn",
        ]
    )
