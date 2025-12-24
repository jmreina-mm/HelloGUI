# ==================================================================================================
#  HelloGUI - Python Data Stream Visualization Demo
#  Module: plot/plot_widget.py (Matplotlib Plot Widget)
#
#  Purpose : Qt-integrated Matplotlib FigureCanvas for XY visualization
# ==================================================================================================

"""
Matplotlib plot widget for displaying XY data.

Integrates Matplotlib FigureCanvas with PySide6 for embedding plots
in the Qt application with efficient updates.
"""

import logging

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout

logger = logging.getLogger("hellogui")


# ==================================================================================================
#  Class PlotWidget(QWidget):
# ==================================================================================================

class PlotWidget(QWidget):
    """
    Matplotlib plot widget for XY scatter/line plots.

    Wraps Matplotlib FigureCanvasQTAgg in a QWidget for Qt integration.
    Provides methods to add points, set labels, clear, and update efficiently.

    Attributes:
        figure (Figure): Matplotlib Figure object.
        canvas (FigureCanvas): Matplotlib FigureCanvas for rendering.
    """
    # --- Initialize the Matplotlib plot widget in Qt ---

    def __init__(self, parent=None):
        """
        ############################################################################################
        @fcn        __init__
        @brief      Initialize Matplotlib plot widget in Qt.
        @details    Creates Figure, axes, FigureCanvas, and embeds in QVBoxLayout.
                    Initializes empty plot ready for data.

        @param[in]  parent     Parent Qt widget (optional). Defaults to None.
        @return     (None)

        @pre        None.
        @post       Widget ready for set_data() or append_point() calls.

        @note       8x5 inch figure at 100 DPI by default.
        ############################################################################################
        """
        super().__init__(parent)

        # Create Matplotlib figure and axes
        self.figure: Figure    = Figure(figsize=(8, 5), dpi=100)
        self.axes              = self.figure.add_subplot(111)

        # Create canvas
        self.canvas: FigureCanvas = FigureCanvas(self.figure)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Store line object for efficient updates
        self.line = None

        # Initialize with empty plot
        self._init_plot()

        logger.debug("PlotWidget initialized")


    # --- [INTERNAL] Initialize plot with empty axes and grid ---
    def _init_plot(self) -> None:
        """
        ############################################################################################
        @fcn        _init_plot
        @brief      Initialize/reset plot to empty clean state.
        @details    Clears axes, sets default labels, configures grid, creates line object.

        @return     (None)

        @pre        None.
        @post       Plot cleared; ready for new data.

        @section    Operation
             1. Clear axes
             2. Set default axis labels
             3. Enable grid with 0.3 alpha
             4. Create empty line object for efficient updates
             5. Request draw_idle() for lazy update

        @note       Called from __init__ and clear().
        ############################################################################################
        """
        self.axes.clear()
        self.axes.set_xlabel("X Label")
        self.axes.set_ylabel("Y Label")
        self.axes.grid(True, alpha=0.3)
        self.line, = self.axes.plot([], [], marker='o', markersize=4, linestyle='-', linewidth=1)
        self.canvas.draw_idle()


    # --- Set X and Y axis labels ---
    def set_axis_labels(self, x_label: str, y_label: str) -> None:
        """
        ############################################################################################
        @fcn        set_axis_labels
        @brief      Update the X and Y axis labels.
        @details    Changes label text and triggers lazy redraw.

        @param[in]  x_label     Label string for X axis.
        @param[in]  y_label     Label string for Y axis.
        @return     (None)

        @pre        x_label and y_label are valid strings.
        @post       Axes updated; draw_idle() called.

        @note       Useful when stream parameter changes to reflect units/meaning.
        ############################################################################################
        """
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.canvas.draw_idle()
        logger.debug("Axis labels updated: %s, %s", x_label, y_label)


    # --- Replace all plot data with new X and Y values ---
    def set_data(self, x_values: list[float], y_values: list[float]) -> None:
        """
        ############################################################################################
        @fcn        set_data
        @brief      Replace all plot data with new arrays.
        @details    Updates line data, auto-scales axes to fit, requests redraw.

        @param[in]  x_values    List of X coordinates.
        @param[in]  y_values    List of Y coordinates (must match x_values length).
        @return     (None)

        @pre        x_values and y_values same length; contain valid floats.
        @post       Plot updated; axes auto-scaled.

        @section    Operation
             1. Validate array lengths match
             2. Update line object with new data
             3. Call relim() + autoscale_view() to fit axes
             4. Request draw_idle()

        @note       Efficient; reuses line object rather than recreating.
        ############################################################################################
        """
        if len(x_values) != len(y_values):
            logger.warning("X and Y arrays have different lengths")
            return

        self.line.set_data(x_values, y_values)

        # Auto-scale axes to fit data
        if x_values:
            self.axes.relim()
            self.axes.autoscale_view()

        self.canvas.draw_idle()
        logger.debug("Plot data updated: %d points", len(x_values))


    # --- Efficiently add a single point to the plot ---
    def append_point(self, x: float, y: float) -> None:
        """
        ############################################################################################
        @fcn        append_point
        @brief      Add a single (x, y) point to existing plot.
        @details    Extracts current data, appends new point, updates axes, redraws.
                    More efficient than recreating entire dataset.

        @param[in]  x     X coordinate.
        @param[in]  y     Y coordinate.
        @return     (None)

        @pre        Line object initialized.
        @post       Plot updated with new point; axes auto-scaled.

        @section    Operation
             1. Get current x/y data from line object
             2. Append new point
             3. Update line with extended data
             4. Auto-scale axes
             5. Request draw_idle()

        @note       Designed for real-time streaming; avoids expensive full redraws.
        ############################################################################################
        """
        if self.line is None:
            logger.warning("Line object not initialized")
            return

        # Get current data
        x_data = list(self.line.get_xdata())
        y_data = list(self.line.get_ydata())

        # Append new point
        x_data.append(x)
        y_data.append(y)

        # Update line
        self.line.set_data(x_data, y_data)

        # Auto-scale to show all data
        self.axes.relim()
        self.axes.autoscale_view()

        # Efficient redraw
        self.canvas.draw_idle()


    # --- Clear all data from the plot ---
    def clear(self) -> None:
        """
        ############################################################################################
        @fcn        clear
        @brief      Reset plot to empty state.
        @details    Calls _init_plot() to clear axes and create fresh line object.

        @return     (None)

        @pre        None.
        @post       Plot cleared; ready for new data.

        @note       Used when user clicks Clear button or loads new dataset.
        ############################################################################################
        """
        self._init_plot()
        logger.debug("Plot cleared")


    # --- Get current X and Y data from the plot ---
    def get_current_data(self) -> tuple[list[float], list[float]]:
        """
        ############################################################################################
        @fcn        get_current_data
        @brief      Retrieve current plot data arrays.
        @details    Extracts x and y data from line object; returns empty lists if uninitialized.

        @return     (tuple[list[float], list[float]]) (x_values, y_values) currently displayed.

        @pre        None.
        @post       None (read-only).

        @note       Useful for saving data or synchronizing external state.
        ############################################################################################
        """
        if self.line is None:
            return [], []
        x_data = list(self.line.get_xdata())
        y_data = list(self.line.get_ydata())
        return x_data, y_data
