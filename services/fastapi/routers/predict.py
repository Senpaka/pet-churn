import logging
from datetime import datetime

from typing import List

import pandas as pd
from celery.result import AsyncResult
from fastapi import APIRouter, Request, HTTPException

from services.fastapi.schemas import CustomerFeatures, PredictionResponse, BatchPredictionResponse
from shared.predict import Predictor
from shared.utils.utils import get_risk_level

from services.celery.tasks import hard_batch_predict_task, predict_from_db_task
from services.celery.celery_app import app as celery_app

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/model",
    tags=["model"],
)

@router.post("/predict", response_model=PredictionResponse)
async def predict(
        customer: CustomerFeatures,
        request: Request
):
    try:
        logger.info("Выполнение предсказания")
        predictor = request.app.state.predictor

        result = make_prediction(predictor, customer.model_dump())
        logger.info("Предсказание выполнено")

        return PredictionResponse(**result)

    except Exception as e:
        logger.exception(f"Ошибка предсказания: {e}")
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )


@router.post("/batch_predict", response_model=BatchPredictionResponse)
async def batch_predict(
        customers: List[CustomerFeatures],
        request: Request
):
    try:
        logger.info("Выполнение batch-предсказания")
        predictor = request.app.state.predictor

        customer_data = [c.model_dump() for c in customers]

        responses = make_batch_prediction(predictor, customer_data)
        logger.info("batch-предсказание выполнено")

        return BatchPredictionResponse(predictions=responses)

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(f"Ошибка batch-предсказания: {e}")
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

@router.post("/predict_from_db")
async def predict_from_db() -> dict:
    try:
        logger.info("Выполнение предсказания для базы данных")
        task = predict_from_db_task.delay()
        logger.info("Предсказание выполнено")

        response = {
            "task_id": task.task_id,
            "status": task.status,
        }

        if task.successful():
            logger.info("Таск выполнен успешно")
            response["result"] = task.result
        elif task.failed():
            logger.info("Таск упал")
            response["error"] = str(task.result)

        return response

    except Exception as e:
        logger.exception(f"Ошибка предсказания: {e}")
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

@router.get("/task/{task_id}")
async def get_task_results(task_id: str) -> dict:
    logger.info("Получение результатов выполнения таска")
    task = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "status": task.status,
    }

    if task.successful():
        logger.info("Таск выполнен")
        response["result"] = task.result
    elif task.failed():
        logger.warning("Таск упал!")
        response["error"] = str(task.result)

    return response

def make_batch_prediction(
        predictor: Predictor,
        customer_features: List[dict]
) -> List[PredictionResponse]:

    df = pd.DataFrame(customer_features)

    probabilities = predictor.predict_proba(df)

    responses = []

    for customer_feature, probability in zip(customer_features, probabilities):
        probability = float(probability)

        prediction = "Churn" if probability > predictor.threshold else "Stay"
        risk = get_risk_level(probability)

        responses.append(PredictionResponse(
            prediction=prediction,
            risk=risk,
            probability=probability,
            customer_id=customer_feature.get("customerID"),
            timestamp=datetime.now(),
        ))

    return responses

def make_prediction(predictor: Predictor, customer_features: dict) -> dict:
    df = pd.DataFrame([customer_features])

    probability = float(predictor.predict_proba(df)[0])
    prediction = "Churn" if probability > predictor.threshold else "Stay"

    risk = get_risk_level(probability)

    return {
        "risk": risk,
        "probability": probability,
        "customer_id": customer_features.get("customerID"),
        "timestamp": datetime.now(),
        "prediction": prediction,
    }


