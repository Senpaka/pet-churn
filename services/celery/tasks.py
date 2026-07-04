import datetime

import pandas as pd

from services.celery.celery_app import app
from services.common.db_client import DBClient
from shared.model_loader import load_predictor
from shared.utils.utils import get_risk_level

import logging


logger = logging.getLogger(__name__)

_predictor = None
_db_client = None

def _get_worker_predictor():
    """
    Получение предсказателя (Predictor)

    :return: Predictor
    """

    global _predictor

    if _predictor is None:
        logger.info("Загрузка predictor в Celery Worker")
        _predictor = load_predictor()
        logger.info("Predictor успешно загружен")

    return _predictor

def _get_db_client():
    """
    Получение клиента базы данных

    :return: клиент бд (DBClient)
    """

    global _db_client

    if _db_client is None:
        logger.info("Загрузка клиента БД в Celery Worker")
        _db_client = DBClient()
        logger.info("Клиент БД загружен")

    return _db_client

@app.task(name="predict_from_db_task", queue="cpu_worker")
def predict_from_db_task():
    """
    Предсказание на всей бд
    с последущим сохранением в таблицу predictions

    :return: словарь-ответ
    """

    logger.info("Загрузка predictor и db_client")
    predictor = _get_worker_predictor()
    db_client = _get_db_client()

    logger.info("Загрузка датафрейма из бд")
    df = db_client.load_table("customers")

    logger.info("Выполнение предсказаний")
    probabilities = predictor.predict_proba(df)
    predictions = []
    created_at = datetime.datetime.now().isoformat()
    threshold = predictor.threshold

    for idx, (_, row) in enumerate(df.iterrows()):

        probability = float(probabilities[idx])

        predictions.append({
            "customer_id": row.get("customerID"),
            "risk": get_risk_level(probability),
            "probability": probability,
            "prediction": "Churn" if probability > threshold else "Stay",
            "timestamp": created_at,
            "threshold": threshold
        })

    predictions_df = pd.DataFrame(predictions)

    logger.info("Сохранение в бд")
    db_client.save_predictions(predictions_df, "predictions")

    return {
        "status": "saved to db",
        "count": len(df),
        "created_at": created_at
    }