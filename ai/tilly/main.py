"""
This is the main entry point for the Tilly FastAPI application. 
The script initializes the application, configures various routes, and
sets up the database and authentication.

Main Components:
    - Initialization of the FastAPI application with metadata such as 
        title, version, description, and other settings.
    - Event handler for startup that sets up the database and creates
        initial users.
    - Inclusion of various routers to handle different functionalities:
        - Dashboard for visualizations.
        - Authentication and user management.
        - Model training and prediction.
        - Room and heartbeat management.

Startup Events:
    - `create_db_and_tables` function is called to initialize the database
        and tables.
    - `create_initial_users` function is called to populate the database with
        initial users.

Routing:
    - The script mounts a dashboard available at `/dashboard` for visualizations.
    - Various routers from different modules are included for handling
        functionalities related to dashboard, authentication, user management,
        model training, prediction, room management, and heartbeat.

Dependencies:
    - Some routes require the user to be authenticated, managed by 
        `current_active_user` from `tilly.users.auth`.

Run:
    - The application is configured to run on 0.0.0.0 with `log_level` 
        set to info and reload enabled.

Example:
    >>> import uvicorn
    >>> uvicorn.run("tilly.main:app", host="0.0.0.0", log_level="info", reload=True)

"""


import uvicorn
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from tilly.database.users.crud import create_db_and_tables
from tilly.routes import predict, train, room, dashboard, heartbeat
from tilly.users.auth import auth_backend, current_active_user, fastapi_users
from tilly.users.initial_users import create_initial_users
from tilly.users.schemas import UserCreate, UserRead, UserUpdate
import tilly.config as c


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


app.mount("/dashboard", StaticFiles(directory="tilly/dashboard/"), name="plots")

app.include_router(
    dashboard.router,
    tags=["dashboard"],
)

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

app.include_router(
    heartbeat.router,
    tags=["heartbeat"],
)


if __name__ == "__main__":
    uvicorn.run("tilly.main:app", host="0.0.0.0", log_level="info", reload=True)
