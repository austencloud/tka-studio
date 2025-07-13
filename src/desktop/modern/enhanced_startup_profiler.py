#!/usr/bin/env python3
"""
Enhanced Startup Performance Profiler - Comprehensive TKA Startup Analysis

This profiler provides detailed performance analysis of the TKA application startup,
including timing instrumentation, splash screen progress correlation, memory usage
tracking, and user experience validation.

Features:
- Detailed timing of all startup operations
- Progress bar correlation with actual work completion
- Memory usage tracking for memory-intensive operations
- Critical path analysis and bottleneck identification
- Production-ready toggle system
- User experience validation metrics
"""

import gc
import logging
import os
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import psutil
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

# Environment variable to enable/disable profiling
PROFILING_ENABLED = os.getenv("TKA_STARTUP_PROFILING", "1").lower() in (
    "1",
    "true",
    "yes",
)


@dataclass
class PerformanceMetric:
    """Represents a single performance measurement."""

    name: str
    start_time: float
    end_time: float
    duration_ms: float
    memory_before_mb: float
    memory_after_mb: float
    memory_delta_mb: float
    progress_before: int = 0
    progress_after: int = 0
    message: str = ""
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)


@dataclass
class ProgressUpdate:
    """Represents a progress bar update."""

    timestamp: float
    progress: int
    message: str
    operation_context: str = ""


class EnhancedStartupProfiler:
    """
    Comprehensive startup profiler with detailed instrumentation.

    Provides timing analysis, memory tracking, progress correlation,
    and user experience validation for TKA startup process.
    """

    def __init__(self, enabled: bool = PROFILING_ENABLED):
        self.enabled = enabled
        self.metrics: Dict[str, PerformanceMetric] = {}
        self.progress_updates: List[ProgressUpdate] = []
        self.operation_stack: List[str] = []
        self.total_start_time: Optional[float] = None
        self.current_operation: Optional[str] = None
        self.process = psutil.Process()

        # Critical path tracking
        self.critical_path: List[str] = []
        self.bottlenecks: List[Tuple[str, float]] = []

        # User experience metrics
        self.splash_visible_time: Optional[float] = None
        self.first_progress_time: Optional[float] = None
        self.last_progress_time: Optional[float] = None
        self.window_show_time: Optional[float] = None

        if self.enabled:
            print("🔍 Enhanced Startup Profiler ENABLED")
            print("   Set TKA_STARTUP_PROFILING=0 to disable")
        else:
            print("⚪ Enhanced Startup Profiler DISABLED")

    def _get_memory_usage_mb(self) -> float:
        """Get current memory usage in MB."""
        if not self.enabled:
            return 0.0
        try:
            return self.process.memory_info().rss / 1024 / 1024
        except:
            return 0.0

    @contextmanager
    def time_operation(self, operation_name: str, parent: Optional[str] = None):
        """Context manager for timing operations with memory tracking."""
        if not self.enabled:
            yield
            return

        # Set up parent-child relationship
        if parent and parent in self.metrics:
            self.metrics[parent].children.append(operation_name)
        elif self.operation_stack:
            current_parent = self.operation_stack[-1]
            if current_parent in self.metrics:
                self.metrics[current_parent].children.append(operation_name)
                parent = current_parent

        self.operation_stack.append(operation_name)
        self.current_operation = operation_name

        # Capture initial state
        start_time = time.perf_counter()
        memory_before = self._get_memory_usage_mb()

        try:
            yield
        finally:
            # Capture final state
            end_time = time.perf_counter()
            memory_after = self._get_memory_usage_mb()
            duration_ms = (end_time - start_time) * 1000

            # Create metric
            metric = PerformanceMetric(
                name=operation_name,
                start_time=start_time,
                end_time=end_time,
                duration_ms=duration_ms,
                memory_before_mb=memory_before,
                memory_after_mb=memory_after,
                memory_delta_mb=memory_after - memory_before,
                parent=parent,
            )

            self.metrics[operation_name] = metric
            self.operation_stack.pop()
            self.current_operation = (
                self.operation_stack[-1] if self.operation_stack else None
            )

            # Track bottlenecks
            if duration_ms > 100:  # Operations > 100ms
                self.bottlenecks.append((operation_name, duration_ms))

            # Real-time output
            memory_info = (
                f" (+{memory_after - memory_before:.1f}MB)"
                if memory_after - memory_before > 1
                else ""
            )
            print(f"⏱️  {operation_name}: {duration_ms:.1f}ms{memory_info}")

    def track_progress_update(self, progress: int, message: str):
        """Track a progress bar update."""
        if not self.enabled:
            return

        timestamp = time.perf_counter()
        update = ProgressUpdate(
            timestamp=timestamp,
            progress=progress,
            message=message,
            operation_context=self.current_operation or "Unknown",
        )
        self.progress_updates.append(update)

        # Track timing milestones
        if self.first_progress_time is None:
            self.first_progress_time = timestamp
        self.last_progress_time = timestamp

        # Update current operation's progress info
        if self.current_operation and self.current_operation in self.metrics:
            metric = self.metrics[self.current_operation]
            if metric.progress_before == 0:
                metric.progress_before = progress
                metric.message = message
            metric.progress_after = progress

    def start_profiling(self):
        """Start the profiling session."""
        if not self.enabled:
            return

        self.total_start_time = time.perf_counter()
        print("🚀 ENHANCED STARTUP PROFILING SESSION STARTED")
        print("=" * 70)
        print(f"📊 Process ID: {os.getpid()}")
        print(f"💾 Initial Memory: {self._get_memory_usage_mb():.1f}MB")
        print(f"🐍 Python Version: {sys.version.split()[0]}")
        print("=" * 70)

    def mark_splash_visible(self):
        """Mark when splash screen becomes visible."""
        if self.enabled:
            self.splash_visible_time = time.perf_counter()

    def mark_window_shown(self):
        """Mark when main window is shown."""
        if self.enabled:
            self.window_show_time = time.perf_counter()

    def end_profiling(self):
        """End profiling and generate comprehensive report."""
        if not self.enabled:
            return

        total_time = (time.perf_counter() - self.total_start_time) * 1000
        print("=" * 70)
        print(f"🎯 TOTAL STARTUP TIME: {total_time:.1f}ms")
        print(f"💾 Final Memory: {self._get_memory_usage_mb():.1f}MB")
        print("=" * 70)

        self._generate_comprehensive_report()
        self._analyze_user_experience()
        self._analyze_progress_correlation()
        self._generate_optimization_recommendations()

    def _generate_comprehensive_report(self):
        """Generate detailed performance analysis report."""
        if not self.enabled:
            return

        print("\n📊 COMPREHENSIVE PERFORMANCE ANALYSIS")
        print("=" * 50)

        # Sort operations by duration
        sorted_metrics = sorted(
            self.metrics.values(), key=lambda x: x.duration_ms, reverse=True
        )

        print("\n🐌 SLOWEST OPERATIONS:")
        total_measured = sum(m.duration_ms for m in self.metrics.values())

        for i, metric in enumerate(sorted_metrics[:15], 1):
            percentage = (metric.duration_ms / total_measured) * 100
            memory_info = (
                f" (+{metric.memory_delta_mb:.1f}MB)"
                if metric.memory_delta_mb > 1
                else ""
            )
            progress_info = ""
            if metric.progress_before != metric.progress_after:
                progress_info = f" [{metric.progress_before}%→{metric.progress_after}%]"

            print(
                f"{i:2d}. {metric.name:<45} {metric.duration_ms:>8.1f}ms ({percentage:>5.1f}%){memory_info}{progress_info}"
            )

        # Memory analysis
        print("\n💾 MEMORY USAGE ANALYSIS:")
        memory_intensive = [m for m in sorted_metrics if m.memory_delta_mb > 5]
        if memory_intensive:
            for metric in memory_intensive[:10]:
                print(f"   • {metric.name:<45} +{metric.memory_delta_mb:>6.1f}MB")
        else:
            print("   ✅ No major memory allocations detected (>5MB)")

        # Bottleneck analysis
        print("\n⚠️  PERFORMANCE BOTTLENECKS:")
        if self.bottlenecks:
            for name, duration in sorted(
                self.bottlenecks, key=lambda x: x[1], reverse=True
            )[:10]:
                print(f"   • {name:<45} {duration:>8.1f}ms")
        else:
            print("   ✅ No major bottlenecks detected (>100ms)")

    def _analyze_user_experience(self):
        """Analyze user experience metrics."""
        if not self.enabled:
            return

        print("\n👤 USER EXPERIENCE ANALYSIS:")

        if self.splash_visible_time and self.first_progress_time:
            time_to_first_progress = (
                self.first_progress_time - self.splash_visible_time
            ) * 1000
            print(
                f"   ⏱️  Time to first progress update: {time_to_first_progress:.1f}ms"
            )

            if time_to_first_progress > 500:
                print("   ⚠️  WARNING: Long delay before first progress update")
            else:
                print("   ✅ Good responsiveness to first progress update")

        if self.first_progress_time and self.last_progress_time:
            progress_duration = (
                self.last_progress_time - self.first_progress_time
            ) * 1000
            print(f"   📊 Total progress bar duration: {progress_duration:.1f}ms")

            # Analyze progress update frequency
            if len(self.progress_updates) > 1:
                intervals = []
                for i in range(1, len(self.progress_updates)):
                    interval = (
                        self.progress_updates[i].timestamp
                        - self.progress_updates[i - 1].timestamp
                    ) * 1000
                    intervals.append(interval)

                avg_interval = sum(intervals) / len(intervals)
                max_interval = max(intervals)

                print(f"   📈 Average progress interval: {avg_interval:.1f}ms")
                print(f"   📈 Maximum progress interval: {max_interval:.1f}ms")

                if max_interval > 2000:
                    print("   ⚠️  WARNING: Long pause in progress updates detected")
                elif avg_interval < 100:
                    print("   ✅ Smooth progress bar updates")
                else:
                    print("   ✅ Reasonable progress update frequency")

        if self.window_show_time and self.total_start_time:
            total_perceived_time = (
                self.window_show_time - self.total_start_time
            ) * 1000
            print(f"   🎯 Total perceived startup time: {total_perceived_time:.1f}ms")

            if total_perceived_time < 3000:
                print("   ✅ Excellent startup performance")
            elif total_perceived_time < 5000:
                print("   ✅ Good startup performance")
            elif total_perceived_time < 8000:
                print("   ⚠️  Acceptable startup performance")
            else:
                print("   ❌ Poor startup performance - optimization needed")

    def _analyze_progress_correlation(self):
        """Analyze correlation between progress updates and actual work."""
        if not self.enabled or not self.progress_updates:
            return

        print("\n📊 PROGRESS BAR CORRELATION ANALYSIS:")

        print(f"   📈 Total progress updates: {len(self.progress_updates)}")

        # Check for logical progress increments
        progress_values = [update.progress for update in self.progress_updates]
        if len(progress_values) > 1:
            increments = [
                progress_values[i] - progress_values[i - 1]
                for i in range(1, len(progress_values))
            ]
            avg_increment = sum(increments) / len(increments)

            print(f"   📊 Average progress increment: {avg_increment:.1f}%")

            # Check for reasonable increments
            large_jumps = [inc for inc in increments if inc > 20]
            if large_jumps:
                print(
                    f"   ⚠️  WARNING: {len(large_jumps)} large progress jumps detected"
                )
            else:
                print("   ✅ Smooth progress increments")

        # Show detailed progress timeline
        print("\n   📋 PROGRESS TIMELINE:")
        for i, update in enumerate(self.progress_updates):
            if i == 0:
                time_since_start = 0
            else:
                time_since_start = (
                    update.timestamp - self.progress_updates[0].timestamp
                ) * 1000

            print(
                f"      {update.progress:3d}% (+{time_since_start:6.0f}ms) {update.message}"
            )
            if update.operation_context != "Unknown":
                print(f"           └─ During: {update.operation_context}")

    def _generate_optimization_recommendations(self):
        """Generate specific optimization recommendations."""
        if not self.enabled:
            return

        print("\n💡 OPTIMIZATION RECOMMENDATIONS:")

        recommendations = []

        # Analyze bottlenecks for specific recommendations
        for name, duration in self.bottlenecks:
            name_lower = name.lower()

            if "pictograph" in name_lower and "pool" in name_lower:
                recommendations.append(f"🎯 PICTOGRAPH POOL ({duration:.1f}ms):")
                recommendations.append(
                    "   • Consider lazy loading - create pool in background thread"
                )
                recommendations.append("   • Implement progressive pool initialization")
                recommendations.append(
                    "   • Use on-demand pictograph creation for rarely used items"
                )

            elif "construct" in name_lower and "tab" in name_lower:
                recommendations.append(f"🎯 CONSTRUCT TAB ({duration:.1f}ms):")
                recommendations.append(
                    "   • Defer option picker initialization until first use"
                )
                recommendations.append(
                    "   • Use placeholder widgets during initial load"
                )
                recommendations.append("   • Consider progressive component loading")

            elif "option" in name_lower and "picker" in name_lower:
                recommendations.append(f"🎯 OPTION PICKER ({duration:.1f}ms):")
                recommendations.append(
                    "   • Implement virtual scrolling for large option lists"
                )
                recommendations.append("   • Cache pictograph frames between sessions")
                recommendations.append("   • Use background loading for option data")

            elif "service" in name_lower and "registration" in name_lower:
                recommendations.append(f"🎯 SERVICE REGISTRATION ({duration:.1f}ms):")
                recommendations.append("   • Consider parallel service registration")
                recommendations.append("   • Optimize dependency injection container")
                recommendations.append("   • Use lazy service initialization")

            elif "session" in name_lower:
                recommendations.append(f"🎯 SESSION OPERATIONS ({duration:.1f}ms):")
                recommendations.append(
                    "   • Defer session restoration until after UI is ready"
                )
                recommendations.append("   • Use background thread for session loading")
                recommendations.append("   • Implement incremental session restoration")

        # Memory-based recommendations
        memory_intensive = [m for m in self.metrics.values() if m.memory_delta_mb > 10]
        if memory_intensive:
            recommendations.append("\n🧠 MEMORY OPTIMIZATION:")
            for metric in memory_intensive[:5]:
                recommendations.append(
                    f"   • {metric.name}: Consider memory pooling (+{metric.memory_delta_mb:.1f}MB)"
                )

        # Progress-based recommendations
        if self.progress_updates:
            long_gaps = []
            for i in range(1, len(self.progress_updates)):
                gap = (
                    self.progress_updates[i].timestamp
                    - self.progress_updates[i - 1].timestamp
                ) * 1000
                if gap > 1000:  # Gaps > 1 second
                    long_gaps.append(
                        (
                            gap,
                            self.progress_updates[i - 1].message,
                            self.progress_updates[i].message,
                        )
                    )

            if long_gaps:
                recommendations.append("\n📊 PROGRESS BAR IMPROVEMENTS:")
                for gap, before_msg, after_msg in long_gaps[:3]:
                    recommendations.append(
                        f"   • Add intermediate progress between '{before_msg}' and '{after_msg}' ({gap:.0f}ms gap)"
                    )

        # General recommendations based on total time
        if self.total_start_time:
            total_time = (time.perf_counter() - self.total_start_time) * 1000
            if total_time > 5000:
                recommendations.append("\n⚡ GENERAL PERFORMANCE:")
                recommendations.append(
                    "   • Consider implementing splash screen preloader"
                )
                recommendations.append(
                    "   • Use background threads for non-UI initialization"
                )
                recommendations.append("   • Implement progressive application loading")

        if not recommendations:
            recommendations.append("✅ No major optimization opportunities identified")
            recommendations.append(
                "   Current performance appears to be well-optimized"
            )

        for rec in recommendations:
            print(f"   {rec}")


def create_instrumented_progress_callback(splash_screen):
    """Create a progress callback that tracks updates for analysis."""

    def progress_callback(progress: int, message: str):
        profiler.track_progress_update(progress, message)
        if splash_screen:
            splash_screen.update_progress(progress, message)

    return progress_callback


def profile_complete_startup():
    """Profile the complete TKA startup process with enhanced instrumentation."""
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
            from core.application.application_factory import (
                ApplicationFactory,
                ApplicationMode,
            )
            from presentation.components.ui.splash_screen import SplashScreen
            from PyQt6.QtGui import QGuiApplication

        # Phase 3: Container & Services
        with profiler.time_operation("3. Container creation"):
            container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

        with profiler.time_operation("4. Service initialization"):
            from core.service_locator import initialize_services

            initialize_services()

        # Phase 4: Splash Screen
        with profiler.time_operation("5. Splash screen creation"):
            screens = QGuiApplication.screens()
            target_screen = screens[0] if screens else None
            splash = SplashScreen(target_screen=target_screen)
            profiler.mark_splash_visible()

        # Phase 5: Main Window Setup with instrumented progress
        with profiler.time_operation("6. Main window creation"):
            from main import TKAMainWindow

            # Create instrumented progress callback
            progress_callback = create_instrumented_progress_callback(splash)

            # Create window with instrumented initialization
            window = TKAMainWindow(
                container=container,
                splash_screen=splash,
                target_screen=target_screen,
                parallel_mode=False,
                parallel_geometry=None,
            )

        # Mark when window is ready to be shown
        profiler.mark_window_shown()

        print("\n✅ Enhanced startup profiling complete!")

    except Exception as e:
        print(f"❌ Error during profiling: {e}")
        import traceback

        traceback.print_exc()

    finally:
        profiler.end_profiling()


# Global profiler instance
profiler = EnhancedStartupProfiler()


if __name__ == "__main__":
    profile_complete_startup()
