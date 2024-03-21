import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    PROJECT_NAME: str

    SECRET_KEY: str = "secret"

    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    SQLALCHEMY_DATABASE_URI: str

    LOG_FILE_NAME: str = "logs.log"
    LOG_MESSAGE_FORMAT: str = "%(asctime)s %(levelname)s: %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    JWT_TOKEN_LIFETIME_MINUTES: int = 60 * 24  # 1 day
    ALGORITHM: str = "HS256"

    @field_validator("SQLALCHEMY_DATABASE_URI")  # type: ignore
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> PostgresDsn | str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=(
                f"{values.get("POSTGRES_HOST") or "127.0.0.1"}"
                f":{values.get("POSTGRES_PORT") or 5432}"
            ),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings()  # type: ignore


log_level = logging.INFO
log_stream_handler = logging.StreamHandler()
log_file_handler = RotatingFileHandler(
    filename="app" + os.sep + settings.LOG_FILE_NAME,
    mode="a",
    maxBytes=5 * 1024 * 1024,
    backupCount=1,
    encoding=None,
)

logging.basicConfig(
    encoding="utf-8",
    level=log_level,
    format=settings.LOG_MESSAGE_FORMAT,
    handlers=[log_file_handler, log_stream_handler],
    datefmt=settings.LOG_DATE_FORMAT,
)
