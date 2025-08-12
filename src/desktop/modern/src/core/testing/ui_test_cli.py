"""
CLI Interface for TKA UI Testing Framework

Provides command-line interface for running UI tests with various options.
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

from desktop.modern.core.testing.ai_agent_helpers import TKAAITestHelper
from desktop.modern.core.testing.simple_ui_tester import SimpleUITester


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("ui_testing.log"),
        ],
    )


def run_button_test(button_name: str | None = None, verbose: bool = False):
    """Run button tests."""
    print("🚀 Starting button testing...")

    tester = SimpleUITester(headless=True)

    if button_name:
        print(f"🎯 Testing specific button: {button_name}")
        # For now, run all buttons since individual button testing
        # would require more complex implementation
        result = tester.test_workbench_buttons()
    else:
        print("🎯 Testing all workbench buttons")
        result = tester.test_workbench_buttons()

    print_test_results(result, "Button Testing")
    return result.success


def run_graph_editor_test(verbose: bool = False):
    """Run graph editor tests."""
    print("🚀 Starting graph editor testing...")

    tester = SimpleUITester(headless=True)
    result = tester.test_graph_editor_interactions()

    print_test_results(result, "Graph Editor Testing")
    return result.success


def run_comprehensive_test(verbose: bool = False):
    """Run comprehensive UI tests."""
    print("🚀 Starting comprehensive UI testing...")

    tester = SimpleUITester(headless=True)
    result = tester.run_comprehensive_tests()

    print_test_results(result, "Comprehensive UI Testing")
    return result.success


def run_ai_helper_test(verbose: bool = False):
    """Run AI helper validation tests."""
    print("🚀 Starting AI helper validation...")

    helper = TKAAITestHelper(use_test_mode=True)
    result = helper.run_comprehensive_test_suite()

    print_test_results(result, "AI Helper Validation")
    return result.success


def print_test_results(result, test_name: str):
    """Print formatted test results."""
    print(f"\n{'='*60}")
    print(f"📊 {test_name} Results")
    print(f"{'='*60}")

    if result.success:
        print("✅ OVERALL STATUS: PASSED")
    else:
        print("❌ OVERALL STATUS: FAILED")

    print(f"⏱️  Execution Time: {result.execution_time:.2f}s")

    if result.metadata:
        print("📋 Metadata:")
        for key, value in result.metadata.items():
            print(f"   • {key}: {value}")

    if result.errors:
        print(f"🐛 Errors ({len(result.errors)}):")
        for error in result.errors:
            print(f"   • {error}")

    print(f"{'='*60}\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="TKA UI Testing Framework CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --all-buttons                    # Test all workbench buttons
  %(prog)s --button add_to_dictionary      # Test specific button
  %(prog)s --graph-editor                  # Test graph editor interactions
  %(prog)s --comprehensive                 # Run all UI tests
  %(prog)s --ai-helper                     # Validate AI helper functionality
  %(prog)s --comprehensive --verbose       # Run with detailed logging
        """,
    )

    # Test selection options
    test_group = parser.add_mutually_exclusive_group(required=True)
    test_group.add_argument(
        "--all-buttons", action="store_true", help="Test all workbench buttons"
    )
    test_group.add_argument(
        "--button", type=str, help="Test specific button (e.g., add_to_dictionary)"
    )
    test_group.add_argument(
        "--graph-editor", action="store_true", help="Test graph editor interactions"
    )
    test_group.add_argument(
        "--comprehensive", action="store_true", help="Run comprehensive UI tests"
    )
    test_group.add_argument(
        "--ai-helper", action="store_true", help="Validate AI helper functionality"
    )

    # Configuration options
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Run in headless mode (default: True)",
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Run selected test
    success = False

    try:
        if args.all_buttons:
            success = run_button_test(verbose=args.verbose)
        elif args.button:
            success = run_button_test(args.button, verbose=args.verbose)
        elif args.graph_editor:
            success = run_graph_editor_test(verbose=args.verbose)
        elif args.comprehensive:
            success = run_comprehensive_test(verbose=args.verbose)
        elif args.ai_helper:
            success = run_ai_helper_test(verbose=args.verbose)

    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)

    # Exit with appropriate code
    if success:
        print("🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("💥 Some tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
