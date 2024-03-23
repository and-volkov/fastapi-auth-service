from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.db import get_db

router = APIRouter()


@router.get("/roles/{role_id}", response_model=schemas.Role)
async def read_role(role_id: int, db: Session = Depends(get_db)):
    role = crud.get_role(db, role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.get("/roles", response_model=schemas.RoleList)
async def read_roles(db: Session = Depends(get_db)):
    roles = crud.get_roles(db)
    return {"roles": roles}


@router.post(
    "/roles", response_model=schemas.Role, status_code=status.HTTP_201_CREATED
)
async def create_role(
    role: schemas.RoleCreate = Depends(schemas.RoleCreate),
    db: Session = Depends(get_db),
):
    try:
        return crud.create_role(db, role)
    except Exception:
        raise HTTPException(status_code=409, detail="Role already exists")


@router.delete("/roles/{role_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    return crud.delete_role(db, role_id)
