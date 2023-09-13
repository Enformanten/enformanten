def exit_report(df, kommune, original_data):
    original = original_data[lambda d: d["KOMMUNE"] == kommune]
    print(
        f"EXIT REPORT - {kommune} | Size: {df.shape[0]} | "
        + f"Orig. size: {original.shape[0]}\n"
        + f"Mean usage rate: {df['in_use'].mean():.2f} | "
        + f"Mean usage score: {df['usage_score'].mean():.2f}\n"
        + "\n\n"
    )
    assert df["ID"].nunique() == original["ID"].nunique(), "Flow dropped rooms!"
    return df
