"""
Settings dialog services initialization.

Handles the creation and initialization of all services required by the settings dialog.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.interfaces.core_services import IUIStateManagementService


class SettingsServices:
    """Service factory and manager for the settings dialog."""

    def __init__(self, ui_state_service: "IUIStateManagementService"):
        self.ui_state_service = ui_state_service
        self._initialize_services()

    def _initialize_services(self):
        """Initialize all the tab-specific services."""
        # Import services only when needed to avoid circular imports
        from application.services.settings.background_service import BackgroundService
        from application.services.settings.beat_layout_service import BeatLayoutService
        from application.services.settings.image_export_service import (
            ImageExportService,
        )
        from application.services.settings.prop_type_service import PropTypeService
        from application.services.settings.user_profile_service import (
            UserProfileService,
        )
        from application.services.settings.visibility_service import VisibilityService

        # Initialize services
        self.user_service = UserProfileService(self.ui_state_service)
        self.prop_service = PropTypeService(self.ui_state_service)
        self.visibility_service = VisibilityService(self.ui_state_service)
        self.layout_service = BeatLayoutService(self.ui_state_service)
        self.export_service = ImageExportService(self.ui_state_service)
        self.background_service = BackgroundService(self.ui_state_service)

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
