from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/room/{school}/{room}")
def read_room(school: str, room: str):
    file_path = Path(f"api/dashboard/{school}/{room}.html")
    if file_path.exists():
        return FileResponse(file_path)
    else:
        return {"detail": "Room file not found"}
