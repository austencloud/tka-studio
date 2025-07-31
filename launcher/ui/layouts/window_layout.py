"""
Launcher Window Layout Manager
=============================

Manages the layout and positioning of all launcher window components.
Handles responsive design and component arrangement.
"""

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)
from ui.components import ReliableButton, ReliableSearchBox
from ui.launcher_components import (
    LauncherHeader,
    LauncherNotification,
    LauncherStatusBar,
)
from ui.pyqt6_compatible_design_system import get_reliable_style_builder
from ui.reliable_effects import get_shadow_manager


class LauncherLayoutManager:
    """Manages the layout of all launcher components."""

    def __init__(self, parent_widget: QWidget):
        self.parent_widget = parent_widget
        self.style_builder = get_reliable_style_builder()
        self.shadow_manager = get_shadow_manager()

        # Layout components
        self.main_layout = None
        self.header_section = None
        self.search_section = None
        self.content_section = None
        self.status_section = None

        # Notification system
        self.notification_area = None
        self.active_notifications = []

    def setup_main_layout(self) -> QVBoxLayout:
        """Setup the main window layout."""
        self.main_layout = QVBoxLayout(self.parent_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Add sections in order
        self._create_header_section()
        self._create_search_section()
        self._create_content_section()
        self._create_status_section()

        return self.main_layout

    def _create_header_section(self):
        """Create and add header section."""
        self.header_section = LauncherHeader()
        self.main_layout.addWidget(self.header_section)

    def _create_search_section(self):
        """Create and add search section."""
        search_container = QFrame()
        search_container.setStyleSheet(
            f"""
            QFrame {{
                background: transparent;
                border: none;
                padding: {self.style_builder.tokens.SPACING["md"]}px;
            }}
        """
        )

        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(24, 16, 24, 16)
        search_layout.setSpacing(16)

        # Search box
        self.search_box = ReliableSearchBox("Search applications...")
        self.search_box.setFixedWidth(400)
        search_layout.addWidget(self.search_box)

        search_layout.addStretch()

        # Refresh button
        self.refresh_button = ReliableButton("Refresh", "secondary")
        search_layout.addWidget(self.refresh_button)

        # Settings button
        self.settings_button = ReliableButton("Settings", "secondary")
        search_layout.addWidget(self.settings_button)

        self.search_section = search_container
        self.main_layout.addWidget(self.search_section)

    def _create_content_section(self):
        """Create and add main content section."""
        content_container = QFrame()
        content_container.setStyleSheet(
            """
            QFrame {
                background: transparent;
                border: none;
            }
        """
        )

        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(24, 0, 24, 16)
        content_layout.setSpacing(16)

        # Application grid will be added here by the main window
        self.content_layout = content_layout

        # Create notification area overlay
        self._create_notification_area(content_container)

        self.content_section = content_container
        self.main_layout.addWidget(self.content_section, 1)  # Stretch to fill

    def _create_notification_area(self, parent):
        """Create floating notification area."""
        self.notification_area = QFrame(parent)
        self.notification_area.setStyleSheet(
            """
            QFrame {
                background: transparent;
                border: none;
            }
        """
        )

        notification_layout = QVBoxLayout(self.notification_area)
        notification_layout.setContentsMargins(0, 16, 0, 0)
        notification_layout.setSpacing(8)
        notification_layout.addStretch()  # Push notifications to top

        # Position overlay at top-right
        self.notification_area.setFixedWidth(350)
        self.notification_area.move(parent.width() - 370, 20)

    def _create_status_section(self):
        """Create and add status section."""
        status_container = QFrame()
        status_container.setStyleSheet(
            """
            QFrame {
                background: transparent;
                border: none;
                padding: 16px 24px;
            }
        """
        )

        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(24, 8, 24, 16)

        # Status bar
        self.status_bar = LauncherStatusBar()
        status_layout.addWidget(self.status_bar)

        self.status_section = status_container
        self.main_layout.addWidget(self.status_section)

    def add_application_grid(self, grid_widget):
        """Add the application grid to the content section."""
        self.content_layout.addWidget(grid_widget)

    def show_notification(self, message: str, notification_type: str = "info"):
        """Show a notification in the notification area."""
        notification = LauncherNotification(message, notification_type)
        notification.dismissed.connect(lambda: self._remove_notification(notification))

        # Add to notification area
        layout = self.notification_area.layout()
        layout.insertWidget(layout.count() - 1, notification)  # Insert before stretch

        # Show with animation
        notification.show_with_animation()

        # Track active notifications
        self.active_notifications.append(notification)

        # Limit number of visible notifications
        if len(self.active_notifications) > 3:
            oldest = self.active_notifications.pop(0)
            oldest.dismiss_with_animation()

    def _remove_notification(self, notification):
        """Remove notification from tracking."""
        if notification in self.active_notifications:
            self.active_notifications.remove(notification)

    def update_status(self, status: str):
        """Update status bar text."""
        if self.status_bar:
            self.status_bar.update_status(status)

    def update_app_count(self, count: int):
        """Update application count in status bar."""
        if self.status_bar:
            self.status_bar.update_app_count(count)

    def get_search_box(self) -> ReliableSearchBox:
        """Get the search box component."""
        return self.search_box

    def get_refresh_button(self) -> ReliableButton:
        """Get the refresh button component."""
        return self.refresh_button

    def get_settings_button(self) -> ReliableButton:
        """Get the settings button component."""
        return self.settings_button

    def resize_notification_area(self, parent_size: QSize):
        """Resize notification area based on parent size."""
        if self.notification_area:
            self.notification_area.move(parent_size.width() - 370, 20)


class ResponsiveLayoutManager:
    """Handles responsive layout adjustments."""

    def __init__(self, layout_manager: LauncherLayoutManager):
        self.layout_manager = layout_manager
        self.breakpoints = {"mobile": 600, "tablet": 900, "desktop": 1200}

    def adjust_layout(self, window_size: QSize):
        """Adjust layout based on window size."""
        width = window_size.width()

        if width <= self.breakpoints["mobile"]:
            self._apply_mobile_layout()
        elif width <= self.breakpoints["tablet"]:
            self._apply_tablet_layout()
        else:
            self._apply_desktop_layout()

        # Adjust notification area
        self.layout_manager.resize_notification_area(window_size)

    def _apply_mobile_layout(self):
        """Apply mobile-optimized layout."""
        # Stack elements vertically
        if self.layout_manager.search_box:
            self.layout_manager.search_box.setFixedWidth(280)

    def _apply_tablet_layout(self):
        """Apply tablet-optimized layout."""
        if self.layout_manager.search_box:
            self.layout_manager.search_box.setFixedWidth(350)

    def _apply_desktop_layout(self):
        """Apply desktop-optimized layout."""
        if self.layout_manager.search_box:
            self.layout_manager.search_box.setFixedWidth(400)
