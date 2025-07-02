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

    # Signals
    mode_changed = pyqtSignal(str)  # new_mode
    dock_mode_requested = pyqtSignal()
    window_mode_requested = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize the mode manager."""
        super().__init__(parent)

        # Initialize with window mode, will be updated when components are set
        self.current_mode = "docked"  # "window" or "docked" - default to docked
        self.main_window = None
        self.dock_window = None
        self.tka_integration = None

    def set_components(self, main_window, tka_integration):
        """Set the main window and TKA integration components."""
        self.main_window = main_window
        self.tka_integration = tka_integration
        
        # Check if we should initialize in docked mode based on settings
        self._initialize_mode_from_settings()

    def _initialize_mode_from_settings(self):
        """Initialize the current mode based on saved settings."""
        try:
            # Try to use TKA integration settings first (if available)
            if self.tka_integration and hasattr(self.tka_integration, 'settings_service'):
                settings_service = self.tka_integration.settings_service
                launch_mode = settings_service.get_setting('launch_mode', 'docked')
                should_dock = launch_mode == 'docked'
                logger.info(f"🔍 TKA Settings check - launch_mode: {launch_mode}, should_dock: {should_dock}")
            else:
                # Fallback to standalone settings manager
                from config.settings import SettingsManager
                settings_manager = SettingsManager()
                
                should_dock = settings_manager.should_restore_to_docked()
                launch_mode = settings_manager.get('launch_mode', 'docked')
                auto_start = settings_manager.get('auto_start_docked', True)
                
                logger.info(f"🔍 Fallback Settings check - launch_mode: {launch_mode}, auto_start_docked: {auto_start}, should_restore_to_docked: {should_dock}")
            
            if should_dock:
                # Set the mode but don't switch yet - this will be handled by the main app
                self.current_mode = "docked"
                logger.info("🔄 Mode manager initialized for docked mode")
            else:
                self.current_mode = "window"
                logger.info("🪟 Mode manager initialized for window mode")
                
        except Exception as e:
            logger.warning(f"⚠️ Failed to read mode from settings, defaulting to window: {e}")
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
            logger.info("🔄 Switching to dock mode...")

            # Create dock window if it doesn't exist
            if not self.dock_window:
                self._create_dock_window()

            # Hide main window if it's visible
            if self.main_window and self.main_window.isVisible():
                self.main_window.hide()

            # Show dock window
            if self.dock_window:
                self.dock_window.show()
                self.dock_window.raise_()
                self.dock_window.activateWindow()

            # Update mode state
            self.current_mode = "docked"
            self.mode_changed.emit("docked")

            logger.info("✅ Switched to dock mode")

        except Exception as e:
            logger.error(f"❌ Failed to switch to dock mode: {e}")

    def switch_to_window_mode(self):
        """Switch from dock mode to window mode."""
        if self.current_mode == "window":
            logger.info("Already in window mode")
            return

        try:
            logger.info("🔄 Switching to window mode...")

            # Hide dock window
            if self.dock_window:
                self.dock_window.hide()

            # Show main window
            if self.main_window:
                self.main_window.show()
                self.main_window.raise_()
                self.main_window.activateWindow()

            # Update mode state
            self.current_mode = "window"
            self.mode_changed.emit("window")

            logger.info("✅ Switched to window mode")

        except Exception as e:
            logger.error(f"❌ Failed to switch to window mode: {e}")

    def _create_dock_window(self):
        """Create the dock window."""
        try:
            from ui.windows.dock_window import TKADockWindow
            from domain.models import DockConfiguration

            # Load dock configuration
            dock_config = self._load_dock_configuration()

            # Create dock window
            self.dock_window = TKADockWindow(self.tka_integration, dock_config)

            # Connect dock signals
            self.dock_window.application_launched.connect(
                self._on_dock_application_launched
            )
            self.dock_window.mode_switch_requested.connect(self.switch_to_window_mode)

            logger.info("✅ Dock window created")

        except Exception as e:
            logger.error(f"❌ Failed to create dock window: {e}")

    def _load_dock_configuration(self):
        """Load dock configuration."""
        from domain.models import DockConfiguration, DockPosition

        # For now, return default configuration
        # In the future, this could load from settings
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
        # Forward signal to main window if it has the signal
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
        logger.info("🧹 Cleaning up window mode manager...")

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
