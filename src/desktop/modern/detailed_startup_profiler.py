#!/usr/bin/env python3
"""
Detailed Startup Profiler - Deep Analysis of TKA Startup Performance

This profiler instruments the actual startup process to measure timing
of individual components within the orchestrator initialization.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import sys
import time


# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


class DetailedProfiler:
    """Detailed profiler for startup operations."""

    def __init__(self):
        self.timings = {}
        self.start_time = None

    @contextmanager
    def time_operation(self, name: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            duration = (time.perf_counter() - start) * 1000
            self.timings[name] = duration
            print(f"⏱️  {name}: {duration:.1f}ms")

    def start_profiling(self):
        self.start_time = time.perf_counter()
        print("🔍 Starting detailed startup profiling...")
        print("=" * 60)

    def end_profiling(self):
        total_time = (time.perf_counter() - self.start_time) * 1000
        print("=" * 60)
        print(f"🎯 TOTAL TIME: {total_time:.1f}ms")
        self.analyze_results()

    def analyze_results(self):
        print("\n📊 DETAILED TIMING BREAKDOWN:")
        sorted_timings = sorted(self.timings.items(), key=lambda x: x[1], reverse=True)

        total_measured = sum(self.timings.values())

        for name, duration in sorted_timings:
            percentage = (duration / total_measured) * 100
            print(f"   {name:<50} {duration:>8.1f}ms ({percentage:>5.1f}%)")

        # Identify major bottlenecks
        print("\n⚠️  BOTTLENECKS (>100ms):")
        bottlenecks = [
            (name, duration) for name, duration in sorted_timings if duration > 100
        ]

        if bottlenecks:
            for name, duration in bottlenecks:
                print(f"   • {name}: {duration:.1f}ms")
        else:
            print("   ✅ No major bottlenecks detected")


def profile_startup():
    """Profile the actual startup process with detailed instrumentation."""
    profiler = DetailedProfiler()
    profiler.start_profiling()

    try:
        # Basic setup
        with profiler.time_operation("QApplication setup"):
            from PyQt6.QtWidgets import QApplication

            app = QApplication.instance()
            if not app:
                app = QApplication(sys.argv)
                app.setStyle("Fusion")

        # Import timing
        with profiler.time_operation("Core imports"):
            from PyQt6.QtGui import QGuiApplication

            from desktop.modern.core.application.application_factory import (
                ApplicationFactory,
                ApplicationMode,
            )
            from desktop.modern.presentation.components.ui.splash_screen import (
                SplashScreen,
            )

        # Container creation
        with profiler.time_operation("Container creation"):
            container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

        # Service initialization
        with profiler.time_operation("Service initialization"):
            from desktop.modern.core.service_locator import initialize_services

            initialize_services()

        # Splash screen
        with profiler.time_operation("Splash screen creation"):
            screens = QGuiApplication.screens()
            target_screen = screens[0] if screens else None
            splash = SplashScreen(target_screen=target_screen)

        # Now instrument the main window creation in detail
        with profiler.time_operation("Main window - imports"):
            from desktop.modern.application.services.core.application_orchestrator import (
                ApplicationOrchestrator,
            )
            from main import TKAMainWindow

        with profiler.time_operation("Main window - constructor setup"):
            # Create window but don't initialize orchestrator yet
            window = TKAMainWindow.__new__(TKAMainWindow)
            window.container = container
            window.splash = splash
            window.target_screen = target_screen
            window.parallel_mode = False
            window.parallel_geometry = None

        with profiler.time_operation("QMainWindow.__init__"):
            super(TKAMainWindow, window).__init__()
            window.hide()  # Hide immediately

        # Now instrument the orchestrator initialization
        if window.container:
            with profiler.time_operation("Orchestrator creation"):
                window.orchestrator = ApplicationOrchestrator(
                    container=window.container
                )

            # Instrument the orchestrator.initialize_application call
            original_initialize = window.orchestrator.initialize_application

            def instrumented_initialize(*args, **kwargs):
                with profiler.time_operation("Lifecycle manager initialization"):
                    # This will be called within initialize_application
                    pass

                with profiler.time_operation("Service registration"):
                    # This will be called within initialize_application
                    pass

                with profiler.time_operation("UI setup"):
                    # This will be called within initialize_application
                    pass

                return original_initialize(*args, **kwargs)

            # Instrument individual orchestrator components
            with profiler.time_operation("Orchestrator.initialize_application"):
                # Manually call the orchestrator initialization steps

                # Step 1: Lifecycle manager
                with profiler.time_operation("  1. Lifecycle manager"):
                    window.orchestrator.lifecycle_manager.initialize_application(
                        window, target_screen, False, None, None
                    )

                # Step 2: Service registration
                with profiler.time_operation("  2. Service registration"):
                    from desktop.modern.core.dependency_injection.di_container import (
                        get_container,
                    )

                    window.orchestrator.container = get_container()
                    window.orchestrator.service_manager.register_all_services(
                        window.orchestrator.container
                    )

                # Step 3: UI setup
                with profiler.time_operation("  3. UI setup"):
                    window.tab_widget = window.orchestrator.ui_manager.setup_main_ui(
                        window,
                        window.orchestrator.container,
                        None,
                        window.orchestrator.lifecycle_manager._session_service,
                    )

                # Step 4: Session restoration
                with profiler.time_operation("  4. Session restoration"):
                    window.orchestrator.lifecycle_manager.trigger_deferred_session_restoration()

                # Step 5: Background setup
                with profiler.time_operation("  5. Background setup"):
                    window.background_widget = (
                        window.orchestrator.background_manager.setup_background(
                            window, window.orchestrator.container, None
                        )
                    )

        print("\n✅ Startup profiling complete!")

    except Exception as e:
        print(f"❌ Error during profiling: {e}")
        import traceback

        traceback.print_exc()

    finally:
        profiler.end_profiling()


if __name__ == "__main__":
    profile_startup()
