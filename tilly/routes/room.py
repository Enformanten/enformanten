from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse

from tilly.config import PLOTS_DIR


router = APIRouter()


@router.get("/room/{municipality}/{school}/{room}")
def read_room(municipality: str, school: str, room: str):
    file_path = Path(f"{PLOTS_DIR}/{municipality}/{school}/{room}.html")
    if file_path.exists():
        return FileResponse(file_path)
    else:
        return {"detail": "Room file not found"}
