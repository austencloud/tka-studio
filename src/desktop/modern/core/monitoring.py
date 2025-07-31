"""
TKA Desktop Performance Monitoring

Enhanced performance monitoring infrastructure for tracking operation duration,
memory usage, and comprehensive performance metrics across the TKA Desktop application.

COMPONENTS:
- PerformanceMonitor: Enhanced monitoring class for metric collection
- monitor_performance: Decorator for automatic performance tracking
- PerformanceReport: Reporting and analysis utilities
- Enhanced profiling support for the new performance framework

INTEGRATION:
- Extends existing monitoring to support the new performance framework
- Maintains backward compatibility with existing monitoring patterns
- Provides foundation for advanced profiling capabilities
"""

import logging
import threading
import time
from collections import deque
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from typing import Any

import psutil

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Individual performance metric data."""

    operation: str
    duration_ms: float
    memory_mb: float
    timestamp: float
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class OperationStats:
    """Aggregated statistics for an operation."""

    operation: str
    count: int = 0
    total_duration_ms: float = 0.0
    max_duration_ms: float = 0.0
    min_duration_ms: float = float("inf")
    avg_duration_ms: float = 0.0
    total_memory_mb: float = 0.0
    max_memory_mb: float = 0.0
    avg_memory_mb: float = 0.0
    recent_metrics: deque = field(default_factory=lambda: deque(maxlen=100))

    def update(self, metric: PerformanceMetric):
        """Update statistics with a new metric."""
        self.count += 1
        self.total_duration_ms += metric.duration_ms
        self.max_duration_ms = max(self.max_duration_ms, metric.duration_ms)
        self.min_duration_ms = min(self.min_duration_ms, metric.duration_ms)
        self.avg_duration_ms = self.total_duration_ms / self.count

        self.total_memory_mb += metric.memory_mb
        self.max_memory_mb = max(self.max_memory_mb, metric.memory_mb)
        self.avg_memory_mb = self.total_memory_mb / self.count

        self.recent_metrics.append(metric)


class PerformanceMonitor:
    """
    Enhanced performance monitoring system for TKA Desktop.

    Tracks operation performance metrics including duration, memory usage,
    and provides aggregated statistics and reporting capabilities.

    ENHANCED FEATURES:
    - Function-level profiling support
    - Real-time performance tracking
    - Integration with advanced performance framework
    - Backward compatibility with existing monitoring
    """

    def __init__(self, max_metrics: int = 10000, enable_profiling: bool = False):
        """
        Initialize enhanced performance monitor.

        Args:
            max_metrics: Maximum number of metrics to retain in memory
            enable_profiling: Enable advanced profiling features
        """
        self.max_metrics = max_metrics
        self.metrics: deque = deque(maxlen=max_metrics)
        self.operation_stats: dict[str, OperationStats] = {}
        self._lock = threading.Lock()
        self._enabled = True

        # Enhanced profiling support
        self._profiling_enabled = enable_profiling
        self._function_metrics: dict[str, dict[str, Any]] = {}
        self._active_sessions: set[str] = set()
        self._session_data: dict[str, dict[str, Any]] = {}

        # Performance thresholds (adjusted for memory delta measurements)
        self.warning_thresholds = {
            "duration_ms": 1000.0,  # 1 second
            "memory_mb": 50.0,  # 50 MB delta (was 100 MB total)
        }

        self.error_thresholds = {
            "duration_ms": 5000.0,  # 5 seconds
            "memory_mb": 200.0,  # 200 MB delta (was 500 MB total)
        }

        # Enhanced thresholds for profiling
        self.profiling_thresholds = {
            "function_duration_ms": 100.0,  # Function execution threshold
            "memory_delta_mb": 10.0,  # Memory delta threshold
            "cache_hit_rate_percent": 80.0,  # Cache performance threshold
        }

    def record_metric(
        self,
        operation: str,
        duration_ms: float,
        memory_mb: float,
        context: dict[str, Any] | None = None,
    ):
        """
        Record a performance metric.

        Args:
            operation: Name of the operation
            duration_ms: Duration in milliseconds
            memory_mb: Memory usage in megabytes
            context: Additional context information
        """
        if not self._enabled:
            return

        metric = PerformanceMetric(
            operation=operation,
            duration_ms=duration_ms,
            memory_mb=memory_mb,
            timestamp=time.time(),
            context=context or {},
        )

        with self._lock:
            self.metrics.append(metric)

            # Update operation statistics
            if operation not in self.operation_stats:
                self.operation_stats[operation] = OperationStats(operation=operation)

            self.operation_stats[operation].update(metric)

        # Check thresholds and log warnings/errors
        self._check_thresholds(metric)

        # Enhanced profiling integration
        if self._profiling_enabled:
            self._update_function_metrics(operation, duration_ms, memory_mb, context)

    def _check_thresholds(self, metric: PerformanceMetric):
        """Check if metric exceeds warning or error thresholds."""
        # Check duration thresholds
        if metric.duration_ms > self.error_thresholds["duration_ms"]:
            logger.error(
                f"Performance ERROR: {metric.operation} took {metric.duration_ms:.1f}ms "
                f"(threshold: {self.error_thresholds['duration_ms']}ms)"
            )
        elif metric.duration_ms > self.warning_thresholds["duration_ms"]:
            logger.warning(
                f"Performance WARNING: {metric.operation} took {metric.duration_ms:.1f}ms "
                f"(threshold: {self.warning_thresholds['duration_ms']}ms)"
            )

        # Check memory thresholds
        if metric.memory_mb > self.error_thresholds["memory_mb"]:
            logger.error(
                f"Memory ERROR: {metric.operation} used {metric.memory_mb:.1f}MB "
                f"(threshold: {self.error_thresholds['memory_mb']}MB)"
            )
        elif metric.memory_mb > self.warning_thresholds["memory_mb"]:
            logger.warning(
                f"Memory WARNING: {metric.operation} used {metric.memory_mb:.1f}MB "
                f"(threshold: {self.warning_thresholds['memory_mb']}MB)"
            )

    def get_operation_stats(self, operation: str) -> OperationStats | None:
        """Get statistics for a specific operation."""
        with self._lock:
            return self.operation_stats.get(operation)

    def get_all_stats(self) -> dict[str, OperationStats]:
        """Get statistics for all operations."""
        with self._lock:
            return dict(self.operation_stats)

    def get_slowest_operations(self, limit: int = 10) -> list[OperationStats]:
        """Get the slowest operations by average duration."""
        with self._lock:
            stats = list(self.operation_stats.values())
            return sorted(stats, key=lambda s: s.avg_duration_ms, reverse=True)[:limit]

    def get_memory_intensive_operations(self, limit: int = 10) -> list[OperationStats]:
        """Get the most memory-intensive operations."""
        with self._lock:
            stats = list(self.operation_stats.values())
            return sorted(stats, key=lambda s: s.avg_memory_mb, reverse=True)[:limit]

    def clear_metrics(self):
        """Clear all collected metrics and statistics."""
        with self._lock:
            self.metrics.clear()
            self.operation_stats.clear()

    def set_enabled(self, enabled: bool):
        """Enable or disable performance monitoring."""
        self._enabled = enabled

    def generate_report(self) -> dict[str, Any]:
        """Generate a comprehensive performance report."""
        with self._lock:
            total_operations = sum(
                stats.count for stats in self.operation_stats.values()
            )

            return {
                "summary": {
                    "total_operations": total_operations,
                    "unique_operations": len(self.operation_stats),
                    "total_metrics": len(self.metrics),
                    "monitoring_enabled": self._enabled,
                },
                "slowest_operations": [
                    {
                        "operation": stats.operation,
                        "avg_duration_ms": round(stats.avg_duration_ms, 2),
                        "max_duration_ms": round(stats.max_duration_ms, 2),
                        "count": stats.count,
                    }
                    for stats in self.get_slowest_operations(5)
                ],
                "memory_intensive_operations": [
                    {
                        "operation": stats.operation,
                        "avg_memory_mb": round(stats.avg_memory_mb, 2),
                        "max_memory_mb": round(stats.max_memory_mb, 2),
                        "count": stats.count,
                    }
                    for stats in self.get_memory_intensive_operations(5)
                ],
                "thresholds": {
                    "warning": self.warning_thresholds,
                    "error": self.error_thresholds,
                },
            }

    # ============================================================================
    # ENHANCED PROFILING METHODS
    # ============================================================================

    def start_profiling_session(self, session_id: str) -> bool:
        """
        Start a new profiling session.

        Args:
            session_id: Unique identifier for the session

        Returns:
            True if session started successfully
        """
        if not self._profiling_enabled:
            return False

        with self._lock:
            if session_id in self._active_sessions:
                logger.warning(f"Profiling session {session_id} already active")
                return False

            self._active_sessions.add(session_id)
            self._session_data[session_id] = {
                "start_time": datetime.now(),
                "function_calls": {},
                "system_metrics": [],
                "metadata": {},
            }

        logger.info(f"Started profiling session: {session_id}")
        return True

    def stop_profiling_session(self, session_id: str) -> dict[str, Any] | None:
        """
        Stop a profiling session and return collected data.

        Args:
            session_id: Session identifier to stop

        Returns:
            Session data if successful, None otherwise
        """
        if not self._profiling_enabled or session_id not in self._active_sessions:
            return None

        with self._lock:
            self._active_sessions.remove(session_id)
            session_data = self._session_data.pop(session_id, None)

        if session_data:
            session_data["end_time"] = datetime.now()
            session_data["duration"] = (
                session_data["end_time"] - session_data["start_time"]
            ).total_seconds()

        logger.info(f"Stopped profiling session: {session_id}")
        return session_data

    def _update_function_metrics(
        self,
        function_name: str,
        duration_ms: float,
        memory_mb: float,
        context: dict[str, Any] | None = None,
    ):
        """Update function-level metrics for profiling."""
        if function_name not in self._function_metrics:
            self._function_metrics[function_name] = {
                "call_count": 0,
                "total_time": 0.0,
                "min_time": float("inf"),
                "max_time": 0.0,
                "total_memory": 0.0,
                "execution_times": deque(maxlen=100),  # Keep last 100 calls
                "memory_deltas": deque(maxlen=100),
            }

        metrics = self._function_metrics[function_name]
        metrics["call_count"] += 1
        metrics["total_time"] += duration_ms
        metrics["min_time"] = min(metrics["min_time"], duration_ms)
        metrics["max_time"] = max(metrics["max_time"], duration_ms)
        metrics["total_memory"] += memory_mb
        metrics["execution_times"].append(duration_ms)
        metrics["memory_deltas"].append(memory_mb)

        # Update active sessions
        for session_id in self._active_sessions:
            session_data = self._session_data[session_id]
            if function_name not in session_data["function_calls"]:
                session_data["function_calls"][function_name] = {
                    "count": 0,
                    "total_time": 0.0,
                    "total_memory": 0.0,
                }

            func_data = session_data["function_calls"][function_name]
            func_data["count"] += 1
            func_data["total_time"] += duration_ms
            func_data["total_memory"] += memory_mb

    def get_function_performance_summary(self) -> dict[str, Any]:
        """Get comprehensive function performance summary."""
        if not self._profiling_enabled:
            return {"error": "Profiling not enabled"}

        with self._lock:
            summary = {
                "total_functions": len(self._function_metrics),
                "active_sessions": len(self._active_sessions),
                "top_functions_by_time": [],
                "top_functions_by_memory": [],
                "performance_issues": [],
            }

            # Sort functions by total time
            sorted_by_time = sorted(
                self._function_metrics.items(),
                key=lambda x: x[1]["total_time"],
                reverse=True,
            )

            for func_name, metrics in sorted_by_time[:10]:
                avg_time = metrics["total_time"] / metrics["call_count"]
                summary["top_functions_by_time"].append(
                    {
                        "function": func_name,
                        "total_time": metrics["total_time"],
                        "avg_time": avg_time,
                        "call_count": metrics["call_count"],
                        "max_time": metrics["max_time"],
                    }
                )

                # Check for performance issues
                if avg_time > self.profiling_thresholds["function_duration_ms"]:
                    summary["performance_issues"].append(
                        {
                            "function": func_name,
                            "issue": "High average execution time",
                            "value": avg_time,
                            "threshold": self.profiling_thresholds[
                                "function_duration_ms"
                            ],
                        }
                    )

            # Sort functions by memory usage
            sorted_by_memory = sorted(
                self._function_metrics.items(),
                key=lambda x: x[1]["total_memory"],
                reverse=True,
            )

            for func_name, metrics in sorted_by_memory[:10]:
                avg_memory = metrics["total_memory"] / metrics["call_count"]
                summary["top_functions_by_memory"].append(
                    {
                        "function": func_name,
                        "total_memory": metrics["total_memory"],
                        "avg_memory": avg_memory,
                        "call_count": metrics["call_count"],
                    }
                )

        return summary

    @contextmanager
    def profile_block(self, block_name: str, session_id: str | None = None):
        """
        Context manager for profiling code blocks.

        Args:
            block_name: Name of the code block
            session_id: Optional session to associate with

        Usage:
            with performance_monitor.profile_block("database_query"):
                # Code to profile
                pass
        """
        if not self._profiling_enabled:
            yield
            return

        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024

        try:
            yield
        finally:
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024

            duration_ms = (end_time - start_time) * 1000
            memory_delta = end_memory - start_memory

            self.record_metric(
                operation=block_name,
                duration_ms=duration_ms,
                memory_mb=memory_delta,
                context={"session_id": session_id} if session_id else None,
            )


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def monitor_performance(
    operation_name: str | None = None, context: dict[str, Any] | None = None
):
    """
    Decorator to monitor operation performance.

    Args:
        operation_name: Custom operation name (defaults to class.method)
        context: Additional context to include with metrics

    Returns:
        Decorated function with performance monitoring

    Example:
        @monitor_performance("layout_calculation")
        def calculate_layout(self, data: LayoutData) -> LayoutResult:
            # Implementation here
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Determine operation name
            if operation_name:
                op_name = operation_name
            elif args and hasattr(args[0], "__class__"):
                op_name = f"{args[0].__class__.__name__}.{func.__name__}"
            else:
                op_name = func.__name__

            # Start monitoring
            start_time = time.perf_counter()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                # Record metrics
                end_time = time.perf_counter()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024

                duration_ms = (end_time - start_time) * 1000
                memory_mb = abs(
                    end_memory - start_memory
                )  # Memory delta used by operation

                # Merge provided context with runtime context
                runtime_context = {
                    "function": func.__name__,
                    "args_count": len(args),
                    "kwargs_count": len(kwargs) if kwargs else 0,
                }

                if context:
                    runtime_context.update(context)

                performance_monitor.record_metric(
                    operation=op_name,
                    duration_ms=duration_ms,
                    memory_mb=memory_mb,
                    context=runtime_context,
                )

        return wrapper

    return decorator


def set_performance_thresholds(
    warning_duration_ms: float | None = None,
    error_duration_ms: float | None = None,
    warning_memory_mb: float | None = None,
    error_memory_mb: float | None = None,
):
    """
    Configure performance monitoring thresholds.

    Args:
        warning_duration_ms: Warning threshold for operation duration
        error_duration_ms: Error threshold for operation duration
        warning_memory_mb: Warning threshold for memory usage
        error_memory_mb: Error threshold for memory usage
    """
    if warning_duration_ms is not None:
        performance_monitor.warning_thresholds["duration_ms"] = warning_duration_ms

    if error_duration_ms is not None:
        performance_monitor.error_thresholds["duration_ms"] = error_duration_ms

    if warning_memory_mb is not None:
        performance_monitor.warning_thresholds["memory_mb"] = warning_memory_mb

    if error_memory_mb is not None:
        performance_monitor.error_thresholds["memory_mb"] = error_memory_mb


def get_performance_report() -> dict[str, Any]:
    """Get a comprehensive performance report."""
    return performance_monitor.generate_report()
