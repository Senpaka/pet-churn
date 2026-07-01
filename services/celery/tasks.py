import datetime
import time
from typing import List

import pandas as pd

from services.celery.celery_app import app
from shared.utils.utils import get_risk_level
from services.fastapi.model_loader import load_predictor

import logging

logger = logging.getLogger(__name__)

_predictor = None

def get_worker_predictor():
    global _predictor

    if _predictor is None:
        logger.info("Загрузка predictor в Celery Worker")
        _predictor = load_predictor()
        logger.info("Predictor успешно загружен")

    return _predictor

@app.task(name="hard_batch_predict_task", queue="cpu_worker")
def hard_batch_predict_task(customers: List[dict]):

    predictor = get_worker_predictor()

    df = pd.DataFrame(customers)

    probabilities = predictor.predict_proba(df)

    predictions = []

    for customer_feature, probability in zip(customers, probabilities):

        probability = float(probability)
        prediction = "Churn" if probability > predictor.threshold else "Stay"

        risk = get_risk_level(probability)

        predictions.append({
            "customer_id": customer_feature.get("customerID"),
            "risk": risk,
            "probability": probability,
            "prediction": prediction,
            "timestamp": datetime.datetime.now().isoformat()
        })

    return {
        "count": len(customers),
        "predictions": predictions
    }



