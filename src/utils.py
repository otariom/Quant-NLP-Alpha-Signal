import logging
import os
from datetime import datetime
from src.config import config


def setup_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger.
    """

    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)

    # Prevent duplicate logs
    if not logger.handlers:

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.LOG_LEVEL)

        # Formatter
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


def ensure_directories():
    """
    Ensure required directories exist.
    """

    dirs = [
        config.DATA_DIR,
        config.RAW_DATA_DIR,
        config.PROCESSED_DATA_DIR,
        config.MODEL_DIR,
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)


def get_timestamp() -> str:
    """
    Returns current timestamp string.
    """

    return datetime.now().strftime("%Y%m%d_%H%M%S")