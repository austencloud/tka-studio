"""
Launcher Window Event Handlers
=============================

Handles all window events, user interactions, and business logic.
Keeps the main window class clean and focused.
"""

import logging
from typing import Optional, List
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QResizeEvent, QCloseEvent

from application_grid import ApplicationGridWidget
from launcher_config import LauncherConfig

logger = logging.getLogger(__name__)


class LauncherEventHandler(QObject):
    """Handles all launcher window events and user interactions."""

    # Signals for communication with main window
    status_update_requested = pyqtSignal(str)
    app_count_update_requested = pyqtSignal(int)
    notification_requested = pyqtSignal(str, str)  # message, type

    def __init__(self, config: LauncherConfig):
        super().__init__()
        self.config = config

        # References to components (set by main window)
        self.application_grid: Optional[ApplicationGridWidget] = None
        self.layout_manager = None

        # State tracking
        self.is_initializing = False
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._perform_search)

    def set_components(self, application_grid, layout_manager):
        """Set references to main components."""
        self.application_grid = application_grid
        self.layout_manager = layout_manager

        # Connect component signals
        self._connect_component_signals()

    def _connect_component_signals(self):
        """Connect signals from all components."""
        if self.application_grid:
            # Application grid events
            self.application_grid.application_launched.connect(
                self._on_application_launched
            )
            self.application_grid.selection_changed.connect(self._on_selection_changed)
            self.application_grid.applications_loaded.connect(
                self._on_applications_loaded
            )

        if self.layout_manager:
            # Search events
            search_box = self.layout_manager.get_search_box()
            if search_box:
                search_box.textChanged.connect(self._on_search_text_changed)
                search_box.returnPressed.connect(self._on_search_submitted)

            # Button events
            refresh_button = self.layout_manager.get_refresh_button()
            if refresh_button:
                refresh_button.clicked.connect(self._on_refresh_clicked)

            settings_button = self.layout_manager.get_settings_button()
            if settings_button:
                settings_button.clicked.connect(self._on_settings_clicked)

    def handle_window_initialization(self):
        """Handle window initialization sequence."""
        self.is_initializing = True
        self.status_update_requested.emit("Initializing launcher...")

        try:
            # Load applications
            if self.application_grid:
                self.application_grid.load_applications()

            self.status_update_requested.emit("Ready")
            self.notification_requested.emit(
                "Launcher initialized successfully", "success"
            )

        except Exception as e:
            logger.error(f"Failed to initialize launcher: {e}")
            self.status_update_requested.emit("Initialization failed")
            self.notification_requested.emit(f"Failed to initialize: {e}", "error")

        finally:
            self.is_initializing = False

    def handle_window_resize(self, event: QResizeEvent):
        """Handle window resize events."""
        if self.layout_manager and hasattr(self.layout_manager, "responsive_manager"):
            self.layout_manager.responsive_manager.adjust_layout(event.size())

    def handle_window_close(self, event: QCloseEvent):
        """Handle window close events."""
        try:
            # Save window state
            self._save_window_state()

            # Clean up resources
            self._cleanup_resources()

            self.status_update_requested.emit("Shutting down...")
            event.accept()

        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
            event.accept()  # Close anyway

    def _save_window_state(self):
        """Save current window state to config."""
        try:
            # Save search text, selected applications, etc.
            if self.layout_manager:
                search_box = self.layout_manager.get_search_box()
                if search_box:
                    self.config.set_value("last_search", search_box.text())

            # Save application grid state
            if self.application_grid:
                selected_apps = self.application_grid.get_selected_applications()
                self.config.set_value(
                    "selected_applications", [app.id for app in selected_apps]
                )

            self.config.save()

        except Exception as e:
            logger.warning(f"Failed to save window state: {e}")

    def _cleanup_resources(self):
        """Clean up resources before shutdown."""
        try:
            # Stop any running timers
            if self.search_timer.isActive():
                self.search_timer.stop()

            # Clean up application grid
            if self.application_grid:
                self.application_grid.cleanup()

        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")

    def _on_search_text_changed(self, text: str):
        """Handle search text changes with debouncing."""
        # Debounce search to avoid excessive filtering
        self.search_timer.stop()
        self.search_timer.start(300)  # 300ms delay
        self._pending_search_text = text

    def _perform_search(self):
        """Perform the actual search operation."""
        if not hasattr(self, "_pending_search_text"):
            return

        search_text = self._pending_search_text

        try:
            if self.application_grid:
                # Filter applications
                filtered_count = self.application_grid.filter_applications(search_text)

                # Update status
                if search_text.strip():
                    self.status_update_requested.emit(
                        f"Found {filtered_count} matching applications"
                    )
                else:
                    self.status_update_requested.emit("Ready")

        except Exception as e:
            logger.error(f"Search failed: {e}")
            self.notification_requested.emit(f"Search failed: {e}", "error")

    def _on_search_submitted(self):
        """Handle search submission (Enter key)."""
        if self.application_grid:
            # Launch first matching application if only one result
            visible_apps = self.application_grid.get_filtered_applications()
            if len(visible_apps) == 1:
                self.application_grid.launch_application(visible_apps[0].id)

    def _on_refresh_clicked(self):
        """Handle refresh button click."""
        try:
            self.status_update_requested.emit("Refreshing applications...")

            if self.application_grid:
                self.application_grid.refresh_applications()

            self.notification_requested.emit("Applications refreshed", "success")

        except Exception as e:
            logger.error(f"Refresh failed: {e}")
            self.notification_requested.emit(f"Refresh failed: {e}", "error")

    def _on_settings_clicked(self):
        """Handle settings button click."""
        try:
            # Open settings window or dialog
            self.notification_requested.emit(
                "Settings functionality coming soon", "info"
            )

        except Exception as e:
            logger.error(f"Failed to open settings: {e}")
            self.notification_requested.emit(f"Failed to open settings: {e}", "error")

    def _on_application_launched(self, app_id: str):
        """Handle application launch events."""
        try:
            self.status_update_requested.emit(f"Launching application: {app_id}")
            self.notification_requested.emit(f"Launched {app_id}", "success")

        except Exception as e:
            logger.error(f"Launch notification failed: {e}")

    def _on_selection_changed(self, selected_apps: List):
        """Handle application selection changes."""
        try:
            count = len(selected_apps)
            if count == 0:
                self.status_update_requested.emit("Ready")
            elif count == 1:
                app_name = (
                    selected_apps[0].title
                    if hasattr(selected_apps[0], "title")
                    else "application"
                )
                self.status_update_requested.emit(f"Selected: {app_name}")
            else:
                self.status_update_requested.emit(f"Selected {count} applications")

        except Exception as e:
            logger.warning(f"Selection change handling failed: {e}")

    def _on_applications_loaded(self, count: int):
        """Handle applications loaded event."""
        try:
            self.app_count_update_requested.emit(count)

            if count == 0:
                self.notification_requested.emit("No applications found", "warning")
            else:
                self.status_update_requested.emit("Ready")

        except Exception as e:
            logger.warning(f"Applications loaded handling failed: {e}")

    def restore_window_state(self):
        """Restore saved window state."""
        try:
            # Restore search text
            last_search = self.config.get_value("last_search", "")
            if last_search and self.layout_manager:
                search_box = self.layout_manager.get_search_box()
                if search_box:
                    search_box.setText(last_search)

            # Restore selected applications
            selected_app_ids = self.config.get_value("selected_applications", [])
            if selected_app_ids and self.application_grid:
                self.application_grid.select_applications(selected_app_ids)

        except Exception as e:
            logger.warning(f"Failed to restore window state: {e}")


class LauncherShortcutHandler(QObject):
    """Handles keyboard shortcuts and hotkeys."""

    def __init__(self, parent_widget: QWidget):
        super().__init__()
        self.parent_widget = parent_widget
        self._setup_shortcuts()

    def _setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        from PyQt6.QtGui import QShortcut, QKeySequence
        from PyQt6.QtCore import Qt

        try:
            # Ctrl+F - Focus search
            self.search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self.parent_widget)
            self.search_shortcut.activated.connect(self._focus_search)

            # Ctrl+R - Refresh
            self.refresh_shortcut = QShortcut(
                QKeySequence("Ctrl+R"), self.parent_widget
            )
            self.refresh_shortcut.activated.connect(self._refresh_applications)

            # Escape - Clear search
            self.escape_shortcut = QShortcut(
                QKeySequence(Qt.Key.Key_Escape), self.parent_widget
            )
            self.escape_shortcut.activated.connect(self._clear_search)

            # F11 - Toggle fullscreen
            self.fullscreen_shortcut = QShortcut(
                QKeySequence(Qt.Key.Key_F11), self.parent_widget
            )
            self.fullscreen_shortcut.activated.connect(self._toggle_fullscreen)

        except Exception as e:
            logger.warning(f"Failed to setup shortcuts: {e}")

    def _focus_search(self):
        """Focus the search box."""
        # This will be connected by the main window
        pass

    def _refresh_applications(self):
        """Refresh applications."""
        # This will be connected by the main window
        pass

    def _clear_search(self):
        """Clear search text."""
        # This will be connected by the main window
        pass

    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.parent_widget.isFullScreen():
            self.parent_widget.showNormal()
        else:
            self.parent_widget.showFullScreen()
