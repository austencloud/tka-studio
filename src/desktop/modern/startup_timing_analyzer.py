#!/usr/bin/env python3
"""
Startup Timing Analyzer - Detailed Performance Profiling for TKA Startup

This tool provides comprehensive timing analysis of the TKA application startup process,
measuring individual function calls and identifying performance bottlenecks.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
import sys
import time


# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


@dataclass
class TimingResult:
    """Represents timing data for a single operation."""

    name: str
    duration_ms: float
    start_time: float
    end_time: float
    parent: str | None = None
    children: list[str] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


class StartupTimingAnalyzer:
    """
    Comprehensive timing analyzer for TKA startup process.

    Provides detailed timing measurements for each phase of startup,
    identifies bottlenecks, and generates performance reports.
    """

    def __init__(self):
        self.timings: dict[str, TimingResult] = {}
        self.operation_stack: list[str] = []
        self.total_start_time = None
        self.phase_times: dict[str, float] = {}

    @contextmanager
    def time_operation(self, operation_name: str, parent: str | None = None):
        """Context manager for timing operations."""
        start_time = time.perf_counter()

        # Set up parent-child relationship
        if parent and parent in self.timings:
            self.timings[parent].children.append(operation_name)
        elif self.operation_stack:
            current_parent = self.operation_stack[-1]
            if current_parent in self.timings:
                self.timings[current_parent].children.append(operation_name)
                parent = current_parent

        self.operation_stack.append(operation_name)

        try:
            yield
        finally:
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000

            self.timings[operation_name] = TimingResult(
                name=operation_name,
                duration_ms=duration_ms,
                start_time=start_time,
                end_time=end_time,
                parent=parent,
            )

            self.operation_stack.pop()

            print(f"⏱️  {operation_name}: {duration_ms:.1f}ms")

    def start_total_timing(self):
        """Start timing the entire startup process."""
        self.total_start_time = time.perf_counter()
        print("🚀 Starting TKA startup timing analysis...")
        print("=" * 60)

    def end_total_timing(self):
        """End timing and generate report."""
        if self.total_start_time:
            total_time = (time.perf_counter() - self.total_start_time) * 1000
            print("=" * 60)
            print(f"🎯 TOTAL STARTUP TIME: {total_time:.1f}ms")
            self.generate_performance_report()

    def generate_performance_report(self):
        """Generate comprehensive performance analysis report."""
        print("\n📊 STARTUP PERFORMANCE ANALYSIS")
        print("=" * 50)

        # Sort operations by duration
        sorted_operations = sorted(
            self.timings.values(), key=lambda x: x.duration_ms, reverse=True
        )

        print("\n🐌 SLOWEST OPERATIONS:")
        for i, timing in enumerate(sorted_operations[:10], 1):
            percentage = (
                timing.duration_ms / sum(t.duration_ms for t in self.timings.values())
            ) * 100
            print(
                f"{i:2d}. {timing.name:<40} {timing.duration_ms:>8.1f}ms ({percentage:>5.1f}%)"
            )

        # Identify bottlenecks
        print("\n⚠️  PERFORMANCE BOTTLENECKS:")
        bottlenecks = [t for t in sorted_operations if t.duration_ms > 500]
        if bottlenecks:
            for timing in bottlenecks:
                print(f"   • {timing.name}: {timing.duration_ms:.1f}ms")
        else:
            print("   ✅ No major bottlenecks detected (>500ms)")

        # Phase analysis
        self._analyze_phases()

        # Recommendations
        self._generate_recommendations(sorted_operations)

    def _analyze_phases(self):
        """Analyze timing by startup phases."""
        phases = {
            "Initialization": [
                "QApplication creation",
                "ApplicationFactory",
                "Container creation",
            ],
            "Service Registration": [
                "Service registration",
                "DI container",
                "Event system",
            ],
            "UI Setup": [
                "UI creation",
                "Tab widget",
                "Option picker",
                "Pictograph pool",
            ],
            "Session & Background": ["Session restoration", "Background setup"],
        }

        print("\n📈 PHASE ANALYSIS:")
        phase_totals = {}

        for phase_name, keywords in phases.items():
            phase_time = 0
            for timing in self.timings.values():
                if any(keyword.lower() in timing.name.lower() for keyword in keywords):
                    phase_time += timing.duration_ms

            phase_totals[phase_name] = phase_time
            print(f"   {phase_name:<20} {phase_time:>8.1f}ms")

        # Find heaviest phase
        heaviest_phase = max(phase_totals.items(), key=lambda x: x[1])
        print(f"\n🎯 HEAVIEST PHASE: {heaviest_phase[0]} ({heaviest_phase[1]:.1f}ms)")

    def _generate_recommendations(self, sorted_operations: list[TimingResult]):
        """Generate performance improvement recommendations."""
        print("\n💡 OPTIMIZATION RECOMMENDATIONS:")

        # Check for specific patterns
        slow_operations = [t for t in sorted_operations if t.duration_ms > 200]

        recommendations = []

        for timing in slow_operations:
            name_lower = timing.name.lower()

            if "pictograph" in name_lower and "pool" in name_lower:
                recommendations.append(
                    f"• Consider lazy loading pictograph pool (currently {timing.duration_ms:.1f}ms)"
                )
            elif "service" in name_lower and "registration" in name_lower:
                recommendations.append(
                    f"• Optimize service registration - consider parallel registration ({timing.duration_ms:.1f}ms)"
                )
            elif "session" in name_lower:
                recommendations.append(
                    f"• Session operations could be deferred ({timing.duration_ms:.1f}ms)"
                )
            elif "ui" in name_lower or "widget" in name_lower:
                recommendations.append(
                    f"• UI creation could be optimized or deferred ({timing.duration_ms:.1f}ms)"
                )

        if not recommendations:
            recommendations.append("✅ No major optimization opportunities identified")

        for rec in recommendations:
            print(f"   {rec}")


# Global analyzer instance
analyzer = StartupTimingAnalyzer()


def time_function_calls():
    """Instrument key functions with timing."""
    analyzer.start_total_timing()

    try:
        # Time QApplication creation
        with analyzer.time_operation("QApplication creation"):
            from PyQt6.QtWidgets import QApplication

            app = QApplication.instance()
            if not app:
                app = QApplication(sys.argv)
                app.setStyle("Fusion")

        # Time ApplicationFactory import and creation
        with analyzer.time_operation("ApplicationFactory import"):
            from desktop.modern.core.application.application_factory import (
                ApplicationFactory,
                ApplicationMode,
            )

        with analyzer.time_operation("Container creation"):
            container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

        # Time service initialization
        with analyzer.time_operation("Event-driven services initialization"):
            from desktop.modern.core.service_locator import initialize_services

            initialize_services()

        # Time splash screen creation
        with analyzer.time_operation("SplashScreen creation"):
            from PyQt6.QtGui import QGuiApplication

            from desktop.modern.presentation.components.ui.splash_screen import (
                SplashScreen,
            )

            screens = QGuiApplication.screens()
            target_screen = screens[0] if screens else None
            splash = SplashScreen(target_screen=target_screen)

        # Time main window creation with detailed breakdown
        with analyzer.time_operation("TKAMainWindow creation"):
            from main import TKAMainWindow

            # Instrument the TKAMainWindow creation process
            original_init = TKAMainWindow.__init__

            def instrumented_init(self, *args, **kwargs):
                with analyzer.time_operation(
                    "TKAMainWindow.__init__", "TKAMainWindow creation"
                ):
                    # Time orchestrator creation
                    if len(args) > 0 or "container" in kwargs:
                        container_arg = args[0] if args else kwargs.get("container")
                        if container_arg:
                            with analyzer.time_operation(
                                "ApplicationOrchestrator import",
                                "TKAMainWindow.__init__",
                            ):
                                from desktop.modern.application.services.core.application_orchestrator import (
                                    ApplicationOrchestrator,
                                )

                            with analyzer.time_operation(
                                "ApplicationOrchestrator creation",
                                "TKAMainWindow.__init__",
                            ):
                                ApplicationOrchestrator(
                                    container=container_arg
                                )

                            with analyzer.time_operation(
                                "orchestrator.initialize_application",
                                "TKAMainWindow.__init__",
                            ):
                                # Call original init but intercept orchestrator initialization
                                original_init(self, *args, **kwargs)
                        else:
                            original_init(self, *args, **kwargs)
                    else:
                        original_init(self, *args, **kwargs)

            # Temporarily replace the __init__ method
            TKAMainWindow.__init__ = instrumented_init

            try:
                TKAMainWindow(
                    container=container,
                    splash_screen=splash,
                    target_screen=target_screen,
                    parallel_mode=False,
                    parallel_geometry=None,
                )
            finally:
                # Restore original __init__
                TKAMainWindow.__init__ = original_init

        print("\n🎯 Startup timing analysis complete!")

    except Exception as e:
        print(f"❌ Error during timing analysis: {e}")
        import traceback

        traceback.print_exc()

    finally:
        analyzer.end_total_timing()


if __name__ == "__main__":
    time_function_calls()
