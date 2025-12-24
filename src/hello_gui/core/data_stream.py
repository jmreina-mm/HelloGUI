"""
Simulated data stream generator using QTimer.

Generates (x, y) data points based on configurable waveforms (sine, square,
random walk) with optional Gaussian noise. Uses Qt signals for point emission.
"""

import logging
import math
import random

from PySide6.QtCore import QObject, QTimer, Signal

from hello_gui.models import ConfigModel

logger = logging.getLogger("hellogui")


class DataStream(QObject):
    """
    Data stream generator using Qt signals.

    Generates (x, y) points at a configurable interval based on a waveform
    model (sine, square, or random walk) with optional noise.

    Signals:
        new_point(float, float): Emitted when a new (x, y) point is generated.
        started(): Emitted when stream starts.
        stopped(): Emitted when stream stops.
    """

    # Define signals
    new_point = Signal(float, float)
    started = Signal()
    stopped = Signal()

    def __init__(self, config: ConfigModel, interval_ms: int = 100) -> None:
        """
        Initialize the data stream.

        Args:
            config (ConfigModel): Configuration for the stream.
            interval_ms (int): Timer interval in milliseconds. Defaults to 100.
        """
        super().__init__()
        self.config: ConfigModel = config
        self.interval_ms: int = interval_ms
        self.x_current: float = 0.0
        self.y_last: float = 0.0  # For random walk

        # Timer for data generation
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self._on_timer)

        logger.info("DataStream initialized with config: %s", config)

    def set_config(self, config: ConfigModel) -> None:
        """
        Update the stream configuration.

        Args:
            config (ConfigModel): New configuration.
        """
        self.config = config
        logger.info("DataStream config updated: %s", config)

    def start(self) -> None:
        """Start the data stream."""
        if not self.timer.isActive():
            self.timer.start(self.interval_ms)
            self.started.emit()
            logger.debug("DataStream started (interval=%d ms)", self.interval_ms)

    def stop(self) -> None:
        """Stop the data stream."""
        if self.timer.isActive():
            self.timer.stop()
            self.stopped.emit()
            logger.debug("DataStream stopped")

    def reset(self) -> None:
        """Reset x position to 0 for a new dataset."""
        self.x_current = 0.0
        self.y_last = 0.0
        logger.debug("DataStream reset")

    def _on_timer(self) -> None:
        """Internal timer callback to generate and emit a new point."""
        y = self._generate_y()
        self.new_point.emit(self.x_current, y)
        self.x_current += self.config.x_step

    def _generate_y(self) -> float:
        """
        Generate a y value based on current configuration and waveform type.

        Returns:
            float: Generated y value with noise applied.
        """
        # Generate base value based on waveform
        if self.config.waveform == "sine":
            base_y = self._sine_wave(self.x_current)
        elif self.config.waveform == "square":
            base_y = self._square_wave(self.x_current)
        elif self.config.waveform == "randomwalk":
            base_y = self._random_walk()
        else:
            base_y = 0.0
            logger.warning("Unknown waveform type: %s", self.config.waveform)

        # Add Gaussian noise
        noise = random.gauss(0, self.config.noise)
        return base_y + noise

    def _sine_wave(self, x: float) -> float:
        """
        Generate a sine wave value.

        Formula: y = amplitude * sin(2π * frequency * x)

        Args:
            x (float): X position.

        Returns:
            float: Y value at position x.
        """
        return self.config.amplitude * math.sin(2 * math.pi * self.config.frequency * x)

    def _square_wave(self, x: float) -> float:
        """
        Generate a square wave value.

        Returns +amplitude or -amplitude based on frequency phase.

        Args:
            x (float): X position.

        Returns:
            float: Y value at position x (±amplitude).
        """
        # Normalize x to period [0, 1)
        period = 1.0 / self.config.frequency if self.config.frequency > 0 else 1.0
        phase = (x % period) / period
        # Return +amplitude for first half, -amplitude for second half
        return self.config.amplitude if phase < 0.5 else -self.config.amplitude

    def _random_walk(self) -> float:
        """
        Generate a random walk value.

        Each step is a small random change from the previous value.

        Returns:
            float: Next value in random walk sequence.
        """
        # Random step: [-amplitude, +amplitude]
        step = random.uniform(-self.config.amplitude, self.config.amplitude)
        self.y_last += step
        return self.y_last
