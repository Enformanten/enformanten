from pathlib import Path


def create_dir(run_id, _KOMMUNE) -> None:
    Path(f"results/{run_id}/{_KOMMUNE}").mkdir(parents=True, exist_ok=True)


def export_plots(data, KOMMUNE, run_id):
    for i, room in data.groupby("ID"):
        _KOMMUNE = KOMMUNE.lower()
        create_dir(run_id, _KOMMUNE)

        fig = room.plot.bar(
            x="DATETIME",
            y="CO2",
            color="in_use",
            title=f"Anvendelsesmodel - Lokale {i} - {KOMMUNE} KOMMUNE",
            width=3000,
            hover_data=data[["CO2_ACC"]],
        )
        fig.update_traces(dict(marker_line_width=0))
        fig.write_html(f"results/{run_id}/{_KOMMUNE}/anomaly-{_KOMMUNE}-{i}.html")

    return data
