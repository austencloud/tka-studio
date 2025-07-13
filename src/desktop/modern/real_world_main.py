#!/usr/bin/env python3
"""
Real-World Instrumented Main - Complete Startup Flow Profiling

This is a modified version of main.py that integrates the real-world startup profiler
to measure the complete user experience from process launch to fully interactive GUI.

This version captures:
- Complete Qt event loop timing
- Splash screen animation and fade timing
- Asynchronous initialization phases
- Real window show and activation timing
- Event processing and rendering measurement
"""

import logging
import os
import sys
from pathlib import Path

# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

# Import the real-world profiler
from real_world_startup_profiler import real_world_profiler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def real_world_main():
    """Main function with complete real-world profiling instrumentation."""
    
    # Start profiling immediately at process start
    real_world_profiler.start_phase("Process Initialization", user_visible=False)
    
    try:
        # Phase 1: Basic Application Setup
        with real_world_profiler.time_operation("QApplication creation", user_visible=False):
            from PyQt6.QtWidgets import QApplication
            from PyQt6.QtCore import QTimer
            from PyQt6.QtGui import QIcon, QGuiApplication
            
            app = QApplication.instance()
            if not app:
                app = QApplication(sys.argv)
                app.setStyle("Fusion")
        
        # Phase 2: Application Factory and Container
        with real_world_profiler.time_operation("Application factory imports", user_visible=False):
            from core.application.application_factory import ApplicationFactory, ApplicationMode
            
        with real_world_profiler.time_operation("Dependency injection container creation", user_visible=False):
            container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)
        
        # Phase 3: Service Initialization
        with real_world_profiler.time_operation("Service locator initialization", user_visible=False):
            from core.service_locator import initialize_services
            initialize_services()
        
        real_world_profiler.end_phase("Process Initialization")
        
        # Phase 4: Screen Detection and Splash Screen Setup
        real_world_profiler.start_phase("Splash Screen Setup", user_visible=True)
        
        with real_world_profiler.time_operation("Screen detection", user_visible=False):
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
                target_screen = screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
        
        with real_world_profiler.time_operation("Splash screen creation", user_visible=True):
            from presentation.components.ui.splash_screen import SplashScreen
            splash = SplashScreen(target_screen=target_screen)
        
        # Phase 5: Splash Screen Animation (USER VISIBLE)
        with real_world_profiler.time_operation("Splash screen animation start", user_visible=True, blocking=False):
            fade_in_animation = splash.show_animated()
            real_world_profiler.mark_milestone("splash_visible", user_visible=True)
            window = None
        
        real_world_profiler.end_phase("Splash Screen Setup")
        
        def start_initialization():
            """Start the initialization process with real-world profiling."""
            nonlocal window
            
            real_world_profiler.start_phase("Async Initialization", user_visible=True)
            real_world_profiler.mark_milestone("splash_animation_complete", user_visible=True)
            
            try:
                with real_world_profiler.time_operation("Initial progress update", user_visible=True, blocking=False):
                    splash.update_progress(5, "Initializing application...")
                    real_world_profiler.track_event_processing("Initial progress processEvents")
                    app.processEvents()
                
                # Track the async delay
                real_world_profiler.track_async_operation("QTimer.singleShot delay", delay_ms=50)
                QTimer.singleShot(50, lambda: continue_initialization())
                
            except Exception as e:
                logger.error(f"Error in start_initialization: {e}")
                import traceback
                traceback.print_exc()
        
        def continue_initialization():
            """Continue initialization with detailed real-world profiling."""
            nonlocal window
            
            try:
                with real_world_profiler.time_operation("Application icon loading", user_visible=True):
                    splash.update_progress(10, "Loading application icon...")
                    real_world_profiler.track_event_processing("Icon loading processEvents")
                    app.processEvents()
                    icon_path = Path(__file__).parent / "images" / "icons" / "app_icon.png"
                    if icon_path.exists():
                        app.setWindowIcon(QIcon(str(icon_path)))
                
                real_world_profiler.end_phase("Async Initialization")
                real_world_profiler.start_phase("Main Window Creation", user_visible=True)
                
                with real_world_profiler.time_operation("Main window progress update", user_visible=True, blocking=False):
                    splash.update_progress(15, "Creating main window and loading all components...")
                    real_world_profiler.track_event_processing("Main window progress processEvents")
                    app.processEvents()
                
                with real_world_profiler.time_operation("TKAMainWindow instantiation", user_visible=True):
                    # Import and create main window
                    from main import TKAMainWindow
                    
                    window = TKAMainWindow(
                        container=container,
                        splash_screen=splash,
                        target_screen=target_screen,
                        parallel_mode=parallel_mode,
                        parallel_geometry=geometry,
                    )
                    real_world_profiler.mark_milestone("main_window_created", user_visible=False)
                
                with real_world_profiler.time_operation("Post-creation event processing", user_visible=True, blocking=False):
                    real_world_profiler.track_event_processing("Post-creation processEvents")
                    app.processEvents()
                
                real_world_profiler.end_phase("Main Window Creation")
                complete_startup()
                
            except Exception as e:
                logger.error(f"Error in continue_initialization: {e}")
                import traceback
                traceback.print_exc()
        
        def complete_startup():
            """Complete the startup process with final profiling."""
            if window is None:
                return
                
            real_world_profiler.start_phase("Startup Completion", user_visible=True)
            
            with real_world_profiler.time_operation("Final progress update", user_visible=True, blocking=False):
                splash.update_progress(100, "Application ready!")
                real_world_profiler.track_event_processing("Final progress processEvents")
                app.processEvents()
                
                print("SUCCESS: TKA application startup completed successfully!")
            
            def show_main_window():
                """Show main window and mark final completion."""
                with real_world_profiler.time_operation("Main window show and activation", user_visible=True):
                    real_world_profiler.mark_milestone("main_window_shown", user_visible=True)
                    window.show()
                    window.raise_()
                    window.activateWindow()
                    real_world_profiler.mark_milestone("application_interactive", user_visible=True)
                
                real_world_profiler.end_phase("Startup Completion")
                
                # Generate the final report after a short delay to ensure everything is settled
                QTimer.singleShot(100, lambda: real_world_profiler.generate_real_world_report())
            
            with real_world_profiler.time_operation("Splash screen hide animation", user_visible=True, blocking=False):
                splash.hide_animated(callback=show_main_window)
        
        # Connect animation to start initialization
        fade_in_animation.finished.connect(start_initialization)
        
        # Mark event loop start and begin Qt event processing
        real_world_profiler.mark_milestone("event_loop_started", user_visible=False)
        
        # Start the Qt event loop (this is where the real timing happens!)
        with real_world_profiler.time_operation("Qt Event Loop Execution", user_visible=True, blocking=True):
            return app.exec()
        
    except Exception as e:
        logger.error(f"Failed to start TKA application: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(real_world_main())
