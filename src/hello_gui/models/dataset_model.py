"""
Dataset model for storing and managing collected data points.

This module defines the DatasetModel dataclass that represents a collection
of (x, y) data points, along with metadata such as the dataset name and
maximum allowed length.
"""

from dataclasses import dataclass, field
from typing import Optional


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

    def add_point(self, x: float, y: float) -> None:
        """
        Add a point to the dataset, respecting the max_length constraint.

        If the dataset is at max_length, the oldest point is removed.

        Args:
            x (float): X-coordinate of the point.
            y (float): Y-coordinate of the point.
        """
        self.points.append((x, y))
        if len(self.points) > self.max_length:
            self.points.pop(0)

    def clear(self) -> None:
        """Clear all points from the dataset."""
        self.points.clear()

    def point_count(self) -> int:
        """
        Get the number of points in the dataset.

        Returns:
            int: Number of (x, y) points.
        """
        return len(self.points)

    def last_point(self) -> Optional[tuple[float, float]]:
        """
        Get the last (most recent) point in the dataset.

        Returns:
            Optional[tuple[float, float]]: The last (x, y) point, or None if empty.
        """
        return self.points[-1] if self.points else None

    def get_x_values(self) -> list[float]:
        """
        Extract all X values from the dataset.

        Returns:
            list[float]: List of X coordinates.
        """
        return [x for x, _ in self.points]

    def get_y_values(self) -> list[float]:
        """
        Extract all Y values from the dataset.

        Returns:
            list[float]: List of Y coordinates.
        """
        return [y for _, y in self.points]
