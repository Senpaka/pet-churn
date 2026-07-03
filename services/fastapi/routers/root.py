from fastapi import APIRouter

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/root",
    tags=["root"],
)

@router.get("/", tags=["root"])
def root():
    """
    Информация про API
    """

    logger.info("Информация об API")
    return {
        "Версия": "1.0.0",
        "Автор": "Senpaka",
        "Описание": "FastAPI сервис для предсказания оттока",
        "Документация": "/docs",
        "Документация (redoc)": "/redoc",
        "Проверка здоровья": "/health",
        "Проверка БД": "/health/ping",
        "Предсказание": "/model/predict",
        "Batch-предсказание": "/model/batch_predict",
        "Тяжелые предсказания": "/model/hard_predict",
    }