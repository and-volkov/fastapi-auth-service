from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.db import get_db

router = APIRouter()


@router.post(
    "/users/",
    response_model=schemas.UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
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
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_roles = crud.get_user_service_role(db, user.id)  # type: ignore
    user_resp = schemas.UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_superuser=user.is_superuser,
        service_roles=[
            schemas.UserServiceRoleResponse(
                service_id=role.service_id,  # type: ignore
                role_id=role.role_id,  # type: ignore
            )
            for role in user_roles
        ],
    )
    return user_resp


@router.get("/users/", response_model=schemas.UserList)
async def read_users(
    db: Session = Depends(get_db),
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


@router.post("/service_role/", status_code=status.HTTP_201_CREATED)
async def add_service_role(
    user_service_role: schemas.UserServiceRoleCreate = Depends(
        schemas.UserServiceRoleCreate
    ),
    db: Session = Depends(get_db),
):
    crud.create_user_service_role(db, user_service_role)
    return {"message": "Service role added"}


@router.delete("/service_role/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_role(
    user_service_role: schemas.UserServiceRoleDelete = Depends(
        schemas.UserServiceRoleDelete
    ),
    db: Session = Depends(get_db),
):
    crud.delete_user_service_role(db, user_service_role)
    return {"message": "Service role deleted"}
