"""
UPGRADED Application Factory with Smart Logging Integration

This is an enhanced version of ApplicationFactory that automatically configures
smart logging based on the application mode.

INTEGRATION BENEFITS:
- Production apps get quiet logging automatically
- Test apps get test-optimized logging  
- Headless apps get performance monitoring
- Recording apps get detailed operation logging
- Arrow positioning verbosity is automatically reduced
"""

from typing import Optional
import sys
import logging
import os

# Import original factory
from .application_factory import ApplicationFactory as OriginalApplicationFactory, ApplicationMode

# Import smart logging system
try:
    from core.logging import (
        setup_smart_logging,
        setup_arrow_positioning_logging_only,
        enable_quiet_mode,
        enable_performance_monitoring,
        configure_from_environment,
        LoggingEnvironments
    )
    SMART_LOGGING_AVAILABLE = True
except ImportError:
    SMART_LOGGING_AVAILABLE = False

logger = logging.getLogger(__name__)


class ApplicationFactoryWithSmartLogging(OriginalApplicationFactory):
    """
    Enhanced ApplicationFactory with automatic smart logging configuration.
    
    Each application mode gets optimized logging:
    - Production: Minimal verbosity, error focus
    - Test: Very quiet, no performance tracking  
    - Headless: Performance monitoring enabled
    - Recording: Detailed logging for workflow capture
    """
    
    @staticmethod
    def create_production_app():
        """
        Create production application with quiet logging.
        
        Logging configuration:
        - Arrow positioning: QUIET (errors only)
        - Performance threshold: 200ms
        - Repetitive logs: SUPPRESSED
        - Error details: FULL
        """
        if SMART_LOGGING_AVAILABLE:
            # Configure quiet logging for production
            setup_arrow_positioning_logging_only(quiet=True)
            
            # Additional production optimizations
            enable_quiet_mode()
            
            logger.info("🔇 Production logging: QUIET mode enabled")
        else:
            # Fallback configuration
            ApplicationFactoryWithSmartLogging._configure_fallback_logging('production')
        
        # Create container using original factory
        container = OriginalApplicationFactory.create_production_app()
        
        return container
    
    @staticmethod
    def create_test_app():
        """
        Create test application with test-optimized logging.
        
        Logging configuration:
        - Arrow positioning: SILENT (except errors)
        - Performance tracking: DISABLED
        - Test output: CLEAN
        - Error details: MINIMAL
        """
        if SMART_LOGGING_AVAILABLE:
            # Configure test logging
            setup_smart_logging('testing')
            
            logger.debug("🧪 Test logging: SILENT mode enabled")
        else:
            # Fallback configuration
            ApplicationFactoryWithSmartLogging._configure_fallback_logging('testing')
        
        # Create container using original factory
        container = OriginalApplicationFactory.create_test_app()
        
        return container
    
    @staticmethod
    def create_headless_app():
        """
        Create headless application with performance monitoring.
        
        Logging configuration:
        - Arrow positioning: SMART (performance-based)
        - Performance tracking: ENABLED
        - Batch summaries: ENABLED
        - Detailed errors: ENABLED
        """
        if SMART_LOGGING_AVAILABLE:
            # Configure development logging with performance monitoring
            setup_smart_logging('development')
            enable_performance_monitoring()
            
            logger.info("📊 Headless logging: PERFORMANCE MONITORING enabled")
        else:
            # Fallback configuration
            ApplicationFactoryWithSmartLogging._configure_fallback_logging('development')
        
        # Create container using original factory
        container = OriginalApplicationFactory.create_headless_app()
        
        return container
    
    @staticmethod
    def create_recording_app():
        """
        Create recording application with detailed logging.
        
        Logging configuration:
        - Arrow positioning: VERBOSE (for workflow capture)
        - Performance tracking: ENABLED
        - All operations: LOGGED
        - Error details: FULL
        """
        if SMART_LOGGING_AVAILABLE:
            # Configure debug logging for detailed recording
            setup_smart_logging('debug')
            
            logger.info("📢 Recording logging: VERBOSE mode enabled for workflow capture")
        else:
            # Fallback configuration
            ApplicationFactoryWithSmartLogging._configure_fallback_logging('debug')
        
        # Create container using original factory
        container = OriginalApplicationFactory.create_recording_app()
        
        return container
    
    @staticmethod
    def create_app(mode: str = ApplicationMode.PRODUCTION):
        """
        Create application with mode-specific logging.
        
        Args:
            mode: Application mode - automatically configures appropriate logging
        
        Returns:
            DIContainer with optimized logging for the mode
        """
        if mode == ApplicationMode.PRODUCTION:
            return ApplicationFactoryWithSmartLogging.create_production_app()
        elif mode == ApplicationMode.TEST:
            return ApplicationFactoryWithSmartLogging.create_test_app()
        elif mode == ApplicationMode.HEADLESS:
            return ApplicationFactoryWithSmartLogging.create_headless_app()
        elif mode == ApplicationMode.RECORDING:
            return ApplicationFactoryWithSmartLogging.create_recording_app()
        else:
            raise ValueError(f"Unknown application mode: {mode}")
    
    @staticmethod
    def create_app_from_args(args: Optional[list] = None):
        """
        Create application from command line args with smart logging.
        
        Additional argument support:
        --quiet: Force quiet logging regardless of mode
        --verbose: Force verbose logging regardless of mode
        --performance: Enable performance monitoring
        """
        if args is None:
            args = sys.argv
        
        # Check for logging arguments first
        if "--quiet" in args:
            if SMART_LOGGING_AVAILABLE:
                enable_quiet_mode()
            else:
                ApplicationFactoryWithSmartLogging._configure_fallback_logging('production')
        elif "--verbose" in args:
            if SMART_LOGGING_AVAILABLE:
                setup_smart_logging('debug')
            else:
                ApplicationFactoryWithSmartLogging._configure_fallback_logging('debug')
        elif "--performance" in args:
            if SMART_LOGGING_AVAILABLE:
                enable_performance_monitoring()
        
        # Create app based on mode arguments
        if "--test" in args:
            return ApplicationFactoryWithSmartLogging.create_test_app()
        elif "--headless" in args:
            return ApplicationFactoryWithSmartLogging.create_headless_app()
        elif "--record" in args:
            return ApplicationFactoryWithSmartLogging.create_recording_app()
        else:
            return ApplicationFactoryWithSmartLogging.create_production_app()
    
    @staticmethod
    def create_app_with_auto_logging():
        """
        Create application with automatic environment-based logging detection.
        
        Auto-detects environment from:
        - Environment variables (TKA_ENVIRONMENT, TKA_DEBUG, etc.)
        - Testing context (PYTEST_CURRENT_TEST)
        - Command line arguments
        """
        if SMART_LOGGING_AVAILABLE:
            # Use smart auto-configuration
            configure_from_environment()
            config = setup_smart_logging()  # Auto-detects environment
            
            # Create app based on detected environment
            detected_env = config.__class__.__name__.replace('Config', '').lower()
            if 'production' in detected_env:
                return ApplicationFactoryWithSmartLogging.create_production_app()
            elif 'test' in detected_env:
                return ApplicationFactoryWithSmartLogging.create_test_app()
            elif 'debug' in detected_env:
                return ApplicationFactoryWithSmartLogging.create_recording_app()
            else:
                return ApplicationFactoryWithSmartLogging.create_headless_app()
        else:
            # Fallback to original factory
            return OriginalApplicationFactory.create_app_from_args()
    
    @staticmethod
    def _configure_fallback_logging(environment: str):
        """
        Fallback logging configuration when smart logging is not available.
        
        Provides basic verbosity reduction for arrow positioning services.
        """
        logger.warning("Smart logging not available, using fallback configuration")
        
        # Reduce arrow positioning verbosity
        verbose_loggers = [
            'application.services.positioning.arrows.orchestration.directional_tuple_processor',
            'application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service',
            'application.services.positioning.arrows.orchestration.arrow_adjustment_lookup_service'
        ]
        
        if environment == 'production':
            level = logging.ERROR
        elif environment == 'testing':
            level = logging.CRITICAL
        elif environment == 'debug':
            level = logging.DEBUG
        else:  # development
            level = logging.WARNING
        
        for logger_name in verbose_loggers:
            logging.getLogger(logger_name).setLevel(level)
        
        logger.info(f"Fallback logging configured for {environment}")


# Convenience functions with smart logging
def get_production_app_with_logging():
    """Get production application with optimized logging."""
    return ApplicationFactoryWithSmartLogging.create_production_app()


def get_test_app_with_logging():
    """Get test application with test-optimized logging."""
    return ApplicationFactoryWithSmartLogging.create_test_app()


def get_headless_app_with_logging():
    """Get headless application with performance monitoring."""
    return ApplicationFactoryWithSmartLogging.create_headless_app()


def get_auto_configured_app():
    """Get application with automatic environment detection and logging."""
    return ApplicationFactoryWithSmartLogging.create_app_with_auto_logging()


# Backward compatibility aliases
ApplicationFactory = ApplicationFactoryWithSmartLogging
get_production_app = get_production_app_with_logging
get_test_app = get_test_app_with_logging 
get_headless_app = get_headless_app_with_logging


# Example usage patterns
def example_usage():
    """Example usage patterns for the enhanced factory."""
    
    # Basic usage - automatically configures logging
    app = ApplicationFactory.create_production_app()  # Quiet logging
    app = ApplicationFactory.create_test_app()        # Silent logging
    app = ApplicationFactory.create_headless_app()    # Performance logging
    
    # Environment-based auto-configuration
    app = ApplicationFactory.create_app_with_auto_logging()
    
    # Command line argument support
    app = ApplicationFactory.create_app_from_args()  # Uses sys.argv
    app = ApplicationFactory.create_app_from_args(['--headless', '--performance'])
    
    # Explicit mode with optimized logging
    app = ApplicationFactory.create_app('production')  # Quiet
    app = ApplicationFactory.create_app('test')        # Silent
    
    return app


if __name__ == "__main__":
    # Quick test
    print("🧪 Testing ApplicationFactory with Smart Logging...")
    
    # Test each mode
    modes = ['production', 'test', 'headless', 'recording']
    
    for mode in modes:
        print(f"\n📱 Testing {mode} mode:")
        try:
            container = ApplicationFactory.create_app(mode)
            print(f"   ✅ {mode} app created successfully")
        except Exception as e:
            print(f"   ❌ {mode} app failed: {e}")
    
    print("\n✅ ApplicationFactory with Smart Logging ready!")
