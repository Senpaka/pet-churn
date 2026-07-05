# Pet Churn Prediction
Pet-проект MLOps-сервиса для предсказания оттока клиентов на основе телеком-датасета.
Проект реализует полный цикл работы с ML-моделью: Обработка данных, Обучение CatBoost модели, подбор гиперпараметров с использованием Optuna, Логирование экспериментов в MLflow, Регистрация модели в MLflow Model Registry и использование модели через FastAPI.
Для асинхронной обработки batch-предсказание используется связка Celery-Redis. Данные клиентов и результаты предсказание сохраняются в PosthreSQL. Структура Базы Данных создается с помощью Alembic migrations. 
Проект контейнеризирован с помощью Docker-compose.


## [Архитектура Проекта](docs/architecture.md)

## Стек технологий

### Backend
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic

### Async processing
- Celery
- Redis

### ML
- CatBoost
- scikit-learn
- Optuna
- Pandas

### MLOps
- MLflow Tracking
- MLflow Model Registry

### DevOps
- Docker
- Docker Compose
- Makefile

---

## Функциональность

### Логирование:
 В проекте реализовано логирование:
- в файл;
- в консоль;
- в MLflow для экспериментов, метрик, параметров и моделей.

### Обучение модели:
Реализован pipeline обучения модели оттока клиентов:

- загрузка датасета;
- подготовка признаков;
- подбор гиперпараметров с помощью Optuna;
- обучение CatBoostClassifier;
- расчёт метрик качества;
- логирование параметров, метрик и артефактов в MLflow;
- регистрация модели в MLflow Model Registry;
- назначение alias для production-модели.

### Предсказания

FastAPI предоставляет endpoints для:

- одиночного предсказания;
- batch-предсказания;
- асинхронного предсказания по данным из PostgreSQL через Celery;
- проверки статуса Celery task.

Для работы с PostgreSQL используются:

- SQLAlchemy models;
- Alembic migrations;
- отдельные Docker-сервисы для миграций и seed-данных.

### Makefile

| Команда                         | Описание                                   |
|:--------------------------------|:-------------------------------------------|
| `make train`                    | Обучение модели                            |
| `make mlflow-run`               | Запуск MLflow server локально              |
| `make fastapi-run`              | Запуск FastAPI локально                    |
| `make celery-cpu-run`           | Запуск Celery worker для тяжёлых CPU-задач |
| `make celery-io-run`            | Запуск Celery worker для лёгких I/O-задач  |
| `make db-migrations`            | Применение миграций до `head`              |
| `make db-downgrade`             | Откат миграций                             |
| `make db-revision m="message"`  | Создание новой Alembic-ревизии             |
| `make db-seed`                  | Заполнение БД данными из .csv              |
| `make docker-build`             | Сборка Docker-образов                      |
| `make docker-up`                | Запуск Docker-контейнеров                  |
| `make docker-up-detached`       | Запуск Docker-контейнеров в фоне           |
| `make docker-down`              | Остановка Docker-контейнеров               |
| `make docker-db-migrate`        | Выполнение миграций в Docker               |
| `make docker-db-seed`           | Заполнение БД данными из CSV в Docker      |
| `make docker-train`             | Обучение модели в Docker                   |
| `make docker-logs`              | Просмотр логов Docker Compose              |
| `make docker-ps`                | Список запущенных контейнеров              |


---

## Быстрый запуск в Docker

```bash
make docker-build
make docker-up-detached
make docker-db-migrate
make docker-db-seed
make docker-train
```

### После запуска 
- FastAPI Swagger UI: http://localhost:8000/docs
- MLflow UI: http://localhost:5001

## Быстрый запуск локально
```bash
make mlflow-run
make db-migrations
make db-seed
make train
make celery-cpu-run
make fastapi-run
```

### После запуска 
- FastAPI Swagger UI: http://localhost:8000/docs
- MLflow UI: http://localhost:5000

## [Примеры .env файлов](docs/env_example.md)

