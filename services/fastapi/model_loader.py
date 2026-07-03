import mlflow
from mlflow import MlflowClient

from shared.predict import Predictor
from core.settings import settings

import logging

logger = logging.getLogger(__name__)

def load_predictor() -> Predictor:

    logger.info(f"Загрузка Predictor")

    tracking_uri = settings.mlflow_tracking_uri

    model_name = settings.model_name
    model_alias = settings.model_alias

    mlflow.set_tracking_uri(tracking_uri)

    model_uri = f"models:/{model_name}@{model_alias}"

    model = mlflow.catboost.load_model(model_uri)

    client = MlflowClient()

    model_version = client.get_model_version_by_alias(
        name=model_name,
        alias=model_alias,
    )

    threshold = float(model_version.tags.get("threshold"))

    logger.info("Predictor успешно получен")
    logger.info(f"model: {model_name}")
    logger.info(f"alias: {model_alias}")
    logger.info(f"threshold: {threshold}")

    return Predictor(
        model=model,
        threshold=threshold,
    )





