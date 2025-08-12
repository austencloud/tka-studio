"""
Advanced Performance Profiler for TKA Desktop Application

Provides comprehensive function-level profiling with minimal overhead,
memory tracking, and statistical analysis. Integrates with existing
monitoring infrastructure and follows TKA architectural patterns.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
import functools
import logging
import sys
import threading
import time
from typing import Any, Callable, ParamSpec, TypeVar

import psutil

from .config import PerformanceConfig, get_performance_config
from .memory_tracker import MemoryTracker

# Result pattern removed - using simple exceptions
from .metrics import FunctionMetrics, PerformanceMetrics, SystemMetrics


logger = logging.getLogger(__name__)

P = ParamSpec("P")
T = TypeVar("T")


@dataclass
class ProfilerSession:
    """Represents a profiling session with all collected data."""

    session_id: str
    start_time: datetime
    end_time: datetime | None = None
    function_metrics: dict[str, FunctionMetrics] = field(default_factory=dict)
    system_metrics: list[SystemMetrics] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class AdvancedProfiler:
    """
    Production-grade profiler with real-time monitoring and comprehensive analysis.

    Features:
    - Function-level timing and memory profiling
    - Minimal overhead (<1% performance impact)
    - Real-time performance monitoring
    - Statistical analysis and regression detection
    - Integration with existing TKA monitoring infrastructure
    """

    def __init__(self, config: PerformanceConfig | None = None):
        self.config = config or get_performance_config()
        self.is_profiling = False
        self.current_session: ProfilerSession | None = None

        # Thread-safe data structures
        self._lock = threading.RLock()
        self._function_stats: dict[str, FunctionMetrics] = {}
        self._call_stack: list[str] = []
        self._start_times: dict[str, float] = {}

        # Performance monitoring
        self.metrics = PerformanceMetrics()
        self.memory_tracker = MemoryTracker(config)

        # Integration with existing monitoring
        self._integrate_with_existing_monitoring()

    def _integrate_with_existing_monitoring(self):
        """Integrate with existing core.monitoring system."""
        try:
            from desktop.modern.core.monitoring import performance_monitor

            # Enable profiling in existing monitor if available
            if hasattr(performance_monitor, "_profiling_enabled"):
                performance_monitor._profiling_enabled = self.config.profiling.enabled
                logger.info("Integrated with existing performance monitoring system")
        except ImportError:
            logger.debug("Existing monitoring system not available for integration")

    def start_session(
        self, session_name: str | None = None
    ) -> Result[str, AppError]:
        """
        Start a new profiling session.

        Args:
            session_name: Optional name for the session

        Returns:
            Result containing session ID or error
        """
        if not self.config.profiling.enabled:
            return failure(
                app_error(
                    ErrorType.CONFIGURATION_ERROR,
                    "Profiling is disabled in configuration",
                )
            )

        if self.is_profiling:
            stop_result = self.stop_session()
            if stop_result.is_failure():
                logger.warning(f"Failed to stop previous session: {stop_result.error}")

        session_id = session_name or f"session_{datetime.now().isoformat()}"

        try:
            with self._lock:
                self.current_session = ProfilerSession(
                    session_id=session_id,
                    start_time=datetime.now(),
                    metadata={
                        "python_version": sys.version,
                        "platform": sys.platform,
                        "process_id": psutil.Process().pid,
                        "config": {
                            "overhead_threshold": self.config.profiling.overhead_threshold_percent,
                            "memory_threshold": self.config.profiling.memory_threshold_mb,
                        },
                    },
                )

                self.is_profiling = True
                self._function_stats.clear()

            logger.info(f"Started profiling session: {session_id}")
            return success(session_id)

        except Exception as e:
            return failure(
                app_error(
                    ErrorType.PROFILING_ERROR,
                    f"Failed to start profiling session: {e}",
                    cause=e,
                )
            )

    def stop_session(self) -> Result[ProfilerSession | None, AppError]:
        """
        Stop the current profiling session and return results.

        Returns:
            Result containing session data or error
        """
        if not self.is_profiling:
            return success(None)

        try:
            with self._lock:
                if self.current_session:
                    self.current_session.end_time = datetime.now()
                    self.current_session.function_metrics = self._function_stats.copy()

                session = self.current_session
                self.current_session = None
                self.is_profiling = False

            if session:
                logger.info(f"Stopped profiling session: {session.session_id}")

            return success(session)

        except Exception as e:
            return failure(
                app_error(
                    ErrorType.PROFILING_ERROR,
                    f"Failed to stop profiling session: {e}",
                    cause=e,
                )
            )

    def profile_function(self, func: Callable[P, T]) -> Callable[P, T]:
        """
        Decorator to profile individual functions with minimal overhead.

        Args:
            func: Function to profile

        Returns:
            Wrapped function with profiling
        """
        # Pre-compute function name to avoid repeated string operations
        function_name = f"{func.__module__}.{func.__qualname__}"

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # Fast path: if profiling disabled, return immediately
            if not self.is_profiling or not self.config.profiling.enabled:
                return func(*args, **kwargs)

            # Minimal timing overhead - only measure execution time
            start_time = time.perf_counter()

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                # Only measure time - memory tracking is too expensive for overhead target
                execution_time = time.perf_counter() - start_time

                # Fast update without expensive operations
                self._fast_update_function_stats(function_name, execution_time)

        return wrapper

    @contextmanager
    def profile_block(self, block_name: str):
        """
        Context manager for profiling code blocks.

        Args:
            block_name: Name of the code block

        Usage:
            with profiler.profile_block("database_query"):
                # Code to profile
                pass
        """
        if not self.is_profiling or not self.config.profiling.enabled:
            yield
            return

        # Minimal timing overhead - only measure execution time
        start_time = time.perf_counter()

        try:
            yield
        finally:
            execution_time = time.perf_counter() - start_time
            # Use fast update method to minimize overhead
            self._fast_update_function_stats(block_name, execution_time)

    def _fast_update_function_stats(self, function_name: str, execution_time: float):
        """Fast thread-safe update of function statistics with minimal overhead."""
        with self._lock:
            if function_name not in self._function_stats:
                self._function_stats[function_name] = FunctionMetrics(
                    name=function_name,
                    call_count=0,
                    total_time=0.0,
                    min_time=float("inf"),
                    max_time=0.0,
                    memory_total=0.0,
                )

            stats = self._function_stats[function_name]
            stats.call_count += 1
            stats.total_time += execution_time
            stats.min_time = min(stats.min_time, execution_time)
            stats.max_time = max(stats.max_time, execution_time)

            # Only calculate essential derived metrics
            stats.avg_time = stats.total_time / stats.call_count

    def _update_function_stats(
        self, function_name: str, execution_time: float, memory_delta: float
    ):
        """Thread-safe update of function statistics."""
        with self._lock:
            if function_name not in self._function_stats:
                self._function_stats[function_name] = FunctionMetrics(
                    name=function_name,
                    call_count=0,
                    total_time=0.0,
                    min_time=float("inf"),
                    max_time=0.0,
                    memory_total=0.0,
                )

            stats = self._function_stats[function_name]
            stats.call_count += 1
            stats.total_time += execution_time
            stats.min_time = min(stats.min_time, execution_time)
            stats.max_time = max(stats.max_time, execution_time)
            stats.memory_total += memory_delta

            # Calculate derived metrics
            stats.avg_time = stats.total_time / stats.call_count
            stats.memory_avg = stats.memory_total / stats.call_count

            # Update historical data
            stats.execution_times.append(execution_time)
            stats.memory_usages.append(memory_delta)
            stats.update_statistics()

    def get_top_bottlenecks(self, limit: int = 10) -> list[FunctionMetrics]:
        """Get the top performance bottlenecks by total execution time."""
        with self._lock:
            sorted_functions = sorted(
                self._function_stats.values(), key=lambda x: x.total_time, reverse=True
            )
            return sorted_functions[:limit]

    def get_memory_hotspots(self, limit: int = 10) -> list[FunctionMetrics]:
        """Get functions with highest memory usage."""
        with self._lock:
            sorted_functions = sorted(
                self._function_stats.values(),
                key=lambda x: x.memory_total,
                reverse=True,
            )
            return sorted_functions[:limit]

    def get_performance_summary(self) -> dict[str, Any]:
        """Get comprehensive performance summary."""
        with self._lock:
            return self.metrics.get_performance_summary()


# Global profiler instance for easy access
_global_profiler: AdvancedProfiler | None = None


def get_profiler() -> AdvancedProfiler:
    """Get the global profiler instance."""
    global _global_profiler
    if _global_profiler is None:
        _global_profiler = AdvancedProfiler()
    return _global_profiler


def profile(func: Callable[P, T]) -> Callable[P, T]:
    """Convenience decorator for profiling functions."""
    return get_profiler().profile_function(func)


def profile_block(name: str):
    """Convenience context manager for profiling code blocks."""
    return get_profiler().profile_block(name)


def reset_profiler():
    """Reset the global profiler instance (mainly for testing)."""
    global _global_profiler
    _global_profiler = None
