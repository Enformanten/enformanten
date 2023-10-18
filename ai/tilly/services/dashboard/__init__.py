from pathlib import Path
import pandas as pd
import warnings

from tilly.config import PLOTS_DIR, FEATURES


# Configure Pandas plotting backend
pd.options.plotting.backend = "plotly"
# Ignore FutureWarnings from Plotly
warnings.filterwarnings(
    "ignore", category=FutureWarning, module="_plotly_utils.basevalidators"
)


def create_dir(municipality: str, school: str) -> None:
    """Creates the municipality/school directores if
    they doesn't exist."""
    Path(f"{PLOTS_DIR}/{municipality}/{school}").mkdir(parents=True, exist_ok=True)


def process_for_dashboard(rooms: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Processes the results for the dashboard."""

    output = {}
    for _, room in rooms.items():
        # retrive the first instance of 'KOMMUNE' and 'SKOLE'
        municipality = room["KOMMUNE"].iloc[0]
        school = room["SKOLE"].iloc[0]
        room_id = room["ID"].iloc[0].replace(".", "_")

        create_dir(municipality, school)

        fig = room.sort_values("DATETIME", ascending=True).plot.bar(
            x="DATETIME",
            y="CO2",
            color="IN_USE",
            title=(f"Lokale {room_id} " + f"- {school} ({municipality} KOMMUNE)"),
            width=2000,
            hover_data=room[FEATURES + ["ANOMALY_SCORE"]],
        )
        # Update bar border width
        fig.update_traces(dict(marker_line_width=0))
        # Update legend position
        fig.update_layout(
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                title=None,
            )
        )
        output[(municipality, school, room_id)] = fig

    return output


def save_figures(named_plots) -> None:
    """Save the images to disk."""

    for (municipality, school, room_id), fig in named_plots.items():
        fig.write_html(f"{PLOTS_DIR}/{municipality}/{school}/{room_id}.html")


def update_dashboard(plot_data: list[str, pd.DataFrame]) -> None:
    """Update the dashboard with the given data."""

    named_plots: dict[tuple(str, str, str), object] = process_for_dashboard(plot_data)
    save_figures(named_plots)
