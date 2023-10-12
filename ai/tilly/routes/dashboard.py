from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import HTTPException

from tilly import config as c


templates = Jinja2Templates(directory=c.PLOTS_DIR.parent)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def read_root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/plots/{municipality}/{school}/{room}")
def get_single_plot(municipality: str, school: str, room: str) -> dict:
    plot_path = c.PLOTS_DIR / municipality / school / f"{room}.html"
    if not plot_path.exists():
        raise HTTPException(status_code=404, detail="Plot not found")
    url_path = f"/static/plots/{municipality}/{school}/{room}.html"
    return {"path": url_path}


@router.get("/get_structure/")
async def get_structure():
    root_path = Path("tilly/dashboard/plots/")
    structure = {}

    for html_file in root_path.glob("**/*.html"):
        parts = html_file.relative_to(root_path).parts
        municipality, school, room = parts

        if municipality not in structure:
            structure[municipality] = {}
        if school not in structure[municipality]:
            structure[municipality][school] = []

        room_name = room.replace(".html", "")
        structure[municipality][school].append(room_name)

    return structure
