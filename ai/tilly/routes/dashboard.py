from pathlib import Path
from typing import Optional, Dict
from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from tilly import config as c


templates = Jinja2Templates(directory=c.PLOTS_DIR.parent)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def read_root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("dashboard.html", {"request": request})


def create_plot_structure(root_path: Path) -> Optional[Dict]:
    if not root_path.is_dir():
        return None
    return {child.name: create_plot_structure(child) for child in root_path.iterdir()}


@router.get("/plots_structure", response_model=Optional[Dict])
def get_plots_structure():
    plot_dir = Path(c.PLOTS_DIR)  # Assume PLOTS_DIR is defined in your config
    result = create_plot_structure(plot_dir)
    if result is None:
        raise HTTPException(status_code=404, detail="Invalid directory structure")
    return result
