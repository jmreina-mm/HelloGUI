"""
Application state management module.

Manages the overall application state including configuration, dataset,
and running state. Provides a centralized state object for the application.
"""

import logging
from typing import Optional

from hello_gui.models import ConfigModel, DatasetModel

logger = logging.getLogger("hellogui")


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

    def __init__(self) -> None:
        """Initialize application state with defaults."""
        self.config: ConfigModel = ConfigModel.defaults()
        self.dataset: DatasetModel = DatasetModel()
        self.running: bool = False

    def start(self) -> None:
        """
        Start the data stream.

        Sets running flag to True and logs the action.
        """
        self.running = True
        logger.info("Data stream started")

    def pause(self) -> None:
        """
        Pause the data stream.

        Sets running flag to False without clearing data.
        """
        self.running = False
        logger.info("Data stream paused")

    def resume(self) -> None:
        """
        Resume the data stream.

        Sets running flag to True to continue from current state.
        """
        self.running = True
        logger.info("Data stream resumed")

    def clear(self) -> None:
        """
        Clear the active dataset.

        Resets the dataset and pauses the stream.
        """
        self.dataset.clear()
        self.running = False
        logger.info("Dataset cleared")

    def apply_config(self, config: ConfigModel) -> bool:
        """
        Apply a new configuration.

        Validates the configuration before applying. If validation fails,
        the configuration is not changed.

        Args:
            config (ConfigModel): New configuration to apply.

        Returns:
            bool: True if configuration was applied successfully, False otherwise.
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

    def reset_config(self) -> None:
        """Reset configuration to factory defaults."""
        self.config = ConfigModel.defaults()
        self.dataset.max_length = self.config.max_points
        logger.info("Configuration reset to defaults")

    def __repr__(self) -> str:
        """Return string representation of application state."""
        return (
            f"AppState(config={self.config}, "
            f"dataset_points={self.dataset.point_count()}, "
            f"running={self.running})"
        )
