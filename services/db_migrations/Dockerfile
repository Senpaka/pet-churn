FROM python:3.12-slim-trixie

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements/ requirements/

RUN pip install --no-cache-dir -r requirements/migrations.txt

COPY services/__init__.py services/__init__.py
COPY services/common/ services/common/

COPY scripts/ scripts/

COPY core/ core/

COPY alembic/ alembic/

COPY alembic.ini alembic.ini
