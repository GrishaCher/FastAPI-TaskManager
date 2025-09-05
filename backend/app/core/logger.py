import logging
from app.core.config import settings
def setup_logger(
    disable_logging: bool = False,
    log_level: int = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    log_file: str = settings.LOG_FILE,
    console_log: bool = True
) -> None:
    if disable_logging:
        logging.disable(logging.CRITICAL)
        return

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Создаем логгер приложения
    logger = logging.getLogger("app")
    logger.setLevel(log_level)

    # Очищаем существующие обработчики
    logger.handlers.clear()

    if console_log:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if log_file:
        from logging.handlers import RotatingFileHandler
        fh = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5,
            encoding="utf-8"
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)