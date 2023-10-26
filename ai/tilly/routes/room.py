"""
Room Plot Serving Endpoint

This module contains a FastAPI router for serving room plot files, located in
a specified directory. It utilizes the FastAPI `FileResponse` class to send the
HTML files back to the client.
"""

from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse

from tilly.config import PLOTS_DIR

# Initialize FastAPI router
router = APIRouter()


@router.get("/room/{municipality}/{school}/{room}")
def read_room(municipality: str, school: str, room: str):
    """
    Serve Room Plot File.

    This endpoint serves an HTML plot file for a specific room within a school
    in a municipality. It constructs the file path based on the provided
    municipality, school, and room identifiers. If the file exists, it will be
    served as a FileResponse; otherwise, a "Room file not found"
    message will be returned.

    Args:
        municipality (str): The identifier for the municipality.
        school (str): The identifier for the school.
        room (str): The identifier for the room.

    Returns:
        Union[FileResponse, dict]: Returns a FileResponse object if the file is
        found, otherwise returns a dictionary with an error message.

    Examples:
        ```bash
        curl http://localhost:8000/room/SampleCity/SampleSchool/SampleRoom
        ```

        If the file exists, this will return the HTML plot file for SampleRoom
        in SampleSchool and SampleCity. If the file does not exist, it will return:

        ```json
        {
            "detail": "Room file not found"
        }
        ```
    """
    file_path = Path(f"{PLOTS_DIR}/{municipality}/{school}/{room}.html")
    if file_path.exists():
        return FileResponse(file_path)
    else:
        return {"detail": "Room file not found"}
