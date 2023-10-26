"""
Dashboard Updater Module

This module contains functions for processing room data,
generating plots, and updating the dashboard by saving the plots to disk.
"""

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
    """
    Create Municipality/School Directories

    Create the directories for storing plots related to a specific municipality
    and school if they do not already exist.

    Args:
        municipality (str): The name of the municipality.
        school (str): The name of the school.
    """
    Path(f"{PLOTS_DIR}/{municipality}/{school}").mkdir(parents=True, exist_ok=True)


def process_for_dashboard(rooms: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """
    Process Room Data for Dashboard

    This function takes room data, processes it, and generates plotly figures.
    It also creates necessary directories for storing the plots.

    Args:
        rooms (dict[str, pd.DataFrame]): Dictionary containing room data as
            Pandas DataFrames.

    Returns:
        dict[str, pd.DataFrame]: A dictionary containing processed plotly figures.
    """
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


def save_figures(named_plots: dict[tuple[str, str, str], object]) -> None:
    """
    Save Figures to Disk

    Takes a dictionary of named plots and saves them to disk.

    Args:
        named_plots (dict): A dictionary containing plotly figures keyed
            by a tuple representing (municipality, school, room_id).
    """

    for (municipality, school, room_id), fig in named_plots.items():
        fig.write_html(f"{PLOTS_DIR}/{municipality}/{school}/{room_id}.html")


def update_dashboard(plot_data: dict[str, pd.DataFrame]) -> None:
    """
    Update Dashboard

    Update the dashboard by processing the provided room data and saving the
    generated plots.

    Args:
        plot_data (dict[str, pd.DataFrame]): dict containing room data as
        Pandas DataFrames, indexed by room name.

    Side Effects:
        - Directories for storing plots may be created.
        - Plot files may be written to disk.
    """

    named_plots: dict[tuple(str, str, str), object] = process_for_dashboard(plot_data)
    save_figures(named_plots)
