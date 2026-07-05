from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

import core.paths as paths

BASE_DIR = paths.BASE_DIR

class Settings(BaseSettings):
    # Database
    database_url: str = Field(..., alias="DATABASE_URL")

    # MLflow
    mlflow_tracking_uri: str = Field("http://127.0.0.1:5000", alias="MLFLOW_TRACKING_URI")
    mlflow_experiment_name: str = Field("churn_prediction_v1", alias="MLFLOW_EXPERIMENT_NAME")
    mlflow_database_uri: str | None = Field(None, alias="MLFLOW_DATABASE_URI")
    mlflow_artifact_uri: str = Field("file:./artifacts/mlflow", alias="MLFLOW_ARTIFACT_URI")
    mlflow_host: str = Field("127.0.0.1", alias="MLFLOW_HOST")
    mlflow_port: int = Field(5000, alias="MLFLOW_PORT")

    # Optuna
    optuna_database_uri: str | None = Field(None, alias="OPTUNA_DATABASE_URI")

    # Model Registry
    model_name: str = Field("CatBoost-model", alias="MODEL_NAME")
    model_alias: str = Field("champion", alias="MODEL_ALIAS")

    # FastAPI
    fastapi_app_path: str = Field("services.fastapi.app", alias="FASTAPI_APP_PATH")
    fastapi_host: str = Field("127.0.0.1", alias="FASTAPI_HOST")
    fastapi_port: int = Field(8000, alias="FASTAPI_PORT")

    # Celery / Redis
    celery_broker_url: str = Field("redis://localhost:6379/0", alias="CELERY_BROKER_URL")
    celery_backend_url: str = Field("redis://localhost:6379/1", alias="CELERY_BACKEND_URL")
    celery_cpu_concurrency: int = Field(1, alias="CELERY_CPU_CONCURRENCY")
    celery_cpu_multiplier: int = Field(1, alias="CELERY_CPU_MULTIPLIER")
    celery_io_concurrency: int = Field(4, alias="CELERY_IO_CONCURRENCY")
    celery_io_multiplier: int = Field(4, alias="CELERY_IO_MULTIPLIER")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()