include .env
export

.PHONY: \
	mlflow-run \
	fastapi-run \
	celery-cpu-run \
	celery-io-run \
	db-migrations \
	db-downgrade \
	db-revision \
	docker-build \
	docker-up \
	docker-up-detached \
	docker-down \
	docker-db-migrate \
	docker-db-seed \
	docker-train \
	docker-logs \
	docker-ps

ALEMBIC_REVISION ?= base

train:
	@echo "Обучение модели"
	python3 -m scripts.train_model

mlflow-run:
	@echo "Запуск mlflow"
	mlflow server \
	--backend-store-uri $(MLFLOW_DATABASE_URI) \
	--default-artifact-root $(MLFLOW_ARTIFACT_URI) \
	--host $(MLFLOW_HOST) \
	--port $(MLFLOW_PORT)

fastapi-run:
	@echo "Запуск fastapi"
	uvicorn $(FASTAPI_APP_PATH):app \
	--reload \
	--host $(FASTAPI_HOST) \
	--port $(FASTAPI_PORT)

celery-cpu-run:
	@echo "Запуск celery для тяжелых задач"
	celery -A services.celery.celery_app:app worker \
	-Q cpu_worker \
	--hostname=cpu_worker@%h \
	--concurrency=$(CELERY_CPU_CONCURRENCY) \
	--prefetch-multiplier=$(CELERY_CPU_MULTIPLIER) \
	--loglevel=info

celery-io-run:
	@echo "Запуск celery для легкиз задач i/o"
	celery -A services.celery.celery_app:app worker \
	-Q io_worker \
	--hostname=io_worker@%h \
	--concurrency=$(CELERY_IO_CONCURRENCY) \
	--prefetch-multiplier=$(CELERY_IO_MULTIPLIER) \
	--loglevel=info

db-migrations:
	@echo "Применение миграций до head"
	alembic upgrade head

db-downgrade:
	@echo "Откат миграций до $(ALEMBIC_REVISION)"
	alembic downgrade $(ALEMBIC_REVISION)

db-revision:
	@echo "Создание новой ревизии"
	alembic revision --autogenerate -m "$(m)"

db-seed:
	@echo "Заполнение БД данными из .csv"
	python3 -m scripts.init_db --load_customers datasets/dataset.csv

docker-build:
	@echo "Сборка Docker-образов"
	docker compose build --no-cache

docker-up:
	@echo "Запуск Docker-контейнеров"
	docker compose up

docker-up-detached:
	@echo "Запуск Docker-контейнеров в фоне"
	docker compose up -d

docker-down:
	@echo "Остановка Docker-контейнеров"
	docker compose down

docker-db-migrate:
	@echo "Выполнение миграций в Docker"
	docker compose --profile db run --rm db-migrate

docker-db-seed:
	@echo "Заполнение БД данными из CSV в Docker"
	docker compose --profile db run --rm db-seed

docker-train:
	@echo "Обучение модели в Docker"
	docker compose --profile train run --rm trainer

docker-logs:
	@echo "Логи Docker Compose"
	docker compose logs -f

docker-ps:
	@echo "Список контейнеров"
	docker compose ps