from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.db import get_db

router = APIRouter()


@router.get("/services/{service_id}", response_model=schemas.Service)
async def read_service(service_id: int, db: Session = Depends(get_db)):
    service = crud.get_service(db, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


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
    except Exception:
        raise HTTPException(status_code=409, detail="Service already exists")


@router.delete(
    "/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
):
    return crud.delete_service(db, service_id)
