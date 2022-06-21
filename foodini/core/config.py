import logging
from typing import Any, Dict, List

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, DirectoryPath, FilePath, constr, validator


class MysqlDsn(AnyUrl):
    allowed_schemas = {"mysql+pymysql"}
    user_required = True


class Settings(BaseSettings):
    class Config:
        case_sensitive = True
        secrets_dir = "/run/secrets/"

    # Project information.
    PROJECT_TITLE: str = "Foodini"
    PROJECT_DESCRIPTION: str = "Foodini, the random food decider app."
    PROJECT_CHANGELOG: FilePath = "/CHANGELOG.md"
    PROJECT_VERSION: str

    # Security settings.
    SECRET_KEY: constr(min_length=128, max_length=128)
    HASHING_ALGORITHM: str = "bcrypt"
    SIGNING_ALGORITHM: str = "HS256"

    # Deployment settings.
    RELOAD: bool = False
    DEBUG: bool = False
    DEBUG_PORT: int = 5678
    UVICORN_PORT: int = 8000

    # Logging settings.
    LOGGING_COLOR: str = "cyan"
    LOGGING_LEVEL: int = logging.INFO

    # Authentication token settings.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ACCESS_TOKEN_HTTPONLY: bool = True
    ACCESS_TOKEN_SECURE: bool = True
    ACCESS_TOKEN_SAMESITE: str = "strict"

    # Cors settings.
    CORS_ORIGIN_REGEX: str | None = None
    CORS_ORIGINS: List[AnyHttpUrl] = []
    CORS_ORIGINS_EXPOSE_HEADERS: List[str] = ["Process-Time", "Total-Count"]

    # API settings.
    API_STATIC_DIRECTORY: DirectoryPath = "static"
    API_STATIC_PREFIX: str = "/static"
    API_HEALTH_PREFIX: str = "/health"
    API_ENDPOINT_PREFIX: str = "/api"
    API_V1_PREFIX: str = "/v1"
    API_TOKEN_SUFFIX: str = "/token"

    DOCS_OFFLINE: bool = True
    DOCS_OPENAPI: str = "/openapi"
    DOCS_SWAGGER: str = "/docs"
    DOCS_SWAGGER_OAUTH: str = DOCS_SWAGGER + "/oauth2"
    DOCS_REDOC: str = "/redoc"

    # Database settings.
    DATABASE_INIT: bool = False
    DATABASE_USER: str = PROJECT_TITLE.lower()
    DATABASE_PASS: str
    DATABASE_HOST: str = "database"
    DATABASE_PORT: int = 3306
    DATABASE_NAME: str = PROJECT_TITLE.lower()
    DATABASE_URI: MysqlDsn | None = None
    DATABASE_LIMIT: int = 100

    @validator("DATABASE_URI", pre=True)
    def assemble_database_uri(cls, value: str | None, values: Dict[str, Any]) -> str:
        if isinstance(value, str):
            return value
        return MysqlDsn.build(
            scheme="mysql+pymysql",
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASS"),
            host=values.get("DATABASE_HOST"),
            port=str(values.get("DATABASE_PORT")),
            path=f"/{values.get('DATABASE_NAME')}"
        )


settings = Settings()
