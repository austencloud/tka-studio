#!/usr/bin/env python3
"""
Kinetic Constructor - Main Application Entry Point

Modified to support different application modes via Application Factory.
Modern modular architecture with dependency injection and clean separation of concerns.
"""

import sys
import logging
import os
import argparse
from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon, QGuiApplication

modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

# Import the new Application Factory
from core.application.application_factory import ApplicationFactory, ApplicationMode
from presentation.components.ui.splash_screen import SplashScreen


class TKAMainWindow(QMainWindow):
    def __init__(
        self,
        container=None,
        splash_screen: Optional[SplashScreen] = None,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
        enable_api=True,
    ):
        super().__init__()
        self.container = container
        self.splash = splash_screen
        self.target_screen = target_screen
        self.parallel_mode = parallel_mode
        self.parallel_geometry = parallel_geometry
        self.enable_api = enable_api

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
                enable_api,
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

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        if hasattr(self, "orchestrator"):
            self.orchestrator.handle_window_resize(self)


def refresh_component_visibility(window):
    """Refresh visibility of all components after main window is shown"""
    try:
        print("🔧 [MAIN] Refreshing component visibility after window shown...")

        # Get the tab widget
        tab_widget = getattr(window, "tab_widget", None)
        if not tab_widget:
            print("❌ [MAIN] No tab widget found")
            return

        # Force tab widget to be visible
        tab_widget.show()
        tab_widget.setVisible(True)

        # Get the construct tab (should be at index 0)
        construct_tab = tab_widget.widget(0)
        if not construct_tab:
            print("❌ [MAIN] No construct tab found")
            return

        # Force construct tab to be visible
        construct_tab.show()
        construct_tab.setVisible(True)

        # Get the workbench from the construct tab
        workbench = getattr(construct_tab, "workbench", None)
        if not workbench:
            print("❌ [MAIN] No workbench found in construct tab")
            return

        # Force workbench to be visible
        workbench.show()
        workbench.setVisible(True)

        # Get the beat frame section from the workbench (using correct attribute name)
        beat_frame_section = getattr(workbench, "_beat_frame_section", None)
        if not beat_frame_section:
            print("❌ [MAIN] No _beat_frame_section found in workbench")
            return

        # Force beat frame section to be visible
        beat_frame_section.show()
        beat_frame_section.setVisible(True)

        # Get the beat frame from the beat frame section (using correct attribute name)
        beat_frame = getattr(beat_frame_section, "_beat_frame", None)
        if not beat_frame:
            print("❌ [MAIN] No _beat_frame found in beat frame section")
            return

        # Force beat frame to be visible
        beat_frame.show()
        beat_frame.setVisible(True)

        # Get the start position view from the beat frame (using correct attribute name)
        start_position_view = getattr(beat_frame, "_start_position_view", None)
        if not start_position_view:
            print("❌ [MAIN] No _start_position_view found in beat frame")
            return

        # Force start position view to be visible
        start_position_view.show()
        start_position_view.setVisible(True)

        # CRITICAL DEBUG: Check start position view size and geometry
        start_pos_size = start_position_view.size()
        start_pos_geometry = start_position_view.geometry()
        start_pos_minimum_size = start_position_view.minimumSize()
        start_pos_maximum_size = start_position_view.maximumSize()
        start_pos_size_hint = start_position_view.sizeHint()

        print(f"🔍 [MAIN] Start position view details:")
        print(f"   Size: {start_pos_size}")
        print(f"   Geometry: {start_pos_geometry}")
        print(f"   Minimum size: {start_pos_minimum_size}")
        print(f"   Maximum size: {start_pos_maximum_size}")
        print(f"   Size hint: {start_pos_size_hint}")

        # Force a specific size if it's collapsed to 1x1 or zero
        if start_pos_size.width() <= 1 or start_pos_size.height() <= 1:
            print(
                "🔧 [MAIN] Start position view has collapsed size, forcing proper size..."
            )
            start_position_view.setMinimumSize(120, 120)
            start_position_view.setMaximumSize(120, 120)
            start_position_view.setFixedSize(120, 120)
            start_position_view.resize(120, 120)
            start_position_view.updateGeometry()

            # Also fix the pictograph component inside
            pictograph_component = getattr(
                start_position_view, "_pictograph_component", None
            )
            if pictograph_component:
                pictograph_component.setMinimumSize(100, 100)
                pictograph_component.resize(100, 100)
                pictograph_component.updateGeometry()

            print(f"🔧 [MAIN] After resize: {start_position_view.size()}")

        # Check final visibility status
        tab_visible = tab_widget.isVisible()
        construct_visible = construct_tab.isVisible()
        workbench_visible = workbench.isVisible()
        section_visible = beat_frame_section.isVisible()
        frame_visible = beat_frame.isVisible()
        start_pos_visible = start_position_view.isVisible()

        print(f"✅ [MAIN] Component visibility refreshed:")
        print(f"   Tab widget: {tab_visible}")
        print(f"   Construct tab: {construct_visible}")
        print(f"   Workbench: {workbench_visible}")
        print(f"   Beat frame section: {section_visible}")
        print(f"   Beat frame: {frame_visible}")
        print(f"   Start position view: {start_pos_visible}")

    except Exception as e:
        print(f"❌ [MAIN] Error refreshing component visibility: {e}")
        import traceback

        traceback.print_exc()


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
        container = ApplicationFactory.create_app(app_mode)
        logger.info(f"Test mode - application ready for automated testing")
        logger.info(f"Available services: {list(container.get_registrations().keys())}")
        return container
    elif "--headless" in sys.argv:
        app_mode = ApplicationMode.HEADLESS
        logger.info("Starting TKA in HEADLESS mode")
        # For headless mode, create container but no UI
        container = ApplicationFactory.create_app(app_mode)
        logger.info("Headless mode - application ready for server-side processing")
        return container
    elif "--record" in sys.argv:
        app_mode = ApplicationMode.RECORDING
        logger.info("Starting TKA in RECORDING mode")
    else:
        logger.info("Starting TKA in PRODUCTION mode")

    # For production and recording modes, continue with UI setup
    try:
        # Create application using factory
        container = ApplicationFactory.create_app(app_mode)
        logger.info(
            f"TKA application container created successfully in {app_mode} mode"
        )

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

        # UI setup with splash screen
        splash = SplashScreen(target_screen=target_screen)
        fade_in_animation = splash.show_animated()
        window = None

        def start_initialization():
            nonlocal window
            try:
                splash.update_progress(5, "Initializing application...")
                app.processEvents()
                icon_path = Path(__file__).parent / "images" / "icons" / "app_icon.png"
                if icon_path.exists():
                    app.setWindowIcon(QIcon(str(icon_path)))
                splash.update_progress(15, "Creating main window...")
                window = TKAMainWindow(
                    container=container,
                    splash_screen=splash,
                    target_screen=target_screen,
                    parallel_mode=parallel_mode,
                    parallel_geometry=geometry,
                )
                complete_startup()
            except Exception:
                import traceback

                traceback.print_exc()
                return

        def complete_startup():
            if window is None:
                return
            splash.update_progress(100, "Ready!")
            app.processEvents()

            # Show window immediately after UI setup
            window.show()
            window.raise_()
            print(f"🔍 [MAIN] Main window shown: visible={window.isVisible()}")

            # Hide splash screen after window is visible
            QTimer.singleShot(200, lambda: splash.hide_animated())

        fade_in_animation.finished.connect(start_initialization)
        return app.exec()

    except Exception as e:
        logger.error(f"Failed to start TKA application: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
