"""
Logging configuration for different environments and use cases.

This module provides predefined logging configurations and setup functions
for TKA's smart logging system.
"""

from __future__ import annotations

import logging
import os

from .arrow_positioning_logger import get_arrow_positioning_logger
from .smart_logger import LoggingConfig


class LoggingEnvironments:
    """Predefined logging configurations for different environments."""

    @staticmethod
    def get_production_config() -> LoggingConfig:
        """
        Production logging configuration.

        - Minimal verbosity to reduce log volume
        - Focus on errors and performance issues
        - Aggressive suppression of repetitive messages
        """
        return LoggingConfig(
            performance_threshold_ms=200.0,  # Only log really slow operations
            error_always_verbose=True,  # Always log error details
            success_summary_only=True,  # No detailed success logs
            batch_operation_summary=True,  # Use batch summaries
            max_repeated_logs=1,  # Suppress almost all repetition
            enable_performance_tracking=True,
        )

    @staticmethod
    def get_development_config() -> LoggingConfig:
        """
        Development logging configuration.

        - Moderate verbosity for debugging
        - Performance tracking enabled
        - Some repetitive message suppression
        """
        return LoggingConfig(
            performance_threshold_ms=100.0,
            error_always_verbose=True,
            success_summary_only=False,  # Show some success details
            batch_operation_summary=True,
            max_repeated_logs=3,  # Allow some repetition for debugging
            enable_performance_tracking=True,
        )

    @staticmethod
    def get_debugging_config() -> LoggingConfig:
        """
        Debug logging configuration.

        - Full verbosity for deep debugging
        - Detailed performance tracking
        - Minimal suppression
        """
        return LoggingConfig(
            performance_threshold_ms=10.0,  # Log everything that's slow
            error_always_verbose=True,
            success_summary_only=False,  # Show all details
            batch_operation_summary=False,  # Individual operation logs
            max_repeated_logs=10,  # Allow more repetition
            enable_performance_tracking=True,
        )

    @staticmethod
    def get_testing_config() -> LoggingConfig:
        """
        Testing logging configuration.

        - Minimal logging to avoid cluttering test output
        - Focus on errors only
        - Maximum suppression
        """
        return LoggingConfig(
            performance_threshold_ms=500.0,  # Only very slow operations
            error_always_verbose=False,  # Brief error messages in tests
            success_summary_only=True,
            batch_operation_summary=True,
            max_repeated_logs=0,  # Suppress all repetition
            enable_performance_tracking=False,  # No perf tracking in tests
        )


def setup_smart_logging(environment: str | None = None) -> LoggingConfig:
    """
    Setup smart logging for the entire TKA application.

    Args:
        environment: Environment name ('production', 'development', 'debug', 'testing')
                    If None, will auto-detect from environment variables

    Returns:
        The logging configuration used
    """
    # Auto-detect environment if not specified
    if environment is None:
        environment = _detect_environment()

    # Get configuration for environment
    configs = {
        "production": LoggingEnvironments.get_production_config(),
        "development": LoggingEnvironments.get_development_config(),
        "debug": LoggingEnvironments.get_debugging_config(),
        "testing": LoggingEnvironments.get_testing_config(),
    }

    config = configs.get(environment, LoggingEnvironments.get_development_config())

    # Configure arrow positioning logger (this fixes the immediate verbosity issue)
    get_arrow_positioning_logger(config)

    # Configure other service loggers
    _configure_service_loggers(environment, config)

    # Set up root logger level based on environment
    _configure_root_logger(environment)

    print(f"🔧 Smart logging configured for '{environment}' environment")
    print(f"   Performance threshold: {config.performance_threshold_ms}ms")
    print("   Arrow positioning verbosity: REDUCED")

    return config


def _detect_environment() -> str:
    """Auto-detect environment from various indicators."""
    # Check environment variables
    env_var = os.getenv("TKA_ENVIRONMENT", "").lower()
    if env_var in ["production", "prod"]:
        return "production"
    if env_var in ["debug", "debugging"]:
        return "debug"
    if env_var in ["test", "testing"]:
        return "testing"

    # Check for testing indicators
    if any(
        test_indicator in os.environ
        for test_indicator in ["PYTEST_CURRENT_TEST", "TESTING"]
    ):
        return "testing"

    # Check for debug indicators
    debug_indicators = [
        os.getenv("TKA_DEBUG", "").lower() == "true",
        os.getenv("DEBUG", "").lower() == "true",
        "--debug" in os.sys.argv if hasattr(os, "sys") else False,
    ]
    if any(debug_indicators):
        return "debug"

    # Default to development
    return "development"


def _configure_service_loggers(environment: str, config: LoggingConfig) -> None:
    """Configure specific service loggers based on environment."""

    # Map environment to log levels
    level_mapping = {
        "production": logging.WARNING,
        "development": logging.INFO,
        "debug": logging.DEBUG,
        "testing": logging.ERROR,
    }

    level = level_mapping.get(environment, logging.INFO)

    # Configure the most verbose services that were causing noise
    verbose_services = [
        # Arrow positioning services (main culprits)
        "application.services.positioning.arrows.orchestration.directional_tuple_processor",
        "application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service",
        "application.services.positioning.arrows.orchestration.arrow_adjustment_lookup_service",
        # Other potentially verbose services
        "application.services.positioning.arrows",
        "application.services.positioning",
        "domain.models",  # If domain models are verbose
        "infrastructure.storage",  # If storage operations are verbose
    ]

    for service_name in verbose_services:
        service_logger = logging.getLogger(service_name)
        service_logger.setLevel(level)

        # In production, be extra aggressive about suppressing noise
        if environment == "production":
            service_logger.setLevel(logging.ERROR)


def _configure_root_logger(environment: str) -> None:
    """Configure the root logger based on environment."""
    root_logger = logging.getLogger()

    if environment == "production":
        root_logger.setLevel(logging.WARNING)
    elif environment == "testing":
        root_logger.setLevel(logging.ERROR)
    elif environment == "debug":
        root_logger.setLevel(logging.DEBUG)
    else:  # development
        root_logger.setLevel(logging.INFO)


# Quick setup functions for common scenarios


def enable_verbose_mode():
    """Enable verbose mode for debugging."""
    setup_smart_logging("debug")
    print("📢 Verbose mode enabled - detailed logging")


def enable_performance_monitoring():
    """Enable performance monitoring mode."""
    config = LoggingConfig(
        performance_threshold_ms=50.0,  # Sensitive to slower operations
        enable_performance_tracking=True,
        batch_operation_summary=True,
    )

    get_arrow_positioning_logger(config)
    print("📊 Performance monitoring enabled")


# Environment variable configuration
def configure_from_environment():
    """Configure logging based on environment variables."""
    # TKA_LOG_LEVEL: Set specific log level
    log_level = os.getenv("TKA_LOG_LEVEL", "").upper()
    if log_level in ["DEBUG", "INFO", "WARNING", "ERROR"]:
        logging.getLogger().setLevel(getattr(logging, log_level))

    # TKA_PERFORMANCE_MONITORING: Enable performance tracking
    if os.getenv("TKA_PERFORMANCE_MONITORING", "").lower() in ["true", "1", "yes"]:
        enable_performance_monitoring()

    # TKA_VERBOSE_DEBUG: Enable full debugging
    if os.getenv("TKA_VERBOSE_DEBUG", "").lower() in ["true", "1", "yes"]:
        enable_verbose_mode()
