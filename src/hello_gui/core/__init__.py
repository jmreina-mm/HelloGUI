"""
Initialize core subpackage.

Exports core application components including state management,
data streaming, file I/O, and logging setup.
"""

from hello_gui.core.data_stream import DataStream
from hello_gui.core.io_manager import read_csv, write_csv
from hello_gui.core.logging_setup import setup_logging
from hello_gui.core.state import AppState

__all__ = ["AppState", "DataStream", "read_csv", "write_csv", "setup_logging"]
