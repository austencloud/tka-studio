"""
UI Adapter for Settings Coordinator

Bridges the gap between Qt-based UI components and the framework-agnostic settings service.
This adapter handles the conversion between Qt signals and the observer pattern.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.core.interfaces.core_services import ISettingsCoordinator


class SettingsUIAdapter(QObject):
    """
    Adapter that bridges Qt UI components with the framework-agnostic SettingsCoordinator.

    This adapter:
    - Converts Qt signals to observer pattern callbacks
    - Provides Qt-compatible interface for UI components
    - Keeps the service layer framework-agnostic
    """

    settings_changed = pyqtSignal(str, object)

    def __init__(self, settings_coordinator: ISettingsCoordinator):
        super().__init__()
        self.settings_coordinator = settings_coordinator

        # Register ourselves as a change listener
        self.settings_coordinator.add_change_listener(self._on_setting_changed)

    def _on_setting_changed(self, key: str, value: Any) -> None:
        """Convert service layer callback to Qt signal"""
        self.settings_changed.emit(key, value)

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.settings_coordinator.get_setting(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value"""
        self.settings_coordinator.set_setting(key, value)

    def update_setting(self, key: str, value: Any) -> None:
        """Update a setting value (alias for set_setting)"""
        self.settings_coordinator.update_setting(key, value)

    def get_all_settings(self) -> dict:
        """Get all settings"""
        return self.settings_coordinator.get_all_settings()

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults"""
        self.settings_coordinator.reset_to_defaults()

    def save_settings(self) -> bool:
        """Save settings to persistent storage"""
        return self.settings_coordinator.save_settings()

    def load_settings(self) -> bool:
        """Load settings from persistent storage"""
        return self.settings_coordinator.load_settings()
