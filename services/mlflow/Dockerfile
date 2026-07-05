FROM python:3.12-slim-trixie

WORKDIR /app

COPY requirements/ requirements/

RUN pip install --no-cache-dir -r requirements/mlflow.txt

CMD mlflow server \
	--backend-store-uri ${MLFLOW_DATABASE_URI} \
	--default-artifact-root ${MLFLOW_ARTIFACT_URI} \
	--host 0.0.0.0 \
	--port 5000 \
	--allowed-hosts "mlflow:5000,localhost:5001,127.0.0.1:5001"
