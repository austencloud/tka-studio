"""
Smart logging that automatically adjusts verbosity based on performance and context.

This module provides intelligent logging that:
- Reduces verbosity for fast, successful operations
- Increases detail for slow or failed operations
- Suppresses repetitive log messages
- Provides batch operation summaries
- Integrates with TKA's service architecture
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
import functools
import logging
import time
from typing import Any


class LogLevel(Enum):
    """Smart logging levels."""

    SILENT = "silent"
    MINIMAL = "minimal"
    NORMAL = "normal"
    VERBOSE = "verbose"
    DEBUG = "debug"


@dataclass
class LoggingConfig:
    """Configuration for smart logging behavior."""

    performance_threshold_ms: float = 100.0  # Log details if operation takes longer
    error_always_verbose: bool = True
    success_summary_only: bool = True
    batch_operation_summary: bool = True
    max_repeated_logs: int = 5  # Suppress repeated identical logs
    enable_performance_tracking: bool = True


class SmartLogger:
    """
    Logger that adapts verbosity based on performance and context.

    Features:
    - Fast operations: minimal logging
    - Slow operations: detailed logging
    - Errors: always verbose
    - Repeated operations: summarized
    - Performance-based log level adjustment
    """

    def __init__(self, name: str, config: LoggingConfig = None):
        self.logger = logging.getLogger(name)
        self.config = config or LoggingConfig()
        self.repeated_log_counts: dict[str, int] = {}
        self.last_log_messages: dict[str, str] = {}
        self.performance_stats: dict[str, list] = {}

    def log_operation(self, operation_name: str, level: LogLevel = LogLevel.NORMAL):
        """Decorator for logging operations with smart verbosity."""

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                operation_id = f"{func.__name__}_{operation_name}"

                try:
                    # Pre-operation logging (minimal)
                    if level in [LogLevel.VERBOSE, LogLevel.DEBUG]:
                        self.logger.debug(f"🔄 Starting {operation_name}")

                    # Execute operation
                    result = func(*args, **kwargs)

                    # Post-operation logging (performance-based)
                    duration_ms = (time.time() - start_time) * 1000

                    # Track performance stats
                    if self.config.enable_performance_tracking:
                        if operation_id not in self.performance_stats:
                            self.performance_stats[operation_id] = []
                        self.performance_stats[operation_id].append(duration_ms)

                    if duration_ms > self.config.performance_threshold_ms:
                        # Slow operation - log details
                        self.logger.warning(
                            f"⚠️ SLOW {operation_name}: {duration_ms:.1f}ms"
                        )
                        if level in [LogLevel.VERBOSE, LogLevel.DEBUG]:
                            self._log_operation_details(
                                operation_name, args, kwargs, result
                            )
                    # Fast operation - minimal logging
                    elif level == LogLevel.DEBUG:
                        self.logger.debug(f"✅ {operation_name}: {duration_ms:.1f}ms")

                    return result

                except Exception as e:
                    duration_ms = (time.time() - start_time) * 1000

                    # Errors always get verbose logging
                    self.logger.exception(
                        f"❌ FAILED {operation_name}: {duration_ms:.1f}ms - {e!s}"
                    )
                    if self.config.error_always_verbose:
                        self._log_operation_details(
                            operation_name, args, kwargs, None, error=e
                        )

                    raise

            return wrapper

        return decorator

    def log_batch_operation(
        self,
        batch_name: str,
        items_processed: int,
        total_duration_ms: float,
        errors: int = 0,
    ):
        """Log summary for batch operations."""
        if self.config.batch_operation_summary:
            avg_time = total_duration_ms / items_processed if items_processed > 0 else 0

            if errors > 0:
                self.logger.warning(
                    f"📊 BATCH {batch_name}: {items_processed} items, "
                    f"{total_duration_ms:.1f}ms total, {avg_time:.1f}ms avg, "
                    f"{errors} errors"
                )
            elif total_duration_ms > self.config.performance_threshold_ms:
                self.logger.info(
                    f"📊 BATCH {batch_name}: {items_processed} items, "
                    f"{total_duration_ms:.1f}ms total, {avg_time:.1f}ms avg"
                )
            else:
                # Fast batch operations - debug only
                self.logger.debug(
                    f"📊 {batch_name}: {items_processed} items, {avg_time:.1f}ms avg"
                )

    def log_with_suppression(self, level: int, message: str, suppress_key: str | None = None):
        """Log with automatic suppression of repeated messages."""
        suppress_key = suppress_key or message

        if suppress_key in self.repeated_log_counts:
            self.repeated_log_counts[suppress_key] += 1

            # Only log every Nth occurrence after the first few
            if self.repeated_log_counts[suppress_key] <= self.config.max_repeated_logs:
                self.logger.log(level, message)
            elif self.repeated_log_counts[suppress_key] % 10 == 0:
                self.logger.log(
                    level,
                    f"{message} (repeated {self.repeated_log_counts[suppress_key]} times)",
                )
        else:
            self.repeated_log_counts[suppress_key] = 1
            self.logger.log(level, message)

    def get_performance_summary(self) -> dict[str, dict[str, float]]:
        """Get performance statistics summary."""
        summary = {}
        for operation_id, times in self.performance_stats.items():
            if times:
                summary[operation_id] = {
                    "count": len(times),
                    "avg_ms": sum(times) / len(times),
                    "min_ms": min(times),
                    "max_ms": max(times),
                    "total_ms": sum(times),
                }
        return summary

    def reset_performance_stats(self):
        """Reset performance tracking statistics."""
        self.performance_stats.clear()
        self.repeated_log_counts.clear()

    def _log_operation_details(
        self,
        operation_name: str,
        args: tuple,
        kwargs: dict,
        result: Any,
        error: Exception | None = None,
    ):
        """Log detailed operation information."""
        self.logger.debug(f"📋 DETAILS for {operation_name}:")

        # Log key arguments (but not huge objects)
        if args:
            safe_args = [self._safe_repr(arg) for arg in args[:3]]  # First 3 args only
            self.logger.debug(f"   Args: {safe_args}")

        if kwargs:
            safe_kwargs = {k: self._safe_repr(v) for k, v in list(kwargs.items())[:3]}
            self.logger.debug(f"   Kwargs: {safe_kwargs}")

        if error:
            self.logger.debug(f"   Error: {type(error).__name__}: {error!s}")
        elif result is not None:
            self.logger.debug(f"   Result: {self._safe_repr(result)}")

    def _safe_repr(self, obj: Any, max_length: int = 100) -> str:
        """Safe representation of objects for logging."""
        try:
            if hasattr(obj, "__dict__") and hasattr(obj, "__class__"):
                # For custom objects, show class name and key attributes
                class_name = obj.__class__.__name__
                return f"<{class_name} object>"

            repr_str = repr(obj)
            if len(repr_str) > max_length:
                return f"{repr_str[:max_length]}..."
            return repr_str
        except:
            return f"<{type(obj).__name__} object>"


# Global registry of smart loggers for easy management
_smart_logger_registry: dict[str, SmartLogger] = {}


def reset_all_smart_loggers():
    """Reset performance stats for all registered smart loggers."""
    for logger in _smart_logger_registry.values():
        logger.reset_performance_stats()


def get_all_performance_stats() -> dict[str, dict[str, dict[str, float]]]:
    """Get performance statistics from all smart loggers."""
    all_stats = {}
    for name, logger in _smart_logger_registry.items():
        stats = logger.get_performance_summary()
        if stats:
            all_stats[name] = stats
    return all_stats
