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


class PlotWidget(QWidget):
    """
    Matplotlib plot widget for XY scatter/line plots.

    Wraps Matplotlib FigureCanvasQTAgg in a QWidget for Qt integration.
    Provides methods to add points, set labels, clear, and update efficiently.

    Attributes:
        figure (Figure): Matplotlib Figure object.
        canvas (FigureCanvas): Matplotlib FigureCanvas for rendering.
    """

    def __init__(self, parent=None):
        """
        Initialize the plot widget.

        Args:
            parent: Parent Qt widget (optional).
        """
        super().__init__(parent)

        # Create Matplotlib figure and axes
        self.figure: Figure = Figure(figsize=(8, 5), dpi=100)
        self.axes = self.figure.add_subplot(111)

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

    def _init_plot(self) -> None:
        """Initialize the plot with empty axes."""
        self.axes.clear()
        self.axes.set_xlabel("X Label")
        self.axes.set_ylabel("Y Label")
        self.axes.grid(True, alpha=0.3)
        self.line, = self.axes.plot([], [], marker='o', markersize=4, linestyle='-', linewidth=1)
        self.canvas.draw_idle()

    def set_axis_labels(self, x_label: str, y_label: str) -> None:
        """
        Set the X and Y axis labels.

        Args:
            x_label (str): Label for X axis.
            y_label (str): Label for Y axis.
        """
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.canvas.draw_idle()
        logger.debug("Axis labels updated: %s, %s", x_label, y_label)

    def set_data(self, x_values: list[float], y_values: list[float]) -> None:
        """
        Replace all plot data with new X and Y values.

        Args:
            x_values (list[float]): X coordinates.
            y_values (list[float]): Y coordinates.
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

    def append_point(self, x: float, y: float) -> None:
        """
        Add a single point to the existing plot.

        Efficiently updates the plot without redrawing all data.

        Args:
            x (float): X coordinate.
            y (float): Y coordinate.
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

    def clear(self) -> None:
        """Clear all data from the plot."""
        self._init_plot()
        logger.debug("Plot cleared")

    def get_current_data(self) -> tuple[list[float], list[float]]:
        """
        Get the current plot data.

        Returns:
            tuple[list[float], list[float]]: (x_values, y_values) currently displayed.
        """
        if self.line is None:
            return [], []
        x_data = list(self.line.get_xdata())
        y_data = list(self.line.get_ydata())
        return x_data, y_data
