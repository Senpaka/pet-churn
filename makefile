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



