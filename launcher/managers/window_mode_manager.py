#!/usr/bin/env python3
"""
Window Mode Manager - Mode Switching Logic
==========================================

Handles switching between window and dock modes for the TKA launcher:
- Mode state management
- Window/dock mode transitions
- UI state synchronization
- Mode-specific configurations

Architecture:
- Extracted from launcher_window.py for better separation of concerns
- Manages mode transitions and state
- Coordinates between main window and dock window
"""

import logging
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)


class WindowModeManager(QObject):
    """Manages switching between window and dock modes."""

    mode_changed = pyqtSignal(str)
    dock_mode_requested = pyqtSignal()
    window_mode_requested = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize the mode manager."""
        super().__init__(parent)
        self.current_mode = "docked"
        self.main_window = None
        self.dock_window = None
        self.tka_integration = None

    def set_components(self, main_window, tka_integration):
        """Set the main window and TKA integration components."""
        self.main_window = main_window
        self.tka_integration = tka_integration
        self._initialize_mode_from_settings()

    def _initialize_mode_from_settings(self):
        """Initialize the current mode based on saved settings."""
        try:
            if self.tka_integration and hasattr(
                self.tka_integration, "settings_service"
            ):
                settings_service = self.tka_integration.settings_service
                launch_mode = settings_service.get_setting("launch_mode", "docked")
                should_dock = launch_mode == "docked"
            else:
                from config.settings import SettingsManager
                settings_manager = SettingsManager()
                should_dock = settings_manager.should_restore_to_docked()
                launch_mode = settings_manager.get("launch_mode", "docked")
                auto_start = settings_manager.get("auto_start_docked", True)
                logger.debug(
                    f"Settings fallback - launch_mode: {launch_mode}, auto_start_docked: {auto_start}, should_restore_to_docked: {should_dock}"
                )

            self.current_mode = "docked" if should_dock else "window"
        except Exception as e:
            logger.warning(
                f"Failed to read mode from settings, defaulting to window: {e}"
            )
            self.current_mode = "window"

    def toggle_mode(self):
        """Toggle between window and dock modes."""
        if self.current_mode == "window":
            self.switch_to_dock_mode()
        else:
            self.switch_to_window_mode()

    def switch_to_dock_mode(self):
        """Switch from window mode to dock mode."""
        try:
            if not self.dock_window:
                self._create_dock_window()
            if self.main_window and self.main_window.isVisible():
                self.main_window.hide()
            if self.dock_window:
                self.dock_window.show()
                self.dock_window.raise_()
                self.dock_window.activateWindow()
            self.current_mode = "docked"
            self.mode_changed.emit("docked")
        except Exception as e:
            logger.error(f"Failed to switch to dock mode: {e}")

    def switch_to_window_mode(self):
        """Switch from dock mode to window mode."""
        if self.current_mode == "window":
            return
        try:
            if self.dock_window:
                self.dock_window.hide()
            if self.main_window:
                self.main_window.show()
                self.main_window.raise_()
                self.main_window.activateWindow()
            self.current_mode = "window"
            self.mode_changed.emit("window")
        except Exception as e:
            logger.error(f"Failed to switch to window mode: {e}")

    def _create_dock_window(self):
        """Create the dock window."""
        try:
            from ui.windows.dock_window import TKADockWindow
            from domain.models import DockConfiguration
            dock_config = self._load_dock_configuration()
            self.dock_window = TKADockWindow(self.tka_integration, dock_config)
            self.dock_window.application_launched.connect(
                self._on_dock_application_launched
            )
            self.dock_window.mode_switch_requested.connect(self.switch_to_window_mode)
        except Exception as e:
            logger.error(f"Failed to create dock window: {e}")

    def _load_dock_configuration(self):
        """Load dock configuration."""
        from domain.models import DockConfiguration, DockPosition
        return DockConfiguration(
            position=DockPosition.BOTTOM_LEFT,
            width=64,
            height=200,
            margin_x=0,
            margin_y=0,
            always_on_top=True,
            auto_hide=False,
        )

    def _on_dock_application_launched(self, app_id: str, app_title: str):
        """Handle application launch from dock."""
        if self.main_window and hasattr(self.main_window, "application_launched"):
            self.main_window.application_launched.emit(app_id, app_title)

    def get_current_mode(self) -> str:
        """Get the current mode."""
        return self.current_mode

    def is_dock_mode(self) -> bool:
        """Check if currently in dock mode."""
        return self.current_mode == "docked"

    def is_window_mode(self) -> bool:
        """Check if currently in window mode."""
        return self.current_mode == "window"

    def cleanup(self):
        """Cleanup resources."""
        if self.dock_window:
            self.dock_window.close()
            self.dock_window = None

    def get_mode_info(self) -> dict:
        """Get information about current mode state."""
        return {
            "current_mode": self.current_mode,
            "has_dock_window": self.dock_window is not None,
            "has_main_window": self.main_window is not None,
            "dock_window_visible": (
                self.dock_window.isVisible() if self.dock_window else False
            ),
            "main_window_visible": (
                self.main_window.isVisible() if self.main_window else False
            ),
        }
