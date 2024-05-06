import os

from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    db_user: str = os.environ.get("POSTGRES_USER", "postgres")
    db_password: str = os.environ.get("POSTGRES_PASSWORD", "postgres-password")
    db_host: str = os.environ.get("POSTGRES_HOST", "127.0.0.1")
    db_port: str = os.environ.get("POSTGRES_PORT", "5432")
    db_name: str = os.environ.get("POSTGRES_DB", "project")
    db_url: str = (
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    redis_host: str = os.environ.get("REDIS_HOST", "127.0.0.1")
    redis_port: str = os.environ.get("REDIS_PORT", "6379")
    redis_url: str = f"redis://{redis_host}:{redis_port}"


class ApplicationSettings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()

    PROJECT_NAME: str = "FastAPI Project"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "현제 FastAPI를 이용한 프로젝트의 코딩 스타일을 확인할 수 있습니다."

    EXCEPT_PATH_LIST: list[str] = ["/health", "/openapi.json"]

    # JWT
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "secret key")
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: str = os.environ.get(
        "ACCESS_TOKEN_EXPIRE_MINUTES", "30"
    )


settings = ApplicationSettings()
