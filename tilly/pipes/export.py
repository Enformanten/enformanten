from pathlib import Path


def create_dir(run_id, _kommune) -> None:
    Path(f"results/{run_id}/{_kommune}").mkdir(parents=True, exist_ok=True)


def export_plots(data, kommune, run_id):
    for i, room in data.groupby("ID"):
        _kommune = kommune.lower()
        create_dir(run_id, _kommune)

        fig = room.plot.bar(
            x="DATETIME",
            y="CO2",
            color="in_use",
            title=f"Anvendelsesmodel - Lokale {i} - {kommune} Kommune",
            width=3000,
            hover_data=data[["CO2_ACC"]],
        )
        fig.update_traces(dict(marker_line_width=0))
        fig.write_html(f"results/{run_id}/{_kommune}/anomaly-{_kommune}-{i}.html")

    return data
