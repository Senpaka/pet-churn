FROM python:3.12-slim-trixie

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements/ requirements/

RUN pip install --no-cache-dir -r requirements/api.txt

COPY services/ services/
COPY core/ core/
COPY shared/ shared/
COPY scripts/ scripts/

CMD uvicorn ${FASTAPI_APP_PATH}:app \
	--host ${FASTAPI_HOST} \
	--port ${FASTAPI_PORT}