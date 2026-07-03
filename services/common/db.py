from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.settings import settings


DB_URL = settings.database_url

if not DB_URL:
    raise ValueError("База данных не найдена")

engine = create_engine(DB_URL)

session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()