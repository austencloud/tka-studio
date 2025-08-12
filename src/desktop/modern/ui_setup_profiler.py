#!/usr/bin/env python3
"""
UI Setup Profiler - Deep Analysis of UI Creation Performance

This profiler specifically targets the UI setup process which takes 1370ms,
breaking it down into individual component creation steps.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import sys
import time


# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


class UIProfiler:
    """Profiler specifically for UI setup operations."""

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
        print("🔍 Starting UI setup profiling...")
        print("=" * 60)

    def end_profiling(self):
        total_time = (time.perf_counter() - self.start_time) * 1000
        print("=" * 60)
        print(f"🎯 UI SETUP TOTAL TIME: {total_time:.1f}ms")
        self.analyze_ui_results()

    def analyze_ui_results(self):
        print("\n📊 UI SETUP TIMING BREAKDOWN:")
        sorted_timings = sorted(self.timings.items(), key=lambda x: x[1], reverse=True)

        total_measured = sum(self.timings.values())

        for name, duration in sorted_timings:
            percentage = (duration / total_measured) * 100
            print(f"   {name:<60} {duration:>8.1f}ms ({percentage:>5.1f}%)")

        # Identify UI bottlenecks
        print("\n⚠️  UI BOTTLENECKS (>50ms):")
        bottlenecks = [
            (name, duration) for name, duration in sorted_timings if duration > 50
        ]

        if bottlenecks:
            for name, duration in bottlenecks:
                print(f"   • {name}: {duration:.1f}ms")

                # Provide specific recommendations
                if "option_picker" in name.lower():
                    print("     💡 Consider lazy loading option picker components")
                elif "pictograph" in name.lower():
                    print("     💡 Consider deferring pictograph pool creation")
                elif "workbench" in name.lower():
                    print("     💡 Consider progressive workbench initialization")
        else:
            print("   ✅ No major UI bottlenecks detected")


def profile_ui_setup():
    """Profile the UI setup process in detail."""
    profiler = UIProfiler()

    try:
        # Quick setup to get to UI profiling
        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
            app.setStyle("Fusion")

        from desktop.modern.core.application.application_factory import (
            ApplicationFactory,
            ApplicationMode,
        )

        container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

        from desktop.modern.core.service_locator import initialize_services

        initialize_services()

        from PyQt6.QtGui import QGuiApplication

        from desktop.modern.presentation.components.ui.splash_screen import SplashScreen

        screens = QGuiApplication.screens()
        target_screen = screens[0] if screens else None
        splash = SplashScreen(target_screen=target_screen)

        from desktop.modern.application.services.core.application_orchestrator import (
            ApplicationOrchestrator,
        )
        from main import TKAMainWindow

        # Create window
        window = TKAMainWindow.__new__(TKAMainWindow)
        super(TKAMainWindow, window).__init__()
        window.hide()

        window.container = container
        window.splash = splash
        window.target_screen = target_screen
        window.parallel_mode = False
        window.parallel_geometry = None

        # Create orchestrator
        window.orchestrator = ApplicationOrchestrator(container=window.container)

        # Initialize lifecycle and services quickly
        window.orchestrator.lifecycle_manager.initialize_application(
            window, target_screen, False, None, None
        )

        from desktop.modern.core.dependency_injection.di_container import get_container

        window.orchestrator.container = get_container()
        window.orchestrator.service_manager.register_all_services(
            window.orchestrator.container
        )

        # NOW PROFILE THE UI SETUP IN DETAIL
        profiler.start_profiling()

        # Get the UI manager
        ui_manager = window.orchestrator.ui_manager

        with profiler.time_operation("Central widget creation"):
            from PyQt6.QtWidgets import QVBoxLayout, QWidget

            central_widget = QWidget()
            central_widget.setStyleSheet("background: transparent;")
            window.setCentralWidget(central_widget)

        with profiler.time_operation("Main layout setup"):
            layout = QVBoxLayout(central_widget)
            layout.setContentsMargins(20, 20, 20, 20)

        with profiler.time_operation("Header layout creation"):
            header_layout = ui_manager.create_header_layout(window)
            layout.addLayout(header_layout)

        with profiler.time_operation("Tab widget creation"):
            tab_widget = ui_manager.create_tab_widget()
            layout.addWidget(tab_widget)

        # Now profile the construct tab creation in detail
        with profiler.time_operation("Construct tab - imports"):
            from presentation.tabs.construct.construct_tab import ConstructTab

        with profiler.time_operation("Construct tab - instantiation"):
            construct_tab = ConstructTab(container, None, None)

        with profiler.time_operation("Construct tab - setup"):
            construct_tab.setup()

        with profiler.time_operation("Tab widget - add construct tab"):
            tab_widget.addTab(construct_tab, "Construct")

        # Profile individual construct tab components
        if hasattr(construct_tab, "layout_manager"):
            layout_mgr = construct_tab.layout_manager

            with profiler.time_operation("Workbench creation"):
                if hasattr(layout_mgr, "_create_workbench_widget"):
                    layout_mgr._create_workbench_widget()

            with profiler.time_operation("Option picker creation"):
                if hasattr(layout_mgr, "_create_option_picker_widget_with_progress"):
                    (
                        layout_mgr._create_option_picker_widget_with_progress()
                    )

            with profiler.time_operation("Graph editor creation"):
                if hasattr(layout_mgr, "_create_graph_editor_widget"):
                    layout_mgr._create_graph_editor_widget()

        # Add placeholder tabs
        with profiler.time_operation("Placeholder tabs creation"):
            ui_manager._add_placeholder_tabs()

        print("\n✅ UI setup profiling complete!")

    except Exception as e:
        print(f"❌ Error during UI profiling: {e}")
        import traceback

        traceback.print_exc()

    finally:
        profiler.end_profiling()


if __name__ == "__main__":
    profile_ui_setup()
