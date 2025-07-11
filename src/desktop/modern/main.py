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

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow

modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

# Lazy imports for performance optimization
# These will be imported when needed to reduce startup time


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

        # Only initialize orchestrator if we have a container (production mode)
        if self.container:
            from application.services.core.application_orchestrator import (
                ApplicationOrchestrator,
            )

            # Pass the container to the orchestrator so it can resolve the session service
            print(
                f"🔍 [MAIN] Creating orchestrator with container for session service resolution"
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
            from debug import attach_to_application

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
            print("🔍 [MAIN_WINDOW] Tab widget and current tab made visible")

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
        logger.info("✅ Smart logging applied - arrow positioning verbosity REDUCED")
    except ImportError:
        # Fallback: Direct suppression without smart logging
        verbose_loggers = [
            "application.services.positioning.arrows.orchestration.directional_tuple_processor",
            "application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service",
            "application.services.positioning.arrows.orchestration.arrow_adjustment_lookup_service",
        ]
        for logger_name in verbose_loggers:
            logging.getLogger(logger_name).setLevel(logging.ERROR)
        logger.info("✅ Fallback logging applied - arrow positioning verbosity REDUCED")
    except Exception as e:
        logger.warning(
            f"⚠️ Could not apply logging fix: {e} - continuing with default logging"
        )

    # Determine application mode from command line arguments
    app_mode = ApplicationMode.PRODUCTION

    if "--test" in sys.argv:
        app_mode = ApplicationMode.TEST
        logger.info("Starting TKA in TEST mode")
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
        logger.info("Starting TKA in HEADLESS mode")
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
        logger.info("Starting TKA in RECORDING mode")
    else:
        logger.info("Starting TKA in PRODUCTION mode")

    # For production and recording modes, continue with UI setup
    try:
        # Lazy import ApplicationFactory when needed
        from core.application.application_factory import ApplicationFactory

        # Create application using factory
        container = ApplicationFactory.create_app(app_mode)
        logger.info(
            f"TKA application container created successfully in {app_mode} mode"
        )

        # Initialize event-driven architecture services
        try:
            from core.service_locator import initialize_services

            if initialize_services():
                logger.info(
                    "✅ Event-driven architecture services initialized successfully"
                )
            else:
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

                # Create window with full initialization (including construct tab loading)
                # This happens during splash screen phase so everything is ready when window appears
                window = TKAMainWindow(
                    container=container,
                    splash_screen=splash,
                    target_screen=target_screen,
                    parallel_mode=parallel_mode,
                    parallel_geometry=geometry,
                )
                # WINDOW MANAGEMENT FIX: Ensure window stays hidden until everything is fully loaded
                window.hide()
                window.setVisible(False)
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

            print(f"✅ TKA application startup completed successfully!")
            print(f"🔧 Construct tab fully loaded and ready for use")

            # PERFECT TIMING FIX: Show main window exactly when splash fades away
            def show_main_window():
                """Show main window exactly when splash finishes fading."""
                window.show()
                window.raise_()
                window.activateWindow()
                print(f"🔍 [MAIN] Main window shown: visible={window.isVisible()}")

            # Hide splash screen with callback to show main window at perfect timing
            splash.hide_animated(callback=show_main_window)

        fade_in_animation.finished.connect(start_initialization)
        return app.exec()

    except Exception as e:
        logger.error(f"Failed to start TKA application: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
