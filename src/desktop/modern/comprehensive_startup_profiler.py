#!/usr/bin/env python3
"""
Comprehensive Startup Profiler - Complete Analysis of TKA Startup Performance

This profiler instruments the entire startup process with detailed timing
for each major component, providing actionable optimization insights.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import sys
import time


# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


class ComprehensiveProfiler:
    """Complete profiler for all startup operations."""

    def __init__(self):
        self.timings = {}
        self.start_time = None
        self.recommendations = []

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
        print("🚀 Starting comprehensive startup profiling...")
        print("=" * 70)

    def end_profiling(self):
        total_time = (time.perf_counter() - self.start_time) * 1000
        print("=" * 70)
        print(f"🎯 TOTAL STARTUP TIME: {total_time:.1f}ms")
        self.analyze_comprehensive_results()

    def analyze_comprehensive_results(self):
        print("\n📊 COMPREHENSIVE STARTUP ANALYSIS")
        print("=" * 50)

        sorted_timings = sorted(self.timings.items(), key=lambda x: x[1], reverse=True)
        total_measured = sum(self.timings.values())

        print("\n🐌 COMPLETE TIMING BREAKDOWN:")
        for name, duration in sorted_timings:
            percentage = (duration / total_measured) * 100
            print(f"   {name:<55} {duration:>8.1f}ms ({percentage:>5.1f}%)")

        # Categorize operations
        categories = {
            "Imports & Setup": ["import", "setup", "creation", "QApplication"],
            "Container & DI": ["container", "service", "registration", "dependency"],
            "UI Components": ["widget", "layout", "tab", "header", "workbench"],
            "Option Picker": ["option", "picker", "pool", "pictograph"],
            "Session & API": ["session", "api", "server", "background"],
        }

        print("\n📈 PERFORMANCE BY CATEGORY:")
        category_totals = {}

        for category, keywords in categories.items():
            category_time = 0
            for name, duration in self.timings.items():
                if any(keyword.lower() in name.lower() for keyword in keywords):
                    category_time += duration

            category_totals[category] = category_time
            percentage = (category_time / total_measured) * 100
            print(f"   {category:<20} {category_time:>8.1f}ms ({percentage:>5.1f}%)")

        # Generate specific recommendations
        self._generate_optimization_recommendations(sorted_timings, category_totals)

    def _generate_optimization_recommendations(self, sorted_timings, category_totals):
        print("\n💡 OPTIMIZATION RECOMMENDATIONS:")

        # Find the heaviest operations
        heavy_operations = [
            (name, duration) for name, duration in sorted_timings if duration > 100
        ]

        if not heavy_operations:
            print("   ✅ No major bottlenecks detected (>100ms)")
            return

        for name, duration in heavy_operations[:5]:  # Top 5 bottlenecks
            name_lower = name.lower()

            if "construct tab" in name_lower:
                print(f"   🎯 CONSTRUCT TAB ({duration:.1f}ms):")
                print("      • Consider lazy loading of construct tab components")
                print("      • Defer option picker initialization until needed")
                print("      • Use progressive loading for workbench components")

            elif "option" in name_lower and "picker" in name_lower:
                print(f"   🎯 OPTION PICKER ({duration:.1f}ms):")
                print("      • Implement lazy loading for pictograph pool")
                print("      • Consider virtual scrolling for large option lists")
                print("      • Cache pictograph frames between sessions")

            elif "pictograph" in name_lower and "pool" in name_lower:
                print(f"   🎯 PICTOGRAPH POOL ({duration:.1f}ms):")
                print("      • Create pool in background thread")
                print("      • Use progressive pool initialization")
                print("      • Implement on-demand pictograph creation")

            elif "api" in name_lower or "server" in name_lower:
                print(f"   🎯 API SERVER ({duration:.1f}ms):")
                print("      • Start API server in background thread")
                print("      • Defer API server startup until after UI is ready")
                print("      • Use async server initialization")

            elif "import" in name_lower:
                print(f"   🎯 IMPORTS ({duration:.1f}ms):")
                print("      • Use lazy imports where possible")
                print("      • Consider import optimization")
                print("      • Profile individual module import times")

        # Category-based recommendations
        heaviest_category = max(category_totals.items(), key=lambda x: x[1])
        if heaviest_category[1] > 200:
            print(
                f"\n   🎯 HEAVIEST CATEGORY: {heaviest_category[0]} ({heaviest_category[1]:.1f}ms)"
            )

            if heaviest_category[0] == "UI Components":
                print("      • Implement progressive UI loading")
                print("      • Use placeholder widgets during initialization")
                print("      • Consider component virtualization")
            elif heaviest_category[0] == "Option Picker":
                print("      • Defer option picker creation until first use")
                print("      • Implement background pool initialization")


def profile_complete_startup():
    """Profile the complete startup process with maximum detail."""
    profiler = ComprehensiveProfiler()
    profiler.start_profiling()

    try:
        # Phase 1: Basic Application Setup
        with profiler.time_operation("1. QApplication setup"):
            from PyQt6.QtWidgets import QApplication

            app = QApplication.instance()
            if not app:
                app = QApplication(sys.argv)
                app.setStyle("Fusion")

        # Phase 2: Core Imports
        with profiler.time_operation("2. Core imports"):
            from PyQt6.QtGui import QGuiApplication

            from desktop.modern.core.application.application_factory import (
                ApplicationFactory,
                ApplicationMode,
            )
            from desktop.modern.presentation.components.ui.splash_screen import (
                SplashScreen,
            )

        # Phase 3: Container & Services
        with profiler.time_operation("3. Container creation"):
            container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

        with profiler.time_operation("4. Service initialization"):
            from desktop.modern.core.service_locator import initialize_services

            initialize_services()

        # Phase 4: Splash Screen
        with profiler.time_operation("5. Splash screen creation"):
            screens = QGuiApplication.screens()
            target_screen = screens[0] if screens else None
            splash = SplashScreen(target_screen=target_screen)

        # Phase 5: Main Window Setup
        with profiler.time_operation("6. Main window imports"):
            from desktop.modern.application.services.core.application_orchestrator import (
                ApplicationOrchestrator,
            )
            from main import TKAMainWindow

        with profiler.time_operation("7. Main window creation"):
            window = TKAMainWindow.__new__(TKAMainWindow)
            super(TKAMainWindow, window).__init__()
            window.hide()

            window.container = container
            window.splash = splash
            window.target_screen = target_screen
            window.parallel_mode = False
            window.parallel_geometry = None

        # Phase 6: Orchestrator Initialization
        with profiler.time_operation("8. Orchestrator creation"):
            window.orchestrator = ApplicationOrchestrator(container=window.container)

        with profiler.time_operation("9. Lifecycle manager"):
            window.orchestrator.lifecycle_manager.initialize_application(
                window, target_screen, False, None, None
            )

        with profiler.time_operation("10. Service registration"):
            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
            )

            window.orchestrator.container = get_container()
            window.orchestrator.service_manager.register_all_services(
                window.orchestrator.container
            )

        # Phase 7: UI Setup (The Big One)
        with profiler.time_operation("11. UI setup - Central widget"):
            from PyQt6.QtWidgets import QVBoxLayout, QWidget

            central_widget = QWidget()
            central_widget.setStyleSheet("background: transparent;")
            window.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)
            layout.setContentsMargins(20, 20, 20, 20)

        with profiler.time_operation("12. UI setup - Header"):
            header_layout = window.orchestrator.ui_manager.create_header_layout(window)
            layout.addLayout(header_layout)

        with profiler.time_operation("13. UI setup - Tab widget"):
            tab_widget = window.orchestrator.ui_manager.create_tab_widget()
            layout.addWidget(tab_widget)

        # Phase 8: Construct Tab (The Biggest Bottleneck)
        with profiler.time_operation("14. Construct tab - Import"):
            from presentation.tabs.construct.construct_tab_widget import (
                ConstructTabWidget,
            )

        with profiler.time_operation("15. Construct tab - Creation"):
            construct_tab = ConstructTabWidget(container, progress_callback=None)

        with profiler.time_operation("16. Construct tab - Setup"):
            construct_tab.setup()

        with profiler.time_operation("17. Tab widget - Add tab"):
            tab_widget.addTab(construct_tab, "🔧 Construct")
            tab_widget.setCurrentIndex(0)

        # Phase 9: Final Steps
        with profiler.time_operation("18. Session restoration"):
            window.orchestrator.lifecycle_manager.trigger_deferred_session_restoration()

        with profiler.time_operation("19. Background setup"):
            window.background_widget = (
                window.orchestrator.background_manager.setup_background(
                    window, window.orchestrator.container, None
                )
            )

        with profiler.time_operation("20. API server startup"):
            window.orchestrator.lifecycle_manager.start_api_server(True)

        print("\n✅ Comprehensive startup profiling complete!")

    except Exception as e:
        print(f"❌ Error during profiling: {e}")
        import traceback

        traceback.print_exc()

    finally:
        profiler.end_profiling()


if __name__ == "__main__":
    profile_complete_startup()
