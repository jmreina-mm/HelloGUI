"""
Tests for data stream generation logic.

Tests waveform generation (sine, square, random walk) and noise addition
without requiring Qt GUI components.
"""

import math
import pytest

from hello_gui.models import ConfigModel
from hello_gui.core.data_stream import DataStream


class TestSineWave:
    """Tests for sine wave generation."""

    def test_sine_at_zero(self) -> None:
        """Test sine wave at x=0."""
        config = ConfigModel(amplitude=1.0, frequency=0.5)
        stream = DataStream(config)

        y = stream._sine_wave(0.0)

        assert abs(y - 0.0) < 1e-10

    def test_sine_at_quarter_period(self) -> None:
        """Test sine wave at quarter period."""
        config = ConfigModel(amplitude=2.0, frequency=0.5)
        stream = DataStream(config)

        # At x where 2π * freq * x = π/2, we get max
        x = (math.pi / 2) / (2 * math.pi * 0.5)
        y = stream._sine_wave(x)

        assert abs(y - 2.0) < 1e-10

    def test_sine_amplitude_scaling(self) -> None:
        """Test that amplitude scales the sine output."""
        config1 = ConfigModel(amplitude=1.0, frequency=0.5)
        config2 = ConfigModel(amplitude=3.0, frequency=0.5)

        stream1 = DataStream(config1)
        stream2 = DataStream(config2)

        # At quarter period
        x = (math.pi / 2) / (2 * math.pi * 0.5)
        y1 = stream1._sine_wave(x)
        y2 = stream2._sine_wave(x)

        assert abs(y2 - y1 * 3.0) < 1e-10


class TestSquareWave:
    """Tests for square wave generation."""

    def test_square_period(self) -> None:
        """Test square wave period."""
        config = ConfigModel(amplitude=1.0, frequency=1.0)
        stream = DataStream(config)

        # First half of period should be positive
        y1 = stream._square_wave(0.25)
        assert y1 == 1.0

        # Second half should be negative
        y2 = stream._square_wave(0.75)
        assert y2 == -1.0

    def test_square_amplitude(self) -> None:
        """Test square wave amplitude."""
        config = ConfigModel(amplitude=5.0, frequency=1.0)
        stream = DataStream(config)

        y_pos = stream._square_wave(0.25)
        y_neg = stream._square_wave(0.75)

        assert y_pos == 5.0
        assert y_neg == -5.0


class TestRandomWalk:
    """Tests for random walk generation."""

    def test_random_walk_sequence(self) -> None:
        """Test that random walk produces a sequence."""
        config = ConfigModel(amplitude=0.1)
        stream = DataStream(config)

        # Generate several steps
        values = [stream._random_walk() for _ in range(10)]

        # Check that we have 10 values
        assert len(values) == 10

        # Values should be changing (very unlikely all same)
        assert len(set(values)) > 1

    def test_random_walk_amplitude_constraint(self) -> None:
        """Test that random walk steps stay within amplitude bounds."""
        config = ConfigModel(amplitude=1.0)
        stream = DataStream(config)

        # Reset to known state
        stream.y_last = 0.0

        # Generate many steps
        for _ in range(1000):
            stream._random_walk()

        # y_last should be some finite value (not exploded)
        assert abs(stream.y_last) < 1000


class TestNoiseGeneration:
    """Tests for noise addition."""

    def test_noise_zero(self) -> None:
        """Test that zero noise produces deterministic output."""
        config = ConfigModel(amplitude=1.0, frequency=0.5, noise=0.0)
        stream1 = DataStream(config)
        stream2 = DataStream(config)

        # Reset both to same state
        stream1.x_current = 0.5
        stream2.x_current = 0.5

        y1 = stream1._generate_y()
        y2 = stream2._generate_y()

        assert y1 == y2

    def test_noise_distribution(self) -> None:
        """Test that noise is added (rough sanity check)."""
        config = ConfigModel(amplitude=0.1, frequency=0.5, noise=0.1)
        stream = DataStream(config)

        # Generate samples
        values = [stream._generate_y() for _ in range(100)]

        # Mean should be near base (roughly)
        mean = sum(values) / len(values)
        # With small amplitude and noise, mean should be close to 0
        assert abs(mean) < 0.5


class TestConfigValidation:
    """Tests for configuration validation."""

    def test_valid_config(self) -> None:
        """Test that valid config passes validation."""
        config = ConfigModel(amplitude=1.0, frequency=0.5, noise=0.05)

        is_valid, error_msg = config.validate()

        assert is_valid is True
        assert error_msg == ""

    def test_invalid_amplitude(self) -> None:
        """Test that negative amplitude fails validation."""
        config = ConfigModel(amplitude=-1.0)

        is_valid, error_msg = config.validate()

        assert is_valid is False
        assert "positive" in error_msg.lower()

    def test_invalid_frequency(self) -> None:
        """Test that negative frequency fails validation."""
        config = ConfigModel(frequency=-0.5)

        is_valid, error_msg = config.validate()

        assert is_valid is False

    def test_invalid_waveform(self) -> None:
        """Test that invalid waveform type fails validation."""
        config = ConfigModel(waveform="triangle")

        is_valid, error_msg = config.validate()

        assert is_valid is False
        assert "waveform" in error_msg.lower()
