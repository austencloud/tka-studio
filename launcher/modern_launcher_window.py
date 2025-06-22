"""
TKA Modern Launcher Window - Simplified & Reliable
=================================================

The main launcher window built with the reliable design system.
This is a clean, focused implementation that coordinates all components.
"""

from typing import Optional
import logging
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import (
    QResizeEvent,
    QCloseEvent,
    QPaintEvent,
    QPainter,
    QLinearGradient,
    QColor,
)

from application_grid import ApplicationGridWidget
from launcher_config import LauncherConfig
from ui.window_layout import LauncherLayoutManager, ResponsiveLayoutManager
from ui.window_handlers import LauncherEventHandler, LauncherShortcutHandler
from ui.reliable_design_system import get_reliable_style_builder

logger = logging.getLogger(__name__)


class TKALauncherWindow(QWidget):
    """
    Simplified TKA Launcher Window

    Coordinates all components using the reliable design system.
    Clean, focused implementation without complex fallback logic.
    """

    # Signals
    application_launched = pyqtSignal(str)
    closing = pyqtSignal()

    def __init__(self, config: Optional[LauncherConfig] = None):
        super().__init__()

        # Initialize configuration
        self.config = config or LauncherConfig()
        self.style_builder = get_reliable_style_builder()

        # Initialize managers
        self.layout_manager = LauncherLayoutManager(self)
        self.responsive_manager = ResponsiveLayoutManager(self.layout_manager)
        self.event_handler = LauncherEventHandler(self.config)
        self.shortcut_handler = LauncherShortcutHandler(self)

        # Application grid
        self.application_grid = None
        # Setup window
        self._setup_window()
        self._setup_layout()
        self._setup_application_grid()
        self._setup_event_handling()
        self._setup_styling()

        # Connect managers
        self.layout_manager.responsive_manager = self.responsive_manager

        logger.info("🚀 TKA Launcher Window initialized successfully")

    def _setup_window(self):
        """Setup basic window properties."""
        self.setWindowTitle("TKA Launcher")
        self.setMinimumSize(800, 600)
        self.resize(1200, 800)

        # Window flags for modern appearance
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
        )

        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)

    def _setup_layout(self):
        """Setup the main window layout."""
        self.layout_manager.setup_main_layout()

    def _setup_application_grid(self):
        """Setup the application grid component."""
        try:
            self.application_grid = ApplicationGridWidget(self.config)
            self.layout_manager.add_application_grid(self.application_grid)

        except Exception as e:
            logger.error(f"Failed to setup application grid: {e}")
            self.layout_manager.show_notification(
                f"Failed to load applications: {e}", "error"
            )

    def _setup_event_handling(self):
        """Setup event handling and connect signals."""
        # Set component references in event handler
        self.event_handler.set_components(self.application_grid, self.layout_manager)

        # Connect event handler signals
        self.event_handler.status_update_requested.connect(
            self.layout_manager.update_status
        )
        self.event_handler.app_count_update_requested.connect(
            self.layout_manager.update_app_count
        )
        self.event_handler.notification_requested.connect(
            self.layout_manager.show_notification
        )

        # Connect application grid signals
        if self.application_grid:
            self.application_grid.application_launched.connect(
                self.application_launched.emit
            )

        # Connect shortcut handler
        self._connect_shortcuts()

        # Initialize window state
        self.event_handler.handle_window_initialization()

    def _connect_shortcuts(self):
        """Connect keyboard shortcuts to actions."""
        try:
            # Focus search shortcut
            self.shortcut_handler._focus_search = self._focus_search
            self.shortcut_handler._refresh_applications = self._refresh_applications
            self.shortcut_handler._clear_search = self._clear_search

        except Exception as e:
            logger.warning(f"Failed to connect shortcuts: {e}")

    def _setup_styling(self):
        """Setup window styling with reliable design system."""
        # Create gradient background
        self.setStyleSheet(
            f"""
            TKALauncherWindow {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0f172a,
                    stop: 0.5 #1e293b,
                    stop: 1 #334155
                );
            }}
        """
        )

    def _focus_search(self):
        """Focus the search box."""
        search_box = self.layout_manager.get_search_box()
        if search_box:
            search_box.setFocus()
            search_box.selectAll()

    def _refresh_applications(self):
        """Refresh applications."""
        if self.application_grid:
            self.application_grid.refresh_applications()

    def _clear_search(self):
        """Clear search text."""
        search_box = self.layout_manager.get_search_box()
        if search_box:
            search_box.clear()

    def resizeEvent(self, event: QResizeEvent):
        """Handle window resize events."""
        super().resizeEvent(event)
        self.event_handler.handle_window_resize(event)

    def closeEvent(self, event: QCloseEvent):
        """Handle window close events."""
        self.closing.emit()
        self.event_handler.handle_window_close(event)

    def paintEvent(self, event: QPaintEvent):
        """Custom paint event for gradient background."""
        painter = QPainter(self)

        # Create gradient background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(15, 23, 42))  # slate-900
        gradient.setColorAt(0.5, QColor(30, 41, 59))  # slate-800
        gradient.setColorAt(1, QColor(51, 65, 85))  # slate-700

        painter.fillRect(self.rect(), gradient)
        painter.end()

    def show_notification(self, message: str, notification_type: str = "info"):
        """Show a notification."""
        self.layout_manager.show_notification(message, notification_type)

    def launch_application(self, app_id: str):
        """Launch an application by ID."""
        if self.application_grid:
            self.application_grid.launch_application(app_id)

    def get_selected_applications(self):
        """Get currently selected applications."""
        if self.application_grid:
            return self.application_grid.get_selected_applications()
        return []

    def filter_applications(self, search_text: str):
        """Filter applications by search text."""
        if self.application_grid:
            return self.application_grid.filter_applications(search_text)
        return 0

    def restore_state(self):
        """Restore saved window state."""
        try:
            # Restore window geometry
            geometry = self.config.get_value("window_geometry")
            if geometry:
                self.restoreGeometry(geometry)

            # Restore other state
            self.event_handler.restore_window_state()

        except Exception as e:
            logger.warning(f"Failed to restore window state: {e}")

    def save_state(self):
        """Save current window state."""
        try:
            # Save window geometry
            self.config.set_value("window_geometry", self.saveGeometry())
            self.config.save()

        except Exception as e:
            logger.warning(f"Failed to save window state: {e}")


def create_launcher_window(
    config: Optional[LauncherConfig] = None,
) -> TKALauncherWindow:
    """
    Factory function to create a launcher window.

    Args:
        config: Optional launcher configuration

    Returns:
        Configured TKALauncherWindow instance
    """
    try:
        window = TKALauncherWindow(config)

        # Restore saved state
        window.restore_state()

        return window

    except Exception as e:
        logger.error(f"Failed to create launcher window: {e}")
        raise


# Convenience function for quick testing
def show_launcher(config: Optional[LauncherConfig] = None):
    """Quick function to show the launcher for testing."""
    import sys

    app = QApplication(sys.argv if len(sys.argv) > 1 else ["launcher"])

    try:
        window = create_launcher_window(config)
        window.show()

        # Show welcome notification
        window.show_notification("Welcome to TKA Launcher!", "success")

        sys.exit(app.exec())

    except Exception as e:
        logger.error(f"Failed to show launcher: {e}")
        sys.exit(1)


if __name__ == "__main__":
    show_launcher()
