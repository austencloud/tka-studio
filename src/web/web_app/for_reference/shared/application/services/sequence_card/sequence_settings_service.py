"""
Sequence Card Settings Service Implementation

Handles persistence of sequence card tab settings.
"""

import logging

from desktop.modern.core.interfaces.sequence_card_services import (
    ISequenceCardSettingsService,
)

logger = logging.getLogger(__name__)


class SequenceCardSettingsService(ISequenceCardSettingsService):
    """Implementation of sequence card settings operations."""

    def __init__(self, settings_service=None):
        self.settings_service = settings_service
        self.section = "sequence_card_tab"

        # If no settings service provided, use internal storage
        if self.settings_service is None:
            self._internal_settings = {"last_length": 16, "column_count": 2}

    def get_last_selected_length(self) -> int:
        """Get last selected length."""
        try:
            if self.settings_service:
                return self.settings_service.get_setting(
                    self.section, "last_length", 16
                )
            else:
                return self._internal_settings.get("last_length", 16)
        except Exception as e:
            logger.warning(f"Error getting last selected length: {e}")
            return 16

    def save_selected_length(self, length: int) -> None:
        """Save selected length."""
        try:
            if self.settings_service:
                self.settings_service.set_setting(self.section, "last_length", length)
            else:
                self._internal_settings["last_length"] = length
            logger.debug(f"Saved selected length: {length}")
        except Exception as e:
            logger.error(f"Error saving selected length {length}: {e}")

    def get_column_count(self) -> int:
        """Get column count setting."""
        try:
            if self.settings_service:
                return self.settings_service.get_setting(
                    self.section, "column_count", 2
                )
            else:
                return self._internal_settings.get("column_count", 2)
        except Exception as e:
            logger.warning(f"Error getting column count: {e}")
            return 2

    def save_column_count(self, count: int) -> None:
        """Save column count setting."""
        try:
            if self.settings_service:
                self.settings_service.set_setting(self.section, "column_count", count)
            else:
                self._internal_settings["column_count"] = count
            logger.debug(f"Saved column count: {count}")
        except Exception as e:
            logger.error(f"Error saving column count {count}: {e}")
