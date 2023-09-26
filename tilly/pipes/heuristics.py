import numpy as np


def add_heuristics(data, apply_rules):
    return (
        data
        if not apply_rules
        else (
            data.assign(
                IN_USE=lambda d: np.where(
                    d["CO2"].lt(600),
                    0,
                    d["IN_USE"],
                ),
            )
            .assign(  # Remove anomalies when CO2 accelerates or CO2 is high
                IN_USE=lambda d: np.where(
                    (d["CO2_ACC"].gt(0.01) & d["CO2"].gt(600)) | (d["CO2"].gt(1400)),
                    1,
                    d["IN_USE"],
                )
            )
            .assign(
                # Combine single usages - 1 IF n-1 = 1, n = 0, n+1 = 1, n+2 = 1
                # Use for cases with a premature prediction of use
                IN_USE=lambda d: np.where(
                    d["IN_USE"].shift(-1).eq(1)
                    & d["IN_USE"].eq(0)
                    & d["IN_USE"].shift(1).eq(1)
                    & d["IN_USE"].shift(2).eq(1),
                    1,
                    d["IN_USE"],
                )
            )
            .assign(
                # Remove single IN_USE - 0 IF n-1 = 0, n = 1, n+1 = 0
                IN_USE=lambda d: np.where(
                    d["IN_USE"].shift(-1).eq(0)
                    & d["IN_USE"].eq(1)
                    & d["IN_USE"].shift(1).eq(0),
                    0,
                    d["IN_USE"],
                )
            )
        )
    )
