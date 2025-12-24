"""
Main application window for HelloGUI.

Contains the main QMainWindow with tabs for Dashboard and Config,
wires up all signal/slot connections, and manages application state.
"""

import logging
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QMessageBox,
    QApplication,
)
from PySide6.QtCore import Qt

from hello_gui.core import AppState, DataStream, read_csv, write_csv
from hello_gui.models import ConfigModel
from hello_gui.ui import DashboardTab, ConfigTab

logger = logging.getLogger("hellogui")


class MainWindow(QMainWindow):
    """
    Main application window.

    Orchestrates the Dashboard and Config tabs, manages the data stream,
    and handles all user interactions and state transitions.

    Attributes:
        app_state (AppState): Central application state.
        data_stream (DataStream): Data generator with Qt signals.
        dashboard_tab (DashboardTab): Dashboard UI tab.
        config_tab (ConfigTab): Configuration UI tab.
    """

    def __init__(self):
        """Initialize the main window and set up all components."""
        super().__init__()

        self.setWindowTitle("HelloGUI - Python Data Stream Visualization")
        self.setGeometry(100, 100, 1200, 700)

        # Initialize application state
        self.app_state: AppState = AppState()

        # Initialize data stream
        self.data_stream: DataStream = DataStream(self.app_state.config, interval_ms=100)

        # Create UI tabs
        self.dashboard_tab: DashboardTab = DashboardTab()
        self.config_tab: ConfigTab = ConfigTab(self.app_state.config)

        # Set up tab widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.config_tab, "Config")

        self.setCentralWidget(self.tabs)

        # Wire up signal/slot connections
        self._connect_signals()

        logger.info("MainWindow initialized")

    def _connect_signals(self) -> None:
        """Connect all Qt signals and slots."""
        # Dashboard buttons
        self.dashboard_tab.pause_button.clicked.connect(self.on_pause)
        self.dashboard_tab.resume_button.clicked.connect(self.on_resume)
        self.dashboard_tab.clear_button.clicked.connect(self.on_clear)
        self.dashboard_tab.save_button.clicked.connect(self.on_save_data)
        self.dashboard_tab.load_button.clicked.connect(self.on_load_data)

        # Config buttons
        self.config_tab.apply_button.clicked.connect(self.on_apply_config)
        self.config_tab.reset_button.clicked.connect(self.on_reset_config)

        # Axis label changes
        self.dashboard_tab.x_label_input.textChanged.connect(self._on_axis_labels_changed)
        self.dashboard_tab.y_label_input.textChanged.connect(self._on_axis_labels_changed)

        # Data stream signals
        self.data_stream.new_point.connect(self.on_new_point)
        self.data_stream.started.connect(self.on_stream_started)
        self.data_stream.stopped.connect(self.on_stream_stopped)

        logger.debug("Signals connected")

    def _on_axis_labels_changed(self) -> None:
        """Handle axis label changes."""
        x_label, y_label = self.dashboard_tab.get_axis_labels()
        self.dashboard_tab.plot_widget.set_axis_labels(x_label, y_label)

    def on_pause(self) -> None:
        """Handle pause button click."""
        self.data_stream.stop()
        self.app_state.pause()
        self.dashboard_tab.update_status("Paused")
        self.dashboard_tab.enable_controls(False)
        logger.info("Data stream paused")

    def on_resume(self) -> None:
        """Handle resume button click."""
        self.data_stream.start()
        self.app_state.resume()
        self.dashboard_tab.update_status("Running")
        self.dashboard_tab.enable_controls(True)
        logger.info("Data stream resumed")

    def on_clear(self) -> None:
        """Handle clear button click."""
        self.data_stream.stop()
        self.app_state.clear()
        self.data_stream.reset()
        self.dashboard_tab.plot_widget.clear()
        self.dashboard_tab.update_status("Cleared")
        self.dashboard_tab.update_point_count(0)
        self.dashboard_tab.update_latest_point(0, 0)
        self.dashboard_tab.enable_controls(False)
        logger.info("Dataset cleared")

    def on_save_data(self) -> None:
        """Handle save data button click."""
        file_path = self.dashboard_tab.file_path_input.text().strip()
        if not file_path:
            QMessageBox.warning(self, "Error", "Please enter a file path to save.")
            return

        success, message = write_csv(file_path, self.app_state.dataset.points)

        if success:
            self.dashboard_tab.update_status(f"Saved: {message}")
            QMessageBox.information(self, "Success", message)
        else:
            self.dashboard_tab.update_status(f"Save failed: {message}")
            QMessageBox.critical(self, "Error", message)

    def on_load_data(self) -> None:
        """Handle load data button click."""
        file_path = self.dashboard_tab.file_path_input.text().strip()
        if not file_path:
            QMessageBox.warning(self, "Error", "Please enter a file path to load.")
            return

        points, message = read_csv(file_path)

        if points:
            # Stop stream and replace dataset
            self.data_stream.stop()
            self.app_state.clear()
            self.data_stream.reset()

            # Load new data
            for x, y in points:
                self.app_state.dataset.add_point(x, y)

            # Update plot
            x_vals = self.app_state.dataset.get_x_values()
            y_vals = self.app_state.dataset.get_y_values()
            self.dashboard_tab.plot_widget.set_data(x_vals, y_vals)

            self.dashboard_tab.update_status(f"Loaded: {message}")
            last_point = self.app_state.dataset.last_point()
            if last_point:
                self.dashboard_tab.update_latest_point(last_point[0], last_point[1])
            self.dashboard_tab.update_point_count(self.app_state.dataset.point_count())
            self.dashboard_tab.enable_controls(False)

            QMessageBox.information(self, "Success", message)
        else:
            self.dashboard_tab.update_status(f"Load failed: {message}")
            QMessageBox.critical(self, "Error", message)

    def on_apply_config(self) -> None:
        """Handle apply config button click."""
        config = self.config_tab.get_config()
        success = self.app_state.apply_config(config)

        if success:
            # Update data stream with new config
            self.data_stream.set_config(config)
            self.dashboard_tab.update_status("Configuration applied")
            QMessageBox.information(self, "Success", "Configuration applied successfully.")
        else:
            is_valid, error_msg = config.validate()
            self.dashboard_tab.update_status(f"Config error: {error_msg}")
            QMessageBox.critical(self, "Configuration Error", error_msg)

    def on_reset_config(self) -> None:
        """Handle reset config button click."""
        self.app_state.reset_config()
        self.config_tab.reset_to_defaults()
        self.data_stream.set_config(self.app_state.config)
        self.dashboard_tab.update_status("Configuration reset to defaults")
        logger.info("Configuration reset to defaults")

    def on_new_point(self, x: float, y: float) -> None:
        """
        Handle new data point from stream.

        Args:
            x (float): X coordinate.
            y (float): Y coordinate.
        """
        # Add to dataset
        self.app_state.dataset.add_point(x, y)

        # Update plot
        self.dashboard_tab.plot_widget.append_point(x, y)

        # Update status
        self.dashboard_tab.update_point_count(self.app_state.dataset.point_count())
        self.dashboard_tab.update_latest_point(x, y)

    def on_stream_started(self) -> None:
        """Handle stream start signal."""
        self.app_state.start()
        self.dashboard_tab.enable_controls(True)
        logger.debug("Stream started signal received")

    def on_stream_stopped(self) -> None:
        """Handle stream stop signal."""
        self.app_state.pause()
        self.dashboard_tab.enable_controls(False)
        logger.debug("Stream stopped signal received")

    def closeEvent(self, event) -> None:
        """
        Handle window close event.

        Args:
            event: Qt close event.
        """
        # Clean up timer
        self.data_stream.stop()
        logger.info("Application closing")
        event.accept()
