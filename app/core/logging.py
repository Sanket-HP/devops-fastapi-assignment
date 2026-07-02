import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from app.core.config import settings

def setup_logging() -> None:
    log_dir = settings.LOG_DIR
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Standard format: timestamp, level, logger name, filename, line number, message
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
    )

    # Console output handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # General application log file
    app_log_path = os.path.join(log_dir, "app.log")
    file_handler = RotatingFileHandler(
        app_log_path, maxBytes=10485760, backupCount=5  # 10MB
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Error-only log file
    error_log_path = os.path.join(log_dir, "error.log")
    error_file_handler = RotatingFileHandler(
        error_log_path, maxBytes=10485760, backupCount=5  # 10MB
    )
    error_file_handler.setFormatter(formatter)
    error_file_handler.setLevel(logging.ERROR)

    # Root logger config
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_file_handler)

    # Direct uvicorn loggers to use our config
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        log = logging.getLogger(logger_name)
        log.handlers.clear()
        log.propagate = True
