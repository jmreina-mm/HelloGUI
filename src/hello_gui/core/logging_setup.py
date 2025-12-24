# ==================================================================================================
#  HelloGUI - Python Data Stream Visualization Demo
#  Module: core/logging_setup.py (Logging Configuration)
#  Purpose: Initialize rotating file and console logging with formatting
# ==================================================================================================

"""
Logging configuration for HelloGUI application.

Sets up a rotating file handler (logs/hellogui.log) and console logging
with appropriate formatting and level configuration.
"""

import logging
import logging.handlers
from pathlib import Path


# --- Initialize rotating file and console logging with formatting ---
def setup_logging(log_dir: str = "logs", log_level: int = logging.INFO) -> logging.Logger:
    """
    ################################################################################################
    @fcn        setup_logging
    @brief      Configure rotating file and console logging.
    @details    Creates logs directory, sets up RotatingFileHandler (10 MB, 5 backups) and
                console handler with consistent formatting. Returns configured logger instance.

    @param[in]  log_dir     Directory for log files. Defaults to "logs".
    @param[in]  log_level   Logging level (DEBUG, INFO, WARNING, ERROR). Defaults to INFO.
    @return     (logging.Logger) Configured "hellogui" logger instance.

    @pre        log_dir is writable; log_level is valid logging level.
    @post       log_dir created if needed; "hellogui" logger configured globally.

    @section    Operation
         1. Create logs directory
         2. Clear any existing handlers (re-initialization safe)
         3. Configure rotating file handler (10 MB max, 5 backups)
         4. Configure console handler at specified level
         5. Apply consistent formatter to both
         6. Return configured logger

    @note       Typical call at application startup before operational logging begins.
    ################################################################################################
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
