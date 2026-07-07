FROM python:3.12-slim-trixie

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements/ requirements/

RUN pip install --no-cache-dir -r requirements/worker.txt

COPY core/ core/
COPY shared/ shared/
COPY services/ services/
COPY scripts/ scripts/

CMD celery -A services.celery.celery_app:app worker \
    -Q cpu_worker \
    --hostname=cpu_worker@%h \
    --concurrency=${CELERY_CPU_CONCURRENCY:-1} \
    --prefetch-multiplier=${CELERY_CPU_MULTIPLIER:-1} \
    --loglevel=info