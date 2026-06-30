# Функциональность

## Логирование:
### В проекте выполнено логирование в файл `.log` и с помощью mlflow
## makefile:
### `make mlflow-run` - поднимает сервер с mlflow для отслеживания 
## Обучение модели:
### Реализовано обучение модели с подбором гиперпарамитров с использованием `optuna`
### Логирование в mlflow и файл 

# Пример .env файла

```
OPTUNA_DATABASE_URI=postgresql+psycopg2://user:password@localhost:5432/db_name_1

MLFLOW_TRACKING_URI=http://0.0.0.0:5000
MLFLOW_EXPERIMENT_NAME=my_experiment
MLFLOW_DATABASE_URI=postgresql+psycopg2://user:password@localhost:5432/db_name_2
MLFLOW_ARTIFACT_URI=file:/path/to/artifacts
MLFLOW_HOST=0.0.0.0
MLFLOW_PORT=5000
```