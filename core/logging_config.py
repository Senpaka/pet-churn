import logging
import sys

import core.paths as paths

def setup_logging(log_name: str = "tmp.log") -> None:
    """
    Установка главного логгера

    :param log_name: имя файла лога
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(paths.LOGS_DIR / log_name, encoding="utf-8")
        ]
    )
