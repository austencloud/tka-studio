"""
Standard Error Handler for TKA Application

Provides consistent error handling across all modules to eliminate
the inconsistency between print(), logger.error(), and silent failures.

PROVIDES:
- Standardized error logging with consistent format
- Graceful fallback mechanisms
- Error recovery strategies
- Context-aware error reporting
"""

from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any


class ErrorSeverity:
    """Constants for error severity levels."""

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class StandardErrorHandler:
    """
    Centralized error handling with consistent formatting and recovery strategies.

    Eliminates the inconsistent error handling patterns found across modules.
    """

    @staticmethod
    def handle_service_error(
        operation: str,
        error: Exception,
        logger: logging.Logger,
        severity: str = ErrorSeverity.ERROR,
        context: dict[str, Any] | None = None,
    ) -> None:
        """
        Handle service-related errors with consistent logging format.

        Args:
            operation: Description of the operation that failed
            error: The exception that occurred
            logger: Logger instance to use
            severity: Error severity level
            context: Additional context information
        """
        context_str = ""
        if context:
            context_items = [f"{k}={v}" for k, v in context.items()]
            context_str = f" [{', '.join(context_items)}]"

        message = f"❌ {operation} failed: {error}{context_str}"

        if severity == ErrorSeverity.CRITICAL:
            logger.critical(message)
        elif severity == ErrorSeverity.ERROR:
            logger.error(message)
        elif severity == ErrorSeverity.WARNING:
            logger.warning(message)
        else:
            logger.info(message)

    @staticmethod
    def handle_ui_error(
        operation: str,
        error: Exception,
        logger: logging.Logger,
        fallback_action: Callable | None = None,
        context: dict[str, Any] | None = None,
    ) -> Any:
        """
        Handle UI-related errors with optional fallback action.

        Args:
            operation: Description of the UI operation that failed
            error: The exception that occurred
            logger: Logger instance to use
            fallback_action: Optional fallback function to execute
            context: Additional context information

        Returns:
            Result of fallback_action if provided, otherwise None
        """
        StandardErrorHandler.handle_service_error(
            f"UI {operation}", error, logger, ErrorSeverity.ERROR, context
        )

        if fallback_action:
            try:
                return fallback_action()
            except Exception as fallback_error:
                StandardErrorHandler.handle_service_error(
                    f"Fallback for {operation}",
                    fallback_error,
                    logger,
                    ErrorSeverity.WARNING,
                )

        return None

    @staticmethod
    def handle_initialization_error(
        component: str,
        error: Exception,
        logger: logging.Logger,
        is_critical: bool = True,
        suggested_action: str | None = None,
    ) -> None:
        """
        Handle component initialization errors with severity assessment.

        Args:
            component: Name of the component that failed to initialize
            error: The exception that occurred
            logger: Logger instance to use
            is_critical: Whether this error should stop application startup
            suggested_action: Optional suggestion for resolving the issue
        """
        severity = ErrorSeverity.CRITICAL if is_critical else ErrorSeverity.WARNING
        context = {"component": component}

        if suggested_action:
            context["suggested_action"] = suggested_action

        StandardErrorHandler.handle_service_error(
            f"{component} initialization", error, logger, severity, context
        )

    @staticmethod
    def handle_dependency_resolution_error(
        interface_name: str,
        error: Exception,
        logger: logging.Logger,
        available_services: list | None = None,
    ) -> None:
        """
        Handle dependency resolution errors with helpful context.

        Args:
            interface_name: Name of the interface that couldn't be resolved
            error: The exception that occurred
            logger: Logger instance to use
            available_services: List of available service names for debugging
        """
        context = {"interface": interface_name}
        if available_services:
            context["available_services"] = ", ".join(
                available_services[:5]
            )  # Limit for readability
            if len(available_services) > 5:
                context["total_available"] = len(available_services)

        StandardErrorHandler.handle_service_error(
            "Dependency resolution", error, logger, ErrorSeverity.ERROR, context
        )

    @staticmethod
    def handle_circular_dependency_error(
        dependency_chain: list, logger: logging.Logger
    ) -> None:
        """
        Handle circular dependency errors with clear chain visualization.

        Args:
            dependency_chain: List of interface names in the circular chain
            logger: Logger instance to use
        """
        chain_str = " -> ".join(dependency_chain)
        context = {"circular_chain": chain_str, "chain_length": len(dependency_chain)}

        error_msg = f"Circular dependency detected in chain: {chain_str}"

        StandardErrorHandler.handle_service_error(
            "Circular dependency detection",
            Exception(error_msg),
            logger,
            ErrorSeverity.CRITICAL,
            context,
        )

    @staticmethod
    def create_graceful_fallback(
        operation_name: str, fallback_result: Any, logger: logging.Logger
    ) -> Callable:
        """
        Create a graceful fallback function with consistent logging.

        Args:
            operation_name: Name of the operation for logging
            fallback_result: The result to return from the fallback
            logger: Logger instance to use

        Returns:
            A function that logs the fallback and returns the result
        """

        def fallback_func():
            logger.info(f"🔄 Using graceful fallback for {operation_name}")
            return fallback_result

        return fallback_func

    @staticmethod
    def validate_and_handle(
        condition: bool,
        error_message: str,
        logger: logging.Logger,
        severity: str = ErrorSeverity.ERROR,
        raise_exception: bool = False,
    ) -> bool:
        """
        Validate a condition and handle the error if it fails.

        Args:
            condition: The condition to validate
            error_message: Message to log if condition fails
            logger: Logger instance to use
            severity: Error severity level
            raise_exception: Whether to raise an exception if condition fails

        Returns:
            True if condition passed, False otherwise

        Raises:
            ValueError: If condition fails and raise_exception is True
        """
        if not condition:
            StandardErrorHandler.handle_service_error(
                "Validation", Exception(error_message), logger, severity
            )

            if raise_exception:
                raise ValueError(error_message)

            return False

        return True
