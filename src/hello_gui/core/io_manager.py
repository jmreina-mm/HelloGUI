"""
CSV-based file I/O manager for dataset persistence.

Provides functions to read and write (x, y) datasets to/from CSV files
with validation and error handling.
"""

import csv
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger("hellogui")


def write_csv(file_path: str, points: list[tuple[float, float]]) -> tuple[bool, str]:
    """
    Write dataset points to a CSV file.

    Creates parent directories if they don't exist. Uses simple CSV format
    with "x,y" header and one point per line.

    Args:
        file_path (str): Path to write CSV file.
        points (list[tuple[float, float]]): List of (x, y) data points.

    Returns:
        tuple[bool, str]: (success, message). If success is True, message describes
            the write operation; if False, message is the error description.
    """
    try:
        path = Path(file_path)

        # Create parent directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write CSV with header
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["x", "y"])
            for x, y in points:
                writer.writerow([x, y])

        msg = f"Saved {len(points)} points to {file_path}"
        logger.info(msg)
        return True, msg

    except IOError as e:
        error_msg = f"Failed to write CSV: {e}"
        logger.error(error_msg)
        return False, error_msg

    except Exception as e:
        error_msg = f"Unexpected error writing CSV: {e}"
        logger.error(error_msg)
        return False, error_msg


def read_csv(file_path: str) -> tuple[list[tuple[float, float]], str]:
    """
    Read dataset points from a CSV file.

    Expects a CSV file with "x,y" header and numeric values per line.
    Validates that values are valid floats and non-NaN.

    Args:
        file_path (str): Path to CSV file to read.

    Returns:
        tuple[list[tuple[float, float]], str]: (points, message).
            If successful, points is the list of (x, y) tuples and message
            describes the read operation. If unsuccessful, points is empty
            list and message is the error description.
    """
    try:
        path = Path(file_path)

        if not path.exists():
            error_msg = f"File not found: {file_path}"
            logger.error(error_msg)
            return [], error_msg

        points: list[tuple[float, float]] = []

        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Read header
            header = next(reader, None)
            if header is None:
                error_msg = "CSV file is empty"
                logger.error(error_msg)
                return [], error_msg

            if header != ["x", "y"]:
                error_msg = f"Expected header ['x', 'y'], got {header}"
                logger.error(error_msg)
                return [], error_msg

            # Read data rows
            for row_num, row in enumerate(reader, start=2):
                if len(row) != 2:
                    error_msg = f"Row {row_num}: expected 2 values, got {len(row)}"
                    logger.error(error_msg)
                    return [], error_msg

                try:
                    x = float(row[0])
                    y = float(row[1])

                    # Validate not NaN or inf
                    if not (isinstance(x, float) and isinstance(y, float)):
                        raise ValueError("Non-numeric values")

                    points.append((x, y))

                except ValueError as e:
                    error_msg = f"Row {row_num}: invalid numeric values: {e}"
                    logger.error(error_msg)
                    return [], error_msg

        msg = f"Loaded {len(points)} points from {file_path}"
        logger.info(msg)
        return points, msg

    except IOError as e:
        error_msg = f"Failed to read CSV: {e}"
        logger.error(error_msg)
        return [], error_msg

    except Exception as e:
        error_msg = f"Unexpected error reading CSV: {e}"
        logger.error(error_msg)
        return [], error_msg
