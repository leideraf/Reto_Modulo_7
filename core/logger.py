import logging
import os
from logging.handlers import TimedRotatingFileHandler


def init_logger():
    """
    Inicializa el sistema de logging con rotación diaria.
    Guarda logs en /logs/app.log
    """
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(
        filename="logs/app.log",
        when="midnight",
        backupCount=7,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger
