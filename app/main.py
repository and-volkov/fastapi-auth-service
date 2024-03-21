from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from .db import check_db_connection, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    check_db_connection()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", dependencies=[Depends(get_db)])
async def root():
    check_db_connection()
    return {"message": "Server is running"}
