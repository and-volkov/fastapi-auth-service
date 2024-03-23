from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.db import get_db

from .auth import get_current_superuser

router = APIRouter()


@router.get("/roles", response_model=schemas.RoleList)
def read_roles(db: Session = Depends(get_db)):
    roles = crud.get_roles(db)
    return {"roles": roles}


@router.post(
    "/roles", response_model=schemas.Role, status_code=status.HTTP_201_CREATED
)
def create_role(
    role: schemas.RoleCreate = Depends(schemas.RoleCreate),
    db: Session = Depends(get_db),
):
    try:
        return crud.create_role(db, role)
    except Exception as e:
        raise HTTPException(status_code=409, detail="Role already exists")


@router.delete("/roles/{role_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_name: str, db: Session = Depends(get_db)):
    return crud.delete_role(db, role_name)
