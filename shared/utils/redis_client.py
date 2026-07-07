import redis
import json
import logging

from core.settings import settings

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self, redis_uri: str | None = None):
        logger.info("Присоединение к Redis")
        self.redis_uri = redis_uri or settings.redis_uri
        if not self.redis_uri:
            logger.warning("Ошибка присоединения, не указан uri")
            raise ValueError("Redis uri не указан")
        self.client = redis.from_url(self.redis_uri, decode_responses=True)
        logger.info("Присоединение прошло успешно")

    def test_connection(self) -> bool:
        logger.info("Тест присоединения...")
        return self.client.ping()

    def set_task_status(self, task_id: str, status: str, payload: dict | None = None) -> None:
        logger.info("Загрузка статуса таска")
        self.client.set(
            f"task: {task_id}",
            json.dumps({
                "status": status,
                "payload": payload or {}
            }),
            ex=3600
        )

    def get_task_status(self, task_id: str) -> dict | None:
        status = self.client.get(f"task: {task_id}")
        logger.info("Получение статуса таска")

        if status is None:
            logger.warning(f"Такого таска не существует {task_id}")
            return None

        return json.loads(status)

if __name__ == "__main__":
    redis_client = RedisClient()
    redis_client.test_connection()