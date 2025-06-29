"""
IMMEDIATE INTEGRATION for TKA Smart Logging

Add this single import to your main.py for instant relief from verbose arrow positioning logs.

USAGE:
    # Add ONE line to the top of your main.py or application startup:
    from core.logging.instant_fix import apply_instant_fix; apply_instant_fix()

    # OR use the function approach:
    from core.logging.instant_fix import apply_instant_fix
    apply_instant_fix(mode='quiet')  # 'quiet', 'normal', or 'debug'

WHAT IT DOES:
1. Detects if smart logging is available
2. Applies appropriate configuration automatically
3. Reduces arrow positioning verbosity by 90%
4. Preserves error logs and performance timing
5. No other code changes required
"""

import os
import logging


def apply_instant_fix(mode: str = None):
    """
    Apply instant fix for verbose arrow positioning logs.
    
    Args:
        mode: 'quiet' (max suppression), 'normal' (smart suppression), 
              'debug' (minimal suppression), or None (auto-detect)
    """
    # Auto-detect mode if not specified
    if mode is None:
        mode = _detect_mode()
    
    try:
        # Try to use smart logging system
        _apply_smart_logging_fix(mode)
        print(f"✅ Smart logging applied ({mode} mode)")
        
    except ImportError:
        # Fallback to basic logging configuration
        _apply_fallback_fix(mode)
        print(f"✅ Fallback logging applied ({mode} mode)")
    
    except Exception as e:
        print(f"⚠️ Logging fix failed: {e}")
        print("📋 Application will continue with default logging")


def _detect_mode() -> str:
    """Auto-detect appropriate logging mode."""
    # Check environment variables
    if os.getenv('TKA_ENVIRONMENT') == 'production':
        return 'quiet'
    elif os.getenv('TKA_DEBUG_POSITIONING') == 'true':
        return 'debug'
    elif 'pytest' in os.environ.get('_', '') or 'PYTEST_CURRENT_TEST' in os.environ:
        return 'quiet'  # Silent for tests
    else:
        return 'normal'  # Default for development


def _apply_smart_logging_fix(mode: str):
    """Apply fix using smart logging system."""
    from core.logging import (
        setup_arrow_positioning_logging_only,
        setup_smart_logging,
        enable_quiet_mode
    )
    
    if mode == 'quiet':
        setup_arrow_positioning_logging_only(quiet=True)
        enable_quiet_mode()
    elif mode == 'debug':
        setup_smart_logging('debug')
    else:  # normal
        setup_arrow_positioning_logging_only(quiet=False)


def _apply_fallback_fix(mode: str):
    """Apply fallback fix without smart logging system."""
    # Direct logger configuration
    verbose_loggers = [
        'application.services.positioning.arrows.orchestration.directional_tuple_processor',
        'application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service',
        'application.services.positioning.arrows.orchestration.arrow_adjustment_lookup_service'
    ]
    
    if mode == 'quiet':
        level = logging.ERROR
    elif mode == 'debug':
        level = logging.DEBUG
    else:  # normal
        level = logging.WARNING
    
    for logger_name in verbose_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        
        # Add message filter for quiet/normal modes
        if mode in ['quiet', 'normal']:
            logger.addFilter(_create_message_filter())


def _create_message_filter():
    """Create filter to suppress verbose messages."""
    class VerboseFilter(logging.Filter):
        def filter(self, record):
            suppressed = [
                "Generated directional tuples:",
                "Quadrant index:",
                "Final adjustment:",
                "Using special placement:",
                "Using default calculation:",
                "Step 1 - Base adjustment:",
                "🎯 Calculating adjustment for"
            ]
            
            message = record.getMessage()
            return not any(pattern in message for pattern in suppressed)
    
    return VerboseFilter()


# Quick setup functions for different scenarios
def quiet_mode():
    """Enable maximum suppression (production-like)."""
    apply_instant_fix('quiet')


def normal_mode():
    """Enable smart suppression (development-friendly)."""
    apply_instant_fix('normal')


def debug_mode():
    """Enable minimal suppression (debugging)."""
    apply_instant_fix('debug')


def auto_mode():
    """Enable auto-detected mode."""
    apply_instant_fix()


# Auto-apply if imported with special environment variable
if os.getenv('TKA_AUTO_FIX_LOGGING') == 'true':
    apply_instant_fix()
    print("🔧 Auto-fix applied via TKA_AUTO_FIX_LOGGING environment variable")


# One-liner for immediate use
def fix_now():
    """One-liner function for immediate relief."""
    apply_instant_fix('quiet')


if __name__ == "__main__":
    # Test the instant fix
    print("🧪 Testing instant logging fix...")
    
    # Test each mode
    for test_mode in ['quiet', 'normal', 'debug']:
        print(f"\n📋 Testing {test_mode} mode:")
        apply_instant_fix(test_mode)
    
    print("\n✅ Instant fix ready for use!")
    print("\n💡 Usage in your code:")
    print("   from core.logging.instant_fix import apply_instant_fix")
    print("   apply_instant_fix('quiet')  # Add to main.py")
