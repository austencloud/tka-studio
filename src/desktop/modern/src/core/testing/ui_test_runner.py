"""
UI Testing Integration for TKA Main Application

Provides integration points for running UI tests from the main application.
"""
from __future__ import annotations

import logging
import sys

from desktop.modern.core.testing.ai_agent_helpers import TKAAITestHelper
from desktop.modern.core.testing.simple_ui_tester import SimpleUITester


logger = logging.getLogger(__name__)


class UITestRunner:
    """Main UI test runner for integration with TKA application."""

    def __init__(self, headless: bool = True, verbose: bool = False):
        self.headless = headless
        self.verbose = verbose
        self.setup_logging()

    def setup_logging(self):
        """Setup logging for UI testing."""
        level = logging.DEBUG if self.verbose else logging.INFO
        logger.setLevel(level)

        # Add console handler if not present
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def run_quick_validation(self) -> bool:
        """Run quick validation tests to ensure basic functionality works."""
        logger.info("🚀 Running quick UI validation tests...")

        try:
            # Test AI helper first
            helper = TKAAITestHelper(use_test_mode=True)
            ai_result = helper.run_comprehensive_test_suite()

            if not ai_result.success:
                logger.error("❌ AI helper validation failed")
                return False

            logger.info("✅ AI helper validation passed")

            # Test basic UI setup
            tester = SimpleUITester(headless=self.headless)
            setup_success = tester.setup_test_environment()

            if not setup_success:
                logger.error("❌ UI test environment setup failed")
                return False

            logger.info("✅ UI test environment setup successful")
            logger.info("🎉 Quick validation completed successfully!")
            return True

        except Exception as e:
            logger.exception(f"❌ Quick validation failed with exception: {e}")
            return False

    def run_button_tests(self) -> bool:
        """Run comprehensive button tests."""
        logger.info("🚀 Running comprehensive button tests...")

        try:
            tester = SimpleUITester(headless=self.headless)
            result = tester.test_workbench_buttons()

            if result.success:
                logger.info("✅ Button tests passed")
                logger.info(f"📊 Results: {result.metadata}")
            else:
                logger.error("❌ Button tests failed")
                logger.error(f"🐛 Errors: {result.errors}")

            return result.success

        except Exception as e:
            logger.exception(f"❌ Button tests failed with exception: {e}")
            return False

    def run_graph_editor_tests(self) -> bool:
        """Run comprehensive graph editor tests."""
        logger.info("🚀 Running comprehensive graph editor tests...")

        try:
            tester = SimpleUITester(headless=self.headless)
            result = tester.test_graph_editor_interactions()

            if result.success:
                logger.info("✅ Graph editor tests passed")
                logger.info(f"📊 Results: {result.metadata}")
            else:
                logger.error("❌ Graph editor tests failed")
                logger.error(f"🐛 Errors: {result.errors}")

            return result.success

        except Exception as e:
            logger.exception(f"❌ Graph editor tests failed with exception: {e}")
            return False

    def run_comprehensive_tests(self) -> bool:
        """Run all comprehensive UI tests."""
        logger.info("🚀 Running comprehensive UI tests...")

        try:
            tester = SimpleUITester(headless=self.headless)
            result = tester.run_comprehensive_tests()

            if result.success:
                logger.info("✅ Comprehensive tests passed")
                logger.info(f"📊 Results: {result.metadata}")
            else:
                logger.error("❌ Comprehensive tests failed")
                logger.error(f"🐛 Errors: {result.errors}")

            return result.success

        except Exception as e:
            logger.exception(f"❌ Comprehensive tests failed with exception: {e}")
            return False


def handle_test_ui_command(args):
    """Handle --test-ui command line argument."""
    verbose = getattr(args, "verbose", False)
    headless = getattr(args, "headless", True)

    runner = UITestRunner(headless=headless, verbose=verbose)

    # Determine which tests to run based on args
    if hasattr(args, "quick") and args.quick:
        return runner.run_quick_validation()
    if hasattr(args, "buttons") and args.buttons:
        return runner.run_button_tests()
    if hasattr(args, "graph_editor") and args.graph_editor:
        return runner.run_graph_editor_tests()
    # Default to comprehensive tests
    return runner.run_comprehensive_tests()


# Convenience functions for direct usage
def quick_ui_test(verbose: bool = False) -> bool:
    """Run quick UI validation test."""
    runner = UITestRunner(headless=True, verbose=verbose)
    return runner.run_quick_validation()


def full_ui_test(verbose: bool = False) -> bool:
    """Run full UI test suite."""
    runner = UITestRunner(headless=True, verbose=verbose)
    return runner.run_comprehensive_tests()


def test_buttons_only(verbose: bool = False) -> bool:
    """Run button tests only."""
    runner = UITestRunner(headless=True, verbose=verbose)
    return runner.run_button_tests()


def test_graph_editor_only(verbose: bool = False) -> bool:
    """Run graph editor tests only."""
    runner = UITestRunner(headless=True, verbose=verbose)
    return runner.run_graph_editor_tests()
