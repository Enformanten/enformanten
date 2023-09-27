from pathlib import Path
import pandas as pd

# set pandas plotting backend to plotly
pd.options.plotting.backend = "plotly"


def load_files(path: str) -> list[object]:
    """Load all files from the given path."""

    plots = []
    for file in Path(path).glob("*.html"):
        plots.append(file.read_text())

    return plots


def create_dir(municipality: str, school: str) -> None:
    Path(f"api/dashboard/{municipality}/{school}").mkdir(parents=True, exist_ok=True)


def process_for_dashboard(rooms: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Processes the results for the dashboard."""

    output = {}
    for name, room in rooms.items():
        # retrive the first instance of 'KOMMUNE' and 'SKOLE'
        KOMMUNE = room["KOMMUNE"].iloc[0]
        school = room["SKOLE"].iloc[0]
        create_dir(KOMMUNE, school)

        fig = room.sort_values("DATETIME", ascending=True).plot.bar(
            x="DATETIME",
            y="CO2",
            color="IN_USE",
            title=f"Anvendelsesmodel - Lokale '{name}' - {school} ({KOMMUNE} KOMMUNE)",
            width=3000,
            hover_data=room[["CO2_ACC"]],
        )
        fig.update_traces(dict(marker_line_width=0))
        output[(KOMMUNE, school, name)] = fig

    return output


def save_figures(named_plots) -> None:
    """Save the images to disk."""

    for (KOMMUNE, school, name), fig in named_plots.items():
        fig.write_html(f"api/dashboard/{KOMMUNE}/{school}/{name}.html")


def update_dashboard(plot_data: list[str, pd.DataFrame]) -> None:
    """Update the dashboard with the given data."""

    named_plots: dict[tuple(str, str, str), object] = process_for_dashboard(plot_data)
    save_figures(named_plots)
