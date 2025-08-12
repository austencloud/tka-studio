#!/usr/bin/env python3
"""
TKA UI Testing Framework - Main Test Script

Run comprehensive UI tests for the TKA application.
This script can be run directly or imported as a module.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path
import sys


# Add the src directory to the Python path
current_dir = Path(__file__).parent
src_dir = current_dir.parent.parent  # Go up to the src directory
sys.path.insert(0, str(src_dir))

from desktop.modern.core.testing import (
    full_ui_test,
    quick_ui_test,
    test_buttons_only,
    test_graph_editor_only,
)


def main():
    """Main entry point for UI testing."""
    parser = argparse.ArgumentParser(
        description="TKA UI Testing Framework - Comprehensive Testing Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ui_test_main.py --quick           # Quick validation tests
  python ui_test_main.py --buttons         # Test all buttons
  python ui_test_main.py --graph-editor    # Test graph editor
  python ui_test_main.py --comprehensive   # Run all tests
  python ui_test_main.py --all --verbose   # Run everything with details
        """,
    )

    # Test selection
    parser.add_argument(
        "--quick", action="store_true", help="Run quick validation tests"
    )
    parser.add_argument("--buttons", action="store_true", help="Test workbench buttons")
    parser.add_argument(
        "--graph-editor", action="store_true", help="Test graph editor interactions"
    )
    parser.add_argument(
        "--comprehensive", action="store_true", help="Run comprehensive tests"
    )
    parser.add_argument("--all", action="store_true", help="Run all test categories")

    # Configuration
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--headless", action="store_true", default=True, help="Run in headless mode"
    )

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Determine what tests to run
    run_quick = args.quick or args.all
    run_buttons = args.buttons or args.all
    run_graph_editor = args.graph_editor or args.all
    run_comprehensive = args.comprehensive or args.all

    # If nothing specified, run quick validation
    if not any([run_quick, run_buttons, run_graph_editor, run_comprehensive]):
        run_quick = True

    success_count = 0
    total_count = 0

    print("🚀 Starting TKA UI Testing Framework")
    print("=" * 60)

    try:
        # Quick validation tests
        if run_quick:
            print("\n📋 Running Quick Validation Tests...")
            total_count += 1
            if quick_ui_test(verbose=args.verbose):
                success_count += 1
                print("✅ Quick validation: PASSED")
            else:
                print("❌ Quick validation: FAILED")

        # Button tests
        if run_buttons:
            print("\n📋 Running Button Tests...")
            total_count += 1
            if test_buttons_only(verbose=args.verbose):
                success_count += 1
                print("✅ Button tests: PASSED")
            else:
                print("❌ Button tests: FAILED")

        # Graph editor tests
        if run_graph_editor:
            print("\n📋 Running Graph Editor Tests...")
            total_count += 1
            if test_graph_editor_only(verbose=args.verbose):
                success_count += 1
                print("✅ Graph editor tests: PASSED")
            else:
                print("❌ Graph editor tests: FAILED")

        # Comprehensive tests
        if run_comprehensive:
            print("\n📋 Running Comprehensive Tests...")
            total_count += 1
            if full_ui_test(verbose=args.verbose):
                success_count += 1
                print("✅ Comprehensive tests: PASSED")
            else:
                print("❌ Comprehensive tests: FAILED")

        # Final summary
        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("=" * 60)
        print(f"✅ Successful test suites: {success_count}/{total_count}")
        print(f"❌ Failed test suites: {total_count - success_count}/{total_count}")

        if success_count == total_count:
            print("🎉 ALL TESTS PASSED!")
            return 0
        print("💥 SOME TESTS FAILED!")
        return 1

    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
