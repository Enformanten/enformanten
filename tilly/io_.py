import pandas as pd


class DataLoader:
    SENSOR_COLUMNS = ["CO2", "TEMP", "MOTION", "IAQ", "BOOKET"]

    @classmethod
    def diagnose(cls, df, col, dfunc="unique", **kwargs):
        print(getattr(df[col], dfunc)(**kwargs))
        return df

    @classmethod
    def fill_na(cls, df, cols, values, types):
        return df.assign(
            **{
                col: df[col].fillna(value).astype(_type)
                for col, value, _type in zip(cols, values, types)
            }
            # .fillna(value).astype(_type
            # fillna(method="ffill", limit=2)
        )

    @classmethod
    def display_missing_values(cls, df, display=False):
        if not display:
            for i, munc in df.groupby("KOMMUNE"):
                print(f"Missing values for {i}")
                print(
                    munc
                    # filter between the first and last timeslot of activity
                    .sort_values("DATETIME", ascending=True)[
                        lambda d: d["DATETIME"].between(
                            *(
                                d.dropna(subset=cls.SENSOR_COLUMNS, how="all")[
                                    "DATETIME"
                                ].iloc[[0, -1]]
                            ),
                            inclusive="both",
                        )
                    ]
                    .groupby("ID")[cls.SENSOR_COLUMNS]
                    .apply(lambda x: x.isnull().sum() / len(x))
                    .style.format(precision=2)
                    .background_gradient(cmap="Reds", axis=0, vmin=0, vmax=1)
                )
        return df

    @classmethod
    def merge_dt(cls, df, date, time, name, sep=" "):
        return df.assign(**{name: lambda d: pd.to_datetime(d[date] + sep + d[time])})

    @classmethod
    def drop_cols(cls, df, cols):
        return df.drop(columns=cols, errors="ignore")

    @classmethod
    def full_process(cls, df, print_nans, **kwargs):
        return (
            df.pipe(cls.drop_cols, cols=["KOMMUNE_DATO_LOKALE_TIME"])
            .pipe(cls.diagnose, col="KOMMUNE", dfunc="unique")
            .pipe(cls.merge_dt, date="DATE", time="TIME", name="DATETIME")
            .pipe(cls.display_missing_values, display=print_nans)
            .pipe(
                cls.fill_na,
                cols=cls.SENSOR_COLUMNS[:-1],
                values=[487, 20.0, 0.0, 0.03],
                types=[float, float, float, float],
            )
        )

    @classmethod
    def _load(cls, path):
        return pd.read_csv(path)

    @classmethod
    def load(
        cls, path="data/Skemaer.csv", steps: dict = {}, print_nans=False, **kwargs
    ):
        dataf = cls._load(path)

        if "all" in steps:
            return cls.full_process(dataf, print_nans, **kwargs)

        for func, func_kwargs in steps.items():
            dataf = getattr(cls, func)(dataf, **func_kwargs)

        return dataf
