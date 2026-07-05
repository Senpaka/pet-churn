import argparse

from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, precision_score, recall_score
from catboost import CatBoostClassifier
import mlflow.catboost
import mlflow
import pandas as pd
import numpy as np
import optuna

from shared.features import FeatureBuilder
from scripts.config import config
from core.logging_config import setup_logging
from core.settings import settings

import logging

setup_logging("train.log")
logger = logging.getLogger(__name__)

class TrainModel:
    """
    Класс для обучения модели CatBoost-Classifier
    """

    def __init__(self):
        """
        Инициалиализирует объект TrainModel

        Устанавливает базовые настройки mlflow
        """

        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        mlflow.set_experiment(settings.mlflow_experiment_name)

        self.model = None
        self.metrics = None
        self.feature_builder = FeatureBuilder()
        self.is_train = False

        logger.info("TrainModel инициализирован")

    def train(self, df: pd.DataFrame) -> None:
        """
        Обучает модель с использованием подбора гиперпараметров (Optuna)
        Так же происходи логирование метрик и данных модели в mlflow

        Процесс обучения:
        1. Проверка входных данных
        2. Разбиение на Train/test
        3. Подбор гиперпараметров через Optuna
        4. Обучение финальной модели
        5. Оценка метрик и логирование в MLFlow

        :param df: датасет для обучения
        """

        if df.empty:
            logger.warning("Датафрейм пустой...")
            raise ValueError("Датафрейм пустой...")

        if "Churn" not in df.columns:
            logger.warning("Отсутствует целевая переменная")
            raise ValueError("Отсутствует целевая переменная")

        logger.info("Старт обучения")
        df_train = self.feature_builder.build(df)
        logger.info("Фичи созданы")

        X = df_train.drop(columns=["Churn"], axis=1)
        y = df_train["Churn"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=config.RANDOM_SEED, stratify=y)

        storage = optuna.storages.RDBStorage(settings.optuna_database_uri)

        logger.info("Подбор параметров оптуной...")

        try:
            with mlflow.start_run(
                    run_name='Подбор параметров с Optuna',
            ):
                study = optuna.create_study(
                    storage=storage,
                    study_name=config.STUDY_NAME,
                    direction="maximize",
                    load_if_exists=True
                )

                study.optimize(lambda trial: self.objective(trial, X_train, y_train), n_trials=10, n_jobs=1)

                mlflow.log_metric("best_roc_auc", study.best_value)

                mlflow.log_params({f"best_{key}": value
                                   for key, value in study.best_trial.params.items()})

                mlflow.set_tag("study_name", study.study_name)
                mlflow.set_tag("n_trials", 100)
                mlflow.set_tag("direction", "maximize")

                mlflow.log_dict(study.best_params, "best_params.json")

                logger.info("Подбор параметров завершен")

                logger.info("Обучение с оптуной")

                params = {
                    "iterations": config.MODEL_ITERATIONS,
                    "random_seed": config.RANDOM_SEED,
                    "verbose": config.VERBOSE,
                    "auto_class_weights": config.AUTO_CLASS_WEIGHTS,
                    **study.best_params
                }

                self.model = CatBoostClassifier(**params)

                logger.info("Модель создана")

        except Exception as e:
            logger.exception(f"Не удалось загрузить параметры Optuna, запускаем с дефолтными параметрами: {e}")
            logger.info("Обучение без оптуны")

            params = {
                "iterations":config.MODEL_ITERATIONS,
                "learning_rate": config.LEARNING_RATE,
                "depth": config.DEPTH,
                "l2_leaf_reg": config.L2_LEAF,
                "random_strength": config.RANDOM_STRENGTH,
                "bagging_temperature": config.BAGGING_TEMPERATURE,
                "auto_class_weights": config.AUTO_CLASS_WEIGHTS,
                "random_state": config.RANDOM_SEED,
                "verbose": config.VERBOSE,
                "thread_count": config.THREADS_COUNT
            }

            self.model = CatBoostClassifier(**params)

            logger.info("Модель создана")

        with mlflow.start_run(run_name="Финальное обучение"):
            logger.info("Обучение модели...")
            self.model.fit(X_train, y_train, cat_features=config.CAT_FEATURES)
            logger.info("Модель обучена!")

            mlflow.set_tags({
                "n_trials": 100,
                "model_type": "CatBoostClassifier"
            })

            mlflow.log_params(
                {
                    "threshold": config.THRESHOLD,
                    "random_seed": config.RANDOM_SEED,
                    "test_size": 0.2,
                    "cv_n_splits": 5,
                    "cv_scoring": "roc_auc",
                    "train_rows": X_train.shape[0],
                    'test_rows': X_test.shape[0],
                    "n_features": X_train.shape[1]
                }
            )

            y_proba = self.model.predict_proba(X_test)[:,1]
            y_prediction = (y_proba > config.THRESHOLD).astype(int)

            roc_auc = roc_auc_score(y_test, y_proba)
            accuracy = accuracy_score(y_test, y_prediction)
            f1 = f1_score(y_test, y_prediction)
            precision = precision_score(y_test, y_prediction)
            recall = recall_score(y_test, y_prediction)

            cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=config.RANDOM_SEED)

            cv_score = cross_val_score(self.model,
                                       X_train, y_train,
                                       cv=cv, verbose=False, scoring="roc_auc",
                                       params={"cat_features": config.CAT_FEATURES})

            metrics = {"roc_auc": roc_auc,
                       "accuracy": accuracy,
                       "f1": f1,
                       "precision": precision,
                       "recall": recall,
                       "cv_roc_auc_mean": cv_score.mean(),
                       "cv_roc_auc_std": cv_score.std()}

            mlflow.log_metrics(metrics)

            logger.info("Модель полностью обучена:")

            for fold_idx, fold_score in enumerate(cv_score):
                mlflow.log_metric("cv_roc_auc_fold", fold_score, step=fold_idx)

            for key, value in metrics.items():
                logger.info(f"{key}: {value}")

            mlflow.log_dict(
                {
                    **metrics,
                    "cv_roc_auc_folds": cv_score
                },
                "metrics/metrics.json"
            )

            mlflow.log_params(self.model.get_params())

            input_expl = X_train.head(5)
            signature = infer_signature(input_expl, self.model.predict_proba(input_expl)[:, 1])
            model_name = config.MODEL_NAME

            mlflow.catboost.log_model(
                cb_model=self.model,
                name="model",
                signature=signature,
                input_example=input_expl,
                registered_model_name=model_name
            )

            mlflow.log_dict(
                {
                    "features": list(X_train.columns),
                    "cat_features": config.CAT_FEATURES
                },
                "features/features.json"
            )

            client = MlflowClient()

            versions = client.search_model_versions(f"name = '{model_name}'")
            current_version = max(versions, key=lambda v: int(v.version))

            client.set_model_version_tag(
                name=model_name,
                version=current_version.version,
                key="status",
                value="candidate"
            )

            client.set_model_version_tag(
                name=model_name,
                version=current_version.version,
                key="threshold",
                value=str(config.THRESHOLD)
            )

            client.set_registered_model_alias(
                name=model_name,
                version=current_version.version,
                alias="candidate"
            )

            self.metrics = metrics
            self.is_train = True

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """
        Возвращает предсказание модели (0/1)

        :param df: Датасет
        :return: numpy массив вероятностей
        """

        if not self.is_train:
            logger.warning("Модель не обучена")
            raise ValueError("Модель не обучена")

        y_proba = self.predict_proba(df)
        y_predict = (y_proba > config.THRESHOLD).astype(int)

        return y_predict


    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """
        Возвращает предсказание модели в виде вероятностей (0-1)

        :param df: Датасет
        :return: numpy массив вероятностей
        """
        if not self.is_train:
            logger.warning("Модель не обучена")
            raise ValueError("Модель не обучена")

        X = self.feature_builder.build(df)

        y_proba = self.model.predict_proba(X)[:,1]

        return y_proba

    def objective(self, trial: optuna.trial.Trial, X_train, y_train) -> float:
        """
        Метод для подбора гиперпараметоров

        :param trial: Триал
        :param X_train: Обучающая выборка
        :param y_train: Обучающая целевая переменная
        :return: cv_score среднее значение кросс валидации
        """

        params = {
            "iterations": config.MODEL_ITERATIONS,
            "learning_rate": trial.suggest_float("learning_rate", 0.005, 0.1, log=True),
            "depth": trial.suggest_int("depth", 3, 8),
            "l2_leaf_reg":trial.suggest_float("l2_leaf_reg", 1, 10),
            "random_strength":trial.suggest_int("random_strength", 1, 10),
            "bagging_temperature":trial.suggest_float("bagging_temperature", 0, 1),
            "auto_class_weights":config.AUTO_CLASS_WEIGHTS,
            "random_state":config.RANDOM_SEED,
            "verbose":False,
            "thread_count":config.THREADS_COUNT
        }

        with mlflow.start_run(
                run_name=f"Запуск_{trial.number}",
                nested=True
        ):
            model = CatBoostClassifier(**params)

            cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=config.RANDOM_SEED)

            cv_score = cross_val_score(model,
                                       X_train, y_train,
                                       cv=cv, verbose=False, scoring="roc_auc",
                                       params={"cat_features": config.CAT_FEATURES}
                                       )

            mlflow.log_metric("roc_auc", cv_score.mean())

            mlflow.log_params(params)

            mlflow.set_tag("Номер попытки", trial.number)
            mlflow.set_tag("Модель", "CatBoostClassifier")

        return cv_score.mean()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset-path", type=str, default="./datasets/dataset.csv")

    args = parser.parse_args()

    if args.dataset_path:
        df = pd.read_csv(args.dataset_path)

        trainer = TrainModel()

        trainer.train(df)