from services.fastapi.db_client import DBClient

def get_db_client():
    return DBClient()