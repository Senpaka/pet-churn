include .env
export

make mlflow-run:
	mlflow server \
	--backend-store-uri $(MLFLOW_DATABASE_URI) \
	--default-artifact-root $(MLFLOW_ARTIFACT_URI) \
	--host $(MLFLOW_HOST) \
	--port $(MLFLOW_PORT)