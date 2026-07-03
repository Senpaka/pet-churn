import argparse
import sys

import pandas as pd
import os
import dotenv
from pathlib import Path
from sqlalchemy import create_engine, text, Engine

from core.logging_config import setup_logging
from core.settings import settings
import logging

setup_logging("bd.log")
logger = logging.getLogger(__name__)

def get_engine() -> Engine:
    db_url = settings.database_url

    if not db_url:
        raise ValueError("БД не найдена")

    return create_engine(db_url)

def load_customers(engine: Engine, csv_url: Path) -> None:

    if not csv_url.exists():
        logger.warning(f"csv файл не найден: {csv_url}")
        raise FileExistsError(f"csv файл не найден: {csv_url}")

    df = pd.read_csv(csv_url)

    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    if "MonthlyCharges" in df.columns:
        df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce")

    if "Churn" in df.columns:
        df.drop("Churn", axis=1, inplace=True)

    df.to_sql("customers", engine, if_exists="append", index=False)

    logger.info("Данные для бд customers успешно загруженны")

def delete_table(engine: Engine, table_name: str) -> None:
    with engine.begin() as conn:
        conn.execute(text(f"""
            DROP TABLE IF EXISTS {table_name};
        """))

if __name__ == "__main__":

    engine = get_engine()

    parser = argparse.ArgumentParser("Утилита для управления бд")

    parser.add_argument("--load_customers", type=str, help="Загрузить csv файл в бд")
    parser.add_argument("--delete_table", type=str, help="Удалить таблицу из бд")

    args = parser.parse_args()

    if args.load_customers:
        logger.info("Загузка csv файл в бд")
        load_customers(engine, Path(args.load_customers))
        logger.info("csv файл успешно загружен в бд")

    if args.delete_table:
        logger.info(f"Удаление таблицы: {args.delete_table}")
        delete_table(engine, args.delete_table)
        logger.info("Таблица удалена")

