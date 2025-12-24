"""
Logging configuration for HelloGUI application.

Sets up a rotating file handler (logs/hellogui.log) and console logging
with appropriate formatting and level configuration.
"""

import logging
import logging.handlers
from pathlib import Path


def setup_logging(log_dir: str = "logs", log_level: int = logging.INFO) -> logging.Logger:
    """
    Configure logging for HelloGUI with file and console handlers.

    Creates a logs directory if it doesn't exist and sets up a rotating file
    handler (10 MB max, 5 backups) plus console output.

    Args:
        log_dir (str): Directory for log files. Defaults to "logs".
        log_level (int): Logging level (DEBUG, INFO, WARNING, ERROR). Defaults to INFO.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create logs directory if needed
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    # Create logger
    logger = logging.getLogger("hellogui")
    logger.setLevel(log_level)

    # Remove any existing handlers (for re-initialization)
    logger.handlers.clear()

    # Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler (rotating)
    file_handler = logging.handlers.RotatingFileHandler(
        log_path / "hellogui.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("Logging initialized: %s", log_dir)
    return logger
