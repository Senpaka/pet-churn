include .env
export

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
	--hostname=@cpu_worker \
	--concurrency=$(CELERY_CPU_CONCURRENCY) \
	--prefetch-multiplier=$(CELERY_CPU_MULTIPLIER) \
	--loglevel=info

celery-io-run:
	@echo "Запуск celery для легкиз задач i/o"
	celery -A services.celery.celery_app:app worker \
	-Q io_worker \
	--hostname=@io_worker \
	--concurrency=$(CELERY_IO_CONCURRENCY) \
	--prefetch-multiplier=$(CELERY_IO_MULTIPLIER) \
	--loglevel=info


