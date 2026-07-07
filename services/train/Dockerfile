FROM python:3.12-slim-trixie

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements/ requirements/

RUN pip install --no-cache-dir -r requirements/train.txt

COPY core/ core/
COPY shared/ shared/
COPY services/ services/
COPY scripts/ scripts/

CMD ["python3", "-m", "scripts.train_model"]