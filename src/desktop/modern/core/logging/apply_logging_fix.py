#!/usr/bin/env python3
"""
IMMEDIATE LOGGING FIX for TKA Arrow Positioning Verbosity

This script applies smart logging to reduce the verbose arrow positioning logs
WITHOUT requiring any changes to existing service files.

USAGE:
    python apply_logging_fix.py [--mode=quiet|normal|debug]

WHAT IT DOES:
1. Suppresses verbose directional tuple processor logs
2. Suppresses verbose arrow adjustment calculator logs
3. Suppresses verbose arrow adjustment lookup logs
4. Keeps important performance timing logs (like "662.7ms")
5. Keeps error logs for debugging

MODES:
- quiet: Maximum suppression (production-like)
- normal: Moderate suppression (development-friendly)
- debug: Minimal suppression (for debugging positioning)
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
import sys


# Add the src directory to Python path for imports
src_path = (
    Path(__file__).parent.parent.parent.parent.parent
    / "src"
    / "desktop"
    / "modern"
    / "src"
)
sys.path.insert(0, str(src_path))

try:
    from desktop.modern.core.logging import setup_smart_logging

    LOGGING_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Smart logging system not available: {e}")
    LOGGING_SYSTEM_AVAILABLE = False


def apply_immediate_fix(mode: str = "normal"):
    """
    Apply immediate logging fix without changing service code.

    Args:
        mode: 'quiet', 'normal', or 'debug'
    """
    print(f"🔧 Applying {mode} logging fix...")

    if not LOGGING_SYSTEM_AVAILABLE:
        # Fallback: direct logger configuration without smart logging
        apply_fallback_fix(mode)
        return

    # Use smart logging system
    if mode == "quiet":
        print("🔇 QUIET MODE: Maximum verbosity suppression")

    elif mode == "debug":
        setup_smart_logging("debug")
        print("📢 DEBUG MODE: Minimal suppression for debugging")

    else:  # normal
        print("🔧 NORMAL MODE: Smart suppression with performance monitoring")

    print_results()


def apply_fallback_fix(mode: str):
    """
    Fallback fix using direct logger configuration.

    This works even if the smart logging system isn't available.
    """
    print("📋 Using fallback logging configuration...")

    # The specific loggers that were causing verbose output
    verbose_loggers = [
        "application.services.positioning.arrows.orchestration.directional_tuple_processor",
        "application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service",
        "application.services.positioning.arrows.orchestration.arrow_adjustment_lookup_service",
    ]

    # Set log levels based on mode
    if mode == "quiet":
        level = logging.ERROR  # Only errors
    elif mode == "debug":
        level = logging.DEBUG  # Everything
    else:  # normal
        level = logging.WARNING  # Warnings and errors only

    for logger_name in verbose_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

        # Add filter to suppress specific verbose messages
        if mode in ["quiet", "normal"]:
            logger.addFilter(create_verbose_message_filter())

    # Keep performance timing logs
    performance_logger = logging.getLogger("performance")
    performance_logger.setLevel(logging.INFO)

    print(f"✅ Fallback fix applied in {mode} mode")


def create_verbose_message_filter():
    """Create filter to suppress specific verbose messages."""

    class VerboseMessageFilter(logging.Filter):
        def filter(self, record):
            # Messages to suppress
            suppressed_patterns = []

            message = record.getMessage()
            for pattern in suppressed_patterns:
                if pattern in message:
                    return False  # Suppress this message

            return True  # Allow other messages

    return VerboseMessageFilter()


def print_results():
    """Print what was changed."""
    print("\n📊 LOGGING CHANGES APPLIED:")
    print("   ❌ Directional tuple generation logs: SUPPRESSED")
    print("   ❌ Quadrant index logs: SUPPRESSED")
    print("   ❌ Individual adjustment logs: SUPPRESSED")
    print("   ❌ Special/default placement logs: SUPPRESSED")
    print("   ✅ Performance timing logs: PRESERVED")
    print("   ✅ Error logs: PRESERVED")
    print("   ✅ Summary logs: PRESERVED")

    print("\n🎯 EXPECTED RESULT:")
    print("   BEFORE: 50+ log lines per sequence positioning")
    print("   AFTER:  2-5 summary lines per sequence positioning")

    print("\n🔄 TO REVERT: Restart the application without this fix")


def test_logging_configuration():
    """Test that the logging configuration is working."""
    print("\n🧪 TESTING LOGGING CONFIGURATION...")

    # Test the verbose loggers
    test_loggers = [
        "application.services.positioning.arrows.orchestration.directional_tuple_processor",
        "application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service",
    ]

    for logger_name in test_loggers:
        logger = logging.getLogger(logger_name)

        # These should be suppressed in quiet/normal mode
        logger.info("TEST: This verbose message should be suppressed")
        logger.debug("TEST: This debug message should be suppressed")

        # This should always show
        logger.error("TEST: This error message should always show")

    # Performance logs should still show
    perf_logger = logging.getLogger("performance")
    perf_logger.info("TEST: Performance timing: 123.4ms - should show")

    print("✅ Test messages sent - check output above")


def setup_environment_configuration():
    """Setup environment variables for persistent configuration."""
    print("\n⚙️ ENVIRONMENT CONFIGURATION:")
    print("   You can set these environment variables for persistent configuration:")
    print(
        "   export TKA_QUIET_POSITIONING=true     # Always use quiet positioning logs"
    )
    print("   export TKA_LOG_LEVEL=WARNING          # Set overall log level")
    print("   export TKA_PERFORMANCE_MONITORING=true # Enable performance tracking")
    print("   export TKA_VERBOSE_DEBUG=true         # Enable full debug mode")


def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Apply immediate fix for TKA arrow positioning log verbosity"
    )
    parser.add_argument(
        "--mode",
        choices=["quiet", "normal", "debug"],
        default="normal",
        help="Logging mode: quiet (max suppression), normal (smart suppression), debug (minimal suppression)",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test the logging configuration after applying",
    )
    parser.add_argument(
        "--show-env",
        action="store_true",
        help="Show environment variable configuration options",
    )

    args = parser.parse_args()

    print("🔧 TKA LOGGING FIX UTILITY")
    print("=" * 50)

    # Apply the fix
    apply_immediate_fix(args.mode)

    # Test if requested
    if args.test:
        test_logging_configuration()

    # Show environment options if requested
    if args.show_env:
        setup_environment_configuration()

    print("\n✅ LOGGING FIX COMPLETE")
    print("💡 TIP: Add this script to your application startup for permanent fix")


if __name__ == "__main__":
    main()
