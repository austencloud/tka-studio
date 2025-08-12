"""
TKA Smart Logging System

This package provides intelligent logging that adapts to application behavior:
- Reduces verbosity for fast, successful operations
- Increases detail for slow or failed operations
- Suppresses repetitive log messages
- Provides specialized logging for arrow positioning
- Filters Qt CSS property warnings

Quick Start:
-----------

# For immediate relief from verbose arrow positioning logs:
from desktop.modern.core.logging import setup_arrow_positioning_logging_only
setup_arrow_positioning_logging_only(quiet=True)

# For full smart logging setup:
from desktop.modern.core.logging import setup_smart_logging
setup_smart_logging('development')

# For Qt message filtering only:
from desktop.modern.core.logging import install_qt_message_filter
install_qt_message_filter()

# For custom loggers:
from desktop.modern.core.logging import get_smart_logger, LoggingConfig
logger = get_smart_logger('my_service', LoggingConfig(performance_threshold_ms=100))

# For arrow positioning specific logging:
from desktop.modern.core.logging import get_arrow_positioning_logger
arrow_logger = get_arrow_positioning_logger()
"""

# Specialized arrow positioning logger
from __future__ import annotations

from .arrow_positioning_logger import (
    ArrowPositioningLogger,
    get_arrow_positioning_logger,
    log_directional_processing,
)

# Configuration and setup
from .config import (
    LoggingEnvironments,
    configure_from_environment,
    enable_performance_monitoring,
    enable_verbose_mode,
    setup_smart_logging,
)

# Qt message filtering
from .qt_message_filter import (
    disable_qt_message_filter,
    get_qt_message_filter_stats,
    install_qt_message_filter,
)

# Core smart logging components
from .smart_logger import (
    LoggingConfig,
    LogLevel,
    SmartLogger,
    get_all_performance_stats,
    reset_all_smart_loggers,
)


# Version info
__version__ = "1.0.0"
__author__ = "TKA Development Team"

# Default exports for convenience
__all__ = [
    "ArrowPositioningLogger",
    "LogLevel",
    "LoggingConfig",
    "LoggingEnvironments",
    # Core classes
    "SmartLogger",
    "configure_from_environment",
    "disable_qt_message_filter",
    "enable_performance_monitoring",
    "enable_verbose_mode",
    "get_all_performance_stats",
    # Factory functions
    "get_arrow_positioning_logger",
    "get_qt_message_filter_stats",
    # Qt message filtering
    "install_qt_message_filter",
    # Decorators for services
    "log_directional_processing",
    # Utilities
    "reset_all_logging_stats",
    "reset_all_smart_loggers",
    # Setup functions (most commonly used)
    "setup_smart_logging",
]


# Auto-configure if environment variables are set
import os


if os.getenv("TKA_AUTO_CONFIGURE_LOGGING", "").lower() in ["true", "1", "yes"]:
    configure_from_environment()
