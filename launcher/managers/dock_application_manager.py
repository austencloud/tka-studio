#!/usr/bin/env python3
"""
Dock Application Manager - Application Loading and Icon Management
=================================================================

Handles application loading and icon management for the TKA dock:
- Loading applications from TKA integration
- Creating and managing dock icons
- Application status updates
- Icon lifecycle management

Architecture:
- Extracted from dock_window.py for better separation of concerns
- Manages application data and UI icon widgets
- Handles communication between dock and applications
"""

import logging
from typing import Optional

from domain.models import ApplicationData, ApplicationStatus
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout

try:
    from .dock_components import DockApplicationIcon
except ImportError:
    from dock_components import DockApplicationIcon

logger = logging.getLogger(__name__)


class DockApplicationManager(QObject):
    """Manages applications and their icons in the dock."""

    # Signals
    application_loaded = pyqtSignal(int)  # application_count
    icon_created = pyqtSignal(str)  # app_id
    status_updated = pyqtSignal(str, object)  # app_id, status

    def __init__(self, tka_integration, style_builder, parent=None):
        """Initialize the application manager."""
        super().__init__(parent)

        self.tka_integration = tka_integration
        self.style_builder = style_builder
        self.applications = []
        self.app_cards = {}  # app_id -> card widget mapping

    def load_applications(self) -> bool:
        """Load applications from TKA integration."""
        try:
            self.applications = self.tka_integration.get_applications()

            # Emit signal with application count
            self.application_loaded.emit(len(self.applications))
            return True

        except Exception as e:
            logger.error(f"❌ Failed to load applications: {e}")
            self.applications = []
            return False

    def update_dock_icons(self, icons_layout: QVBoxLayout) -> list[DockApplicationIcon]:
        """Update dock icons display."""
        # Clear existing icons
        self.clear_icons(icons_layout)

        # Create icon widgets for each application
        created_icons = []
        for app in self.applications:
            icon_widget = self.create_dock_icon(app)
            if icon_widget:
                icons_layout.addWidget(icon_widget)
                self.app_cards[app.id] = icon_widget
                created_icons.append(icon_widget)
                self.icon_created.emit(app.id)

        return created_icons

    def clear_icons(self, icons_layout: QVBoxLayout):
        """Clear all existing icon widgets."""
        while icons_layout.count():
            child = icons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.app_cards.clear()

    def create_dock_icon(self, app: ApplicationData) -> Optional[DockApplicationIcon]:
        """Create a dock icon widget for an application."""
        try:
            # Create a compact version of the application card
            icon_widget = DockApplicationIcon(app, self.style_builder)
            return icon_widget

        except Exception as e:
            logger.error(f"❌ Failed to create dock icon for {app.title}: {e}")
            return None

    def connect_icon_signals(
        self, icon_widget: DockApplicationIcon, launch_callback, context_menu_callback
    ):
        """Connect icon widget signals to dock window callbacks."""
        icon_widget.launch_requested.connect(launch_callback)
        icon_widget.context_menu_requested.connect(context_menu_callback)

    def update_application_status(self, app_id: str, status: ApplicationStatus):
        """Update visual status of an application."""
        if app_id in self.app_cards:
            self.app_cards[app_id].update_status(status)
            self.status_updated.emit(app_id, status)
            logger.debug(f"🔄 Updated status for {app_id}: {status}")

    def get_application_by_id(self, app_id: str) -> Optional[ApplicationData]:
        """Get application data by ID."""
        return next((app for app in self.applications if app.id == app_id), None)

    def get_application_count(self) -> int:
        """Get total number of applications."""
        return len(self.applications)

    def get_applications(self) -> list[ApplicationData]:
        """Get all applications."""
        return self.applications.copy()

    def refresh_applications(self, icons_layout: QVBoxLayout) -> bool:
        """Refresh applications and update icons."""
        success = self.load_applications()
        if success:
            self.update_dock_icons(icons_layout)
        return success

    def get_application_status(self, app_id: str) -> Optional[ApplicationStatus]:
        """Get current status of an application."""
        app = self.get_application_by_id(app_id)
        return app.status if app else None

    def has_application(self, app_id: str) -> bool:
        """Check if application exists in the dock."""
        return app_id in self.app_cards

    def get_icon_widget(self, app_id: str) -> Optional[DockApplicationIcon]:
        """Get icon widget for an application."""
        return self.app_cards.get(app_id)

    def simulate_status_progression(
        self,
        app_id: str,
        from_status: ApplicationStatus,
        to_status: ApplicationStatus,
        delay_ms: int = 2000,
    ):
        """Simulate status progression for testing/demo purposes."""

        def update_status():
            self.update_application_status(app_id, to_status)

        QTimer.singleShot(delay_ms, update_status)

    def get_manager_info(self) -> dict:
        """Get information about the application manager state."""
        return {
            "total_applications": len(self.applications),
            "active_icons": len(self.app_cards),
            "application_ids": [app.id for app in self.applications],
            "icon_ids": list(self.app_cards.keys()),
        }

    def cleanup(self):
        """Cleanup resources."""
        logger.info("🧹 Cleaning up dock application manager...")
        self.app_cards.clear()
        self.applications.clear()
