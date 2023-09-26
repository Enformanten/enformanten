import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from plotly.graph_objects import Figure as PlotlyFigure
from typing import Type

import tilly.api.config as c
from tilly.api.database.users.crud import create_db_and_tables
from tilly.api.routes import predict, train, dashboard, room
from tilly.api.users.auth import auth_backend, current_active_user, fastapi_users
from tilly.api.users.initial_users import create_initial_users
from tilly.api.users.schemas import UserCreate, UserRead, UserUpdate


async def on_startup():
    await create_db_and_tables()
    await create_initial_users()


templates = Jinja2Templates(directory="dashboard")


app = FastAPI(
    title=c.TITLE,
    version=c.GIT_METADATA,
    debug=c.DEBUG,
    description=c.DESCRIPTION,
    docs_url="/docs",
    on_startup=on_startup,
    on_shutdown=None,
)


@app.get("/", response_class=HTMLResponse)
def read_root():
    plots: list[Type[PlotlyFigure]] = dashboard.load_files(c.PLOT_DIR)
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
    dashboard.router,
    tags=["dashboard"],
    dependencies=[Depends(current_active_user)],
)

app.include_router(
    room.router,
    tags=["room"],
    dependencies=[Depends(current_active_user)],
)


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", log_level="info", reload=True)