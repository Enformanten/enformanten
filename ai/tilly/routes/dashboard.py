"""
FastAPI Router for Tilly Dashboard and Plots

This module contains routes for serving the Tilly dashboard and for retrieving
the directory structure of the plots. It uses FastAPI and depends on the Jinja2 
templating engine to render HTML responses.
"""

from pathlib import Path
from typing import Optional, Dict
from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from tilly import config as c

# Initialize Jinja2 templates
templates = Jinja2Templates(directory=c.PLOTS_DIR.parent)

# Initialize FastAPI router
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def read_root(request: Request) -> HTMLResponse:
    """
    Serve the Tilly Dashboard.

    This route returns an HTML response that serves the Tilly dashboard.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        HTMLResponse: The HTML response containing the rendered Tilly dashboard.

    Examples:
        ```bash
        curl http://localhost:8000/
        ```

        This will return the HTML content of the Tilly dashboard.
    """
    return templates.TemplateResponse("dashboard.html", {"request": request})


def create_plot_structure(root_path: Path) -> Optional[Dict]:
    """
    Generate Plot Directory Structure.

    This function takes a root path and returns a dictionary representing the
        directory structure rooted at that path.

    Args:
        root_path (Path): The root path from which to generate the directory
            structure.

    Returns:
        Optional[Dict]: The dictionary representing the directory structure or
            `None` if the provided path is not a directory.

    Examples:
        ```python
        from pathlib import Path

        root_path = Path("/path/to/plots")
        structure = create_plot_structure(root_path)
        ```
    """
    if not root_path.is_dir():
        return None
    return {child.name: create_plot_structure(child) for child in root_path.iterdir()}


@router.get("/plots_structure", response_model=Optional[Dict])
def get_plots_structure() -> Optional[Dict] | HTTPException:
    """
    Get Plot Directory Structure.

    This route returns the directory structure of the plots as a JSON object.
    If the directory structure is invalid, a 404 HTTP error is raised.

    Returns:
        Optional[Dict]: The dictionary representing the directory structure.

    Examples:
        ```bash
        curl http://localhost:8000/plots_structure
        ```

        This will return a JSON object representing the directory structure of
        the plots.
    """
    plot_dir = Path(c.PLOTS_DIR)
    result = create_plot_structure(plot_dir)
    if result is None:
        raise HTTPException(status_code=404, detail="Invalid directory structure")
    return result
