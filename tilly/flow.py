import pandas as pd
from datetime import datetime

from tilly.usage import estimate_usage
import tilly.pipes as p
from tilly.config import FEATURES, OUTPUT_COLUMNS


def flow(
    data,
    run_id: str,
    usage_coeff: float,
    usage_limit: float,
    random_state: int,
    apply_rules: bool,
    room_features: list = FEATURES,
):
    for kommune in data["KOMMUNE"].unique():
        print(f"Running flow for {kommune}")

        est_contamination = estimate_usage(
            data, kommune, usage_coeff=usage_coeff, usage_limit=usage_limit
        )

        yield (
            # Processing
            data.pipe(p.filter_values, col="KOMMUNE", values=[kommune])
            .pipe(p.drop_inactive_ranges)
            .pipe(p.acceleration_features)
            .pipe(p.preprocess_for_modelling)
            # Modelling
            .groupby("ID")
            .apply(
                p.UsageModel.run_model,
                features=room_features,
                contamination=est_contamination,
                random_state=random_state,
            )
            .reset_index(drop=True)
            # heuristics
            .pipe(p.add_heuristics, apply_rules=apply_rules)
            # Export plots
            .pipe(p.export_plots, kommune=kommune, run_id=run_id)
            # Postprocess
            [OUTPUT_COLUMNS]
            .assign(KOMMUNE=kommune)
            # Exit report
            .pipe(p.exit_report, kommune=kommune, original_data=data)
        )


def run_flow(**kwargs):
    run_id = f"RUN-{datetime.now().strftime('%Y-%m-%d-%H-%M')}"
    print(f"RUNNING FLOW '{run_id}'\n")

    return {"run_id": run_id, "data": pd.concat(flow(run_id=run_id, **kwargs))}
