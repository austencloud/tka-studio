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

import logging
import os
import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

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
        print("📋 Initializing TKA Modern Launcher...")
        logger.info("Initializing TKA Modern Launcher...")

        self.app = QApplication(argv)
        print("✅ QApplication created")

        self.app.setApplicationName("TKA Modern Launcher")
        self.app.setApplicationVersion("4.0.0")
        self.app.setOrganizationName("The Kinetic Constructor")
        print("✅ QApplication configured")

        self.main_window = None
        self.tka_integration = None

        print("🎨 Setting up modern theme...")
        self._setup_modern_theme()
        print("✅ Modern theme setup complete")

        print("⚠️ Setting up error handling...")
        self._setup_error_handling()
        print("✅ Error handling setup complete")

        print("🎉 TKA Modern Launcher initialization complete")

    def debug_window_state(self, label="Window State"):
        """Debug helper to print current window state."""
        if self.main_window:
            print(f"🔍 {label}:")
            print(f"   Visible: {self.main_window.isVisible()}")
            print(f"   Size: {self.main_window.size()}")
            print(f"   Position: {self.main_window.pos()}")
            print(f"   Active: {self.main_window.isActiveWindow()}")
            print(f"   Enabled: {self.main_window.isEnabled()}")
        else:
            print(f"🔍 {label}: main_window is None")

    def _setup_modern_theme(self):
        """Setup the modern glassmorphism theme."""
        try:
            font = QFont("Inter", 10)
            font.setStyleHint(QFont.StyleHint.SansSerif)
            self.app.setFont(font)
            self.app.setStyleSheet(self._get_modern_stylesheet())
        except Exception as e:
            logger.warning(f"Theme setup failed, using defaults: {e}")

    def _get_modern_stylesheet(self):
        """Get the modern glassmorphism stylesheet."""
        return """
        QApplication {
            background-color: #0f0f0f;
            color: #ffffff;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
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
                "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
            )

        sys.excepthook = handle_exception

    def initialize(self):
        """Initialize the launcher components."""
        print("🛠️ Initializing launcher components...")
        try:
            print("📦 Importing launcher components...")
            from integration.tka_integration import TKAIntegrationService
            from ui.windows.launcher_window import TKALauncherWindow

            print("✅ Launcher components imported successfully")

            print("🔗 Creating TKA integration service...")
            self.tka_integration = TKAIntegrationService()
            print("✅ TKA integration service created")

            print("📺 Creating main launcher window...")
            self.main_window = TKALauncherWindow(self.tka_integration)
            print("✅ Main launcher window created")

            print("🗗️ Setting up cleanup handler...")
            self.app.aboutToQuit.connect(self._cleanup)
            print("✅ Cleanup handler connected")

            print("🎉 Launcher initialization successful!")
            return True

        except ImportError as e:
            print(f"❌ Failed to import launcher components: {e}")
            logger.error(f"Failed to import launcher components: {e}")
            import traceback

            traceback.print_exc()
            return False
        except Exception as e:
            print(f"❌ Failed to initialize launcher: {e}")
            logger.error(f"Failed to initialize launcher: {e}")
            import traceback

            traceback.print_exc()
            return False

    def run(self):
        """Run the launcher application."""
        print("🏃 Starting launcher run sequence...")
        try:
            print("📋 Initializing launcher...")
            if not self.initialize():
                print("❌ Launcher initialization failed")
                logger.error("Launcher initialization failed")
                return 1

            print("✅ Launcher initialized successfully")
            print("🎨 Setting up initial display mode...")
            self._setup_initial_mode()
            print("✅ Initial mode setup complete")

            print("📋 Starting Qt event loop...")
            result = self.app.exec()
            print(f"🏁 Qt event loop finished with result: {result}")
            return result

        except Exception as e:
            print(f"❌ Fatal error in launcher run: {e}")
            logger.error(f"Fatal error in launcher: {e}")
            import traceback

            traceback.print_exc()
            return 1

    def _setup_initial_mode(self):
        """Setup the initial display mode based on saved preferences."""
        try:
            current_mode = self.main_window.mode_manager.current_mode
            logger.info(f"🚀 Setting up initial mode: {current_mode}")
            if current_mode == "docked":
                logger.info("📌 Switching to dock mode")
                self.main_window.mode_manager.switch_to_dock_mode()
            else:
                logger.info("🪟 Showing window mode")
                self.main_window.show()
                self.main_window.raise_()  # Bring to front
                self.main_window.activateWindow()  # Make it active
                self._center_window()
                logger.info("✅ Window should now be visible and active")
        except Exception as e:
            logger.warning(f"Failed to setup initial mode, defaulting to window: {e}")
            logger.info("🪟 Fallback: Showing window mode")
            self.main_window.show()
            self.main_window.raise_()  # Bring to front
            self.main_window.activateWindow()  # Make it active
            self._center_window()
            logger.info("✅ Fallback window should now be visible and active")

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
        try:
            if self.tka_integration:
                self.tka_integration.cleanup()
            if self.main_window:
                self.main_window.cleanup()
        except Exception as e:
            logger.warning(f"Cleanup warning: {e}")


def main():
    """Main entry point for TKA Modern Launcher."""
    try:
        print("=" * 60)
        print("🚀 TKA MODERN LAUNCHER MAIN.PY STARTING")
        print("=" * 60)
        print(f"📁 Working directory: {os.getcwd()}")
        print(f"🐍 Python version: {sys.version}")
        print(f"📦 Python path: {sys.path[:3]}...")  # First 3 entries
        print(f"📄 Script file: {__file__}")

        logger.info("🚀 TKA Modern Launcher starting...")

        # Test PyQt6 import first
        print("🧪 Testing PyQt6 import...")
        from PyQt6.QtWidgets import QApplication

        print("✅ PyQt6 imported successfully")

        launcher = TKAModernLauncherApp(sys.argv)
        print("📱 Launcher app created")

        logger.info("📱 Launcher app created, running...")
        print("🏃 Starting launcher app.run()...")

        exit_code = launcher.run()

        print(f"🏁 Launcher finished with exit code: {exit_code}")
        logger.info(f"🏁 Launcher finished with exit code: {exit_code}")
        return exit_code

    except KeyboardInterrupt:
        print("⚠️ Launcher interrupted by user")
        logger.info("Launcher interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Fatal launcher error: {e}")
        logger.error(f"Fatal launcher error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
