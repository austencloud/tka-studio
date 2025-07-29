"""
Qt Application Manager for TKA Application

Handles Qt-specific application lifecycle, event loop management, and Qt setup.
Extracted from main.py to follow Single Responsibility Principle.

This class centralizes all Qt-related concerns including:
- QApplication creation and configuration
- Qt message handler installation
- Screen detection and multi-monitor support
- Qt event loop management
- Qt-specific application properties
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from PyQt6.QtGui import QGuiApplication, QIcon, QScreen
from PyQt6.QtWidgets import QApplication

from desktop.modern.core.error_handling import ErrorSeverity, StandardErrorHandler

from .configuration_manager import ApplicationConfiguration


class QtApplicationManager:
    """
    Manages Qt-specific application lifecycle and configuration.

    Provides centralized Qt application management to replace scattered
    Qt setup code throughout main.py.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._app: Optional[QApplication] = None
        self._target_screen: Optional[QScreen] = None

    def create_qt_application(self, config: ApplicationConfiguration) -> QApplication:
        """
        Create and configure Qt application instance.

        Args:
            config: Application configuration

        Returns:
            QApplication: Configured Qt application instance

        Raises:
            QtApplicationError: If Qt application creation fails
        """
        try:
            # Check if QApplication already exists
            self._app = QApplication.instance()
            if not self._app:
                self._app = QApplication(sys.argv)
                self.logger.debug("✅ Created new QApplication instance")
            else:
                self.logger.debug("✅ Using existing QApplication instance")

            # Configure Qt application
            self._configure_qt_application()

            # Set up application icon
            self._setup_application_icon()

            # Detect target screen for display
            self._target_screen = self._detect_target_screen(config)

            return self._app

        except Exception as e:
            StandardErrorHandler.handle_initialization_error(
                "Qt application creation",
                e,
                self.logger,
                is_critical=True,
                suggested_action="Check Qt installation and display configuration",
            )
            raise

    def run_event_loop(self) -> int:
        """
        Run the Qt event loop.

        Returns:
            int: Application exit code
        """
        if not self._app:
            raise RuntimeError(
                "Qt application not created - call create_qt_application() first"
            )

        try:
            self.logger.info("🚀 Starting Qt event loop...")
            return self._app.exec()
        except Exception as e:
            StandardErrorHandler.handle_service_error(
                "Qt event loop execution", e, self.logger, ErrorSeverity.CRITICAL
            )
            return 1

    def _configure_qt_application(self) -> None:
        """Configure Qt application properties and settings."""
        try:
            # Set Qt style
            self._app.setStyle("Fusion")

            # Set application metadata
            self._app.setApplicationName("TKA Modern")
            self._app.setApplicationVersion("4.0.0")
            self._app.setOrganizationName("The Kinetic Constructor")

            self.logger.debug("✅ Qt application configured successfully")

        except Exception as e:
            self.logger.warning(f"Failed to configure Qt application: {e}")

    def _setup_application_icon(self) -> None:
        """Set up the application icon if available."""
        try:
            icon_path = (
                Path(__file__).parent.parent.parent
                / "images"
                / "icons"
                / "app_icon.png"
            )
            if icon_path.exists():
                self._app.setWindowIcon(QIcon(str(icon_path)))
                self.logger.debug(f"✅ Application icon set: {icon_path}")
            else:
                self.logger.debug("⚠️ Application icon not found, using default")

        except Exception as e:
            self.logger.warning(f"Failed to set application icon: {e}")

    def _detect_target_screen(
        self, config: ApplicationConfiguration
    ) -> Optional[QScreen]:
        """
        Detect target screen based on configuration.

        Args:
            config: Application configuration

        Returns:
            QScreen: Target screen for application display
        """
        try:
            screens = QGuiApplication.screens()

            # Default behavior: use secondary screen if available, otherwise primary
            target_screen = (
                screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
            )
            self.logger.debug(f"✅ Using default screen: {target_screen.name()}")
            return target_screen

        except Exception as e:
            self.logger.warning(f"Failed to detect target screen: {e}")
            return QGuiApplication.primaryScreen()
