#!/usr/bin/env python3
"""
Instrumented Main - TKA Startup with Enhanced Performance Profiling

This is a modified version of main.py that integrates the enhanced startup profiler
to provide comprehensive performance analysis of the actual startup process.

Usage:
    python instrumented_main.py

Environment Variables:
    TKA_STARTUP_PROFILING=1    Enable profiling (default)
    TKA_STARTUP_PROFILING=0    Disable profiling
"""

import logging
import os
import sys
from pathlib import Path

# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

# Import the enhanced profiler and patches
from enhanced_startup_profiler import create_instrumented_progress_callback, profiler
from orchestrator_profiling_patch import apply_all_profiling_patches

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def instrumented_main():
    """Main function with enhanced profiling instrumentation."""
    # Apply profiling patches before starting
    apply_all_profiling_patches()

    profiler.start_profiling()

    try:
        # Phase 1: Basic Application Setup
        with profiler.time_operation("QApplication initialization"):
            from PyQt6.QtCore import QTimer
            from PyQt6.QtGui import QGuiApplication, QIcon
            from PyQt6.QtWidgets import QApplication

            app = QApplication.instance()
            if not app:
                app = QApplication(sys.argv)
                app.setStyle("Fusion")

        # Phase 2: Application Factory and Container
        with profiler.time_operation("Application factory setup"):
            from core.application.application_factory import (
                ApplicationFactory,
                ApplicationMode,
            )

        with profiler.time_operation("Dependency injection container"):
            container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

        # Phase 3: Service Initialization
        with profiler.time_operation("Service locator initialization"):
            from core.service_locator import initialize_services

            initialize_services()

        # Phase 4: Screen Detection and Splash Screen
        with profiler.time_operation("Screen detection"):
            screens = QGuiApplication.screens()

            # Determine target screen (same logic as original main.py)
            parallel_mode = "--parallel" in sys.argv
            geometry = None

            if parallel_mode:
                target_screen = QGuiApplication.primaryScreen()
            elif len(screens) > 1:
                primary_screen = screens[0]
                secondary_screen = screens[1]
                if secondary_screen.geometry().x() < primary_screen.geometry().x():
                    target_screen = secondary_screen
                else:
                    target_screen = primary_screen
            else:
                target_screen = (
                    screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
                )

        with profiler.time_operation("Splash screen creation"):
            from presentation.components.ui.splash_screen import SplashScreen

            splash = SplashScreen(target_screen=target_screen)
            profiler.mark_splash_visible()

        # Phase 5: Splash Screen Animation and Initial Progress
        with profiler.time_operation("Splash screen animation"):
            fade_in_animation = splash.show_animated()
            window = None

        # Create instrumented progress callback
        progress_callback = create_instrumented_progress_callback(splash)

        def start_initialization():
            """Start the initialization process with profiling."""
            nonlocal window
            try:
                with profiler.time_operation("Initial progress setup"):
                    progress_callback(5, "Initializing application...")
                    app.processEvents()

                # Small delay to ensure splash is visible
                QTimer.singleShot(50, lambda: continue_initialization())

            except Exception as e:
                logger.error(f"Error in start_initialization: {e}")
                import traceback

                traceback.print_exc()

        def continue_initialization():
            """Continue initialization with detailed profiling."""
            nonlocal window
            try:
                with profiler.time_operation("Application icon loading"):
                    progress_callback(10, "Loading application icon...")
                    app.processEvents()
                    icon_path = (
                        Path(__file__).parent / "images" / "icons" / "app_icon.png"
                    )
                    if icon_path.exists():
                        app.setWindowIcon(QIcon(str(icon_path)))

                with profiler.time_operation("Main window creation and initialization"):
                    progress_callback(
                        15, "Creating main window and loading all components..."
                    )
                    app.processEvents()

                    # Import and create main window
                    from main import TKAMainWindow

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

            except Exception as e:
                logger.error(f"Error in continue_initialization: {e}")
                import traceback

                traceback.print_exc()

        def complete_startup():
            """Complete the startup process."""
            if window is None:
                return

            with profiler.time_operation("Startup completion"):
                progress_callback(100, "Application ready!")
                app.processEvents()

                print("SUCCESS: TKA application startup completed successfully!")

                def show_main_window():
                    """Show main window and mark completion."""
                    profiler.mark_window_shown()
                    window.show()
                    window.raise_()
                    window.activateWindow()

                # Hide splash screen with callback to show main window
                splash.hide_animated(callback=show_main_window)

        # Connect animation to start initialization
        fade_in_animation.finished.connect(start_initialization)

        # Start the Qt event loop
        return app.exec()

    except Exception as e:
        logger.error(f"Failed to start TKA application: {e}")
        import traceback

        traceback.print_exc()
        return 1

    finally:
        profiler.end_profiling()


if __name__ == "__main__":
    sys.exit(instrumented_main())
