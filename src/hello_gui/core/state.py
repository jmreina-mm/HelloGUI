# ==================================================================================================
#  HelloGUI - Python Data Stream Visualization Demo
#  Module: core/state.py (Application State Management)
#
#  Purpose : Central state container for configuration, dataset, and status
# ==================================================================================================

"""
Application state management module.

Manages the overall application state including configuration, dataset,
and running state. Provides a centralized state object for the application.
"""

import logging
from typing import Optional

from hello_gui.models import ConfigModel, DatasetModel

logger = logging.getLogger("hellogui")


# ==================================================================================================
#  Class AppState(object):
# ==================================================================================================

class AppState:
    """
    Central application state container.

    Maintains the current configuration, active dataset, and running state
    of the application. Provides methods to modify state consistently.

    Attributes:
        config (ConfigModel): Current stream configuration.
        dataset (DatasetModel): Active dataset.
        running (bool): Whether the data stream is currently running.
    """
    # --- Initialize application state with default config and empty dataset ---

    def __init__(self) -> None:
        """
        ############################################################################################
        @fcn        __init__
        @brief      Initialize the application state container.
        @details    Creates default configuration, empty dataset, and sets running=False.

        @return     (None) Instance initialized.

        @pre        None.
        @post       AppState instance ready with defaults.

        @note       Typically called once at application startup.
        ############################################################################################
        """
        self.config: ConfigModel   = ConfigModel.defaults()
        self.dataset: DatasetModel = DatasetModel()
        self.running: bool         = False


    # --- Set running flag to True ---
    def start(self) -> None:
        """
        ############################################################################################
        @fcn        start
        @brief      Mark the data stream as running.
        @details    Sets running=True and logs the state transition.

        @return     (None)

        @pre        None.
        @post       running flag set to True.

        @note       Typically called when user clicks Start/Resume button.
        ############################################################################################
        """
        self.running = True
        logger.info("Data stream started")


    # --- Pause the stream without clearing data ---
    def pause(self) -> None:
        """
        ############################################################################################
        @fcn        pause
        @brief      Pause the data stream.
        @details    Sets running=False. Dataset remains intact for potential resume.

        @return     (None)

        @pre        None.
        @post       running flag set to False.

        @note       Unlike clear(), data is preserved for resume.
        ############################################################################################
        """
        self.running = False
        logger.info("Data stream paused")


    # --- Resume the stream from current state ---
    def resume(self) -> None:
        """
        ############################################################################################
        @fcn        resume
        @brief      Resume the data stream from paused state.
        @details    Sets running=True to continue generation without clearing dataset.

        @return     (None)

        @pre        Stream should be paused (running=False).
        @post       running flag set to True.

        @note       Preserves all accumulated data; resumes x-position where paused.
        ############################################################################################
        """
        self.running = True
        logger.info("Data stream resumed")


    # --- Clear dataset and pause stream ---
    def clear(self) -> None:
        """
        ############################################################################################
        @fcn        clear
        @brief      Clear the dataset and pause the stream.
        @details    Removes all accumulated data points and stops generation.

        @return     (None)

        @pre        None.
        @post       Dataset empty; running=False.

        @note       Destructive operation; data loss is permanent unless saved first.
        ############################################################################################
        """
        self.dataset.clear()
        self.running = False
        logger.info("Dataset cleared")


    # --- Apply new configuration if valid ---
    def apply_config(self, config: ConfigModel) -> bool:
        """
        ############################################################################################
        @fcn        apply_config
        @brief      Apply a new stream configuration after validation.
        @details    Validates configuration; if valid, replaces current config and updates
                    dataset max_length. Returns success status.

        @param[in]  config      New ConfigModel to apply.
        @return     (bool) True if applied successfully; False if validation failed.

        @pre        config fields should be set.
        @post       If True: config replaced, max_length updated. If False: no changes.

        @section    Operation
             1. Call config.validate()
             2. If invalid, log error and return False
             3. Update self.config and dataset.max_length
             4. Log success and return True

        @note       Validation prevents invalid configurations from being active.
        ############################################################################################
        """
        is_valid, error_msg = config.validate()
        if not is_valid:
            logger.error("Configuration validation failed: %s", error_msg)
            return False

        self.config = config
        # Update dataset max length based on config
        self.dataset.max_length = config.max_points
        logger.info("Configuration applied: %s", config)
        return True


    # --- Reset configuration to factory defaults ---
    def reset_config(self) -> None:
        """
        ############################################################################################
        @fcn        reset_config
        @brief      Reset configuration to factory defaults.
        @details    Restores all parameters to ConfigModel.defaults() values.

        @return     (None)

        @pre        None.
        @post       config and dataset.max_length reset to defaults.

        @note       Useful for "Reset" button or error recovery.
        ############################################################################################
        """
        self.config = ConfigModel.defaults()
        self.dataset.max_length = self.config.max_points
        logger.info("Configuration reset to defaults")


    # --- Return string representation of current state ---
    def __repr__(self) -> str:
        """
        ############################################################################################
        @fcn        __repr__
        @brief      Return string representation of application state.
        @details    Shows current configuration, dataset size, and running status.

        @return     (str) Human-readable state summary.

        @pre        None.
        @post       None (read-only).

        @note       Useful for debugging and logging.
        ############################################################################################
        """
        return (
            f"AppState(config={self.config}, "
            f"dataset_points={self.dataset.point_count()}, "
            f"running={self.running})"
        )
