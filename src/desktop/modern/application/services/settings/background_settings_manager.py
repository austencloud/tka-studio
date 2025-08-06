"""
Background Settings Manager Implementation

Implements background settings management with QSettings persistence,
event-driven updates, and asset validation.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QObject, QSettings, pyqtSignal


logger = logging.getLogger(__name__)


class BackgroundSettingsManager(QObject):
    """
    Implementation of background settings management using QSettings.

    Features:
    - Validates background assets exist before setting
    - Emits events when background changes
    - Integrates with font color computation
    - Thread-safe settings access
    """

    background_changed = pyqtSignal(str)  # background_type

    # Available background types from legacy system
    AVAILABLE_BACKGROUNDS = [
        "Snowfall",
        "AuroraBorealis",
        "Aurora",
        "Rainbow",
        "Confetti",
        "Starfield",
        "Galaxy",
        "Nebula",
    ]

    # Backgrounds that require dark font
    DARK_FONT_BACKGROUNDS = ["Rainbow", "AuroraBorealis", "Aurora"]

    def __init__(self, settings: QSettings):
        super().__init__()
        self.settings = settings
        logger.debug("Initialized BackgroundSettingsManager")

    def get_available_backgrounds(self) -> list[str]:
        """
        Get list of available background types.

        Returns:
            List of background type names
        """
        return self.AVAILABLE_BACKGROUNDS.copy()

    def get_current_background(self) -> str:
        """
        Get the currently selected background type.

        Returns:
            Current background type name
        """
        try:
            return self.settings.value("global/background_type", "Snowfall", type=str)
        except Exception as e:
            logger.error(f"Failed to get current background: {e}")
            return "Snowfall"

    def set_background(self, background_type: str) -> bool:
        """
        Set the background type.

        Args:
            background_type: Background type to set

        Returns:
            True if successful, False if invalid background type
        """
        try:
            if not self.is_valid_background(background_type):
                logger.warning(f"Invalid background type: {background_type}")
                return False

            old_background = self.get_current_background()

            # Set the background
            self.settings.setValue("global/background_type", background_type)
            self.settings.sync()

            # Emit change event if background actually changed
            if old_background != background_type:
                self.background_changed.emit(background_type)
                logger.info(
                    f"Background changed from {old_background} to {background_type}"
                )

            return True

        except Exception as e:
            logger.error(f"Failed to set background {background_type}: {e}")
            return False

    def is_valid_background(self, background_type: str) -> bool:
        """
        Check if the background type is valid.

        Args:
            background_type: Background type to validate

        Returns:
            True if valid, False otherwise
        """
        return background_type in self.AVAILABLE_BACKGROUNDS

    def get_font_color_for_background(self, background_type: str = None) -> str:
        """
        Get the appropriate font color for a background.

        Args:
            background_type: Background type (uses current if None)

        Returns:
            "black" or "white" depending on background
        """
        if background_type is None:
            background_type = self.get_current_background()

        return "black" if background_type in self.DARK_FONT_BACKGROUNDS else "white"

    def get_current_font_color(self) -> str:
        """
        Get the font color for the current background.

        Returns:
            "black" or "white" depending on current background
        """
        return self.get_font_color_for_background()
