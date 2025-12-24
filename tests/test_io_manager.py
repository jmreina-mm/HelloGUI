# =================================================================================================
#  HelloGUI - Python Data Stream Visualization Demo
#  Module: tests/test_io_manager.py (File I/O Tests)
#  Purpose: Unit tests for CSV read/write operations and validation
# =================================================================================================

"""
Tests for CSV file I/O manager.

Tests read/write operations including roundtrip consistency,
error handling, and validation of CSV format.
"""

import tempfile
import pytest
from pathlib import Path

from hello_gui.core import read_csv, write_csv


# --- Test suite for CSV write operations ---

class TestWriteCsv:
    """Tests for write_csv function."""


    def test_write_basic(self) -> None:
        """Test writing a basic CSV file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.csv"
            points = [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)]

            success, message = write_csv(str(file_path), points)

            assert success is True
            assert file_path.exists()


    def test_write_creates_parent_dirs(self) -> None:
        """Test that write_csv creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "subdir1" / "subdir2" / "test.csv"
            points = [(1.0, 2.0)]

            success, message = write_csv(str(file_path), points)

            assert success is True
            assert file_path.exists()


    def test_write_empty_list(self) -> None:
        """Test writing an empty point list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "empty.csv"
            points = []

            success, message = write_csv(str(file_path), points)

            assert success is True
            # File should exist with just header
            with open(file_path, "r") as f:
                lines = f.readlines()
                assert len(lines) == 1  # Just header


    def test_write_large_dataset(self) -> None:
        """Test writing a large number of points."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "large.csv"
            points = [(float(i), float(i * 2)) for i in range(5000)]

            success, message = write_csv(str(file_path), points)

            assert success is True


# --- Test suite for CSV read operations ---

class TestReadCsv:
    """Tests for read_csv function."""


    def test_read_basic(self) -> None:
        """Test reading a basic CSV file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.csv"
            original_points = [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)]

            # Write and read
            write_csv(str(file_path), original_points)
            points, message = read_csv(str(file_path))

            assert points == original_points


    def test_read_nonexistent_file(self) -> None:
        """Test reading a file that doesn't exist."""
        points, message = read_csv("/nonexistent/path/file.csv")

        assert points == []
        assert "not found" in message.lower()


    def test_read_invalid_header(self) -> None:
        """Test reading a CSV with invalid header."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "bad_header.csv"

            # Write invalid CSV
            with open(file_path, "w") as f:
                f.write("a,b\n")
                f.write("1,2\n")

            points, message = read_csv(str(file_path))

            assert points == []
            assert "header" in message.lower()


    def test_read_invalid_numeric(self) -> None:
        """Test reading a CSV with non-numeric values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "bad_numeric.csv"

            # Write CSV with non-numeric values
            with open(file_path, "w") as f:
                f.write("x,y\n")
                f.write("1,2\n")
                f.write("abc,def\n")

            points, message = read_csv(str(file_path))

            assert points == []
            assert "invalid" in message.lower()


    def test_read_empty_file(self) -> None:
        """Test reading an empty CSV file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "empty.csv"
            file_path.write_text("")

            points, message = read_csv(str(file_path))

            assert points == []
            assert "empty" in message.lower()


    def test_roundtrip(self) -> None:
        """Test write-then-read roundtrip consistency."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "roundtrip.csv"
            original_points = [
                (0.1, 1.1),
                (0.2, 2.2),
                (0.3, 3.3),
                (10.5, 20.7),
            ]

            # Write
            write_csv(str(file_path), original_points)

            # Read
            read_points, _ = read_csv(str(file_path))

            assert read_points == original_points
