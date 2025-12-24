# ==================================================================================================
#  HelloGUI - Python Data Stream Visualization Demo
#  Module: ui/config_tab.py (Configuration Tab UI)
#  Purpose: Configuration UI for waveform and parameter tuning
# ==================================================================================================

"""
Configuration tab UI for the main application window.

Provides controls for configuring the simulated data stream parameters
including waveform type, amplitude, frequency, noise, and sampling rate.
"""

import logging

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDoubleSpinBox,
    QSpinBox,
    QComboBox,
    QPushButton,
    QGroupBox,
)

from hello_gui.models import ConfigModel

logger = logging.getLogger("hellogui")


# ==================================================================================================
#  Class ConfigTab(QWidget):
# ==================================================================================================

class ConfigTab(QWidget):
    """
    Configuration tab UI component.

    Allows users to configure stream parameters and apply new configurations.

    Attributes:
        amplitude_spin (QDoubleSpinBox): Waveform amplitude control.
        frequency_spin (QDoubleSpinBox): Oscillation frequency control.
        noise_spin (QDoubleSpinBox): Gaussian noise standard deviation.
        x_step_spin (QDoubleSpinBox): X-axis sampling interval.
        waveform_combo (QComboBox): Waveform type selector (sine, square, randomwalk).
        max_points_spin (QSpinBox): Maximum dataset buffer size.
        apply_button, reset_button (QPushButton): Action buttons.
    """
    # --- Initialize the Config tab with parameter controls ---

    def __init__(self, default_config: ConfigModel, parent=None):
        """
        ############################################################################################
        @fcn        __init__
        @brief      Initialize Config tab UI with parameter controls.
        @details    Creates spinboxes for amplitude, frequency, noise, x_step, max_points and 
                    combobox for waveform selection. Loads initial configuration from default_config.

        @param[in]  default_config  ConfigModel object with initial parameter values.
        @param[in]  parent          Parent Qt widget (optional).
        @return     (None)

        @pre        ConfigModel properly instantiated.
        @post       All spinboxes and combobox populated; ready for signal connections.

        @note       Signal connections to Apply/Reset buttons made by MainWindow.
        ############################################################################################
        """
        super().__init__(parent)

        main_layout = QVBoxLayout()

        # --- Waveform selection ---

        waveform_layout = QHBoxLayout()
        waveform_layout.addWidget(QLabel("Waveform Type:"))
        self.waveform_combo = QComboBox()
        self.waveform_combo.addItems(["sine", "square", "randomwalk"])
        waveform_layout.addWidget(self.waveform_combo)
        waveform_layout.addStretch()
        main_layout.addLayout(waveform_layout)

        # --- Amplitude ---

        amp_layout = QHBoxLayout()
        amp_layout.addWidget(QLabel("Amplitude:"))
        self.amplitude_spin = QDoubleSpinBox()
        self.amplitude_spin.setRange(0.01, 100.0)
        self.amplitude_spin.setSingleStep(0.1)
        self.amplitude_spin.setDecimals(3)
        amp_layout.addWidget(self.amplitude_spin)
        amp_layout.addStretch()
        main_layout.addLayout(amp_layout)

        # --- Frequency ---

        freq_layout = QHBoxLayout()
        freq_layout.addWidget(QLabel("Frequency (Hz):"))
        self.frequency_spin = QDoubleSpinBox()
        self.frequency_spin.setRange(0.0, 10.0)
        self.frequency_spin.setSingleStep(0.1)
        self.frequency_spin.setDecimals(2)
        freq_layout.addWidget(self.frequency_spin)
        freq_layout.addStretch()
        main_layout.addLayout(freq_layout)

        # --- Noise ---

        noise_layout = QHBoxLayout()
        noise_layout.addWidget(QLabel("Noise (Std Dev):"))
        self.noise_spin = QDoubleSpinBox()
        self.noise_spin.setRange(0.0, 1.0)
        self.noise_spin.setSingleStep(0.01)
        self.noise_spin.setDecimals(3)
        noise_layout.addWidget(self.noise_spin)
        noise_layout.addStretch()
        main_layout.addLayout(noise_layout)

        # --- X-Step (sampling interval) ---

        xstep_layout = QHBoxLayout()
        xstep_layout.addWidget(QLabel("X-Step (sample interval):"))
        self.x_step_spin = QDoubleSpinBox()
        self.x_step_spin.setRange(0.001, 1.0)
        self.x_step_spin.setSingleStep(0.01)
        self.x_step_spin.setDecimals(3)
        xstep_layout.addWidget(self.x_step_spin)
        xstep_layout.addStretch()
        main_layout.addLayout(xstep_layout)

        # --- Max points ---

        maxp_layout = QHBoxLayout()
        maxp_layout.addWidget(QLabel("Max Points in Buffer:"))
        self.max_points_spin = QSpinBox()
        self.max_points_spin.setRange(10, 100000)
        self.max_points_spin.setSingleStep(100)
        maxp_layout.addWidget(self.max_points_spin)
        maxp_layout.addStretch()
        main_layout.addLayout(maxp_layout)

        # --- Buttons ---

        button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Apply")
        self.reset_button = QPushButton("Reset Defaults")
        button_layout.addStretch()
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.reset_button)
        main_layout.addLayout(button_layout)

        main_layout.addStretch()

        self.setLayout(main_layout)

        # Load initial config
        self.load_config(default_config)

        logger.debug("ConfigTab initialized")


    # --- Load configuration values into UI controls ---
    def load_config(self, config: ConfigModel) -> None:
        """
        ############################################################################################
        @fcn        load_config
        @brief      Load configuration values into UI spinboxes and combobox.
        @details    Updates all parameter controls (amplitude, frequency, noise, x_step, max_points,
                    waveform) to reflect values from the provided ConfigModel.

        @param[in]  config      ConfigModel object with values to load.
        @return     (None)

        @pre        UI controls created.
        @post       All controls display values from config; may trigger valueChanged signals.

        @note       Used when applying config, resetting defaults, or loading from file.
        ############################################################################################
        """
        self.waveform_combo.setCurrentText(config.waveform)
        self.amplitude_spin.setValue(config.amplitude)
        self.frequency_spin.setValue(config.frequency)
        self.noise_spin.setValue(config.noise)
        self.x_step_spin.setValue(config.x_step)
        self.max_points_spin.setValue(config.max_points)


    # --- Build ConfigModel from current UI values ---
    def get_config(self) -> ConfigModel:
        """
        ############################################################################################
        @fcn        get_config
        @brief      Build ConfigModel from current UI control values.
        @details    Reads all spinboxes and combobox values and constructs a new ConfigModel
                    representing the user's current configuration selections.

        @return     (ConfigModel) New ConfigModel with current UI values.

        @pre        All UI controls exist and have values.
        @post       New ConfigModel created; no side effects.

        @note       Used when user clicks Apply Config or Save Data.
        ############################################################################################
        """
        return ConfigModel(
            amplitude=self.amplitude_spin.value(),
            frequency=self.frequency_spin.value(),
            noise=self.noise_spin.value(),
            x_step=self.x_step_spin.value(),
            waveform=self.waveform_combo.currentText(),
            max_points=self.max_points_spin.value(),
        )


    # --- Reset all controls to factory defaults ---
    def reset_to_defaults(self) -> None:
        """
        ############################################################################################
        @fcn        reset_to_defaults
        @brief      Reset all parameter controls to factory default values.
        @details    Obtains default configuration from ConfigModel.defaults() and loads it
                    into all UI controls via load_config().

        @return     (None)

        @pre        UI controls created and initialized.
        @post       All controls display factory default values; log message recorded.

        @note       Connected to Reset Defaults button in MainWindow.
        ############################################################################################
        """
        default_config = ConfigModel.defaults()
        self.load_config(default_config)
        logger.info("Config tab reset to defaults")
