#!/usr/bin/env python3
"""
Graph Editor Logging Utilities
==============================

Provides structured logging utilities for graph editor components
with context information and consistent formatting.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
import functools
import logging
import traceback
from typing import Any


class GraphEditorLogger:
    """
    Enhanced logger for graph editor components with structured logging.

    Provides consistent logging format with context information,
    performance tracking, and error reporting.
    """

    def __init__(self, component_name: str, logger_name: str = None):
        self.component_name = component_name
        self.logger = logging.getLogger(logger_name or f"graph_editor.{component_name}")
        self._setup_formatter()

    def _setup_formatter(self):
        """Set up consistent log formatting."""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _format_context(self, context: dict[str, Any]) -> str:
        """Format context dictionary for logging."""
        if not context:
            return ""

        context_parts = []
        for key, value in context.items():
            if value is None:
                context_parts.append(f"{key}=None")
            elif isinstance(value, str):
                context_parts.append(f"{key}='{value}'")
            else:
                context_parts.append(f"{key}={value}")

        return f" | Context: {', '.join(context_parts)}"

    def info(self, message: str, context: dict[str, Any] = None):
        """Log info message with context."""
        full_message = (
            f"[{self.component_name}] {message}{self._format_context(context)}"
        )
        self.logger.info(full_message)

    def warning(self, message: str, context: dict[str, Any] = None):
        """Log warning message with context."""
        full_message = (
            f"[{self.component_name}] {message}{self._format_context(context)}"
        )
        self.logger.warning(full_message)

    def error(
        self, message: str, context: dict[str, Any] = None, exception: Exception = None
    ):
        """Log error message with context and optional exception."""
        full_message = (
            f"[{self.component_name}] {message}{self._format_context(context)}"
        )

        if exception:
            full_message += f" | Exception: {type(exception).__name__}: {exception!s}"
            self.logger.error(full_message, exc_info=True)
        else:
            self.logger.error(full_message)

    def debug(self, message: str, context: dict[str, Any] = None):
        """Log debug message with context."""
        full_message = (
            f"[{self.component_name}] {message}{self._format_context(context)}"
        )
        self.logger.debug(full_message)

    def method_call(
        self, method_name: str, args: dict[str, Any] = None, result: Any = None
    ):
        """Log method call with arguments and result."""
        context = {"method": method_name}
        if args:
            context.update(args)
        if result is not None:
            context["result"] = result

        self.debug(f"Method call: {method_name}", context)

    def validation_error(
        self, field: str, value: Any, error_message: str, context: dict[str, Any] = None
    ):
        """Log validation error with structured information."""
        validation_context = {
            "validation_field": field,
            "validation_value": value,
            "validation_error": error_message,
        }
        if context:
            validation_context.update(context)

        self.error(f"Validation failed for {field}", validation_context)

    def state_change(
        self, from_state: Any, to_state: Any, context: dict[str, Any] = None
    ):
        """Log state change with before/after information."""
        state_context = {"from_state": from_state, "to_state": to_state}
        if context:
            state_context.update(context)

        self.info(f"State changed: {from_state} -> {to_state}", state_context)

    def performance_warning(
        self,
        operation: str,
        duration_ms: float,
        threshold_ms: float = 100,
        context: dict[str, Any] = None,
    ):
        """Log performance warning for slow operations."""
        perf_context = {
            "operation": operation,
            "duration_ms": duration_ms,
            "threshold_ms": threshold_ms,
        }
        if context:
            perf_context.update(context)

        self.warning(
            f"Slow operation detected: {operation} took {duration_ms:.2f}ms",
            perf_context,
        )


def create_component_logger(component_name: str) -> GraphEditorLogger:
    """
    Factory function to create a logger for a graph editor component.

    Args:
        component_name: Name of the component (e.g., "StateManager", "GraphEditor")

    Returns:
        Configured GraphEditorLogger instance
    """
    return GraphEditorLogger(component_name)


def log_method_call(logger: GraphEditorLogger, include_result: bool = False):
    """
    Decorator to automatically log method calls with arguments and results.

    Args:
        logger: GraphEditorLogger instance to use for logging
        include_result: Whether to log the method result

    Returns:
        Decorator function
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract method name and arguments
            method_name = func.__name__

            # Build argument context (skip 'self' parameter)
            arg_context = {}
            if args and len(args) > 1:  # Skip self
                arg_names = func.__code__.co_varnames[1 : len(args)]
                for i, arg_name in enumerate(arg_names):
                    if i + 1 < len(args):
                        arg_context[arg_name] = args[i + 1]

            # Add keyword arguments
            arg_context.update(kwargs)

            # Log method entry
            logger.debug(f"Entering method: {method_name}", arg_context)

            try:
                # Execute method
                start_time = datetime.now()
                result = func(*args, **kwargs)
                end_time = datetime.now()

                # Calculate duration
                duration_ms = (end_time - start_time).total_seconds() * 1000

                # Log method completion
                result_context = {"duration_ms": duration_ms}
                if include_result and result is not None:
                    result_context["result"] = result

                logger.debug(f"Completed method: {method_name}", result_context)

                # Log performance warning if slow
                if duration_ms > 100:  # 100ms threshold
                    logger.performance_warning(
                        method_name, duration_ms, context=arg_context
                    )

                return result

            except Exception as e:
                # Log method error
                error_context = {**arg_context, "error_type": type(e).__name__}
                logger.error(f"Method failed: {method_name}", error_context, e)
                raise

        return wrapper

    return decorator


def log_error_with_context(
    logger: GraphEditorLogger, operation: str, context: dict[str, Any] = None
):
    """
    Decorator to log errors with context information.

    Args:
        logger: GraphEditorLogger instance to use for logging
        operation: Description of the operation being performed
        context: Additional context to include in error logs

    Returns:
        Decorator function
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Build error context
                error_context = context or {}
                error_context.update(
                    {
                        "operation": operation,
                        "function": func.__name__,
                        "error_type": type(e).__name__,
                        "traceback": traceback.format_exc(),
                    }
                )

                # Log the error
                logger.error(f"Error in {operation}", error_context, e)
                raise

        return wrapper

    return decorator


# Convenience function for quick error logging
def log_validation_errors(
    logger: GraphEditorLogger, validation_result, operation: str = "validation"
):
    """
    Log all validation errors from a ValidationResult.

    Args:
        logger: GraphEditorLogger instance
        validation_result: ValidationResult with errors to log
        operation: Description of the operation that failed validation
    """
    if validation_result.has_errors:
        for error in validation_result.errors:
            logger.validation_error(
                field=error.field or "unknown",
                value=error.value,
                error_message=error.message,
                context={**error.context, "operation": operation},
            )

    if validation_result.has_warnings:
        for warning in validation_result.warnings:
            logger.warning(f"Validation warning in {operation}: {warning}")


# Global logger instances for common components
state_manager_logger = create_component_logger("StateManager")
signal_coordinator_logger = create_component_logger("SignalCoordinator")
graph_editor_logger = create_component_logger("GraphEditor")
layout_manager_logger = create_component_logger("LayoutManager")
