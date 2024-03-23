from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.db import get_db

from .auth import get_current_superuser

router = APIRouter(
    responses={
        404: {"description": "User not found"},
        409: {"description": "User already exists"},
    },
)


@router.post(
    "/users/", response_model=schemas.UserCreateResponse, status_code=201
)
async def create_user(
    db: Session = Depends(get_db),
    user: schemas.UserCreate = Depends(schemas.UserCreate),
):
    try:
        return crud.create_user(db, user)
    except Exception:
        raise HTTPException(status_code=409, detail="User already exists")


@router.get("/users/{email_or_username}/", response_model=schemas.UserResponse)
async def read_user(email_or_username: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, email_or_username)
    user = schemas.UserResponse(**user.__dict__)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", response_model=schemas.UserList)
async def read_users(
    db: Session = Depends(get_db),
    _: schemas.User = Depends(get_current_superuser),
):
    users = crud.get_users(db)
    return {"users": users}


@router.delete(
    "/users/{email_or_username}/",
    status_code=204,
)
async def delete_user(email_or_username: str, db: Session = Depends(get_db)):
    user = crud.delete_user(db, email_or_username)
    return user
