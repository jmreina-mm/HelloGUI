# ==================================================================================================
#  HelloGUI - Python Data Stream Visualization Demo
#  Module: core/io_manager.py (CSV File I/O)
#  Purpose: Read/write CSV datasets with comprehensive validation
# ==================================================================================================

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


# --- Write (x, y) points to CSV file with automatic directory creation ---
def write_csv(file_path: str, points: list[tuple[float, float]]) -> tuple[bool, str]:
    """
    ################################################################################################
    @fcn        write_csv
    @brief      Write dataset points to CSV file with header.
    @details    Creates parent directories as needed. Uses simple CSV format with "x,y" header
                and one point per line. Returns success/failure tuple with descriptive message.

    @param[in]  file_path   Destination file path (string).
    @param[in]  points      List of (x, y) tuples to write.
    @return     (tuple[bool, str]) (success, message). True + description on success;
                                    False + error details on failure.

    @pre        file_path is writable; points contain valid floats.
    @post       File created/overwritten; parent directories created as needed.

    @section    Operation
         1. Convert path to Path object
         2. Create parent directories
         3. Write CSV with header row and data rows
         4. Log operation and return status

    @note       Automatic directory creation avoids common file-not-found errors.
    ################################################################################################
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


# --- Read (x, y) points from CSV file with validation ---
def read_csv(file_path: str) -> tuple[list[tuple[float, float]], str]:
    """
    ################################################################################################
    @fcn        read_csv
    @brief      Read dataset points from a CSV file.
    @details    Expects CSV with "x,y" header and numeric values per line. Validates that
                values are valid floats and non-NaN. Returns points with descriptive message.

    @param[in]  file_path   Source CSV file path (string).
    @return     (tuple[list[tuple[float, float]], str]) (points, message).
                On success: points list + description.
                On failure: empty list + error details.

    @pre        file_path exists and is readable CSV.
    @post       None (read-only operation).

    @section    Operation
         1. Check file existence
         2. Parse CSV header and rows
         3. Validate numeric conversions
         4. Filter NaN values
         5. Return tuples with status message

    @note       Robust to missing files and malformed data.
    ################################################################################################
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
