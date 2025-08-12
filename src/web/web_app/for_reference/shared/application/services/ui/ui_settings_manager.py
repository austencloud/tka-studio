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

    def __init__(self, ui_state_service: "IUIStateManager"):
        self.ui_state_service = ui_state_service
        self._initialize_services()

    def _initialize_services(self):
        """Initialize all the tab-specific services."""
        # Import services only when needed to avoid circular imports
        from shared.application.services.settings.background_settings_manager import (
            BackgroundSettingsManager,
        )
        from shared.application.services.settings.beat_layout_settings_manager import (
            BeatLayoutSettingsManager,
        )
        from shared.application.services.settings.image_export_settings_manager import (
            ImageExportSettingsManager,
        )
        from shared.application.services.settings.prop_type_settings_manager import (
            PropTypeSettingsManager,
        )
        from shared.application.services.settings.user_profile_settings_manager import (
            UserProfileSettingsManager,
        )
        from shared.application.services.settings.visibility_settings_manager import (
            VisibilitySettingsManager,
        )

        # Initialize services
        self.user_service = UserProfileSettingsManager(self.ui_state_service)
        self.prop_service = PropTypeSettingsManager(self.ui_state_service)
        self.visibility_service = VisibilitySettingsManager(self.ui_state_service)
        self.layout_service = BeatLayoutSettingsManager(self.ui_state_service)
        self.export_service = ImageExportSettingsManager(self.ui_state_service)
        self.background_service = BackgroundSettingsManager(self.ui_state_service)

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
