def estimate_usage(data, kommune, usage_coeff=2.1, usage_limit=0.2):
    df = data[lambda d: d["KOMMUNE"] == kommune]
    est_usage = min(
        usage_coeff
        * (df["SKEMALAGT"].astype(bool) | df["BOOKET"].fillna(0).astype(bool)).sum()
        / df.shape[0],
        usage_limit,
    )
    print(f"Est. usage score {est_usage:.2f} | usage coeff: {usage_coeff:.2f}")
    return est_usage
