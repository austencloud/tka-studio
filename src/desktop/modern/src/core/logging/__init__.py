"""
TKA Smart Logging System

This package provides intelligent logging that adapts to application behavior:
- Reduces verbosity for fast, successful operations
- Increases detail for slow or failed operations  
- Suppresses repetitive log messages
- Provides specialized logging for arrow positioning

Quick Start:
-----------

# For immediate relief from verbose arrow positioning logs:
from core.logging import setup_arrow_positioning_logging_only
setup_arrow_positioning_logging_only(quiet=True)

# For full smart logging setup:
from core.logging import setup_smart_logging
setup_smart_logging('development')

# For custom loggers:
from core.logging import get_smart_logger, LoggingConfig
logger = get_smart_logger('my_service', LoggingConfig(performance_threshold_ms=100))

# For arrow positioning specific logging:
from core.logging import get_arrow_positioning_logger
arrow_logger = get_arrow_positioning_logger()
"""

# Core smart logging components
from .smart_logger import (
    SmartLogger,
    LoggingConfig,
    LogLevel,
    create_smart_logger,
    get_smart_logger,
    reset_all_smart_loggers,
    get_all_performance_stats
)

# Specialized arrow positioning logger
from .arrow_positioning_logger import (
    ArrowPositioningLogger,
    get_arrow_positioning_logger,
    reset_arrow_positioning_logger,
    log_arrow_adjustment,
    log_directional_processing,
    log_adjustment_lookup
)

# Configuration and setup
from .config import (
    LoggingEnvironments,
    setup_smart_logging,
    setup_arrow_positioning_logging_only,
    enable_quiet_mode,
    enable_verbose_mode,
    enable_performance_monitoring,
    configure_from_environment,
    get_logging_performance_report,
    reset_all_logging_stats
)

# Version info
__version__ = "1.0.0"
__author__ = "TKA Development Team"

# Default exports for convenience
__all__ = [
    # Core classes
    'SmartLogger',
    'LoggingConfig', 
    'LogLevel',
    'ArrowPositioningLogger',
    'LoggingEnvironments',
    
    # Factory functions
    'create_smart_logger',
    'get_smart_logger',
    'get_arrow_positioning_logger',
    
    # Setup functions (most commonly used)
    'setup_smart_logging',
    'setup_arrow_positioning_logging_only',
    'enable_quiet_mode',
    'enable_verbose_mode',
    'enable_performance_monitoring',
    'configure_from_environment',
    
    # Decorators for services
    'log_arrow_adjustment',
    'log_directional_processing', 
    'log_adjustment_lookup',
    
    # Utilities
    'get_logging_performance_report',
    'reset_all_logging_stats',
    'reset_all_smart_loggers',
    'reset_arrow_positioning_logger',
    'get_all_performance_stats'
]


def quick_setup(mode: str = 'auto') -> None:
    """
    Quick setup function for common use cases.
    
    Args:
        mode: 'quiet', 'normal', 'verbose', or 'auto' (default)
    """
    if mode == 'auto':
        # Auto-detect and configure
        configure_from_environment()
        setup_smart_logging()
    elif mode == 'quiet':
        enable_quiet_mode()
    elif mode == 'normal':
        setup_smart_logging('development')
    elif mode == 'verbose':
        enable_verbose_mode()
    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'auto', 'quiet', 'normal', or 'verbose'")


# Auto-configure if environment variables are set
import os
if os.getenv('TKA_AUTO_CONFIGURE_LOGGING', '').lower() in ['true', '1', 'yes']:
    configure_from_environment()
