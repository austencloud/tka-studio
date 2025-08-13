"""
Settings dialog coordinator for managing settings state and updates.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.application.services.settings.settings_coordinator import (
    SettingsCoordinator,
)


class SettingsCoordinator(QObject):
    """Coordinates settings updates across all tabs."""

    settings_changed = pyqtSignal(str, object)  # setting_key, new_value

    def __init__(self, settings_service: SettingsCoordinator):
        super().__init__()
        self.settings_service = settings_service
        self._callbacks: dict[str, list[Callable]] = {}

    def register_callback(self, setting_key: str, callback: Callable):
        """Register callback for setting changes."""
        if setting_key not in self._callbacks:
            self._callbacks[setting_key] = []
        self._callbacks[setting_key].append(callback)

    def update_setting(self, key: str, value: Any):
        """Update a setting and notify observers."""
        self.settings_service.set_setting(key, value)
        self.settings_changed.emit(key, value)

        # Call registered callbacks
        if key in self._callbacks:
            for callback in self._callbacks[key]:
                callback(value)

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.settings_service.get_setting(key, default)

    def get_all_settings(self) -> dict[str, Any]:
        """Get all settings."""
        return self.settings_service.get_all_settings()

    def save_settings(self):
        """Save all settings to disk."""
        self.settings_service.save_settings()

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings_service.reset_to_defaults()
        # Emit signals for all settings
        for key, value in self.get_all_settings().items():
            self.settings_changed.emit(key, value)
