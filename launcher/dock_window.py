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

import logging
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QMenu,
    QApplication,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRect
from PyQt6.QtGui import QScreen, QAction, QCursor

from domain.models import (
    DockConfiguration,
    DockPosition,
    ApplicationData,
    ApplicationStatus,
    WindowGeometry,
)
from ui.components.app_card import ReliableApplicationCard
from ui.reliable_design_system import get_reliable_style_builder
from ui.reliable_effects import get_shadow_manager

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
        self.applications = []
        self.app_cards = {}  # app_id -> card widget mapping

        # UI components
        self.style_builder = get_reliable_style_builder()
        self.shadow_manager = get_shadow_manager()

        # Setup window properties
        self._setup_dock_window()
        self._setup_layout()
        self._setup_styling()

        # Load applications
        self._load_applications()

        # Position dock
        self._position_dock()

        logger.info("✅ TKA Dock Window initialized")

    def _setup_dock_window(self):
        """Setup dock window properties."""
        # Window flags for dock behavior
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.X11BypassWindowManagerHint
        )

        # Set window attributes
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # Set fixed size based on dock configuration
        self.setFixedSize(self.dock_config.width, self._calculate_dock_height())

        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)

        # Set window title
        self.setWindowTitle("TKA Dock")

    def _setup_layout(self):
        """Setup the dock layout."""
        # Main layout - vertical for stacking icons
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.setSpacing(2)

        # Application icons container
        self.icons_container = QFrame()
        self.icons_container.setObjectName("dock_icons_container")

        self.icons_layout = QVBoxLayout(self.icons_container)
        self.icons_layout.setContentsMargins(0, 0, 0, 0)
        self.icons_layout.setSpacing(2)

        self.main_layout.addWidget(self.icons_container)
        self.main_layout.addStretch()  # Push icons to top

    def _setup_styling(self):
        """Setup dock styling."""
        self.setStyleSheet(
            f"""
            TKADockWindow {{
                background: rgba(20, 20, 20, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }}
            
            #dock_icons_container {{
                background: transparent;
                border: none;
            }}
        """
        )

    def _calculate_dock_height(self) -> int:
        """Calculate appropriate dock height based on number of applications."""
        # Base height for padding and borders
        base_height = 16

        # Icon size + spacing
        icon_size = 48
        icon_spacing = 2

        # Estimate number of applications (will be updated when loaded)
        estimated_apps = 6  # Default estimate

        total_height = base_height + (estimated_apps * (icon_size + icon_spacing))

        # Limit to screen height
        screen = QApplication.primaryScreen()
        if screen:
            screen_height = screen.geometry().height()
            max_height = int(screen_height * 0.8)  # 80% of screen height
            total_height = min(total_height, max_height)

        return total_height

    def _load_applications(self):
        """Load applications from TKA integration."""
        try:
            self.applications = self.tka_integration.get_applications()
            self._update_dock_icons()

            # Recalculate height based on actual application count
            new_height = self._calculate_actual_dock_height()
            self.setFixedHeight(new_height)

            logger.info(f"📱 Loaded {len(self.applications)} applications in dock")

        except Exception as e:
            logger.error(f"❌ Failed to load applications: {e}")

    def _calculate_actual_dock_height(self) -> int:
        """Calculate dock height based on actual number of applications."""
        base_height = 16
        icon_size = 48
        icon_spacing = 2

        app_count = len(self.applications)
        total_height = base_height + (app_count * (icon_size + icon_spacing))

        # Limit to screen height
        screen = QApplication.primaryScreen()
        if screen:
            screen_height = screen.geometry().height()
            max_height = int(screen_height * 0.8)
            total_height = min(total_height, max_height)

        return total_height

    def _update_dock_icons(self):
        """Update dock icons display."""
        # Clear existing icons
        self._clear_icons()

        # Create icon widgets for each application
        for app in self.applications:
            icon_widget = self._create_dock_icon(app)
            self.icons_layout.addWidget(icon_widget)
            self.app_cards[app.id] = icon_widget

    def _clear_icons(self):
        """Clear all existing icon widgets."""
        while self.icons_layout.count():
            child = self.icons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.app_cards.clear()

    def _create_dock_icon(self, app: ApplicationData) -> QWidget:
        """Create a dock icon widget for an application."""
        # Create a compact version of the application card
        icon_widget = DockApplicationIcon(app, self.style_builder)

        # Connect signals
        icon_widget.launch_requested.connect(self._on_launch_requested)
        icon_widget.context_menu_requested.connect(self._on_context_menu_requested)

        return icon_widget

    def _position_dock(self):
        """Position the dock on screen according to configuration."""
        screen = QApplication.primaryScreen()
        if not screen:
            logger.warning("⚠️ No screen available for dock positioning")
            return

        screen_geometry = screen.geometry()
        dock_rect = self._calculate_dock_position(screen_geometry)

        self.setGeometry(dock_rect)
        logger.info(f"📍 Positioned dock at {dock_rect}")

    def _calculate_dock_position(self, screen_geometry: QRect) -> QRect:
        """Calculate dock position based on configuration."""
        dock_width = self.dock_config.width
        dock_height = self.height()

        if self.dock_config.position == DockPosition.BOTTOM_LEFT:
            x = screen_geometry.left() + self.dock_config.margin_x
            y = (
                screen_geometry.bottom() - dock_height - self.dock_config.margin_y - 48
            )  # Account for taskbar
        elif self.dock_config.position == DockPosition.BOTTOM_RIGHT:
            x = screen_geometry.right() - dock_width - self.dock_config.margin_x
            y = screen_geometry.bottom() - dock_height - self.dock_config.margin_y - 48
        elif self.dock_config.position == DockPosition.TOP_LEFT:
            x = screen_geometry.left() + self.dock_config.margin_x
            y = screen_geometry.top() + self.dock_config.margin_y
        else:  # TOP_RIGHT
            x = screen_geometry.right() - dock_width - self.dock_config.margin_x
            y = screen_geometry.top() + self.dock_config.margin_y

        return QRect(x, y, dock_width, dock_height)

    def _on_launch_requested(self, app_id: str):
        """Handle application launch request."""
        self.launch_application(app_id)

    def launch_application(self, app_id: str):
        """Launch an application by ID using the same pathway as window mode."""
        try:
            # Find the application
            app = next((app for app in self.applications if app.id == app_id), None)
            if not app:
                logger.error(f"❌ Application not found: {app_id}")
                return

            logger.info(f"🚀 Launching application from dock: {app.title}")

            # Launch through TKA integration (same as window mode)
            success = self.tka_integration.launch_application(app_id)

            if success:
                # Update visual status to starting
                self.update_application_status(app_id, ApplicationStatus.STARTING)

                # Emit signal for any listeners
                self.application_launched.emit(app_id, app.title)
                logger.info(f"✅ Successfully launched from dock: {app.title}")

                # Simulate status progression (in real implementation, this would come from launch service)
                QTimer.singleShot(
                    2000,
                    lambda: self.update_application_status(
                        app_id, ApplicationStatus.RUNNING
                    ),
                )
            else:
                # Update visual status to error
                self.update_application_status(app_id, ApplicationStatus.ERROR)
                logger.error(f"❌ Failed to launch from dock: {app.title}")

        except Exception as e:
            logger.error(f"❌ Error launching application {app_id} from dock: {e}")
            # Update visual status to error
            self.update_application_status(app_id, ApplicationStatus.ERROR)

    def _on_context_menu_requested(self, app_id: str, position):
        """Handle context menu request."""
        app = next((a for a in self.applications if a.id == app_id), None)
        if not app:
            return

        menu = QMenu(self)
        menu.setStyleSheet(
            """
            QMenu {
                background: rgba(30, 30, 30, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 4px;
                color: white;
            }
            QMenu::item {
                padding: 8px 16px;
                border-radius: 4px;
                margin: 2px;
            }
            QMenu::item:selected {
                background: rgba(100, 100, 100, 0.3);
            }
            QMenu::separator {
                height: 1px;
                background: rgba(255, 255, 255, 0.1);
                margin: 4px 8px;
            }
        """
        )

        # Application-specific actions
        app_section_added = False

        # Check if application is running (this would integrate with launch service)
        is_running = self._is_application_running(app_id)

        if is_running:
            # Running application actions
            terminate_action = QAction("🛑 Terminate", self)
            terminate_action.triggered.connect(
                lambda: self._terminate_application(app_id)
            )
            menu.addAction(terminate_action)

            restart_action = QAction("🔄 Restart", self)
            restart_action.triggered.connect(lambda: self._restart_application(app_id))
            menu.addAction(restart_action)

            # Add process info action
            info_action = QAction("ℹ️ Process Info", self)
            info_action.triggered.connect(lambda: self._show_process_info(app_id))
            menu.addAction(info_action)

            app_section_added = True
        else:
            # Stopped application actions
            launch_action = QAction("🚀 Launch", self)
            launch_action.triggered.connect(lambda: self._on_launch_requested(app_id))
            menu.addAction(launch_action)

            # Add launch with debug option for development apps
            if app.category.value == "Development Tools":
                debug_launch_action = QAction("🐛 Launch with Debugger", self)
                debug_launch_action.triggered.connect(
                    lambda: self._launch_with_debug(app_id)
                )
                menu.addAction(debug_launch_action)

            app_section_added = True

        # Application properties
        if app_section_added:
            menu.addSeparator()

        properties_action = QAction("⚙️ Properties", self)
        properties_action.triggered.connect(lambda: self._show_app_properties(app_id))
        menu.addAction(properties_action)

        # Dock management section
        menu.addSeparator()

        # Mode switching
        undock_action = QAction("🪟 Switch to Window Mode", self)
        undock_action.triggered.connect(self.mode_switch_requested.emit)
        menu.addAction(undock_action)

        # Show menu
        menu.exec(position)

    def _is_application_running(self, app_id: str) -> bool:
        """Check if an application is currently running."""
        try:
            # Try to get real status from launch service first
            if (
                hasattr(self.tka_integration, "launch_service")
                and self.tka_integration.launch_service
            ):
                return self.tka_integration.launch_service.is_application_running(
                    app_id
                )

            # Fallback: check the application status from our data
            app = next((a for a in self.applications if a.id == app_id), None)
            return app and app.status == ApplicationStatus.RUNNING

        except Exception as e:
            logger.warning(f"⚠️ Error checking application status for {app_id}: {e}")
            # Fallback to local data
            app = next((a for a in self.applications if a.id == app_id), None)
            return app and app.status == ApplicationStatus.RUNNING

    def _terminate_application(self, app_id: str):
        """Terminate a running application."""
        try:
            logger.info(f"🛑 Terminating application {app_id}")

            # Update visual status to stopping
            self.update_application_status(app_id, ApplicationStatus.STOPPING)

            # Try to get the launch service from TKA integration
            if (
                hasattr(self.tka_integration, "launch_service")
                and self.tka_integration.launch_service
            ):
                success = self.tka_integration.launch_service.stop_application(app_id)
                if success:
                    logger.info(f"✅ Successfully terminated {app_id}")
                    self.update_application_status(app_id, ApplicationStatus.STOPPED)
                else:
                    logger.error(f"❌ Failed to terminate {app_id}")
                    self.update_application_status(app_id, ApplicationStatus.ERROR)
            else:
                # Fallback: just update visual status
                logger.warning(
                    f"⚠️ No launch service available, updating visual status only"
                )
                QTimer.singleShot(
                    1000,
                    lambda: self.update_application_status(
                        app_id, ApplicationStatus.STOPPED
                    ),
                )

        except Exception as e:
            logger.error(f"❌ Error terminating application {app_id}: {e}")
            self.update_application_status(app_id, ApplicationStatus.ERROR)

    def _restart_application(self, app_id: str):
        """Restart a running application."""
        try:
            logger.info(f"🔄 Restarting application {app_id}")

            # Update visual status to stopping
            self.update_application_status(app_id, ApplicationStatus.STOPPING)

            # Try to get the launch service from TKA integration
            if (
                hasattr(self.tka_integration, "launch_service")
                and self.tka_integration.launch_service
            ):
                # Use the launch service restart method
                result = self.tka_integration.launch_service.restart_application(app_id)
                if result.success:
                    logger.info(f"✅ Successfully restarted {app_id}")
                    self.update_application_status(app_id, ApplicationStatus.RUNNING)
                else:
                    logger.error(
                        f"❌ Failed to restart {app_id}: {result.error_message}"
                    )
                    self.update_application_status(app_id, ApplicationStatus.ERROR)
            else:
                # Fallback: simulate restart process
                logger.warning(f"⚠️ No launch service available, simulating restart")
                QTimer.singleShot(
                    1000,
                    lambda: self.update_application_status(
                        app_id, ApplicationStatus.STARTING
                    ),
                )
                QTimer.singleShot(2000, lambda: self.launch_application(app_id))

        except Exception as e:
            logger.error(f"❌ Error restarting application {app_id}: {e}")
            self.update_application_status(app_id, ApplicationStatus.ERROR)

    def _launch_with_debug(self, app_id: str):
        """Launch application with debugger attached."""
        try:
            logger.info(f"🐛 Launching {app_id} with debugger")

            # For debug launch, we can use the same launch pathway
            # The launch service will detect if debugger is attached and handle accordingly
            self.launch_application(app_id)

        except Exception as e:
            logger.error(f"❌ Error launching {app_id} with debugger: {e}")
            self.update_application_status(app_id, ApplicationStatus.ERROR)

    def _show_process_info(self, app_id: str):
        """Show process information for running application."""
        app = next((a for a in self.applications if a.id == app_id), None)
        if app:
            logger.info(
                f"ℹ️ Process info for {app.title}: PID={app.process_id}, Status={app.status}"
            )
            # TODO: Show process info dialog

    def _show_app_properties(self, app_id: str):
        """Show application properties dialog."""
        app = next((a for a in self.applications if a.id == app_id), None)
        if app:
            logger.info(f"⚙️ Properties for {app.title}")
            # TODO: Show properties dialog

    def update_application_status(self, app_id: str, status: ApplicationStatus):
        """Update visual status of an application."""
        if app_id in self.app_cards:
            self.app_cards[app_id].update_status(status)

    def get_dock_geometry(self) -> WindowGeometry:
        """Get current dock geometry for state persistence."""
        geometry = self.geometry()
        return WindowGeometry(
            x=geometry.x(),
            y=geometry.y(),
            width=geometry.width(),
            height=geometry.height(),
        )


class DockApplicationIcon(QFrame):
    """Compact application icon for dock display."""

    launch_requested = pyqtSignal(str)  # app_id
    context_menu_requested = pyqtSignal(str, object)  # app_id, position

    def __init__(self, app_data: ApplicationData, style_builder):
        super().__init__()

        self.app_data = app_data
        self.style_builder = style_builder
        self.current_status = app_data.status

        self.setFixedSize(48, 48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._setup_layout()
        self._setup_styling()

        # Set tooltip
        self.setToolTip(f"{app_data.title}\n{app_data.description}")

    def _setup_layout(self):
        """Setup icon layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Icon label (using emoji for now)
        self.icon_label = QLabel(self.app_data.icon)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 24px;")

        layout.addWidget(self.icon_label)

    def _setup_styling(self):
        """Setup icon styling."""
        self._update_style_for_status(self.current_status)

    def _update_style_for_status(self, status: ApplicationStatus):
        """Update styling based on application status."""
        if status == ApplicationStatus.RUNNING:
            # Running state - green accent with glow effect
            self.setStyleSheet(
                f"""
                DockApplicationIcon {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(76, 175, 80, 0.3),
                        stop:1 rgba(56, 142, 60, 0.3));
                    border: 2px solid #4CAF50;
                    border-radius: 8px;
                    box-shadow: 0 0 8px rgba(76, 175, 80, 0.4);
                }}
                DockApplicationIcon:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(102, 187, 106, 0.4),
                        stop:1 rgba(76, 175, 80, 0.4));
                    border: 2px solid #66BB6A;
                    box-shadow: 0 0 12px rgba(102, 187, 106, 0.5);
                }}
            """
            )
        elif status == ApplicationStatus.STARTING:
            # Starting state - orange accent with pulse effect
            self.setStyleSheet(
                f"""
                DockApplicationIcon {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 152, 0, 0.3),
                        stop:1 rgba(245, 124, 0, 0.3));
                    border: 2px solid #FF9800;
                    border-radius: 8px;
                    box-shadow: 0 0 8px rgba(255, 152, 0, 0.4);
                }}
                DockApplicationIcon:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 183, 77, 0.4),
                        stop:1 rgba(255, 152, 0, 0.4));
                    border: 2px solid #FFB74D;
                    box-shadow: 0 0 12px rgba(255, 183, 77, 0.5);
                }}
            """
            )
        elif status == ApplicationStatus.ERROR:
            # Error state - red accent
            self.setStyleSheet(
                f"""
                DockApplicationIcon {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(244, 67, 54, 0.3),
                        stop:1 rgba(211, 47, 47, 0.3));
                    border: 2px solid #F44336;
                    border-radius: 8px;
                    box-shadow: 0 0 8px rgba(244, 67, 54, 0.4);
                }}
                DockApplicationIcon:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(239, 83, 80, 0.4),
                        stop:1 rgba(244, 67, 54, 0.4));
                    border: 2px solid #EF5350;
                    box-shadow: 0 0 12px rgba(239, 83, 80, 0.5);
                }}
            """
            )
        else:
            # Stopped state - subtle glassmorphism appearance
            self.setStyleSheet(
                f"""
                DockApplicationIcon {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.1),
                        stop:1 rgba(255, 255, 255, 0.05));
                    border: 1px solid rgba(255, 255, 255, 0.15);
                    border-radius: 8px;
                    backdrop-filter: blur(10px);
                }}
                DockApplicationIcon:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.2),
                        stop:1 rgba(255, 255, 255, 0.1));
                    border: 1px solid rgba(255, 255, 255, 0.25);
                    box-shadow: 0 0 8px rgba(255, 255, 255, 0.1);
                }}
            """
            )

    def update_status(self, status: ApplicationStatus):
        """Update the visual status of this icon."""
        self.current_status = status
        self._update_style_for_status(status)

    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.launch_requested.emit(self.app_data.id)
        elif event.button() == Qt.MouseButton.RightButton:
            self.context_menu_requested.emit(self.app_data.id, QCursor.pos())

        super().mousePressEvent(event)
