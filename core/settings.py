from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

import core.paths as paths

BASE_DIR = paths.BASE_DIR

class Settings(BaseSettings):
    # База данных
    database_url: str = Field(..., alias="DATABASE_URL")

    # mlflow
    mlflow_tracking_uri: str = Field(..., alias="MLFLOW_TRACKING_URI")
    mlflow_experiment_name: str = Field(..., alias="MLFLOW_EXPERIMENT_NAME")
    mlflow_database_uri: str = Field(..., alias="MLFLOW_DATABASE_URI")
    mlflow_artifact_uri: str = Field(..., alias="MLFLOW_ARTIFACT_URI")
    mlflow_host: str = Field(..., alias="MLFLOW_HOST")
    mlflow_port: int = Field(..., alias="MLFLOW_PORT")

    # Celery + Redis
    celery_broker_url: str = Field(..., alias="CELERY_BROKER_URL")
    celery_backend_url: str = Field(..., alias="CELERY_BACKEND_URL")

    celery_cpu_concurrency: int = Field(..., alias="CELERY_CPU_CONCURRENCY")
    celery_cpu_multiplier: int = Field(..., alias="CELERY_CPU_MULTIPLIER")
    celery_io_concurrency: int = Field(..., alias="CELERY_IO_CONCURRENCY")
    celery_io_multiplier: int = Field(..., alias="CELERY_IO_MULTIPLIER")

    # Optuna
    optuna_database_uri: str = Field(..., alias="OPTUNA_DATABASE_URI")

    # Model
    model_name: str = Field(..., alias="MODEL_NAME")
    model_alias: str = Field(..., alias="MODEL_ALIAS")

    # FastAPI
    fastapi_app_path: str = Field(..., alias="FASTAPI_APP_PATH")
    fastapi_host: str = Field(..., alias="FASTAPI_HOST")
    fastapi_port: int = Field(..., alias="FASTAPI_PORT")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()