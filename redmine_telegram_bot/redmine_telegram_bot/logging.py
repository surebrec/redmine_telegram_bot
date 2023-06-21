import logging
from logging.handlers import RotatingFileHandler

from django.conf import settings


def configure_logging() -> None:
    """Configure logger"""
    log_dir = settings.BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'parser.log'
    rotating_handler = RotatingFileHandler(
        log_file,
        maxBytes=settings.MAX_LOG_FILE_BYTES,
        backupCount=settings.MAX_LOG_FILE_NUMBER,
        encoding='utf-8',
    )
    logging.basicConfig(
        datefmt=settings.LOG_DATE_FORMAT,
        format=settings.LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )


configure_logging()
