"""
Settings dialog services initialization.

Handles the creation and initialization of all services required by the settings dialog.
"""

from typing import TYPE_CHECKING, Any

from desktop.modern.core.interfaces.core_services import IUIStateManager

if TYPE_CHECKING:
    pass


class UISettingsManager(IUIStateManager):
    """Service factory and manager for the settings dialog."""

    def __init__(self, ui_state_service: "IUIStateManager", container=None):
        self.ui_state_service = ui_state_service
        self.container = container
        self._initialize_services()

    def _initialize_services(self):
        """Initialize all the tab-specific services using DI container."""
        from desktop.modern.core.interfaces.settings_services import (
            IBackgroundSettingsManager,
            IBeatLayoutSettingsManager,
            IImageExportSettingsManager,
            IPropTypeSettingsManager,
            IUserProfileSettingsManager,
            IVisibilitySettingsManager,
        )

        # Get services from DI container (they're properly configured with QSettings)
        try:
            self.user_service = self.container.resolve(IUserProfileSettingsManager)
            self.prop_service = self.container.resolve(IPropTypeSettingsManager)
            self.visibility_service = self.container.resolve(IVisibilitySettingsManager)
            self.layout_service = self.container.resolve(IBeatLayoutSettingsManager)
            self.export_service = self.container.resolve(IImageExportSettingsManager)
            self.background_service = self.container.resolve(IBackgroundSettingsManager)
        except Exception as e:
            print(f"Failed to resolve settings services from DI container: {e}")
            # Fallback: create QSettings directly
            from PyQt6.QtCore import QSettings
            settings = QSettings("TKA", "KineticConstructor")

            from desktop.modern.application.services.settings.background_settings_manager import BackgroundSettingsManager
            from desktop.modern.application.services.settings.beat_layout_settings_manager import BeatLayoutSettingsManager
            from desktop.modern.application.services.settings.image_export_settings_manager import ImageExportSettingsManager
            from desktop.modern.application.services.settings.prop_type_settings_manager import PropTypeSettingsManager
            from desktop.modern.application.services.settings.user_profile_settings_manager import UserProfileSettingsManager
            from desktop.modern.application.services.settings.visibility_settings_manager import VisibilitySettingsManager

            self.user_service = UserProfileSettingsManager(settings)
            self.prop_service = PropTypeSettingsManager(settings)
            self.visibility_service = VisibilitySettingsManager(settings)
            self.layout_service = BeatLayoutSettingsManager(settings)
            self.export_service = ImageExportSettingsManager(settings)
            self.background_service = BackgroundSettingsManager(settings)

    def get_user_service(self):
        """Get the user profile service."""
        return self.user_service

    def get_prop_service(self):
        """Get the prop type service."""
        return self.prop_service

    def get_visibility_service(self):
        """Get the visibility service."""
        return self.visibility_service

    def get_layout_service(self):
        """Get the beat layout service."""
        return self.layout_service

    def get_export_service(self):
        """Get the image export service."""
        return self.export_service

    def get_background_service(self):
        """Get the background service."""
        return self.background_service

    # Interface implementation methods
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value (interface implementation)."""
        return self.ui_state_service.get_setting(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value (interface implementation)."""
        self.ui_state_service.set_setting(key, value)

    def get_tab_state(self, tab_name: str) -> dict[str, Any]:
        """Get state for a specific tab (interface implementation)."""
        return self.ui_state_service.get_tab_state(tab_name)

    def get_all_settings(self) -> dict[str, Any]:
        """Get all settings (interface implementation)."""
        return self.ui_state_service.get_all_settings()

    def clear_settings(self) -> None:
        """Clear all settings (interface implementation)."""
        self.ui_state_service.clear_settings()

    def save_state(self) -> None:
        """Save current state to persistent storage (interface implementation)."""
        self.ui_state_service.save_state()

    def load_state(self) -> None:
        """Load state from persistent storage (interface implementation)."""
        self.ui_state_service.load_state()

    def toggle_graph_editor(self) -> bool:
        """Toggle graph editor visibility (interface implementation)."""
        return self.ui_state_service.toggle_graph_editor()
