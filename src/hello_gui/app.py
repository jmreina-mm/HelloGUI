# =================================================================================================
#  HelloGUI - Python Data Stream Visualization Demo
#  Module: app.py (Application Entry Point)
#  Purpose: Qt application bootstrap and main window initialization
#  License: MIT (unless otherwise specified in repository)
#  Author: HelloGUI Development Team
#  Created: 2025-12-23
#  Last Rev: 2025-12-23
# =================================================================================================

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


# --- Main application entry point: initialize Qt and run event loop ---
def main() -> int:
    """
    ################################################################################################
    @fcn        main
    @brief      Main entry point for HelloGUI application.
    @details    Initializes logging system, creates QApplication instance, instantiates MainWindow,
                shows the window, starts the Qt event loop, and handles any fatal exceptions.
                Returns application exit code to operating system.

    @return     (int) Exit code for operating system: 0 on success, 1 on fatal error.

    @pre        Python environment with PySide6 and dependencies installed.
    @post       Application running and responsive; event loop blocking until window closed.

    @note       Entry point called from __main__ block. Exception handling logs and returns 1.\n    ################################################################################################
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
