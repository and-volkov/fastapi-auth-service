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


def get_user_service_role(db: Session, user_id: int):
    user_service_role = (
        db.query(models.UserRole)
        .filter(models.UserRole.user_id == user_id)
        .all()
    )
    if not user_service_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User service role not found",
        )
    return user_service_role


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


def get_role(db: Session, role_id: int):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
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


def delete_role(db: Session, role_id: int):
    role = get_role(db, role_id)
    db.delete(role)
    db.commit()
    return role


def get_service(db: Session, service_id: int):
    service = (
        db.query(models.Service)
        .filter(models.Service.id == service_id)
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


def delete_service(db: Session, service_id: int):
    service = get_service(db, service_id)
    db.delete(service)
    db.commit()
    return service


def create_user_service_role(
    db: Session, user_service_role: schemas.UserServiceRoleCreate
):
    if not db.query(models.User).get(user_service_role.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not db.query(models.Role).get(user_service_role.role_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    if not db.query(models.Service).get(user_service_role.service_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    db_user_service_role = models.UserRole(
        user_id=user_service_role.user_id,
        role_id=user_service_role.role_id,
        service_id=user_service_role.service_id,
    )
    try:
        db.add(db_user_service_role)
        db.commit()
        db.refresh(db_user_service_role)
        return db_user_service_role
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="User service role already exists",
        )


def delete_user_service_role(
    db: Session,
    user_service_role: schemas.UserServiceRoleDelete,
):
    db_user_service_role = (
        db.query(models.UserRole)
        .filter(
            models.UserRole.user_id == user_service_role.user_id,
            models.UserRole.service_id == user_service_role.service_id,
        )
        .first()
    )
    if not db_user_service_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User service role not found",
        )
    db.delete(db_user_service_role)
    db.commit()
    return db_user_service_role
