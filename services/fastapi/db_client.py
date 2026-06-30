import os
import dotenv
from pathlib import Path

import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
dotenv.load_dotenv(BASE_DIR / ".env")


class DBClient:

    def __init__(self, db_uri: str | None = None):
        logger.info("Присоединение к базу данных")
        self.db_url = db_uri or os.getenv("DATABASE_URL")
        if not self.db_url:
            logger.warning("Ошибка присоединения, не указан uri")
            raise ValueError("База данных не задана")
        self.engine = create_engine(self.db_url)
        logger.info("Присоединение прошло успешно")


    def test_connection(self) -> bool:
        logger.info("Тест присоединения...")
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.exception(f"Ошибка присоединения БД: {e}")
            return False

    def load_table(self, table_name: str) -> DataFrame:
        logger.info("Получение таблицы")
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, self.engine)

    def save_predictions(self, df: DataFrame, table_name: str = "Predictions") -> None:
        logger.info("Сохранение предсказаний")
        df.to_sql(table_name, self.engine, if_exists="append", index=False)

if __name__ == "__main__":
    db = DBClient()
    db.test_connection()