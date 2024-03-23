from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.db import get_db

from .auth import get_current_superuser

router = APIRouter()


@router.get("/services", response_model=schemas.ServiceList)
async def read_services(db: Session = Depends(get_db)):
    return {"services": crud.get_services(db)}


@router.post(
    "/services",
    response_model=schemas.Service,
    status_code=status.HTTP_201_CREATED,
)
async def create_service(
    service: schemas.ServiceCreate = Depends(schemas.ServiceCreate),
    db: Session = Depends(get_db),
):
    try:
        return crud.create_service(db, service)
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete(
    "/services/{service_name}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_service(
    service_name: str,
    db: Session = Depends(get_db),
):
    return crud.delete_service(db, service_name)