from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import plotly.express as px
import pandas as pd
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def create_mock_data(school_id: int, room_id: int):
    x_values = np.linspace(0, 10, 20)
    y_values = np.sin(x_values) + np.random.normal(scale=0.2, size=len(x_values))

    df = pd.DataFrame({"x": x_values, "y": y_values})
    fig = px.line(
        df, x="x", y="y", title=f"Performance of Room {room_id} in School {school_id}"
    )

    # Here, the HTML files are stored directly within the "templates" folder
    fig.write_html(
        f"templates/school_{school_id}_room_{room_id}.html",
        config={"displayModeBar": False},
    )


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, school_id: int = 1):
    room_files = [f"school_{school_id}_room_{i}.html" for i in range(1, 4)]

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "room_files": room_files, "school_id": school_id},
    )
