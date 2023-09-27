import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from plotly.graph_objects import Figure as PlotlyFigure
from typing import Type

import tilly.config as c
from tilly.database.users.crud import create_db_and_tables
from tilly.routes import predict, train, room
from tilly.services import dashboard
from tilly.users.auth import auth_backend, current_active_user, fastapi_users
from tilly.users.initial_users import create_initial_users
from tilly.users.schemas import UserCreate, UserRead, UserUpdate


templates = Jinja2Templates(directory="dashboard")


app = FastAPI(
    title=c.TITLE,
    version=c.GIT_METADATA,
    debug=c.DEBUG,
    description=c.DESCRIPTION,
    docs_url="/docs",
    on_shutdown=None,
)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    await create_initial_users()


@app.get("/", response_class=HTMLResponse)
def read_root():
    plots: list[Type[PlotlyFigure]] = dashboard.load_files(c.PLOTS_DIR)
    return templates.TemplateResponse("dashboard/index.html", {plots: plots})


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    train.router,
    tags=["train"],
    dependencies=[Depends(current_active_user)],
)

app.include_router(
    predict.router,
    tags=["predict"],
    dependencies=[Depends(current_active_user)],
)

app.include_router(
    room.router,
    tags=["room"],
    dependencies=[Depends(current_active_user)],
)


if __name__ == "__main__":
    uvicorn.run("tilly.main:app", host="0.0.0.0", log_level="info", reload=True)
