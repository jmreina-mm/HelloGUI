# ==================================================================================================
#  HelloGUI - Python Data Stream Visualization Demo
#  Module: main_window.py (Main Window Orchestration)
#  Purpose: Central Qt QMainWindow with Dashboard/Config tabs and signal wiring
# ==================================================================================================

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


# ==================================================================================================
#  Class MainWindow(QMainWindow):
# ==================================================================================================

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
    # --- Initialize main window with tabs and data stream ---

    def __init__(self):
        """
        ############################################################################################
        @fcn        __init__
        @brief      Initialize main application window with Dashboard and Config tabs.
        @details    Creates AppState and DataStream instances, builds Dashboard and Config tabs,
                    sets up tab widget, establishes Qt signal/slot connections, and configures
                    window geometry. All initialization complete before returning control.

        @return     (None)

        @pre        None.
        @post       MainWindow fully initialized; data stream running; all signals wired.

        @note       Window shown by caller after __init__. DataStream initialized with 100ms interval.
        ############################################################################################
        """
        super().__init__()

        self.setWindowTitle("HelloGUI - Python Data Stream Visualization")
        self.setGeometry(100, 100, 1200, 700)

        # Initialize application state
        self.app_state: AppState       = AppState()

        # Initialize data stream
        self.data_stream: DataStream   = DataStream(self.app_state.config, interval_ms=100)

        # Create UI tabs
        self.dashboard_tab: DashboardTab = DashboardTab()
        self.config_tab: ConfigTab     = ConfigTab(self.app_state.config)

        # Set up tab widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.config_tab, "Config")

        self.setCentralWidget(self.tabs)

        # Wire up signal/slot connections
        self._connect_signals()

        logger.info("MainWindow initialized")


    # --- [INTERNAL] Wire up all Qt signal/slot connections ---
    def _connect_signals(self) -> None:
        """
        ############################################################################################
        @fcn        _connect_signals
        @brief      Wire up all Qt signal/slot connections between UI and handlers.
        @details    Connects dashboard buttons (pause, resume, clear, save, load) to slot handlers.
                    Connects config buttons (apply, reset) to configuration handlers. Connects axis
                    label input signals. Connects data_stream signals (new_point, started, stopped)
                    to appropriate handlers.

        @return     (None)

        @pre        All UI tabs and DataStream fully initialized.
        @post       All signals/slots connected; application responsive to user input.

        @note       Called from __init__. Order of connections doesn't matter for this implementation.
        ############################################################################################
        """
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


    # --- [INTERNAL] Handle axis label input changes ---
    def _on_axis_labels_changed(self) -> None:
        """
        ############################################################################################
        @fcn        _on_axis_labels_changed
        @brief      Update plot axis labels when user changes input fields.
        @details    Reads current x_label and y_label from dashboard inputs and applies to plot
                    widget via set_axis_labels(). Called whenever either axis label input field
                    text changes.

        @return     (None)

        @pre        Dashboard tab inputs exist and are writable.
        @post       Plot widget displays updated axis labels.

        @note       Connected to textChanged signals of both axis label inputs.
        ############################################################################################
        """
        x_label, y_label = self.dashboard_tab.get_axis_labels()
        self.dashboard_tab.plot_widget.set_axis_labels(x_label, y_label)


    # --- Handle pause button click ---
    def on_pause(self) -> None:
        """
        ############################################################################################
        @fcn        on_pause
        @brief      Pause data stream when user clicks Pause button.
        @details    Stops the data generation timer, updates app state, disables Pause button and
                    enables Resume button. Updates status label and logs the pause event.

        @return     (None)

        @pre        Data stream is running.
        @post       Stream paused; UI controls updated; status displayed.

        @note       User can resume from paused state with Resume button.
        ############################################################################################
        """
        self.data_stream.stop()
        self.app_state.pause()
        self.dashboard_tab.update_status("Paused")
        self.dashboard_tab.enable_controls(False)
        logger.info("Data stream paused")


    # --- Handle resume button click ---
    def on_resume(self) -> None:
        """
        ############################################################################################
        @fcn        on_resume
        @brief      Resume data stream when user clicks Resume button.
        @details    Restarts the data generation timer, updates app state, enables Pause button
                    and disables Resume button. Updates status label and logs the resume event.

        @return     (None)

        @pre        Data stream is paused.
        @post       Stream running; UI controls updated; status displayed.

        @note       Continues appending to existing dataset (does not clear).
        ############################################################################################
        """
        self.data_stream.start()
        self.app_state.resume()
        self.dashboard_tab.update_status("Running")
        self.dashboard_tab.enable_controls(True)
        logger.info("Data stream resumed")


    # --- Handle clear button click ---
    def on_clear(self) -> None:
        """
        ############################################################################################
        @fcn        on_clear
        @brief      Clear dataset and reset stream to initial state.
        @details    Stops data generation, clears app_state and resets data_stream, removes all
                    points from plot, resets point count and latest point display, disables
                    stream control buttons, and logs the clear event.

        @return     (None)

        @pre        Any state of the application.
        @post       Dataset cleared; plot empty; controls disabled; status updated.

        @note       User can Resume after Clear to start fresh data collection.
        ############################################################################################
        """
        self.data_stream.stop()
        self.app_state.clear()
        self.data_stream.reset()
        self.dashboard_tab.plot_widget.clear()
        self.dashboard_tab.update_status("Cleared")
        self.dashboard_tab.update_point_count(0)
        self.dashboard_tab.update_latest_point(0, 0)
        self.dashboard_tab.enable_controls(False)
        logger.info("Dataset cleared")


    # --- Handle save data button click ---
    def on_save_data(self) -> None:
        """
        ############################################################################################
        @fcn        on_save_data
        @brief      Save current dataset points to CSV file.
        @details    Reads file path from dashboard input field. If empty, shows warning dialog.
                    Otherwise calls write_csv() to save all dataset points. Updates status label
                    and shows success or error dialog based on write_csv result.

        @return     (None)

        @pre        File path input field accessible; dataset may be empty.
        @post       File written if path provided; dialogs shown; status updated.

        @note       write_csv handles file creation/overwrite. Empty dataset saves empty CSV.
        ############################################################################################
        """
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


    # --- Handle load data button click ---
    def on_load_data(self) -> None:
        """
        ############################################################################################
        @fcn        on_load_data
        @brief      Load dataset points from CSV file and display in plot.
        @details    Reads file path from dashboard input. If empty, shows warning. Otherwise calls
                    read_csv() to load points. If successful, stops current stream, clears dataset,
                    loads new points, updates plot and status displays. Shows success/error dialog
                    and logs outcome.

        @return     (None)

        @pre        File path input field accessible.
        @post       Dataset updated; plot refreshed; stream stopped; dialogs shown; status updated.

        @note       Stops active stream before loading. User can Resume to continue collection.
        ############################################################################################
        """
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


    # --- Handle apply config button click ---
    def on_apply_config(self) -> None:
        """
        ############################################################################################
        @fcn        on_apply_config
        @brief      Apply new configuration parameters to data stream.
        @details    Reads configuration from config_tab controls via get_config(). Validates
                    config and applies to app_state and data_stream. On success, updates data
                    stream with new config and shows success dialog. On failure, shows error
                    dialog with validation error message.

        @return     (None)

        @pre        ConfigModel has validate() and defaults() working.
        @post       Stream configuration updated if valid; user informed of result.

        @note       Does not stop/restart stream; new config takes effect on next data point.
        ############################################################################################
        """
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


    # --- Handle reset config button click ---
    def on_reset_config(self) -> None:
        """
        ############################################################################################
        @fcn        on_reset_config
        @brief      Reset all configuration parameters to factory defaults.
        @details    Calls app_state.reset_config() to reset app state, then config_tab.reset_to_defaults()
                    to update UI controls, then updates data_stream with new default config.
                    Updates status label and logs the reset event.

        @return     (None)

        @pre        ConfigModel.defaults() working and accessible.
        @post       All config values reset to defaults; UI and stream synchronized.

        @note       Does not affect existing dataset; only changes generation parameters.
        ############################################################################################
        """
        self.app_state.reset_config()
        self.config_tab.reset_to_defaults()
        self.data_stream.set_config(self.app_state.config)
        self.dashboard_tab.update_status("Configuration reset to defaults")
        logger.info("Configuration reset to defaults")


    # --- Handle new data point from stream ---
    def on_new_point(self, x: float, y: float) -> None:
        """
        ############################################################################################
        @fcn        on_new_point
        @brief      Handle new data point generated by data stream.
        @details    Receives (x, y) coordinate from data_stream.new_point signal. Adds point to
                    dataset via app_state, appends to plot widget for visualization, and updates
                    status displays (point count and latest point values).

        @param[in]  x               X coordinate of new point.
        @param[in]  y               Y coordinate of new point.
        @return     (None)

        @pre        Dataset initialized; plot widget ready.
        @post       Point added to dataset and plot; status labels updated.

        @note       Called frequently during active stream collection (every interval_ms).
        ############################################################################################
        """
        # Add to dataset
        self.app_state.dataset.add_point(x, y)

        # Update plot
        self.dashboard_tab.plot_widget.append_point(x, y)

        # Update status
        self.dashboard_tab.update_point_count(self.app_state.dataset.point_count())
        self.dashboard_tab.update_latest_point(x, y)


    # --- Handle stream started signal ---
    def on_stream_started(self) -> None:
        """
        ############################################################################################
        @fcn        on_stream_started
        @brief      Handle data stream started signal from DataStream.
        @details    Updates app_state to started state and enables Pause button (disables Resume).
                    Logs that stream start signal was received. Called when DataStream timer
                    begins generating data points.

        @return     (None)

        @pre        Stream timer running; data generation active.
        @post       App state updated; UI controls reflect running state.

        @note       May be called multiple times if stream paused and resumed.
        ############################################################################################
        """
        self.app_state.start()
        self.dashboard_tab.enable_controls(True)
        logger.debug("Stream started signal received")


    # --- Handle stream stopped signal ---
    def on_stream_stopped(self) -> None:
        """
        ############################################################################################
        @fcn        on_stream_stopped
        @brief      Handle data stream stopped signal from DataStream.
        @details    Updates app_state to paused state and disables Pause button (enables Resume).
                    Logs that stream stop signal was received. Called when DataStream timer
                    stops generating data points.

        @return     (None)

        @pre        Stream timer halted.
        @post       App state updated; UI controls reflect paused state.

        @note       Different from on_pause() in that it's signal-driven from DataStream.
        ############################################################################################
        """
        self.app_state.pause()
        self.dashboard_tab.enable_controls(False)
        logger.debug("Stream stopped signal received")


    # --- Handle window close event ---
    def closeEvent(self, event) -> None:
        """
        ############################################################################################
        @fcn        closeEvent
        @brief      Handle main window close event for graceful shutdown.
        @details    Stops the data generation timer, logs application closing message, and
                    accepts the close event to allow Qt to proceed with window closure.

        @param[in]  event           Qt QCloseEvent object from system.
        @return     (None)

        @pre        Window open and running.
        @post       Timer stopped; application closed; cleanup complete.

        @note       Prevents data stream from continuing after window closed.\n        ####################################################################################################
        """
        # Clean up timer
        self.data_stream.stop()
        logger.info("Application closing")
        event.accept()
