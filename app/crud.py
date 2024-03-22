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
