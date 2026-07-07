## Пример `.env` файла для локального запуска

```env
# PostgreSQL
DATABASE_URL=postgresql+psycopg2://app:app@localhost:5432/app_db

# MLflow
MLFLOW_TRACKING_URI=http://127.0.0.1:5001
MLFLOW_EXPERIMENT_NAME=churn_prediction_v1
MLFLOW_DATABASE_URI=postgresql+psycopg2://mlflow:mlflow@localhost:5432/mlflow_db
MLFLOW_ARTIFACT_URI=file:/Users/senpaka/programming/pet_churn/artifacts/mlflow
MLFLOW_HOST=127.0.0.1
MLFLOW_PORT=5000

# Optuna
OPTUNA_DATABASE_URI=postgresql+psycopg2://optuna:optuna@localhost:5432/optuna_db

# Model Registry
MODEL_NAME=CatBoost-model
MODEL_ALIAS=champion

# FastAPI
FASTAPI_APP_PATH=services.fastapi.app
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000

# Celery / Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_BACKEND_URL=redis://localhost:6379/1

CELERY_CPU_CONCURRENCY=1
CELERY_CPU_MULTIPLIER=1

CELERY_IO_CONCURRENCY=4
CELERY_IO_MULTIPLIER=4
```

## Пример `.env.docker` файла для запуска с docker compose 

```env
# PostgreSQL
DATABASE_URL=postgresql+psycopg2://app:app@postgres:5432/app_db

# MLflow
MLFLOW_TRACKING_URI=http://mlflow:5000
MLFLOW_EXPERIMENT_NAME=churn_prediction_v1
MLFLOW_DATABASE_URI=postgresql+psycopg2://mlflow:mlflow@postgres:5432/mlflow_db
MLFLOW_ARTIFACT_URI=file:/app/artifacts/mlflow
MLFLOW_HOST=0.0.0.0
MLFLOW_PORT=5000

# Optuna
OPTUNA_DATABASE_URI=postgresql+psycopg2://optuna:optuna@postgres:5432/optuna_db

# Model Registry
MODEL_NAME=CatBoost-model
MODEL_ALIAS=champion

# FastAPI
FASTAPI_APP_PATH=services.fastapi.app
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Celery / Redis
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_BACKEND_URL=redis://redis:6379/1

CELERY_CPU_CONCURRENCY=1
CELERY_CPU_MULTIPLIER=1

CELERY_IO_CONCURRENCY=4
CELERY_IO_MULTIPLIER=4
```
