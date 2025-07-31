#!/usr/bin/env python3
"""
TKA Dock Window - Dockable Launcher Implementation
=================================================

A dockable version of the TKA launcher that transforms into a horizontal taskbar
positioned at the bottom-left edge of the primary screen. Maintains all existing
launcher functionality while providing a compact, always-on-top dock interface.

Features:
- Always-on-top dock positioning
- Windows taskbar integration
- Application status indicators
- Context menu functionality
- Smooth transitions between modes
- State persistence

Architecture:
- Clean separation from main launcher window
- Reuses existing application grid and services
- Follows TKA's clean architecture patterns
- PyQt6 implementation with reliable design system
"""

import ctypes
import logging
import sys
from typing import Optional

from domain.models import ApplicationStatus, DockConfiguration, WindowGeometry
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QWidget
from ui.pyqt6_compatible_design_system import get_reliable_style_builder
from ui.reliable_effects import get_shadow_manager

try:
    from managers.dock_application_manager import DockApplicationManager
    from managers.dock_context_menu import DockContextMenuManager
    from managers.dock_position_manager import DockPositionManager
    from managers.dock_window_setup import DockWindowSetup
except ImportError:
    # Fallback for direct imports (e.g., in tests)
    from managers.dock_application_manager import DockApplicationManager
    from managers.dock_context_menu import DockContextMenuManager
    from managers.dock_position_manager import DockPositionManager
    from managers.dock_window_setup import DockWindowSetup

logger = logging.getLogger(__name__)


class TKADockWindow(QWidget):
    """
    Dockable TKA launcher window.

    Provides a compact, always-on-top dock interface that displays application
    icons vertically and maintains all launcher functionality.
    """

    # Signals
    application_launched = pyqtSignal(str, str)  # app_id, app_title
    mode_switch_requested = pyqtSignal()  # Request to switch back to window mode
    dock_configuration_changed = pyqtSignal(object)  # DockConfiguration

    def __init__(
        self, tka_integration, dock_config: Optional[DockConfiguration] = None
    ):
        """Initialize the dock window."""
        super().__init__()

        self.tka_integration = tka_integration
        self.dock_config = dock_config or DockConfiguration()

        # UI components
        self.style_builder = get_reliable_style_builder()
        self.shadow_manager = get_shadow_manager()

        # Helper managers
        self.position_manager = DockPositionManager(self.dock_config)
        self.application_manager = DockApplicationManager(
            tka_integration, self.style_builder, self
        )
        self.window_setup = DockWindowSetup(self.dock_config)
        self.context_menu_manager = DockContextMenuManager(self)

        # Connect signals
        self._connect_signals()

        # Setup window
        self._initialize_window()

        # TKA Dock Window initialized - log removed to reduce startup noise
        # Ensure always-on-top after initial show
        self._install_always_on_top()

    def _connect_signals(self):
        """Connect all manager signals to dock window methods."""
        # Context menu signals
        self.context_menu_manager.launch_requested.connect(self._on_launch_requested)
        self.context_menu_manager.stop_requested.connect(self._terminate_application)
        self.context_menu_manager.restart_requested.connect(self._restart_application)
        self.context_menu_manager.process_info_requested.connect(
            self._show_process_info
        )
        self.context_menu_manager.properties_requested.connect(
            self._show_app_properties
        )
        self.context_menu_manager.mode_switch_requested.connect(
            self.mode_switch_requested.emit
        )

        # Application manager signals
        self.application_manager.application_loaded.connect(
            self._on_applications_loaded
        )

    def _initialize_window(self):
        """Initialize the dock window with all components."""
        # Calculate initial height
        initial_height = self.position_manager.calculate_dock_height()

        # Setup window properties
        self.window_setup.setup_dock_window(self)
        self.window_setup.apply_size_configuration(self, initial_height)

        # Setup layout
        self.main_layout, self.icons_container, self.icons_layout = (
            self.window_setup.setup_layout(self)
        )

        # Apply styling
        self.window_setup.setup_styling(self)

        # Load applications and create icons
        if self.application_manager.load_applications():
            icons = self.application_manager.update_dock_icons(self.icons_layout)
            self._connect_icon_signals(icons)

            # Recalculate height based on actual application count
            actual_height = self.position_manager.calculate_actual_dock_height(
                self.application_manager.get_applications()
            )
            self.setFixedHeight(actual_height)

        # Position dock
        self.position_manager.position_dock(self)

    def _connect_icon_signals(self, icons):
        """Connect signals for all icon widgets."""
        for icon in icons:
            self.application_manager.connect_icon_signals(
                icon, self._on_launch_requested, self._on_context_menu_requested
            )

    def _on_applications_loaded(self, application_count: int):
        """Handle applications loaded signal."""
        # Remove the "Applications loaded" log message

    def _on_launch_requested(self, app_id: str):
        """Handle application launch request."""
        self.launch_application(app_id)

    def launch_application(self, app_id: str):
        """Launch an application by ID using the same pathway as window mode."""
        try:
            # Find the application using application manager
            app = self.application_manager.get_application_by_id(app_id)
            if not app:
                logger.error(f"❌ Application not found: {app_id}")
                return

            logger.info(f"🚀 Launching application from dock: {app.title}")

            # Launch through TKA integration (same as window mode)
            success = self.tka_integration.launch_application(app_id)

            if success:
                # Update visual status to starting
                self.application_manager.update_application_status(
                    app_id, ApplicationStatus.STARTING
                )

                # Emit signal for any listeners
                self.application_launched.emit(app_id, app.title)
                logger.info(f"✅ Successfully launched from dock: {app.title}")

                # Simulate status progression
                self.application_manager.simulate_status_progression(
                    app_id, ApplicationStatus.STARTING, ApplicationStatus.RUNNING, 2000
                )
            else:
                # Update visual status to error
                self.application_manager.update_application_status(
                    app_id, ApplicationStatus.ERROR
                )
                logger.error(f"❌ Failed to launch from dock: {app.title}")

        except Exception as e:
            logger.error(f"❌ Error launching application {app_id} from dock: {e}")
            # Update visual status to error
            self.application_manager.update_application_status(
                app_id, ApplicationStatus.ERROR
            )

    def _on_context_menu_requested(self, app_id: str, position):
        """Handle context menu request."""
        applications = self.application_manager.get_applications()
        self.context_menu_manager.show_context_menu(app_id, applications, position)

    def _terminate_application(self, app_id: str):
        """Terminate a running application."""
        try:
            logger.info(f"🛑 Terminating application {app_id}")

            # Update visual status to stopping
            self.application_manager.update_application_status(
                app_id, ApplicationStatus.STOPPING
            )

            # Try to get the launch service from TKA integration
            if (
                hasattr(self.tka_integration, "launch_service")
                and self.tka_integration.launch_service
            ):
                success = self.tka_integration.launch_service.stop_application(app_id)
                if success:
                    logger.info(f"✅ Successfully terminated {app_id}")
                    self.application_manager.update_application_status(
                        app_id, ApplicationStatus.STOPPED
                    )
                else:
                    logger.error(f"❌ Failed to terminate {app_id}")
                    self.application_manager.update_application_status(
                        app_id, ApplicationStatus.ERROR
                    )
            else:
                # Fallback: just update visual status
                logger.warning(
                    "⚠️ No launch service available, updating visual status only"
                )
                self.application_manager.simulate_status_progression(
                    app_id, ApplicationStatus.STOPPING, ApplicationStatus.STOPPED, 1000
                )

        except Exception as e:
            logger.error(f"❌ Error terminating application {app_id}: {e}")
            self.application_manager.update_application_status(
                app_id, ApplicationStatus.ERROR
            )

    def _restart_application(self, app_id: str):
        """Restart a running application."""
        try:
            logger.info(f"🔄 Restarting application {app_id}")

            # Update visual status to stopping
            self.application_manager.update_application_status(
                app_id, ApplicationStatus.STOPPING
            )

            # Try to get the launch service from TKA integration
            if (
                hasattr(self.tka_integration, "launch_service")
                and self.tka_integration.launch_service
            ):
                # Use the launch service restart method
                result = self.tka_integration.launch_service.restart_application(app_id)
                if result.success:
                    logger.info(f"✅ Successfully restarted {app_id}")
                    self.application_manager.update_application_status(
                        app_id, ApplicationStatus.RUNNING
                    )
                else:
                    logger.error(
                        f"❌ Failed to restart {app_id}: {result.error_message}"
                    )
                    self.application_manager.update_application_status(
                        app_id, ApplicationStatus.ERROR
                    )
            else:
                # Fallback: simulate restart process
                logger.warning("⚠️ No launch service available, simulating restart")
                self.application_manager.simulate_status_progression(
                    app_id, ApplicationStatus.STOPPING, ApplicationStatus.STARTING, 1000
                )
                QTimer.singleShot(2000, lambda: self.launch_application(app_id))

        except Exception as e:
            logger.error(f"❌ Error restarting application {app_id}: {e}")
            self.application_manager.update_application_status(
                app_id, ApplicationStatus.ERROR
            )

    def _show_process_info(self, app_id: str):
        """Show process information for running application."""
        app = self.application_manager.get_application_by_id(app_id)
        if app:
            logger.info(
                f"ℹ️ Process info for {app.title}: PID={app.process_id}, Status={app.status}"
            )
            # TODO: Show process info dialog

    def _show_app_properties(self, app_id: str):
        """Show application properties dialog."""
        app = self.application_manager.get_application_by_id(app_id)
        if app:
            logger.info(f"⚙️ Properties for {app.title}")
            # TODO: Show properties dialog

    def update_application_status(self, app_id: str, status: ApplicationStatus):
        """Update visual status of an application."""
        self.application_manager.update_application_status(app_id, status)

    def get_dock_geometry(self) -> WindowGeometry:
        """Get current dock geometry for state persistence."""
        return self.position_manager.get_dock_geometry(self)

    def _install_always_on_top(self):
        """Install topmost enforcement via Win32 API after window is shown."""
        # Install timer to periodically enforce topmost status
        self.topmost_timer = QTimer()
        self.topmost_timer.timeout.connect(self._enforce_topmost)
        self.topmost_timer.start(100)  # Check every 100ms

    def _enforce_topmost(self):
        """Periodically enforce topmost status."""
        try:
            if sys.platform.startswith("win") and self.isVisible():
                hwnd = int(self.winId())
                # Check if window is still topmost
                topmost_hwnd = ctypes.windll.user32.GetTopWindow(0)
                if topmost_hwnd != hwnd:
                    # Force back to topmost
                    SWP_NOMOVE = 0x0002
                    SWP_NOSIZE = 0x0001
                    SWP_NOACTIVATE = 0x0010
                    HWND_TOPMOST = -1
                    ctypes.windll.user32.SetWindowPos(
                        hwnd,
                        HWND_TOPMOST,
                        0,
                        0,
                        0,
                        0,
                        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE,
                    )
                    self.raise_()
        except Exception:
            pass  # Silently fail to avoid spam
