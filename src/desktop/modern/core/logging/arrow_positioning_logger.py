"""
Specialized logger for arrow positioning operations.

This module provides optimized logging for the arrow positioning services
that were generating excessive verbosity in the original logs.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from .smart_logger import LoggingConfig, LogLevel, SmartLogger


class ArrowPositioningLogger:
    """
    Specialized logger for arrow positioning operations.

    Designed specifically to reduce the verbosity seen in logs like:
    - directional_tuple_processor
    - arrow_adjustment_calculator_service
    - arrow_adjustment_lookup_service

    Features:
    - Batch summaries instead of step-by-step logging
    - Performance-based detail level
    - Suppression of repetitive calculations
    - Letter-based operation grouping
    """

    def __init__(self, config: LoggingConfig = None):
        # Specialized config for arrow positioning
        arrow_config = config or LoggingConfig(
            performance_threshold_ms=50.0,  # Arrow positioning should be fast
            success_summary_only=True,
            batch_operation_summary=True,
            max_repeated_logs=2,  # Very aggressive suppression for repetitive operations
            enable_performance_tracking=True,
        )

        self.smart_logger = SmartLogger("positioning.arrows", arrow_config)

        # Track operations per letter for batching
        self.letter_operations: dict[str, dict[str, Any]] = {}
        self.current_letter = None
        self.current_letter_start_time = None

    def start_letter_positioning(self, letter: str):
        """Start tracking operations for a specific letter."""
        self.current_letter = letter
        self.current_letter_start_time = time.time()
        self.letter_operations[letter] = {
            "arrows_processed": 0,
            "calculations": 0,
            "adjustments": 0,
            "errors": [],
            "start_time": self.current_letter_start_time,
        }

    def finish_letter_positioning(self, letter: str = None):
        """Finish tracking and log summary for letter positioning."""
        letter = letter or self.current_letter
        if not letter or letter not in self.letter_operations:
            return

        ops = self.letter_operations[letter]
        duration_ms = (time.time() - ops["start_time"]) * 1000

        # Log summary based on performance and errors
        if ops["errors"]:
            self.smart_logger.logger.warning(
                f"🏹 POSITIONED {letter}: {ops['arrows_processed']} arrows, "
                f"{ops['calculations']} calculations, {duration_ms:.1f}ms, "
                f"{len(ops['errors'])} errors"
            )
            for error in ops["errors"][:3]:  # Show first 3 errors
                self.smart_logger.logger.warning(f"   Error: {error}")
        elif duration_ms > self.smart_logger.config.performance_threshold_ms:
            self.smart_logger.logger.info(
                f"🏹 POSITIONED {letter}: {ops['arrows_processed']} arrows, "
                f"{ops['calculations']} calculations, {duration_ms:.1f}ms"
            )
        else:
            # Fast successful case - debug only
            self.smart_logger.logger.debug(
                f"🏹 {letter}: {ops['arrows_processed']} arrows, {duration_ms:.1f}ms"
            )

        # Clean up
        if letter == self.current_letter:
            self.current_letter = None
            self.current_letter_start_time = None

    def log_adjustment_calculation(self, operation_name: str = "arrow_adjustment"):
        """Decorator for adjustment calculations - with suppression."""

        def decorator(func):
            @self.smart_logger.log_operation(operation_name, LogLevel.MINIMAL)
            def wrapper(*args, **kwargs):
                # Track calculation for current letter
                if self.current_letter:
                    self.letter_operations[self.current_letter]["calculations"] += 1

                result = func(*args, **kwargs)

                # Only log if it's slow or an error occurred
                # Normal fast calculations are silent
                return result

            return wrapper

        return decorator

    def log_directional_processing(
        self, operation_name: str = "directional_processing"
    ):
        """Decorator for directional tuple processing - heavily suppressed."""

        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()

                try:
                    result = func(*args, **kwargs)
                    duration_ms = (time.time() - start_time) * 1000

                    # Track for current letter
                    if self.current_letter:
                        self.letter_operations[self.current_letter]["adjustments"] += 1

                    # Only log if exceptionally slow
                    if (
                        duration_ms > 20.0
                    ):  # 20ms threshold for individual tuple processing
                        self.smart_logger.logger.warning(
                            f"⚠️ SLOW directional processing: {duration_ms:.1f}ms"
                        )

                    return result

                except Exception as e:
                    if self.current_letter:
                        self.letter_operations[self.current_letter]["errors"].append(
                            str(e)
                        )

                    self.smart_logger.logger.error(
                        f"❌ Directional processing failed: {e!s}"
                    )
                    raise

            return wrapper

        return decorator

    def log_lookup_operation(self, operation_name: str = "adjustment_lookup"):
        """Decorator for adjustment lookup operations."""

        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)

                # Track for current letter
                if self.current_letter:
                    self.letter_operations[self.current_letter]["arrows_processed"] += 1

                return result

            return wrapper

        return decorator

    def log_sequence_positioning_summary(
        self,
        sequence_name: str,
        total_letters: int,
        total_arrows: int,
        total_duration_ms: float,
        error_count: int = 0,
    ):
        """Log final summary for entire sequence positioning."""
        if error_count > 0:
            self.smart_logger.logger.warning(
                f"🎯 SEQUENCE POSITIONED: {sequence_name} - {total_letters} letters, "
                f"{total_arrows} arrows, {total_duration_ms:.1f}ms, {error_count} errors"
            )
        elif total_duration_ms > 500.0:  # Warn if sequence positioning is slow
            self.smart_logger.logger.info(
                f"🎯 SEQUENCE POSITIONED: {sequence_name} - {total_letters} letters, "
                f"{total_arrows} arrows, {total_duration_ms:.1f}ms"
            )
        else:
            self.smart_logger.logger.debug(
                f"🎯 {sequence_name}: {total_letters} letters, {total_duration_ms:.1f}ms"
            )

    def suppress_verbose_positioning_logs(self):
        """Configure suppression of the most verbose positioning logs."""
        # These are the specific loggers generating the noise
        verbose_loggers = [
            "application.services.positioning.arrows.orchestration.directional_tuple_processor",
            "application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service",
            "application.services.positioning.arrows.orchestration.arrow_adjustment_lookup_service",
        ]

        for logger_name in verbose_loggers:
            logger = logging.getLogger(logger_name)
            # Set to WARNING to suppress INFO/DEBUG noise
            logger.setLevel(logging.WARNING)

            # Add filter to catch and suppress specific messages
            logger.addFilter(self._create_message_filter())

    def _create_message_filter(self):
        """Create filter to suppress specific verbose messages."""

        class VerboseMessageFilter(logging.Filter):
            def filter(self, record):
                # Suppress these specific messages that were causing noise
                suppressed_patterns = []

                for pattern in suppressed_patterns:
                    if pattern in record.getMessage():
                        return False  # Suppress this message

                return True  # Allow other messages

        return VerboseMessageFilter()

    def get_positioning_performance_report(self) -> dict[str, Any]:
        """Generate performance report for positioning operations."""
        total_letters = len(self.letter_operations)
        total_duration = 0
        total_arrows = 0
        total_calculations = 0
        total_errors = 0

        for letter, ops in self.letter_operations.items():
            total_duration += (time.time() - ops["start_time"]) * 1000
            total_arrows += ops["arrows_processed"]
            total_calculations += ops["calculations"]
            total_errors += len(ops["errors"])

        avg_time_per_letter = total_duration / total_letters if total_letters > 0 else 0
        avg_time_per_arrow = total_duration / total_arrows if total_arrows > 0 else 0

        return {
            "total_letters": total_letters,
            "total_arrows": total_arrows,
            "total_calculations": total_calculations,
            "total_errors": total_errors,
            "total_duration_ms": total_duration,
            "avg_time_per_letter_ms": avg_time_per_letter,
            "avg_time_per_arrow_ms": avg_time_per_arrow,
            "performance_threshold_ms": self.smart_logger.config.performance_threshold_ms,
        }


# Global instance for easy access throughout the positioning services
_global_arrow_logger: ArrowPositioningLogger | None = None


def get_arrow_positioning_logger(
    config: LoggingConfig = None,
) -> ArrowPositioningLogger:
    """Get the global arrow positioning logger instance."""
    global _global_arrow_logger
    if _global_arrow_logger is None:
        _global_arrow_logger = ArrowPositioningLogger(config)
        # Automatically suppress verbose logs when created
        _global_arrow_logger.suppress_verbose_positioning_logs()
    return _global_arrow_logger


# Convenience decorators for easy use in services
def log_directional_processing(func):
    """Decorator for directional tuple processing."""
    logger = get_arrow_positioning_logger()
    return logger.log_directional_processing("directional_processing")(func)
