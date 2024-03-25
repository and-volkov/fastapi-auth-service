from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import check_db_connection
from .routers import auth as auth_router
from .routers import roles as roles_router
from .routers import services as services_router
from .routers import users as users_router
from .settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    check_db_connection()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    lifespan=lifespan,
)

app.include_router(
    auth_router.router, prefix=settings.API_V1_STR, tags=["auth"]
)
app.include_router(
    users_router.router, prefix=settings.API_V1_STR, tags=["users"]
)
app.include_router(
    roles_router.router,
    prefix=settings.API_V1_STR,
    tags=["roles"],
)
app.include_router(
    services_router.router,
    prefix=settings.API_V1_STR,
    tags=["services"],
)
