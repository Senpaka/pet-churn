import uuid
import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware для логгирования FastAPI запросов
    """

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            process_time = time.perf_counter() - start_time

            response.headers["X-Process-Time"] = str(round(process_time, 4))
            response.headers["X-Request-Id"] = request_id

            logger.info(
                f"request_id={request_id}, "
                f" method={request.method}, "
                f"path={request.url.path} , "
                f"status_code={response.status_code}, "
                f"process_time={process_time}"
            )

            return response

        except Exception as e:
            process_time = time.perf_counter() - start_time

            logger.info(
                f"request_id={request_id}, "
                f" method={request.method}, "
                f"path={request.url.path} , "
                f"process_time={process_time}, "
                f"error={e} "
            )

            raise
