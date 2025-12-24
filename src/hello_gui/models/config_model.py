"""
Configuration model for the data stream simulator.

This module defines the ConfigModel dataclass that holds all configurable
parameters for the simulated data stream, including waveform type, amplitude,
frequency, noise level, and sampling parameters.
"""

from dataclasses import dataclass, field
from typing import ClassVar, Literal


@dataclass
class ConfigModel:
    """
    Configuration model for the data stream simulator.

    Attributes:
        amplitude (float): Peak amplitude of the waveform. Defaults to 1.0.
        frequency (float): Frequency of oscillation in Hz. Defaults to 0.5.
        noise (float): Standard deviation of Gaussian noise. Defaults to 0.05.
        x_step (float): Step size for x-axis (sampling interval). Defaults to 0.05.
        waveform (str): Type of waveform: "sine", "square", or "randomwalk". Defaults to "sine".
        max_points (int): Maximum number of points in the dataset buffer. Defaults to 5000.
    """

    amplitude: float = 1.0
    frequency: float = 0.5
    noise: float = 0.05
    x_step: float = 0.05
    waveform: str = "sine"
    max_points: int = 5000

    # Class constants for valid waveform types
    VALID_WAVEFORMS: ClassVar[tuple[str, ...]] = ("sine", "square", "randomwalk")

    def validate(self) -> tuple[bool, str]:
        """
        Validate the configuration parameters.

        Returns:
            tuple[bool, str]: (is_valid, error_message). If is_valid is True,
                error_message is empty.
        """
        if self.amplitude <= 0:
            return False, "Amplitude must be positive."
        if self.frequency < 0:
            return False, "Frequency must be non-negative."
        if self.noise < 0:
            return False, "Noise must be non-negative."
        if self.x_step <= 0:
            return False, "X-step must be positive."
        if self.waveform not in self.VALID_WAVEFORMS:
            return False, f"Waveform must be one of {self.VALID_WAVEFORMS}."
        if self.max_points < 10:
            return False, "Max points must be at least 10."
        return True, ""

    @classmethod
    def defaults(cls) -> "ConfigModel":
        """
        Return a ConfigModel instance with default values.

        Returns:
            ConfigModel: A new instance with factory defaults.
        """
        return cls()
