# ==================================================================================================
#  HelloGUI - Python Data Stream Visualization Demo
#  Module: models/dataset_model.py (Dataset Data Model)
#  Purpose: Dataclass for (x, y) point storage with auto-truncation
# ==================================================================================================

"""
Dataset model for storing and managing collected data points.

This module defines the DatasetModel dataclass that represents a collection
of (x, y) data points, along with metadata such as the dataset name and
maximum allowed length.
"""

from dataclasses import dataclass, field
from typing import Optional


# ==================================================================================================
#  Class DatasetModel(object):
# ==================================================================================================

@dataclass
class DatasetModel:
    """
    Dataset model representing a collection of (x, y) points.

    Attributes:
        name (str): Name of the dataset. Defaults to "Untitled".
        points (list[tuple[float, float]]): List of (x, y) data points. Defaults to empty list.
        max_length (int): Maximum number of points to retain. Defaults to 5000.
    """

    name: str = "Untitled"
    points: list[tuple[float, float]] = field(default_factory=list)
    max_length: int = 5000
    # --- Add a point to the dataset (FIFO truncation if needed) ---

    def add_point(self, x: float, y: float) -> None:
        """
        ############################################################################################
        @fcn        add_point
        @brief      Add a single (x, y) point to the dataset.
        @details    Appends point and enforces max_length constraint via FIFO removal of oldest point.

        @param[in]  x     X-coordinate value.
        @param[in]  y     Y-coordinate value.
        @return     (None)

        @pre        x and y are valid floats.
        @post       Point added; dataset may be truncated if at max_length.

        @note       Automatic truncation ensures bounded memory usage.
        ############################################################################################
        """
        self.points.append((x, y))
        if len(self.points) > self.max_length:
            self.points.pop(0)
    # --- Remove all points from the dataset ---

    def clear(self) -> None:
        """
        ############################################################################################
        @fcn        clear
        @brief      Remove all points from the dataset.
        @details    Resets the points list to empty.

        @return     (None)

        @pre        None.
        @post       Dataset contains zero points.

        @note       Used when resetting or starting a new measurement.
        ############################################################################################
        """
        self.points.clear()
    # --- Return the number of points in the dataset ---

    def point_count(self) -> int:
        """
        ############################################################################################
        @fcn        point_count
        @brief      Get the total number of points currently in the dataset.
        @details    Returns length of the points list.

        @return     (int) count of (x, y) points.

        @pre        None.
        @post       None (read-only).

        @note       Efficient O(1) operation.
        ############################################################################################
        """
        return len(self.points)
    # --- Get the most recent point or None if dataset is empty ---

    def last_point(self) -> Optional[tuple[float, float]]:
        """
        ############################################################################################
        @fcn        last_point
        @brief      Retrieve the most recent (x, y) point.
        @details    Returns last element of points list, or None if empty.

        @return     (Optional[tuple[float, float]]) Last (x, y) pair, or None.

        @pre        None.
        @post       None (read-only).

        @note       Useful for status display and real-time feedback.
        ############################################################################################
        """
        return self.points[-1] if self.points else None
    # --- Extract all X coordinates from the dataset ---

    def get_x_values(self) -> list[float]:
        """
        ############################################################################################
        @fcn        get_x_values
        @brief      Extract all X-coordinates from the dataset.
        @details    Returns a list of x values suitable for plotting.

        @return     (list[float]) All x-coordinates in order.

        @pre        None.
        @post       None (read-only; creates new list).

        @note       Commonly used for plot rendering.
        ############################################################################################
        """
        return [x for x, _ in self.points]
    # --- Extract all Y coordinates from the dataset ---

    def get_y_values(self) -> list[float]:
        """
        ############################################################################################
        @fcn        get_y_values
        @brief      Extract all Y-coordinates from the dataset.
        @details    Returns a list of y values suitable for plotting.

        @return     (list[float]) All y-coordinates in order.

        @pre        None.
        @post       None (read-only; creates new list).

        @note       Commonly used for plot rendering.
        ############################################################################################
        """
        return [y for _, y in self.points]
