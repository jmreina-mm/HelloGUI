# ==================================================================================================
#  HelloGUI - Python Data Stream Visualization Demo
#  Module: ui/dashboard_tab.py (Dashboard Tab UI)
#  Purpose: Dashboard UI with plot, controls, and status display
# ==================================================================================================

"""
Dashboard tab UI for the main application window.

Provides the Dashboard tab with plot display, controls (Pause, Resume, Clear,
Save, Load), and status information.
"""

import logging

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QGroupBox,
)
from PySide6.QtCore import Qt

from hello_gui.plot import PlotWidget

logger = logging.getLogger("hellogui")

# ==================================================================================================
#  Class DashboardTab(QWidget):
# ==================================================================================================

class DashboardTab(QWidget):
    """
    Dashboard tab UI component.

    Contains a Matplotlib plot widget, controls for data stream management,
    and status display.

    Attributes:
        plot_widget (PlotWidget): Embedded Matplotlib plot.
        pause_button, resume_button, clear_button (QPushButton): Stream controls.
        save_button, load_button (QPushButton): File I/O buttons.
        file_path_input (QLineEdit): File path for save/load operations.
        dataset_name_input (QLineEdit): Name of the current dataset.
        x_label_input, y_label_input (QLineEdit): Axis labels.
        status_label (QLabel): Status message display.
        point_count_label (QLabel): Current point count display.
        latest_point_label (QLabel): Latest (x, y) display.
    """
    # --- Initialize the Dashboard tab with plot and controls ---

    def __init__(self, parent=None):
        """
        ############################################################################################
        @fcn        __init__
        @brief      Initialize Dashboard tab UI.
        @details    Creates plot widget, control buttons, status labels, and axis label inputs.
                    Organizes in vertical layout with plot prominent.

        @param[in]  parent     Parent Qt widget (optional).
        @return     (None)

        @pre        None.
        @post       Tab ready for signal/slot connections from MainWindow.

        @note       Signal connections made by MainWindow, not in __init__.
        ############################################################################################
        """
        super().__init__(parent)

        # Main layout
        main_layout = QVBoxLayout()

        # --- Top section: Axis labels ---

        labels_layout = QHBoxLayout()

        labels_layout.addWidget(QLabel("X Label:"))
        self.x_label_input      = QLineEdit("X")
        self.x_label_input.setMaximumWidth(150)
        labels_layout.addWidget(self.x_label_input)

        labels_layout.addWidget(QLabel("Y Label:"))
        self.y_label_input    = QLineEdit("Y")
        self.y_label_input.setMaximumWidth(150)
        labels_layout.addWidget(self.y_label_input)

        labels_layout.addWidget(QLabel("Dataset Name:"))
        self.dataset_name_input = QLineEdit("Untitled")
        self.dataset_name_input.setMaximumWidth(150)
        labels_layout.addWidget(self.dataset_name_input)

        labels_layout.addStretch()
        main_layout.addLayout(labels_layout)

        # --- Middle section: Plot widget ---

        self.plot_widget = PlotWidget()
        main_layout.addWidget(self.plot_widget)

        # --- Bottom section: Controls and status ---

        bottom_layout = QVBoxLayout()

        # Control buttons
        controls_layout = QHBoxLayout()

        self.pause_button  = QPushButton("Pause")
        self.resume_button = QPushButton("Resume")
        self.clear_button  = QPushButton("Clear")
        self.save_button   = QPushButton("Save Data")
        self.load_button   = QPushButton("Load Data")

        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.resume_button)
        controls_layout.addWidget(self.clear_button)
        controls_layout.addWidget(self.save_button)
        controls_layout.addWidget(self.load_button)
        controls_layout.addStretch()

        bottom_layout.addLayout(controls_layout)

        # File path input
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("File Path:"))
        self.file_path_input = QLineEdit()
        file_layout.addWidget(self.file_path_input)
        bottom_layout.addLayout(file_layout)

        # Status area
        status_group = QGroupBox("Status")
        status_layout = QHBoxLayout()

        self.point_count_label  = QLabel("Points: 0")
        self.latest_point_label = QLabel("Latest: (-, -)")
        self.status_label       = QLabel("Ready")

        status_layout.addWidget(self.point_count_label)
        status_layout.addWidget(self.latest_point_label)
        status_layout.addStretch()
        status_layout.addWidget(self.status_label)

        status_group.setLayout(status_layout)
        bottom_layout.addWidget(status_group)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
        logger.debug("DashboardTab initialized")


    def update_status(self, message: str) -> None:
        """
        Update the status label.

        Args:
            message (str): Status message to display.
        """
        self.status_label.setText(message)
        logger.debug("Status updated: %s", message)


    # --- Update point count display label ---
    def update_point_count(self, count: int) -> None:
        """
        ############################################################################################
        @fcn        update_point_count
        @brief      Display current number of points in dataset.
        @details    Updates point_count_label with formatted string.

        @param[in]  count     Integer count of points.
        @return     (None)

        @pre        point_count_label widget created.
        @post       Label updated to show "Points: {count}".

        @note       Updated each time a new point arrives.
        ############################################################################################
        """
        self.point_count_label.setText(f"Points: {count}")


    # --- Update latest point (x, y) display label ---
    def update_latest_point(self, x: float, y: float) -> None:
        """
        ############################################################################################
        @fcn        update_latest_point
        @brief      Display the most recent (x, y) data point.
        @details    Updates latest_point_label with formatted x and y (2 decimal places).

        @param[in]  x     X coordinate.
        @param[in]  y     Y coordinate.
        @return     (None)

        @pre        latest_point_label widget created.
        @post       Label updated to show "Latest: (x, y)" with 2 decimals.

        @note       Updated each time a new point arrives; provides real-time feedback.
        ############################################################################################
        """
        self.latest_point_label.setText(f"Latest: ({x:.2f}, {y:.2f})")


    # --- Get current X and Y axis labels from inputs ---
    def get_axis_labels(self) -> tuple[str, str]:
        """
        ############################################################################################
        @fcn        get_axis_labels
        @brief      Retrieve user-entered axis labels.
        @details    Reads x_label_input and y_label_input QLineEdit widgets.

        @return     (tuple[str, str]) (x_label, y_label) from inputs.

        @pre        Input widgets created and populated.
        @post       None (read-only).

        @note       Used when axis labels change to update plot.
        ############################################################################################
        """
        return self.x_label_input.text(), self.y_label_input.text()


    # --- Set axis labels in the UI input fields ---
    def set_axis_labels(self, x_label: str, y_label: str) -> None:
        """
        ############################################################################################
        @fcn        set_axis_labels
        @brief      Update the axis label input fields.
        @details    Sets text in x_label_input and y_label_input widgets.

        @param[in]  x_label     X axis label string.
        @param[in]  y_label     Y axis label string.
        @return     (None)

        @pre        Input widgets created.
        @post       Input fields updated; may trigger textChanged signals.

        @note       Programmatic update; used when loading config or resetting.
        ############################################################################################
        """
        self.x_label_input.setText(x_label)
        self.y_label_input.setText(y_label)


    # --- Enable/disable controls based on stream state ---
    def enable_controls(self, running: bool) -> None:
        """
        ############################################################################################
        @fcn        enable_controls
        @brief      Enable/disable UI buttons based on stream running state.
        @details    Pause button enabled when running; Resume enabled when paused.
                    Clear/Save/Load always enabled for user flexibility.

        @param[in]  running     bool: True if stream is active, False if paused.
        @return     (None)

        @pre        Buttons created.
        @post       Button enabled/disabled states updated.

        @section    Logic
             - Pause enabled when running
             - Resume enabled when paused (not running)
             - Clear/Save/Load always enabled

        @note       Prevents user from clicking invalid buttons for current state.
        ############################################################################################
        """
        self.pause_button.setEnabled(running)
        self.resume_button.setEnabled(not running)
        self.clear_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.load_button.setEnabled(True)
