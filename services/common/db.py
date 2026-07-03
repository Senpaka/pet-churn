
import os
import dotenv
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = Path(__file__).resolve().parents[2]
dotenv.load_dotenv(str(BASE_DIR / '.env'))

DB_URL = os.getenv("DATABASE_URL")

if not DB_URL:
    raise ValueError("База данных не найдена")

engine = create_engine(DB_URL)

session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()