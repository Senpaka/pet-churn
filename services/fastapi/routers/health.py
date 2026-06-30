from datetime import datetime

from fastapi import APIRouter, Depends

from services.fastapi.dependencies import get_db_client
from services.fastapi.schemas import HealthResponse, DataBaseResponse
from services.fastapi.db_client import DBClient

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/health",
    tags=["health"],
)

@router.get("/", response_model=HealthResponse)
async def health():
    logger.info(f"Проверка здоровья")
    return HealthResponse(
        status=200,
        timestamp=datetime.now(),
    )

@router.get("/ping", response_model=DataBaseResponse)
async def ping(
        db_client: DBClient = Depends(get_db_client)
):
    logger.info("Проверка присоединения бд")
    if db_client.test_connection():
        logger.info("БД присоединена")
        return DataBaseResponse(
            status="ok",
            timestamp=datetime.now(),
        )

    logger.warning("Ошибка присоединения")
    return DataBaseResponse(
        status="Not Connected",
        timestamp=datetime.now(),
    )