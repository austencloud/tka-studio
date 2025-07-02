#!/usr/bin/env python3
"""
TKA Modern Launcher - Premium Application Launcher
==================================================

A premium, modern application launcher for The Kinetic Constructor (TKA) built with
pure PyQt6 and custom glassmorphism design. Features dual-mode operation, smooth
animations, and seamless TKA integration.

Architecture:
- Clean separation of concerns
- Pure PyQt6 with custom styling
- TKA dependency injection integration
- Modern responsive design patterns
- Glassmorphism effects and micro-animations

Author: TKA Development Team
Version: 4.0.0 (Pure PyQt6 Rewrite)
"""

import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TKAModernLauncherApp:
    """
    Main application class for TKA Modern Launcher.

    Responsibilities:
    - Application lifecycle management
    - Modern theme and styling setup
    - Error handling and recovery
    - Clean shutdown procedures
    """

    def __init__(self, argv):
        """Initialize the launcher application."""
        logger.info("🚀 Initializing TKA Modern Launcher...")

        # Create QApplication
        self.app = QApplication(argv)
        self.app.setApplicationName("TKA Modern Launcher")
        self.app.setApplicationVersion("4.0.0")
        self.app.setOrganizationName("The Kinetic Constructor")

        # Setup application properties for high DPI displays
        # Note: In PyQt6, high DPI scaling is enabled by default

        # Initialize components
        self.main_window = None
        self.tka_integration = None

        # Setup modern theme and styling
        self._setup_modern_theme()

        # Setup error handling
        self._setup_error_handling()

        logger.info("✅ TKA Modern Launcher initialized successfully")

    def _setup_modern_theme(self):
        """Setup the modern glassmorphism theme."""
        try:
            # Set Inter font family for modern typography
            font = QFont("Inter", 10)
            font.setStyleHint(QFont.StyleHint.SansSerif)
            self.app.setFont(font)

            # Apply modern dark theme via application-wide stylesheet
            self.app.setStyleSheet(self._get_modern_stylesheet())

            logger.info("🎨 Applied modern glassmorphism theme with Inter typography")

        except Exception as e:
            logger.warning(f"⚠️ Theme setup failed, using defaults: {e}")

    def _get_modern_stylesheet(self):
        """Get the modern glassmorphism stylesheet."""
        return """
        QApplication {
            background-color: #0f0f0f;
            color: #ffffff;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }

        /* Modern glassmorphism base styling */
        QWidget {
            background-color: transparent;
            color: #ffffff;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
        """

    def _setup_error_handling(self):
        """Setup global error handling."""

        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            logger.error(
                "💥 Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
            )

        sys.excepthook = handle_exception

    def initialize(self):
        """Initialize the launcher components."""
        try:
            # Import here to avoid circular imports
            from ui.windows.launcher_window import TKALauncherWindow
            from integration.tka_integration import TKAIntegrationService

            # Initialize TKA integration
            logger.info("🔗 Initializing TKA integration...")
            self.tka_integration = TKAIntegrationService()

            # Create main window
            logger.info("🪟 Creating main launcher window...")
            self.main_window = TKALauncherWindow(self.tka_integration)

            # Connect cleanup signals
            self.app.aboutToQuit.connect(self._cleanup)

            logger.info("✅ Launcher initialization complete")
            return True

        except ImportError as e:
            logger.error(f"❌ Failed to import launcher components: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to initialize launcher: {e}")
            return False

    def run(self):
        """Run the launcher application."""
        try:
            if not self.initialize():
                logger.error("❌ Launcher initialization failed")
                return 1

            # Check if we should start in docked mode
            self._setup_initial_mode()

            logger.info("🎯 TKA Fluent Launcher is ready!")

            # Start the event loop
            return self.app.exec()

        except Exception as e:
            logger.error(f"💥 Fatal error in launcher: {e}")
            return 1

    def _setup_initial_mode(self):
        """Setup the initial display mode based on saved preferences."""
        try:
            # Check the mode manager's current mode (which was set based on TKA settings)
            current_mode = self.main_window.mode_manager.current_mode
            
            if current_mode == "docked":
                logger.info("🔄 Starting in docked mode based on saved preferences")
                # Switch to dock mode immediately
                self.main_window.mode_manager.switch_to_dock_mode()
            else:
                logger.info("🪟 Starting in window mode")
                # Show the main window
                self.main_window.show()
                # Center the window on screen  
                self._center_window()
                
        except Exception as e:
            logger.warning(f"⚠️ Failed to setup initial mode, defaulting to window: {e}")
            # Fallback to window mode
            self.main_window.show()
            self._center_window()

    def _center_window(self):
        """Center the main window on the screen."""
        if self.main_window:
            screen = self.app.primaryScreen().geometry()
            window = self.main_window.geometry()

            x = (screen.width() - window.width()) // 2
            y = (screen.height() - window.height()) // 2

            self.main_window.move(x, y)

    def _cleanup(self):
        """Cleanup resources on application exit."""
        logger.info("🧹 Cleaning up launcher resources...")

        try:
            if self.tka_integration:
                self.tka_integration.cleanup()

            if self.main_window:
                self.main_window.cleanup()

        except Exception as e:
            logger.warning(f"⚠️ Cleanup warning: {e}")

        logger.info("👋 TKA Fluent Launcher shutdown complete")


def main():
    """Main entry point for TKA Modern Launcher."""
    try:
        # Create and run the launcher
        launcher = TKAModernLauncherApp(sys.argv)
        exit_code = launcher.run()

        return exit_code

    except KeyboardInterrupt:
        logger.info("⏹️ Launcher interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"💥 Fatal launcher error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
