from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas
from app.security import get_password_hash


def is_email(email: str):
    return True if "@" in email else False


def get_user(db: Session, email_or_username: str):
    if is_email(email_or_username):
        user = (
            db.query(models.User)
            .filter(models.User.email == email_or_username)
            .first()
        )
    else:
        user = (
            db.query(models.User)
            .filter(models.User.username == email_or_username)
            .first()
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, email_or_username: str):
    user = get_user(db, email_or_username)
    db.delete(user)
    db.commit()
    return user


def get_role(db: Session, role_name: str):
    role = db.query(models.Role).filter(models.Role.name == role_name).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    return role


def get_roles(db: Session):
    return db.query(models.Role).all()


def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(name=role.name)
    try:
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="Role already exists")


def delete_role(db: Session, role_name: str):
    role = get_role(db, role_name)
    db.delete(role)
    db.commit()
    return role


def get_service(db: Session, service_name: str):
    service = (
        db.query(models.Service)
        .filter(models.Service.name == service_name)
        .first()
    )
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    return service


def get_services(db: Session):
    return db.query(models.Service).all()


def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(name=service.name)
    try:
        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        return db_service
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="Service already exists")


def delete_service(db: Session, service_name: str):
    service = get_service(db, service_name)
    db.delete(service)
    db.commit()
    return service
