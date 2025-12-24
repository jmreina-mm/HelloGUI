"""
HelloGUI - Python GUI Demo Project

A comprehensive, well-structured demonstration of a Python GUI application
using PySide6/Qt and Matplotlib for data visualization and real-time plotting.

This package includes:
- Modular architecture with separate concerns (UI, data, plotting, I/O)
- Qt signals/slots for event-driven programming
- Matplotlib embedding for scientific plotting
- Configuration management and validation
- CSV file I/O with error handling
- Comprehensive logging with rotating file handler
- Type hints and detailed docstrings for educational value
"""

__version__ = "1.0.0"
__author__ = "HelloGUI Team"

from hello_gui.main_window import MainWindow
from hello_gui.core import AppState, DataStream

__all__ = ["MainWindow", "AppState", "DataStream"]
