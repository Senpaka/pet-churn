from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import services.fastapi.routers.root as root
import services.fastapi.routers.predict as predict
import services.fastapi.routers.health as health

from services.fastapi.middleware import RequestLoggingMiddleware
from services.fastapi.model_loader import load_predictor

from core.logging_config import setup_logging

import logging

setup_logging("fastapi.log")
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

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(health.router)
app.include_router(predict.router)

if __name__ == "__main__":
    uvicorn.run(app="app:app", reload=True, port=8000)

