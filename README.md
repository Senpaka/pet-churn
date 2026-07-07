# Pet Churn Prediction
Pet-проект MLOps-сервиса для предсказания оттока клиентов на основе телеком-датасета.
Проект реализует полный цикл работы с ML-моделью: Обработка данных, Обучение CatBoost модели, подбор гиперпараметров с использованием Optuna, Логирование экспериментов в MLflow, Регистрация модели в MLflow Model Registry и использование модели через FastAPI.
Для асинхронной обработки batch-предсказание используется связка Celery-Redis. Данные клиентов и результаты предсказание сохраняются в PosthreSQL. Структура Базы Данных создается с помощью Alembic migrations. 
Проект контейнеризирован с помощью Docker-compose.

---

## [Архитектура Проекта](docs/architecture.md)
## [Docker архитектура](docs/docker_architecture.md)

---

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

## Принимаемые признаки

| Признак            | Тип данных       | Используется моделью | Описание                                                                                                             |
|:-------------------|:-----------------|:---------------------|:---------------------------------------------------------------------------------------------------------------------|
| `customerID`       | `str`            | Нет                  | Уникальный идентификатор клиента. Используется для связи предсказания с клиентом, но не используется как ML-признак. |
| `gender`           | `str`            | Да                   | Пол клиента. Возможные значения: `Male`, `Female`.                                                                   |
| `SeniorCitizen`    | `int`            | Да                   | Флаг пожилого клиента: `1` — да, `0` — нет.                                                                          |
| `Partner`          | `str`            | Да                   | Наличие партнёра у клиента. Возможные значения: `Yes`, `No`.                                                         |
| `Dependents`       | `str`            | Да                   | Наличие иждивенцев. Возможные значения: `Yes`, `No`.                                                                 |
| `tenure`           | `int`            | Да                   | Количество месяцев в течение которых клиент пользуется услугами компании.                                            |
| `PhoneService`     | `str`            | Да                   | Наличие телефонной услуги. На этапе feature engineering преобразуется в числовой флаг.                               |
| `MultipleLines`    | `str`            | Да                   | Наличие нескольких телефонных линий. Возможные значения: `Yes`, `No`, `No phone service`.                            |
| `InternetService`  | `str`            | Да                   | Тип интернет-услуги клиента. Возможные значения: `DSL`, `Fiber optic`, `No`.                                         |
| `OnlineSecurity`   | `str`            | Да                   | Наличие услуги онлайн-безопасности.                                                                                  |
| `OnlineBackup`     | `str`            | Да                   | Наличие услуги онлайн-резервного копирования.                                                                        |
| `DeviceProtection` | `str`            | Да                   | Наличие услуги защиты устройства.                                                                                    |
| `TechSupport`      | `str`            | Да                   | Наличие технической поддержки.                                                                                       |
| `StreamingTV`      | `str`            | Да                   | Наличие услуги стримингового телевидения.                                                                            |
| `StreamingMovies`  | `str`            | Да                   | Наличие услуги стриминговых фильмов.                                                                                 |
| `Contract`         | `str`            | Да                   | Тип контракта клиента. Возможные значения: `Month-to-month`, `One year`, `Two year`.                                 |
| `PaperlessBilling` | `str`            | Да                   | Использует ли клиент безбумажные счета. Возможные значения: `Yes`, `No`.                                             |
| `PaymentMethod`    | `str`            | Да                   | Способ оплаты клиента.                                                                                               |
| `MonthlyCharges`   | `float`          | Да                   | Ежемесячный платёж клиента.                                                                                          |
| `TotalCharges`     | `float` / `null` | Да                   | Общая сумма платежей клиента. В исходном датасете может быть пустой, поэтому приводится к числовому типу.            |

## Целевая переменная

| Признак | Тип данных | Используется в inference | Описание                                                                                                                                |
|:--------|:-----------|:-------------------------|:----------------------------------------------------------------------------------------------------------------------------------------|
| `Churn` | `str`      | Нет                      | Целевая переменная для обучения модели. Показывает, ушёл клиент или нет. Возможные значения: `Yes`, `No`. В API-запросах не передаётся. |

## Признаки, создаваемые на этапе feature engineering

| Признак        | Тип данных  | Описание                                                                                |
|:---------------|:------------|:----------------------------------------------------------------------------------------|
| `Has_internet` | `int`       | Флаг наличия интернет-услуги у клиента. Создаётся на основе признака `InternetService`. |
| `NumServices`  | `int`       | Количество подключённых дополнительных сервисов клиента.                                |
| `has_services` | `int`       | Флаг наличия хотя бы одной дополнительной услуги.                                       |

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

