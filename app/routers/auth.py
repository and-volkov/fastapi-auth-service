import logging
from datetime import UTC, datetime, timedelta
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.crud import get_user
from app.db import SessionLocal, get_db
from app.schemas import Token, User
from app.security import verify_password
from app.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()


logger = logging.getLogger(__name__)


class OAuth2ExtendedForm:
    def __init__(
        self,
        email_or_username: str = Body(
            alias="email_or_username", example="email"
        ),
        password: str = Body(alias="password", example="password"),
    ):
        self.email_or_username = email_or_username
        self.password = password


def authenticate_user(db, email_or_username: str, password: str):
    logger.info(f"Email or username: {email_or_username}")
    user = get_user(db, email_or_username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict):
    logger.info(f"Data: {data}")
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(settings.JWT_TOKEN_LIFETIME_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2ExtendedForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    logger.info(f"Form data: {form_data}")
    user = authenticate_user(
        db, form_data.email_or_username, form_data.password
    )
    logger.info(f"User: {user}")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.info(f"Token: {token}")
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")  # type: ignore
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, email_or_username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_superuser(
    current_user: User = Depends(get_current_user),
):
    logger.info(f"Current user: {current_user}")
    if current_user.is_superuser:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
    )
