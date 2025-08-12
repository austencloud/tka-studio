"""
Settings Service - EXTRACTED FROM UISetupManager

Handles all settings-related functionality that was previously
mixed into the UISetupManager god object.

PROVIDES:
- Clean settings dialog management
- Proper separation of concerns
- Focused responsibility
"""

from __future__ import annotations

from PyQt6.QtWidgets import QMainWindow


class SettingsService:
    """
    Focused service for settings management.

    Extracted from UISetupManager to follow single responsibility principle.
    """

    def show_settings_dialog(self, main_window: QMainWindow) -> None:
        """Show the settings dialog with proper error handling."""
        try:
            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
            )
            from desktop.modern.core.interfaces.core_services import IUIStateManager
            from desktop.modern.presentation.components.ui.settings.settings_dialog import (
                SettingsDialog,
            )

            # Get UI state service from container
            container = get_container()
            ui_state_service = container.resolve(IUIStateManager)

            # Create and show dialog
            dialog = SettingsDialog(ui_state_service, main_window, container)

            # Connect to settings changes
            dialog.settings_changed.connect(
                lambda key, value: self._handle_setting_changed(key, value, main_window)
            )

            # Show modal dialog
            result = dialog.exec()

            # Clean up
            dialog.deleteLater()

            print(f"🔧 Settings dialog closed with result: {result}")

        except Exception as e:
            print(f"⚠️ Failed to open settings dialog: {e}")

    def _handle_setting_changed(
        self, key: str, value, main_window: QMainWindow
    ) -> None:
        """Handle settings changes with focused responsibility."""
        print(f"🔧 Setting changed: {key} = {value}")

        # Delegate specific setting changes to appropriate services
        if key == "background_type":
            self._handle_background_change(value, main_window)
        # Add other setting handlers as needed

    def _handle_background_change(self, value, main_window: QMainWindow) -> None:
        """Handle background setting changes."""
        try:
            from desktop.modern.application.services.ui.background_manager import (
                BackgroundManager,
            )

            background_manager = BackgroundManager()
            background_manager.apply_background_change(main_window, value)

        except Exception as e:
            print(f"⚠️ Failed to apply background change: {e}")
