# ==================================================================================================
#  HelloGUI - Python Data Stream Visualization Demo
#  Module: core/data_stream.py (Timer-Driven Data Generator)
#
#  Purpose : Qt-integrated data stream with configurable waveforms and noise
# ==================================================================================================

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


# ==================================================================================================
#  Class DataStream(QObject):
# ==================================================================================================

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


    # --- Initialize stream with config and timer interval ---
    def __init__(self, config: ConfigModel, interval_ms: int = 100) -> None:
        """
        ############################################################################################
        @fcn        __init__
        @brief      Initialize the data stream generator.
        @details    Sets up Qt timer, configuration, and internal state for waveform generation.
                    Timer is not started; call start() to begin generation.

        @param[in]  config      ConfigModel with amplitude, frequency, waveform, noise settings.
        @param[in]  interval_ms Timer interval in milliseconds. Defaults to 100.
        @return     (None)

        @pre        config has valid parameters.
        @post       Timer initialized but not started; ready to call start().

        @note       Inherits from QObject to participate in Qt signal/slot system.
        ############################################################################################
        """
        super().__init__()
        self.config: ConfigModel = config
        self.interval_ms: int    = interval_ms
        self.x_current: float    = 0.0
        self.y_last: float       = 0.0  # For random walk

        # Timer for data generation
        self.timer: QTimer        = QTimer()
        self.timer.timeout.connect(self._on_timer)

        logger.info("DataStream initialized with config: %s", config)


    # --- Update the stream configuration ---
    def set_config(self, config: ConfigModel) -> None:
        """
        ############################################################################################
        @fcn        set_config
        @brief      Update stream configuration at runtime.
        @details    Changes waveform type, amplitude, frequency, noise without restarting.

        @param[in]  config      New ConfigModel to use for subsequent generation.
        @return     (None)

        @pre        config has valid parameters.
        @post       self.config updated; next generated point uses new settings.

        @note       Safe to call while stream is running.
        ############################################################################################
        """
        self.config = config
        logger.info("DataStream config updated: %s", config)


    # --- Start the data generation timer ---
    def start(self) -> None:
        """
        ############################################################################################
        @fcn        start
        @brief      Start the timer-driven data generation.
        @details    Emits started signal and begins emitting new_point signals at interval_ms.

        @return     (None)

        @pre        Timer should not already be running.
        @post       Timer started; new_point signals emitted at configured interval.

        @note       Idempotent if already running (checked via isActive()).
        ############################################################################################
        """
        if not self.timer.isActive():
            self.timer.start(self.interval_ms)
            self.started.emit()
            logger.debug("DataStream started (interval=%d ms)", self.interval_ms)


    # --- Stop the data generation timer ---
    def stop(self) -> None:
        """
        ############################################################################################
        @fcn        stop
        @brief      Stop the timer-driven data generation.
        @details    Halts timer, emits stopped signal, data point generation ceases.

        @return     (None)

        @pre        Timer may or may not be running.
        @post       Timer stopped; no new signals emitted until start() called.

        @note       Idempotent if already stopped; safe to call multiple times.
        ############################################################################################
        """
        if self.timer.isActive():
            self.timer.stop()
            self.stopped.emit()
            logger.debug("DataStream stopped")


    # --- Reset x position and random walk state ---
    def reset(self) -> None:
        """
        ############################################################################################
        @fcn        reset
        @brief      Reset internal state for a new dataset.
        @details    Resets x_current to 0.0 and y_last to 0.0 (for random walk tracking).

        @return     (None)

        @pre        None.
        @post       x_current=0.0, y_last=0.0 for clean start.

        @note       Typically called when user clicks Clear or starts a new measurement.
        ############################################################################################
        """
        self.x_current = 0.0
        self.y_last = 0.0
        logger.debug("DataStream reset")


    # --- [INTERNAL] Timer callback to generate and emit a point ---
    def _on_timer(self) -> None:
        """
        ############################################################################################
        @fcn        _on_timer
        @brief      Internal timer callback for periodic point generation.
        @details    Called by Qt timer at configured interval. Generates y value, emits
                    new_point signal, advances x by x_step.

        @return     (None)

        @pre        Timer is running; config is valid.
        @post       new_point signal emitted; x_current advanced.

        @section    Operation
             1. Call _generate_y() to get next y value
             2. Emit new_point signal with (x_current, y)
             3. Increment x_current by config.x_step

        @note       Private method; should not be called directly. Timer invokes automatically.
        ############################################################################################
        """
        y = self._generate_y()
        self.new_point.emit(self.x_current, y)
        self.x_current += self.config.x_step


    # --- [INTERNAL] Generate y value based on waveform and add noise ---
    def _generate_y(self) -> float:
        """
        ############################################################################################
        @fcn        _generate_y
        @brief      Generate y value using current waveform and add Gaussian noise.
        @details    Delegates to waveform-specific method, applies noise scaling, returns result.

        @return     (float) Generated y value with noise applied.

        @pre        config is valid; x_current is current position.
        @post       None (read-only side-effect: may update y_last for random walk).

        @section    Operation
             1. Dispatch to _sine_wave, _square_wave, or _random_walk based on config.waveform
             2. Generate Gaussian noise via random.gauss(0, config.noise)
             3. Return base_value + noise

        @note       Noise is applied to all waveforms uniformly.
        ############################################################################################
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
    

    # --- [INTERNAL] Generate sine wave value at position x ---
    def _sine_wave(self, x: float) -> float:
        """
        ############################################################################################
        @fcn        _sine_wave
        @brief      Compute sine wave value at position x.
        @details    Formula: y = amplitude * sin(2π * frequency * x).

        @param[in]  x     X position for evaluation.
        @return     (float) Computed sine wave y value.

        @pre        x is a valid float.
        @post       None (pure function).

        @note       Maximum amplitude reached at 1/4 period; zero at x=0.
        ############################################################################################
        """
        return self.config.amplitude * math.sin(2 * math.pi * self.config.frequency * x)
    

    # --- [INTERNAL] Generate square wave value at position x ---
    def _square_wave(self, x: float) -> float:
        """
        ############################################################################################
        @fcn        _square_wave
        @brief      Compute square wave value at position x.
        @details    Returns +amplitude or -amplitude depending on phase within period.
                    First half of period: +amplitude; second half: -amplitude.

        @param[in]  x     X position for evaluation.
        @return     (float) Y value (±amplitude).

        @pre        x is a valid float; frequency > 0 for defined period.
        @post       None (pure function).

        @section    Operation
             1. Compute period from frequency
             2. Normalize x to [0, 1) within period
             3. Return +amplitude if < 0.5, else -amplitude

        @note       Discontinuous at period transitions.
        ############################################################################################
        """
        # Normalize x to period [0, 1)
        period = 1.0 / self.config.frequency if self.config.frequency > 0 else 1.0
        phase = (x % period) / period
        # Return +amplitude for first half, -amplitude for second half
        return self.config.amplitude if phase < 0.5 else -self.config.amplitude
    

    # --- [INTERNAL] Generate next random walk value ---
    def _random_walk(self) -> float:
        """
        ############################################################################################
        @fcn        _random_walk
        @brief      Compute next value in a random walk sequence.
        @details    Generates random step in [-amplitude, +amplitude], updates y_last,
                    returns new cumulative value.

        @return     (float) Next y value in random walk.

        @pre        y_last initialized (typically 0.0).
        @post       y_last updated; call again for next step.

        @section    Operation
             1. Generate random step in [-amplitude, +amplitude]
             2. Add step to y_last (cumulative)
             3. Return updated y_last

        @note       Stateful; successive calls produce path with memory of prior values.
        ############################################################################################
        """
        # Random step: [-amplitude, +amplitude]
        step = random.uniform(-self.config.amplitude, self.config.amplitude)
        self.y_last += step
        return self.y_last
