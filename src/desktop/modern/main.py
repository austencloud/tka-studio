#!/usr/bin/env python3
"""
Kinetic Constructor - Main Application Entry Point

Modified to support different application modes via Application Factory.
Modern modular architecture with dependency injection and clean separation of concerns.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from presentation.components.ui.splash_screen import SplashScreen
    from core.application.application_factory import ApplicationMode

from PyQt6.QtCore import QTimer, QtMsgType, qInstallMessageHandler
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def _install_qt_message_handler():
    """Install Qt message handler to suppress CSS property warnings and other noise."""

    def qt_message_handler(msg_type, context, message):
        # ULTRA-AGGRESSIVE SUPPRESSION: Block ALL CSS and styling warnings to eliminate processing overhead
        suppressed_patterns = [
            "unknown property",
            "transition",
            "transform",
            "box-shadow",
            "backdrop-filter",
            "qobject::setparent",
            "qbasictimer",
            "timers cannot be started",
            "different thread",
            "qwidget",
            "qpainter",
            "stylesheet",
            "css",
            "style",
            "font",
            "color",
            "border",
            "margin",
            "padding",
            "background",
            "qml",
            "opengl",
            "shader",
            "texture",
            "pixmap",
            "image",
        ]

        message_lower = message.lower()
        if any(pattern in message_lower for pattern in suppressed_patterns):
            return  # Completely suppress these messages to eliminate processing overhead

        # Only show critical errors
        if msg_type == QtMsgType.QtCriticalMsg or msg_type == QtMsgType.QtFatalMsg:
            print(f"Qt {msg_type.name}: {message}")

    qInstallMessageHandler(qt_message_handler)


class TKAMainWindow(QMainWindow):
    def __init__(
        self,
        container=None,
        splash_screen: Optional["SplashScreen"] = None,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
    ):
        super().__init__()

        # Hide window immediately to prevent temporary flash
        self.hide()

        self.container = container
        self.splash = splash_screen
        self.target_screen = target_screen
        self.parallel_mode = parallel_mode
        self.parallel_geometry = parallel_geometry

        if self.container:
            from application.services.core.application_orchestrator import (
                ApplicationOrchestrator,
            )

            self.orchestrator = ApplicationOrchestrator(container=self.container)
            self.tab_widget = self.orchestrator.initialize_application(
                self,
                splash_screen,
                target_screen,
                parallel_mode,
                parallel_geometry,
            )

    def _attach_production_debugger(self) -> None:
        try:
            from debug import attach_to_application, get_production_debugger
            from PyQt6.QtCore import QTimer

            QTimer.singleShot(1000, lambda: self._do_debugger_attachment())
        except Exception:
            pass

    def _do_debugger_attachment(self) -> None:
        try:
            from debug import attach_to_application, get_production_debugger

            attach_to_application(self)
        except Exception:
            import traceback

            traceback.print_exc()

    def show(self):
        """Override show to ensure tab widget is properly displayed."""
        super().show()
        # WINDOW MANAGEMENT FIX: Ensure tab widget is shown when main window is shown
        if hasattr(self, "tab_widget") and self.tab_widget:
            self.tab_widget.show()
            self.tab_widget.setVisible(True)
            # Also show the current tab
            current_tab = self.tab_widget.currentWidget()
            if current_tab:
                current_tab.show()
                current_tab.setVisible(True)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        if hasattr(self, "orchestrator"):
            self.orchestrator.handle_window_resize(self)


def detect_parallel_testing_mode():
    import argparse
    import os

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--parallel-testing", action="store_true")
    parser.add_argument("--monitor", choices=["primary", "secondary", "left", "right"])
    args, _ = parser.parse_known_args()

    env_parallel = os.environ.get("TKA_PARALLEL_TESTING", "").lower() == "true"
    env_monitor = os.environ.get("TKA_PARALLEL_MONITOR", "")
    env_geometry = os.environ.get("TKA_PARALLEL_GEOMETRY", "")

    parallel_mode = args.parallel_testing or env_parallel
    monitor = args.monitor or env_monitor

    return parallel_mode, monitor, env_geometry


def create_application():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        # PERFORMANCE OPTIMIZATION: Install Qt message handler to suppress CSS warnings
        _install_qt_message_handler()

    # Create container for dependency injection
    from core.application.application_factory import ApplicationFactory, ApplicationMode

    container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

    # Initialize services
    try:
        from core.service_locator import initialize_services

        initialize_services()
    except Exception as e:
        print(f"Warning: Could not initialize services: {e}")

    parallel_mode, monitor, geometry = detect_parallel_testing_mode()
    screens = QGuiApplication.screens()
    if parallel_mode and monitor == "secondary" and len(screens) > 1:
        target_screen = screens[1]
    elif parallel_mode and monitor == "primary":
        target_screen = screens[0]
    else:
        target_screen = (
            screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
        )

    window = TKAMainWindow(
        container=container,
        splash_screen=None,
        target_screen=target_screen,
        parallel_mode=parallel_mode,
        parallel_geometry=geometry,
    )

    return app, window


def main():
    """Main entry point with support for different application modes."""

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Import ApplicationMode when needed
    from core.application.application_factory import ApplicationMode

    # INSTANT FIX: Suppress verbose arrow positioning logs
    try:
        from core.logging.instant_fix import apply_instant_fix

        apply_instant_fix("quiet")

    except Exception as e:
        logger.warning(
            f"⚠️ Could not apply logging fix: {e} - continuing with default logging"
        )

    # Determine application mode from command line arguments
    app_mode = ApplicationMode.PRODUCTION

    if "--test" in sys.argv:
        app_mode = ApplicationMode.TEST
        # For test mode, just create container and return it
        from core.application.application_factory import ApplicationFactory

        container = ApplicationFactory.create_app(app_mode)

        # Initialize services for test mode too
        try:
            from core.service_locator import initialize_services

            initialize_services()
            logger.info("✅ Event-driven services initialized for test mode")
        except Exception as e:
            logger.warning(
                f"⚠️ Could not initialize event-driven services in test mode: {e}"
            )

        logger.info(f"Test mode - application ready for automated testing")
        logger.info(f"Available services: {list(container.get_registrations().keys())}")
        return container
    elif "--headless" in sys.argv:
        app_mode = ApplicationMode.HEADLESS
        # For headless mode, create container but no UI
        from core.application.application_factory import ApplicationFactory

        container = ApplicationFactory.create_app(app_mode)

        # Initialize services for headless mode too
        try:
            from core.service_locator import initialize_services

            initialize_services()
            logger.info("✅ Event-driven services initialized for headless mode")
        except Exception as e:
            logger.warning(
                f"⚠️ Could not initialize event-driven services in headless mode: {e}"
            )

        logger.info("Headless mode - application ready for server-side processing")
        return container
    elif "--record" in sys.argv:
        app_mode = ApplicationMode.RECORDING
    # For production and recording modes, continue with UI setup
    try:
        # Lazy import ApplicationFactory when needed
        from core.application.application_factory import ApplicationFactory

        # Create application using factory
        container = ApplicationFactory.create_app(app_mode)

        # Initialize event-driven architecture services
        try:
            from core.service_locator import initialize_services

            if not initialize_services():
                logger.warning(
                    "⚠️ Failed to initialize event-driven services - falling back to legacy architecture"
                )
        except Exception as e:
            logger.error(f"❌ Error initializing event-driven services: {e}")
            logger.warning("⚠️ Continuing with legacy architecture")

        # Continue with existing UI setup for production mode
        parallel_mode, monitor, geometry = detect_parallel_testing_mode()
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        screens = QGuiApplication.screens()

        if parallel_mode and len(screens) > 1:
            if monitor in ["secondary", "right"]:
                primary_screen = screens[0]
                secondary_screen = screens[1]
                if secondary_screen.geometry().x() > primary_screen.geometry().x():
                    target_screen = secondary_screen
                else:
                    target_screen = primary_screen
            elif monitor in ["primary", "left"]:
                primary_screen = screens[0]
                secondary_screen = screens[1]
                if secondary_screen.geometry().x() < primary_screen.geometry().x():
                    target_screen = secondary_screen
                else:
                    target_screen = primary_screen
            else:
                target_screen = screens[1]
        else:
            target_screen = (
                screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
            )

        # Lazy import splash screen when needed
        from presentation.components.ui.splash_screen import SplashScreen

        # UI setup with splash screen
        splash = SplashScreen(target_screen=target_screen)
        fade_in_animation = splash.show_animated()
        window = None

        def start_initialization():
            nonlocal window
            try:
                # Give splash screen time to fully appear
                splash.update_progress(5, "Initializing application...")
                app.processEvents()

                # Small delay to ensure splash is visible before heavy operations
                QTimer.singleShot(50, lambda: continue_initialization())

            except Exception:
                import traceback

                traceback.print_exc()
                return

        def continue_initialization():
            nonlocal window
            try:
                splash.update_progress(10, "Loading application icon...")
                app.processEvents()
                icon_path = Path(__file__).parent / "images" / "icons" / "app_icon.png"
                if icon_path.exists():
                    app.setWindowIcon(QIcon(str(icon_path)))

                splash.update_progress(
                    15, "Creating main window and loading all components..."
                )
                app.processEvents()

                splash.update_progress(
                    15, "Creating main window and loading all components..."
                )

                window = TKAMainWindow(
                    container=container,
                    splash_screen=splash,
                    target_screen=target_screen,
                    parallel_mode=parallel_mode,
                    parallel_geometry=geometry,
                )

                # Process events to ensure hide takes effect
                app.processEvents()

                complete_startup()
            except Exception:
                import traceback

                traceback.print_exc()
                return

        def complete_startup():
            if window is None:
                return
            splash.update_progress(100, "Application ready!")
            app.processEvents()

            def show_main_window():
                """Show main window exactly when splash finishes fading."""
                window.show()
                window.raise_()
                window.activateWindow()

            # TEMPORARY FIX: Show window immediately for debugging
            show_main_window()

            # Also hide splash screen with callback
            splash.hide_animated()

        fade_in_animation.finished.connect(start_initialization)

        # Run generation tests if requested
        if "--test-generation" in sys.argv:

            def run_tests_after_init():
                try:
                    from test_generation_simple import test_generation_functionality

                    test_success = test_generation_functionality()
                    if not test_success:
                        print("❌ Generation tests failed!")
                except Exception as e:
                    print(f"❌ Failed to run generation tests: {e}")
                    import traceback

                    traceback.print_exc()

            # Run tests after a short delay to ensure app is fully initialized
            QTimer.singleShot(2000, run_tests_after_init)

        return app.exec()

    except Exception as e:
        logger.error(f"Failed to start TKA application: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
