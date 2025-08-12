from collections.abc import Callable
from typing import Any

from desktop.modern.core.interfaces.core_services import (
    ISettingsCoordinator,
    IUIStateManager,
)


class SettingsCoordinator(ISettingsCoordinator):
    """Main settings service that coordinates all settings operations"""

    def __init__(self, ui_state_service: IUIStateManager):
        self.ui_state_service = ui_state_service
        self._change_listeners: list[Callable[[str, Any], None]] = []

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.ui_state_service.get_setting(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value"""
        old_value = self.ui_state_service.get_setting(key)
        self.ui_state_service.set_setting(key, value)

        # Notify listeners if value changed
        if old_value != value:
            self._notify_change_listeners(key, value)

    def update_setting(self, key: str, value: Any) -> None:
        """Update a setting value (alias for set_setting for UI compatibility)"""
        self.set_setting(key, value)

    def add_change_listener(self, listener: Callable[[str, Any], None]) -> None:
        """Add a listener for setting changes"""
        if listener not in self._change_listeners:
            self._change_listeners.append(listener)

    def remove_change_listener(self, listener: Callable[[str, Any], None]) -> None:
        """Remove a listener for setting changes"""
        if listener in self._change_listeners:
            self._change_listeners.remove(listener)

    def _notify_change_listeners(self, key: str, value: Any) -> None:
        """Notify all listeners of a setting change"""
        for listener in self._change_listeners:
            try:
                listener(key, value)
            except Exception as e:
                # Log error but don't let one listener break others
                print(f"Error notifying settings change listener: {e}")

    def get_all_settings(self) -> dict[str, Any]:
        """Get all settings"""
        return self.ui_state_service.get_all_settings()

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults"""
        # Keep essential settings but clear others
        essential_keys = ["current_user", "user_profiles"]
        current_settings = self.get_all_settings()
        essential_settings = {
            key: current_settings.get(key)
            for key in essential_keys
            if key in current_settings
        }

        # Clear all settings
        self.ui_state_service.clear_settings()

        # Restore essential settings
        for key, value in essential_settings.items():
            if value is not None:
                self.set_setting(key, value)

    def save_settings(self) -> bool:
        """Save settings to persistent storage"""
        try:
            self.ui_state_service.save_state()
            return True
        except Exception:
            return False

    def load_settings(self) -> bool:
        """Load settings from persistent storage"""
        try:
            self.ui_state_service.load_state()
            return True
        except Exception:
            return False
