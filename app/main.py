from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from .db import check_db_connection, get_db
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
    users_router.router, prefix=settings.API_V1_STR, tags=["users"]
)


@app.get("/", dependencies=[Depends(get_db)])
async def root():
    check_db_connection()
    return {"message": "Server is running"}
