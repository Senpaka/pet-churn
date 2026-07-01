import datetime
import time
from typing import List

import pandas as pd

from services.celery.celery_app import app
from services.fastapi.db_client import DBClient
from shared.utils.utils import get_risk_level
from services.fastapi.model_loader import load_predictor

import logging

logger = logging.getLogger(__name__)

_predictor = None
_db_client = None

def _get_worker_predictor():
    global _predictor

    if _predictor is None:
        logger.info("Загрузка predictor в Celery Worker")
        _predictor = load_predictor()
        logger.info("Predictor успешно загружен")

    return _predictor

def _get_db_client():
    global _db_client

    if _db_client is None:
        logger.info("Загрузка клиента БД в Celery Worker")
        _db_client = DBClient()
        logger.info("Клиент БД загружен")

    return _db_client

@app.task(name="predict_from_db_task", queue="cpu_worker")
def predict_from_db_task():

    logger.info("Загрузка predictor и db_client")
    predictor = _get_worker_predictor()
    db_client = _get_db_client()

    logger.info("Загрузка датафрейма из бд")
    df = db_client.load_table("customers")

    logger.info("Выполнение предсказаний")
    probabilities = predictor.predict_proba(df)
    predictions = []
    created_at = datetime.datetime.now().isoformat()

    for idx, (_, row) in enumerate(df.iterrows()):

        probability = float(probabilities[idx])

        predictions.append({
            "customer_id": row.get("customerID"),
            "risk": get_risk_level(probability),
            "probability": probability,
            "prediction": "Churn" if probability > predictor.threshold else "Stay",
            "timestamp": created_at
        })

    predictions_df = pd.DataFrame(predictions)

    logger.info("Сохранение в бд")
    db_client.save_predictions(predictions_df, "predictions")

    return {
        "status": "saved to db",
        "count": len(df),
        "timestamp": created_at
    }

@app.task(name="hard_batch_predict_task", queue="cpu_worker")
def hard_batch_predict_task(customers: List[dict]):

    predictor = _get_worker_predictor()

    df = pd.DataFrame(customers)

    probabilities = predictor.predict_proba(df)

    predictions = []
    created_at = datetime.datetime.now().isoformat()

    for customer_feature, probability in zip(customers, probabilities):

        probability = float(probability)
        prediction = "Churn" if probability > predictor.threshold else "Stay"

        risk = get_risk_level(probability)

        predictions.append({
            "customer_id": customer_feature.get("customerID"),
            "risk": risk,
            "probability": probability,
            "prediction": prediction,
            "timestamp": created_at
        })

    return {
        "count": len(customers),
        "predictions": predictions
    }



