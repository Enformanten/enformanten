import pandas as pd

from tilly.io_ import DataLoader
from tilly.flow import run_flow
from tilly.config import USAGE_COEFF, USAGE_LIMIT, RANDOM_STATE, APPLY_RULES, DATA_PATH


if __name__ == "__main__":
    _data: pd.DataFrame = DataLoader.load(path=DATA_PATH, steps=["all"])

    #######################
    # RUN FLOW
    #######################

    results: dict = run_flow(
        data=_data,
        usage_coeff=USAGE_COEFF,
        usage_limit=USAGE_LIMIT,
        random_state=RANDOM_STATE,
        apply_rules=APPLY_RULES,
    )

    #######################
    # EXPORT RESULTS
    #######################

    (
        DataLoader.load(
            steps={"merge_dt": dict(date="Date", time="Time", name="DATETIME")},
            print_nans=False,
        )
        .merge(results["data"], on=["DATETIME", "ID", "KOMMUNE"], how="left")[
            ["Date", "TIME", "DATETIME", "ID", "KOMMUNE", "in_use", "usage_score"]
        ]
        .to_csv(f"results/{results['run_id']}/results.csv", index=False)
    )
