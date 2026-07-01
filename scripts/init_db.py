import argparse
import sys

import pandas as pd
import os
import dotenv
from pathlib import Path
from sqlalchemy import create_engine, text, Engine

BASE_DIR = Path(__file__).resolve().parents[1]
dotenv.load_dotenv(BASE_DIR / ".env")

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(BASE_DIR / "logs/bd.log")
    ]
)
logger = logging.getLogger(__name__)

def get_engine() -> Engine:
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise ValueError("БД не найдена")

    return create_engine(db_url)

def create_table(engine: Engine) -> None:

    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                "customerID" VARCHAR(50) PRIMARY KEY,
                "gender" VARCHAR(20),
                "SeniorCitizen" INTEGER,
                "Partner" VARCHAR(10),
                "Dependents" VARCHAR(10),
                "tenure" INTEGER,
                "PhoneService" VARCHAR(30),
                "MultipleLines" VARCHAR(30),
                "InternetService" VARCHAR(30),
                "OnlineSecurity" VARCHAR(30),
                "OnlineBackup" VARCHAR(30),
                "DeviceProtection" VARCHAR(30),
                "TechSupport" VARCHAR(30),
                "StreamingTV" VARCHAR(30),
                "StreamingMovies" VARCHAR(30),
                "Contract" VARCHAR(50),
                "PaperlessBilling" VARCHAR(10),
                "PaymentMethod" VARCHAR(50),
                "MonthlyCharges" DOUBLE PRECISION,
                "TotalCharges" DOUBLE PRECISION
                );
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                customer_id VARCHAR(10) NOT NULL,
                risk VARCHAR(10) NOT NULL,
                probability FLOAT NOT NULL,
                prediction VARCHAR(6) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
        """))

        logger.info("Таблицы успешно созданы или уже существовали")

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
    create_table(engine)

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

