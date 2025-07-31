#!/usr/bin/env python3
"""
TKA Dock Context Menu Manager - Context Menu Logic
=================================================

Manages context menu functionality for dock applications including:
- Application-specific actions (launch, stop, restart)
- Process management options
- Dock configuration and mode switching
- Application properties and information

Architecture:
- Extracted from dock_window.py for better separation of concerns
- Centralized context menu logic
- Clean interface with main dock window
"""

import logging

from domain.models import ApplicationData, ApplicationStatus
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu

logger = logging.getLogger(__name__)


class DockContextMenuManager(QObject):
    """Manages context menu creation and actions for dock applications."""

    # Signals for actions that need to be handled by the dock window
    launch_requested = pyqtSignal(str)  # app_id
    stop_requested = pyqtSignal(str)  # app_id
    restart_requested = pyqtSignal(str)  # app_id
    process_info_requested = pyqtSignal(str)  # app_id
    properties_requested = pyqtSignal(str)  # app_id
    mode_switch_requested = pyqtSignal()  # Switch to window mode

    def __init__(self, parent=None):
        super().__init__(parent)

    def create_context_menu(
        self, app_id: str, applications: list[ApplicationData], position
    ) -> QMenu:
        """Create and show context menu for an application."""
        # Find the application
        app = next((a for a in applications if a.id == app_id), None)
        if not app:
            logger.warning(f"⚠️ Application not found for context menu: {app_id}")
            return None

        # Create menu
        menu = QMenu()
        menu.setStyleSheet(self._get_menu_stylesheet())

        # Application title header
        title_action = QAction(f"📱 {app.title}", menu)
        title_action.setEnabled(False)
        menu.addAction(title_action)
        menu.addSeparator()

        # Application actions based on status
        self._add_application_actions(menu, app)

        # Process management section (if running)
        if app.status == ApplicationStatus.RUNNING:
            menu.addSeparator()
            self._add_process_actions(menu, app_id)

        # Application information section
        menu.addSeparator()
        self._add_info_actions(menu, app_id)

        # Dock management section
        menu.addSeparator()
        self._add_dock_actions(menu)

        return menu

    def _add_application_actions(self, menu: QMenu, app: ApplicationData):
        """Add application-specific actions to menu."""
        if app.status == ApplicationStatus.STOPPED:
            # Launch action
            launch_action = QAction("🚀 Launch", menu)
            launch_action.triggered.connect(lambda: self.launch_requested.emit(app.id))
            menu.addAction(launch_action)

        elif app.status == ApplicationStatus.RUNNING:
            # Stop action
            stop_action = QAction("⏹️ Stop", menu)
            stop_action.triggered.connect(lambda: self.stop_requested.emit(app.id))
            menu.addAction(stop_action)

            # Restart action
            restart_action = QAction("🔄 Restart", menu)
            restart_action.triggered.connect(
                lambda: self.restart_requested.emit(app.id)
            )
            menu.addAction(restart_action)

        elif app.status == ApplicationStatus.STARTING:
            # Starting - show status
            starting_action = QAction("⏳ Starting...", menu)
            starting_action.setEnabled(False)
            menu.addAction(starting_action)

        elif app.status == ApplicationStatus.ERROR:
            # Error - allow retry
            retry_action = QAction("🔄 Retry Launch", menu)
            retry_action.triggered.connect(lambda: self.launch_requested.emit(app.id))
            menu.addAction(retry_action)

    def _add_process_actions(self, menu: QMenu, app_id: str):
        """Add process management actions to menu."""
        process_info_action = QAction("ℹ️ Process Info", menu)
        process_info_action.triggered.connect(
            lambda: self.process_info_requested.emit(app_id)
        )
        menu.addAction(process_info_action)

    def _add_info_actions(self, menu: QMenu, app_id: str):
        """Add application information actions to menu."""
        properties_action = QAction("⚙️ Properties", menu)
        properties_action.triggered.connect(
            lambda: self.properties_requested.emit(app_id)
        )
        menu.addAction(properties_action)

    def _add_dock_actions(self, menu: QMenu):
        """Add dock management actions to menu."""
        # Mode switching
        undock_action = QAction("🪟 Switch to Window Mode", menu)
        undock_action.triggered.connect(self.mode_switch_requested.emit)
        menu.addAction(undock_action)

    def _get_menu_stylesheet(self) -> str:
        """Get stylesheet for context menu."""
        return """
            QMenu {
                background: rgba(20, 20, 20, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 4px;
                color: white;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 12px;
            }

            QMenu::item {
                background: transparent;
                padding: 6px 12px;
                border-radius: 4px;
                margin: 1px;
            }

            QMenu::item:selected {
                background: rgba(255, 255, 255, 0.1);
            }

            QMenu::item:disabled {
                color: rgba(255, 255, 255, 0.5);
            }

            QMenu::separator {
                height: 1px;
                background: rgba(255, 255, 255, 0.1);
                margin: 4px 8px;
            }
        """

    def show_context_menu(
        self, app_id: str, applications: list[ApplicationData], position
    ):
        """Create and show context menu at the specified position."""
        menu = self.create_context_menu(app_id, applications, position)
        if menu:
            menu.exec(position)
            return True
        return False
