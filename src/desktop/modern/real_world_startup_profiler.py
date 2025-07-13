#!/usr/bin/env python3
"""
Real-World Startup Profiler - Accurate Wall-Clock Time Measurement

This profiler measures the complete user experience from process launch to fully
interactive application, including all Qt event loop operations, splash screen
animations, and asynchronous initialization phases.

Key Features:
- Wall-clock time measurement from process start to interactive GUI
- Complete Qt event loop integration and timing
- Splash screen animation and fade timing
- Asynchronous initialization phase tracking
- Real window show and activation timing
- Event processing and rendering measurement
"""

import os
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional

import psutil
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication

# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

# Environment variable to enable/disable profiling
PROFILING_ENABLED = os.getenv("TKA_REAL_WORLD_PROFILING", "1").lower() in (
    "1",
    "true",
    "yes",
)


@dataclass
class RealWorldMetric:
    """Represents a real-world performance measurement with wall-clock timing."""

    name: str
    start_time: float
    end_time: float
    duration_ms: float
    memory_before_mb: float
    memory_after_mb: float
    memory_delta_mb: float
    wall_clock_from_start: float
    phase: str = "unknown"
    user_visible: bool = False
    blocking_operation: bool = True


@dataclass
class StartupPhase:
    """Represents a major startup phase with multiple operations."""

    name: str
    start_time: float
    end_time: Optional[float] = None
    operations: List[RealWorldMetric] = field(default_factory=list)
    user_visible: bool = False

    @property
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0.0


class RealWorldStartupProfiler(QObject):
    """
    Real-world startup profiler that measures complete user experience.

    This profiler integrates with the Qt event loop and measures the actual
    wall-clock time from application launch to fully interactive GUI.
    """

    # Signals for tracking async operations
    phase_started = pyqtSignal(str)
    phase_completed = pyqtSignal(str)
    window_shown = pyqtSignal()
    application_ready = pyqtSignal()

    def __init__(self, enabled: bool = PROFILING_ENABLED):
        super().__init__()
        self.enabled = enabled
        self.process_start_time = time.perf_counter()
        self.metrics: Dict[str, RealWorldMetric] = {}
        self.phases: Dict[str, StartupPhase] = {}
        self.current_phase: Optional[str] = None
        self.process = psutil.Process()

        # Critical timing milestones
        self.splash_visible_time: Optional[float] = None
        self.splash_animation_complete_time: Optional[float] = None
        self.main_window_created_time: Optional[float] = None
        self.main_window_shown_time: Optional[float] = None
        self.application_interactive_time: Optional[float] = None

        # Event loop integration
        self.event_loop_started: bool = False
        self.event_loop_start_time: Optional[float] = None

        if self.enabled:
            print("🌍 Real-World Startup Profiler ENABLED")
            print("   Measuring complete user experience from process start")
            print(f"   Process start time: {self.process_start_time}")
        else:
            print("⚪ Real-World Startup Profiler DISABLED")

    def _get_memory_usage_mb(self) -> float:
        """Get current memory usage in MB."""
        if not self.enabled:
            return 0.0
        try:
            return self.process.memory_info().rss / 1024 / 1024
        except:
            return 0.0

    def _get_wall_clock_from_start(self) -> float:
        """Get wall-clock time in milliseconds from process start."""
        return (time.perf_counter() - self.process_start_time) * 1000

    def start_phase(self, phase_name: str, user_visible: bool = False):
        """Start a new startup phase."""
        if not self.enabled:
            return

        current_time = time.perf_counter()
        wall_clock = self._get_wall_clock_from_start()

        # End previous phase if exists
        if self.current_phase and self.current_phase in self.phases:
            self.phases[self.current_phase].end_time = current_time

        # Start new phase
        phase = StartupPhase(
            name=phase_name, start_time=current_time, user_visible=user_visible
        )
        self.phases[phase_name] = phase
        self.current_phase = phase_name

        print(f"🚀 PHASE START: {phase_name} (t+{wall_clock:.1f}ms)")
        self.phase_started.emit(phase_name)

    def end_phase(self, phase_name: str):
        """End a startup phase."""
        if not self.enabled or phase_name not in self.phases:
            return

        current_time = time.perf_counter()
        wall_clock = self._get_wall_clock_from_start()

        phase = self.phases[phase_name]
        phase.end_time = current_time

        print(
            f"✅ PHASE END: {phase_name} (t+{wall_clock:.1f}ms, duration: {phase.duration_ms:.1f}ms)"
        )
        self.phase_completed.emit(phase_name)

        if self.current_phase == phase_name:
            self.current_phase = None

    @contextmanager
    def time_operation(
        self, operation_name: str, user_visible: bool = False, blocking: bool = True
    ):
        """Context manager for timing operations with real-world context."""
        if not self.enabled:
            yield
            return

        start_time = time.perf_counter()
        memory_before = self._get_memory_usage_mb()
        wall_clock_start = self._get_wall_clock_from_start()

        try:
            yield
        finally:
            end_time = time.perf_counter()
            memory_after = self._get_memory_usage_mb()
            duration_ms = (end_time - start_time) * 1000
            wall_clock_end = self._get_wall_clock_from_start()

            metric = RealWorldMetric(
                name=operation_name,
                start_time=start_time,
                end_time=end_time,
                duration_ms=duration_ms,
                memory_before_mb=memory_before,
                memory_after_mb=memory_after,
                memory_delta_mb=memory_after - memory_before,
                wall_clock_from_start=wall_clock_start,
                phase=self.current_phase or "unknown",
                user_visible=user_visible,
                blocking_operation=blocking,
            )

            self.metrics[operation_name] = metric

            # Add to current phase
            if self.current_phase and self.current_phase in self.phases:
                self.phases[self.current_phase].operations.append(metric)

            # Real-time output with wall-clock context
            memory_info = (
                f" (+{memory_after - memory_before:.1f}MB)"
                if memory_after - memory_before > 1
                else ""
            )
            visibility = " [USER VISIBLE]" if user_visible else ""
            blocking_info = " [NON-BLOCKING]" if not blocking else ""

            print(
                f"⏱️  t+{wall_clock_end:.1f}ms: {operation_name}: {duration_ms:.1f}ms{memory_info}{visibility}{blocking_info}"
            )

    def mark_milestone(self, milestone_name: str, user_visible: bool = True):
        """Mark a critical timing milestone."""
        if not self.enabled:
            return

        current_time = time.perf_counter()
        wall_clock = self._get_wall_clock_from_start()

        # Store milestone timing
        if milestone_name == "splash_visible":
            self.splash_visible_time = current_time
        elif milestone_name == "splash_animation_complete":
            self.splash_animation_complete_time = current_time
        elif milestone_name == "main_window_created":
            self.main_window_created_time = current_time
        elif milestone_name == "main_window_shown":
            self.main_window_shown_time = current_time
            self.window_shown.emit()
        elif milestone_name == "application_interactive":
            self.application_interactive_time = current_time
            self.application_ready.emit()
        elif milestone_name == "event_loop_started":
            self.event_loop_started = True
            self.event_loop_start_time = current_time

        visibility = " [USER VISIBLE]" if user_visible else ""
        print(f"🎯 MILESTONE: {milestone_name} (t+{wall_clock:.1f}ms){visibility}")

    def track_event_processing(self, operation_name: str):
        """Track Qt event processing operations."""
        if not self.enabled:
            return

        wall_clock = self._get_wall_clock_from_start()
        print(f"🔄 EVENT PROCESSING: {operation_name} (t+{wall_clock:.1f}ms)")

    def track_async_operation(self, operation_name: str, delay_ms: int = 0):
        """Track asynchronous operations like QTimer.singleShot."""
        if not self.enabled:
            return

        wall_clock = self._get_wall_clock_from_start()
        delay_info = f" (delay: {delay_ms}ms)" if delay_ms > 0 else ""
        print(
            f"⏰ ASYNC OPERATION: {operation_name} (t+{wall_clock:.1f}ms){delay_info}"
        )

    def generate_real_world_report(self):
        """Generate comprehensive real-world performance report."""
        if not self.enabled:
            return

        total_time = self._get_wall_clock_from_start()

        print("\n" + "=" * 80)
        print("🌍 REAL-WORLD STARTUP PERFORMANCE ANALYSIS")
        print("=" * 80)
        print(f"🎯 TOTAL WALL-CLOCK TIME: {total_time:.1f}ms")
        print(f"💾 Final Memory Usage: {self._get_memory_usage_mb():.1f}MB")

        # Critical milestones analysis
        print("\n🎯 CRITICAL MILESTONES:")
        milestones = [
            ("Process Start", 0.0, False),
            ("Splash Visible", self.splash_visible_time, True),
            ("Splash Animation Complete", self.splash_animation_complete_time, True),
            ("Event Loop Started", self.event_loop_start_time, False),
            ("Main Window Created", self.main_window_created_time, False),
            ("Main Window Shown", self.main_window_shown_time, True),
            ("Application Interactive", self.application_interactive_time, True),
        ]

        for name, timestamp, user_visible in milestones:
            if timestamp is not None:
                wall_clock = (
                    (timestamp - self.process_start_time) * 1000
                    if timestamp > 0
                    else 0.0
                )
                visibility = " [USER VISIBLE]" if user_visible else ""
                print(f"   {name:<25} t+{wall_clock:>8.1f}ms{visibility}")

        # Phase analysis
        print("\n📊 STARTUP PHASES:")
        for phase_name, phase in self.phases.items():
            if phase.end_time:
                wall_clock_start = (phase.start_time - self.process_start_time) * 1000
                visibility = " [USER VISIBLE]" if phase.user_visible else ""
                print(
                    f"   {phase_name:<25} {phase.duration_ms:>8.1f}ms (t+{wall_clock_start:.1f}ms){visibility}"
                )

        # User experience analysis
        self._analyze_user_experience()

        # Performance bottlenecks
        self._analyze_real_world_bottlenecks()

        # Recommendations
        self._generate_real_world_recommendations()

    def _analyze_user_experience(self):
        """Analyze user experience metrics."""
        print("\n👤 USER EXPERIENCE ANALYSIS:")

        if self.splash_visible_time:
            time_to_splash = (self.splash_visible_time - self.process_start_time) * 1000
            print(f"   ⏱️  Time to splash screen: {time_to_splash:.1f}ms")

            if time_to_splash < 500:
                print("   ✅ Excellent responsiveness - splash appears quickly")
            elif time_to_splash < 1000:
                print("   ✅ Good responsiveness - splash appears reasonably fast")
            else:
                print("   ⚠️  Slow responsiveness - splash takes too long to appear")

        if self.main_window_shown_time:
            time_to_window = (
                self.main_window_shown_time - self.process_start_time
            ) * 1000
            print(f"   🎯 Time to interactive window: {time_to_window:.1f}ms")

            if time_to_window < 3000:
                print("   ✅ Excellent startup performance")
            elif time_to_window < 5000:
                print("   ✅ Good startup performance")
            elif time_to_window < 8000:
                print("   ⚠️  Acceptable startup performance")
            else:
                print("   ❌ Poor startup performance - requires optimization")

        # Analyze gaps between milestones
        if self.splash_visible_time and self.main_window_shown_time:
            loading_time = (
                self.main_window_shown_time - self.splash_visible_time
            ) * 1000
            print(f"   📊 Loading time (splash to window): {loading_time:.1f}ms")

    def _analyze_real_world_bottlenecks(self):
        """Analyze real-world performance bottlenecks."""
        print("\n⚠️  REAL-WORLD BOTTLENECKS:")

        # Sort operations by duration
        sorted_metrics = sorted(
            self.metrics.values(), key=lambda x: x.duration_ms, reverse=True
        )

        bottlenecks = [m for m in sorted_metrics if m.duration_ms > 100]
        if bottlenecks:
            for metric in bottlenecks[:10]:
                wall_clock = metric.wall_clock_from_start
                visibility = " [USER VISIBLE]" if metric.user_visible else ""
                blocking = (
                    " [BLOCKING]" if metric.blocking_operation else " [NON-BLOCKING]"
                )
                print(
                    f"   • {metric.name:<40} {metric.duration_ms:>8.1f}ms (t+{wall_clock:.1f}ms){visibility}{blocking}"
                )
        else:
            print("   ✅ No major bottlenecks detected (>100ms)")

    def _generate_real_world_recommendations(self):
        """Generate real-world optimization recommendations."""
        print("\n💡 REAL-WORLD OPTIMIZATION RECOMMENDATIONS:")

        recommendations = []

        # Analyze time to splash
        if self.splash_visible_time:
            time_to_splash = (self.splash_visible_time - self.process_start_time) * 1000
            if time_to_splash > 1000:
                recommendations.append("🎯 SPLASH SCREEN RESPONSIVENESS:")
                recommendations.append(
                    "   • Optimize imports before splash screen creation"
                )
                recommendations.append(
                    "   • Consider showing splash earlier in startup process"
                )
                recommendations.append(
                    "   • Move heavy initialization after splash is visible"
                )

        # Analyze loading time
        if self.splash_visible_time and self.main_window_shown_time:
            loading_time = (
                self.main_window_shown_time - self.splash_visible_time
            ) * 1000
            if loading_time > 5000:
                recommendations.append("🎯 LOADING TIME OPTIMIZATION:")
                recommendations.append(
                    "   • Implement progressive loading of UI components"
                )
                recommendations.append(
                    "   • Use background threads for non-UI initialization"
                )
                recommendations.append("   • Consider lazy loading of heavy components")

        # Analyze blocking operations during user-visible phases
        user_visible_blocking = [
            m
            for m in self.metrics.values()
            if m.user_visible and m.blocking_operation and m.duration_ms > 200
        ]

        if user_visible_blocking:
            recommendations.append("🎯 USER-VISIBLE BLOCKING OPERATIONS:")
            for metric in user_visible_blocking[:5]:
                recommendations.append(
                    f"   • {metric.name}: Consider making non-blocking ({metric.duration_ms:.1f}ms)"
                )

        if not recommendations:
            recommendations.append("✅ No major optimization opportunities identified")
            recommendations.append(
                "   Current real-world performance appears well-optimized"
            )

        for rec in recommendations:
            print(f"   {rec}")


# Global profiler instance
real_world_profiler = RealWorldStartupProfiler()
