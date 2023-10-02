from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

from tilly.services import dashboard
from tilly import config as c


templates = Jinja2Templates(directory=c.PLOTS_DIR.parent)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def read_root(request: Request) -> HTMLResponse:
    plots: list[str] = dashboard.load_files(c.PLOTS_DIR)
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "plots": plots}
    )


@router.get("/plots/{municipality}/{school}/{room}")
def get_plot(municipality: str, school: str, room: str) -> FileResponse:
    path = Path("plots") / municipality / school / f"{room}.html"
    return FileResponse(path)
