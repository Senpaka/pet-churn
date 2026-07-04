from fastapi import APIRouter

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["root"],
)

@router.get("/", tags=["root"])
def root():
    """
    Информация про API
    """

    logger.info("Информация об API")
    return {
        "version": "1.0.0",
        "author": "Senpaka",
        "description": "FastAPI service for churn prediction",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "db_health": "/health/ping",
        "predict": "/model/predict",
        "batch_predict": "/model/batch_predict",
        "predict_from_db": "/model/predict_from_db",
    }