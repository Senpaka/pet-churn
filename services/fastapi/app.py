import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

import services.fastapi.routers.root as root
import services.fastapi.routers.predict as predict
import services.fastapi.routers.health as health

from pathlib import Path

from services.fastapi.model_loader import load_predictor

BASE_DIR = Path(__file__).resolve().parents[2]

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(BASE_DIR / "logs/fastapi.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Загрузка модели")
    app.state.predictor = load_predictor()
    logger.info("Модель загружена")

    yield

    logger.info("Остановка приложения")

app = FastAPI(
    version="1.0.0",
    title="API предсказания",
    description="Предсказание оттока клиентов",
    lifespan=lifespan
)

app.include_router(root.router)
app.include_router(health.router)
app.include_router(predict.router)

if __name__ == "__main__":
    uvicorn.run(app="app:app", reload=True, port=8000)

