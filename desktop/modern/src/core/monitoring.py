"""
Performance monitoring and profiling utilities for TKA application.

Provides decorators and utilities for monitoring service performance,
memory usage, and execution times.
"""

from __future__ import annotations

import functools
import logging
import time
from typing import Any, Callable, TypeVar


F = TypeVar("F", bound=Callable[..., Any])

logger = logging.getLogger(__name__)


def monitor_performance(name_or_func=None):
    """
    Decorator to monitor function performance.

    Can be used with or without parameters:
    @monitor_performance
    @monitor_performance("custom_name")

    Logs execution time and can be extended to track memory usage
    and other performance metrics.
    """

    def decorator(func: F) -> F:
        # Determine the name to use for logging
        if isinstance(name_or_func, str):
            operation_name = name_or_func
        else:
            operation_name = func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            start_memory = _get_memory_usage()

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.perf_counter()
                end_memory = _get_memory_usage()

                execution_time = (
                    end_time - start_time
                ) * 1000  # Convert to milliseconds
                memory_delta = (
                    end_memory - start_memory if end_memory and start_memory else 0
                )

                logger.debug(
                    f"Performance: {operation_name} - "
                    f"Time: {execution_time:.2f}ms, "
                    f"Memory: {memory_delta:+.2f}MB"
                )

        return wrapper

    # Handle both @monitor_performance and @monitor_performance("name") usage
    if callable(name_or_func):
        # Used as @monitor_performance (without parentheses)
        return decorator(name_or_func)
    else:
        # Used as @monitor_performance("name") (with parentheses)
        return decorator


def profile_method(include_args: bool = False):
    """
    Decorator to profile method calls with optional argument logging.

    Args:
        include_args: Whether to include method arguments in the log
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()

            # Log method entry
            if include_args:
                logger.debug(
                    f"Entering {func.__name__} with args={args}, kwargs={kwargs}"
                )
            else:
                logger.debug(f"Entering {func.__name__}")

            try:
                result = func(*args, **kwargs)

                end_time = time.perf_counter()
                execution_time = (end_time - start_time) * 1000

                logger.debug(f"Exiting {func.__name__} - Time: {execution_time:.2f}ms")
                return result

            except Exception as e:
                end_time = time.perf_counter()
                execution_time = (end_time - start_time) * 1000

                logger.error(
                    f"Exception in {func.__name__} after {execution_time:.2f}ms: {e}"
                )
                raise

        return wrapper

    return decorator


def track_memory_usage(func: F) -> F:
    """
    Decorator to track memory usage of a function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_memory = _get_memory_usage()

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_memory = _get_memory_usage()

            if start_memory and end_memory:
                memory_delta = end_memory - start_memory
                logger.debug(f"Memory usage for {func.__name__}: {memory_delta:+.2f}MB")

    return wrapper


def benchmark(iterations: int = 1):
    """
    Decorator to benchmark function performance over multiple iterations.

    Args:
        iterations: Number of times to run the function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if iterations <= 1:
                return func(*args, **kwargs)

            times = []
            result = None

            for i in range(iterations):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                times.append((end_time - start_time) * 1000)

            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)

            logger.info(
                f"Benchmark {func.__name__} ({iterations} iterations): "
                f"Avg: {avg_time:.2f}ms, Min: {min_time:.2f}ms, Max: {max_time:.2f}ms"
            )

            return result

        return wrapper

    return decorator


def _get_memory_usage() -> float | None:
    """
    Get current memory usage in MB.

    Returns:
        Memory usage in MB, or None if psutil is not available
    """
    try:
        import os

        import psutil

        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        return memory_info.rss / 1024 / 1024  # Convert bytes to MB

    except ImportError:
        # psutil not available, return None
        return None
    except Exception as e:
        logger.debug(f"Error getting memory usage: {e}")
        return None


class PerformanceTracker:
    """
    Context manager for tracking performance of code blocks.
    """

    def __init__(self, operation_name: str, log_level: int = logging.DEBUG):
        self.operation_name = operation_name
        self.log_level = log_level
        self.start_time = None
        self.start_memory = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        self.start_memory = _get_memory_usage()
        logger.log(self.log_level, f"Starting {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.perf_counter()
        end_memory = _get_memory_usage()

        execution_time = (end_time - self.start_time) * 1000
        memory_delta = (
            end_memory - self.start_memory if end_memory and self.start_memory else 0
        )

        if exc_type is None:
            logger.log(
                self.log_level,
                f"Completed {self.operation_name} - "
                f"Time: {execution_time:.2f}ms, Memory: {memory_delta:+.2f}MB",
            )
        else:
            logger.error(
                f"Failed {self.operation_name} after {execution_time:.2f}ms: "
                f"{exc_type.__name__}: {exc_val}"
            )


class MetricsCollector:
    """
    Simple metrics collector for application performance monitoring.
    """

    def __init__(self):
        self.metrics = {}
        self.counters = {}

    def record_timing(self, metric_name: str, duration_ms: float):
        """Record a timing metric."""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append(duration_ms)

    def increment_counter(self, counter_name: str, value: int = 1):
        """Increment a counter metric."""
        if counter_name not in self.counters:
            self.counters[counter_name] = 0
        self.counters[counter_name] += value

    def get_timing_stats(self, metric_name: str) -> dict[str, float]:
        """Get timing statistics for a metric."""
        if metric_name not in self.metrics or not self.metrics[metric_name]:
            return {}

        times = self.metrics[metric_name]
        return {
            "count": len(times),
            "avg": sum(times) / len(times),
            "min": min(times),
            "max": max(times),
            "total": sum(times),
        }

    def get_counter_value(self, counter_name: str) -> int:
        """Get counter value."""
        return self.counters.get(counter_name, 0)

    def reset(self):
        """Reset all metrics."""
        self.metrics.clear()
        self.counters.clear()


# Global metrics collector instance
_metrics_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance."""
    return _metrics_collector
