#!/usr/bin/env python3
"""
TKA Global Hotkey Handler - F5 Launcher
======================================

Global F5 hotkey handler to show/hide the simple TKA launcher from anywhere.
This runs in the background and listens for F5 presses system-wide.

Features:
- Global F5 hotkey detection
- Shows/hides simple launcher
- Runs in system tray
- Auto-start with Windows (optional)
"""

import logging
import sys
import time

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

# Try to import global hotkey libraries
try:
    import keyboard  # pip install keyboard

    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("⚠️ keyboard library not available. Install with: pip install keyboard")

logger = logging.getLogger(__name__)


class GlobalHotkeyThread(QThread):
    """Thread to handle global hotkey detection"""

    f5_pressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        """Run the hotkey detection loop"""
        if not KEYBOARD_AVAILABLE:
            logger.warning("⚠️ Keyboard library not available, F5 hotkey disabled")
            return

        try:
            # Register F5 hotkey
            keyboard.add_hotkey("f5", self._on_f5_pressed)
            logger.info("🎹 Global F5 hotkey registered")

            # Keep thread alive
            while self.running:
                time.sleep(0.1)

        except Exception as e:
            logger.error(f"❌ Failed to register global hotkey: {e}")

    def _on_f5_pressed(self):
        """Handle F5 key press"""
        logger.info("🔄 F5 pressed globally")
        self.f5_pressed.emit()

    def stop(self):
        """Stop the hotkey thread"""
        self.running = False
        if KEYBOARD_AVAILABLE:
            try:
                keyboard.unhook_all()
            except:
                pass


class TKASystemTray:
    """System tray handler for TKA launcher"""

    def __init__(self, app):
        self.app = app
        self.launcher_process = None
        self.launcher_app = None
        self.hotkey_thread = None

        # Setup system tray
        self._setup_tray()
        self._setup_hotkey()

    def _setup_tray(self):
        """Setup system tray icon and menu"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            logger.error("❌ System tray not available")
            return

        # Create tray icon (using default icon for now)
        self.tray_icon = QSystemTrayIcon()

        # Create tray menu
        tray_menu = QMenu()

        # Show launcher action
        show_action = QAction("📱 Show TKA Launcher", self.app)
        show_action.triggered.connect(self._show_launcher)
        tray_menu.addAction(show_action)

        tray_menu.addSeparator()

        # Launch actions
        modern_action = QAction("🖥️ Run Modern", self.app)
        modern_action.triggered.connect(self._run_modern)
        tray_menu.addAction(modern_action)

        legacy_action = QAction("🏛️ Run Legacy", self.app)
        legacy_action.triggered.connect(self._run_legacy)
        tray_menu.addAction(legacy_action)

        web_action = QAction("🌐 Run Web", self.app)
        web_action.triggered.connect(self._run_web)
        tray_menu.addAction(web_action)

        animator_action = QAction("🎬 Run Animator", self.app)
        animator_action.triggered.connect(self._run_animator)
        tray_menu.addAction(animator_action)

        tray_menu.addSeparator()

        # Exit action
        exit_action = QAction("❌ Exit", self.app)
        exit_action.triggered.connect(self._exit)
        tray_menu.addAction(exit_action)

        # Set menu and show tray icon
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("TKA Launcher - Press F5 to toggle")

        # Show tray icon
        self.tray_icon.show()
        logger.info("🔔 System tray icon created")

    def _setup_hotkey(self):
        """Setup global hotkey handler"""
        self.hotkey_thread = GlobalHotkeyThread()
        self.hotkey_thread.f5_pressed.connect(self._toggle_launcher)
        self.hotkey_thread.start()

    def _toggle_launcher(self):
        """Toggle launcher visibility"""
        try:
            if not self.launcher_app or not self.launcher_app.launcher:
                self._show_launcher()
            else:
                self.launcher_app.launcher.toggle_visibility()

        except Exception as e:
            logger.error(f"❌ Failed to toggle launcher: {e}")

    def _run_modern(self):
        """Launch TKA Modern from tray"""
        if self.launcher_app and self.launcher_app.launcher:
            self.launcher_app.launcher._run_modern()

    def _run_legacy(self):
        """Launch TKA Legacy from tray"""
        if self.launcher_app and self.launcher_app.launcher:
            self.launcher_app.launcher._run_legacy()

    def _run_web(self):
        """Launch TKA Web from tray"""
        if self.launcher_app and self.launcher_app.launcher:
            self.launcher_app.launcher._run_web()

    def _run_animator(self):
        """Launch TKA Animator from tray"""
        if self.launcher_app and self.launcher_app.launcher:
            self.launcher_app.launcher._run_animator()

    def _exit(self):
        """Exit the TKA system"""
        logger.info("👋 Exiting TKA system...")

        # Stop hotkey thread
        if self.hotkey_thread:
            self.hotkey_thread.stop()
            self.hotkey_thread.wait(1000)  # Wait 1 second for thread to stop

        # Close launcher
        if self.launcher_app and self.launcher_app.launcher:
            self.launcher_app.launcher.close()

        # Hide tray icon
        self.tray_icon.hide()

        # Quit application
        self.app.quit()


def main():
    """Main entry point for TKA global hotkey handler"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("TKA Global Hotkeys")
        app.setQuitOnLastWindowClosed(False)  # Keep running in background

        # Check for keyboard library
        if not KEYBOARD_AVAILABLE:
            logger.warning("⚠️ Global hotkeys require 'keyboard' library")
            logger.warning("💡 Install with: pip install keyboard")
            logger.warning("🔄 Running without global hotkeys...")

        # Create system tray handler
        tray_handler = TKASystemTray(app)

        logger.info("🚀 TKA Global Hotkey Handler started")
        logger.info("🎹 Press F5 anywhere to toggle TKA launcher")
        logger.info("🔔 Check system tray for TKA options")

        # Run application
        return app.exec()

    except KeyboardInterrupt:
        logger.info("⏹️ TKA Global Hotkeys interrupted")
        return 0
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
