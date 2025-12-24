"""
HelloGUI application entry point and bootstrapper.

Initializes logging, creates the Qt application and main window,
and starts the event loop.
"""

import sys
import logging

from PySide6.QtWidgets import QApplication

from hello_gui.core import setup_logging
from hello_gui.main_window import MainWindow


def main() -> int:
    """
    Main entry point for HelloGUI application.

    Initializes logging, creates QApplication, main window,
    and runs the event loop.

    Returns:
        int: Application exit code.
    """
    # Setup logging
    logger = setup_logging(log_dir="logs", log_level=logging.INFO)
    logger.info("=" * 60)
    logger.info("HelloGUI Application Starting")
    logger.info("=" * 60)

    try:
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("HelloGUI")
        app.setApplicationVersion("1.0.0")

        # Create main window
        window = MainWindow()
        window.show()

        logger.info("Main window displayed")

        # Run event loop
        exit_code = app.exec()

        logger.info("Application exiting with code: %d", exit_code)
        return exit_code

    except Exception as e:
        logger.exception("Fatal error in main: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
