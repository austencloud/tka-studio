"""
Optimized E2E Test Runner - Fast, Efficient, No Duplication
===========================================================

Runs all tab workflow tests efficiently with shared infrastructure.
Replaces scattered test execution with coordinated, fast testing.
"""

import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from .test_construct_tab_workflow import TestConstructTabWorkflow
from .test_infrastructure import TestInfrastructure, get_test_infrastructure
from .test_sequence_card_workflow import TestSequenceCardWorkflow


class OptimizedTestRunner:
    """
    Optimized test runner that eliminates duplication and runs tests efficiently.

    Features:
    - Single infrastructure setup for all tests
    - Coordinated test execution
    - Fast reset between tests instead of full teardown/setup
    - Comprehensive reporting
    - Failure isolation
    """

    def __init__(self, debug: bool = False, visual_mode: bool = True):
        self.debug = debug
        self.visual_mode = visual_mode
        self.infra: Optional[TestInfrastructure] = None
        self.results = {}
        self.total_time = 0

    def run_all_tab_workflows(self) -> Dict[str, Any]:
        """
        Run all tab workflow tests with optimized infrastructure.

        Returns comprehensive results for all tabs.
        """
        start_time = time.time()

        print("🚀 Starting Optimized E2E Test Suite")
        print("=" * 50)

        # Initialize infrastructure once
        try:
            print("🔧 Initializing test infrastructure...")
            self.infra = get_test_infrastructure(visual_mode=self.visual_mode)

            if self.visual_mode:
                print("👁️ Visual mode enabled - you should see UI interactions!")
            else:
                print("🤖 Headless mode - no UI will be shown")

            if not self.infra.validate_service_health():
                return self._create_error_result("Infrastructure validation failed")

            print("✅ Infrastructure ready")

        except Exception as e:
            return self._create_error_result(f"Infrastructure setup failed: {e}")

        # Define test classes to run
        test_classes = [
            ("Construct Tab", TestConstructTabWorkflow),
            ("Sequence Card Tab", TestSequenceCardWorkflow),
            # Add more tab tests here as they're created
        ]

        # Run each test class
        for tab_name, test_class in test_classes:
            try:
                print(f"\\n📋 Running {tab_name} workflow test...")
                result = self._run_single_tab_test(test_class)
                self.results[tab_name] = result

                if result["success"]:
                    print(f"✅ {tab_name}: PASSED in {result['duration']:.0f}ms")
                else:
                    print(
                        f"❌ {tab_name}: FAILED - {result.get('error', 'Unknown error')}"
                    )

            except Exception as e:
                print(f"❌ {tab_name}: EXCEPTION - {e}")
                self.results[tab_name] = {
                    "success": False,
                    "error": str(e),
                    "duration": 0,
                }

        # Final cleanup
        try:
            if self.infra:
                self.infra.cleanup()
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

        self.total_time = (time.time() - start_time) * 1000

        # Generate summary
        return self._generate_summary()

    def _run_single_tab_test(self, test_class) -> Dict[str, Any]:
        """Run a single tab test with proper error handling."""
        start_time = time.time()

        try:
            # Create test instance
            test_instance = test_class()
            test_instance.setup_class()
            test_instance.setup_method()

            # Run the test
            test_instance.test_complete_tab_workflow()

            # Clean up
            test_instance.teardown_method()

            duration = (time.time() - start_time) * 1000

            return {
                "success": True,
                "duration": duration,
                "errors": getattr(test_instance, "errors", []),
            }

        except Exception as e:
            duration = (time.time() - start_time) * 1000

            return {
                "success": False,
                "duration": duration,
                "error": str(e),
                "errors": (
                    getattr(test_instance, "errors", [])
                    if "test_instance" in locals()
                    else []
                ),
            }

    def _create_error_result(self, error_msg: str) -> Dict[str, Any]:
        """Create error result structure."""
        return {
            "overall_success": False,
            "error": error_msg,
            "results": {},
            "summary": {"total_tests": 0, "passed": 0, "failed": 0, "total_time": 0},
        }

    def _generate_summary(self) -> Dict[str, Any]:
        """Generate comprehensive test summary."""
        passed = sum(
            1 for result in self.results.values() if result.get("success", False)
        )
        failed = len(self.results) - passed
        overall_success = failed == 0

        summary = {
            "overall_success": overall_success,
            "results": self.results,
            "summary": {
                "total_tests": len(self.results),
                "passed": passed,
                "failed": failed,
                "total_time": self.total_time,
                "average_time": (
                    self.total_time / len(self.results) if self.results else 0
                ),
            },
        }

        # Print summary
        print("\\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print(f"Total Tests: {summary['summary']['total_tests']}")
        print(f"✅ Passed: {summary['summary']['passed']}")
        print(f"❌ Failed: {summary['summary']['failed']}")
        print(f"⏱️ Total Time: {summary['summary']['total_time']:.0f}ms")
        print(f"⏱️ Average Time: {summary['summary']['average_time']:.0f}ms")

        if overall_success:
            print("\\n🎉 ALL TESTS PASSED!")
            print("✅ Optimized E2E testing is working efficiently")
        else:
            print("\\n⚠️ Some tests failed")
            for tab_name, result in self.results.items():
                if not result.get("success", False):
                    print(f"   - {tab_name}: {result.get('error', 'Unknown error')}")

        return summary

    def run_specific_tab(self, tab_name: str) -> Dict[str, Any]:
        """Run a specific tab test only."""
        tab_tests = {
            "construct": TestConstructTabWorkflow,
            "sequence_card": TestSequenceCardWorkflow,
        }

        test_class = tab_tests.get(tab_name.lower())
        if not test_class:
            return self._create_error_result(f"Unknown tab: {tab_name}")

        print(f"🚀 Running {tab_name} tab test only...")

        try:
            self.infra = get_test_infrastructure(visual_mode=self.visual_mode)
            result = self._run_single_tab_test(test_class)
            self.results[tab_name] = result

            if self.infra:
                self.infra.cleanup()

            return {
                "overall_success": result["success"],
                "results": {tab_name: result},
                "summary": {
                    "total_tests": 1,
                    "passed": 1 if result["success"] else 0,
                    "failed": 0 if result["success"] else 1,
                    "total_time": result["duration"],
                },
            }

        except Exception as e:
            return self._create_error_result(f"Failed to run {tab_name} test: {e}")


def run_optimized_e2e_tests(
    debug: bool = False, visual_mode: bool = True
) -> Dict[str, Any]:
    """
    Main entry point for optimized E2E testing.

    Args:
        debug: Enable debug output
        visual_mode: Show UI interactions (True) or run headless (False)

    Usage:
        results = run_optimized_e2e_tests(visual_mode=True)  # See UI interactions
        results = run_optimized_e2e_tests(visual_mode=False) # Fast headless
    """
    runner = OptimizedTestRunner(debug=debug, visual_mode=visual_mode)
    return runner.run_all_tab_workflows()


def run_tab_test(
    tab_name: str, debug: bool = False, visual_mode: bool = True
) -> Dict[str, Any]:
    """
    Run a specific tab test.

    Args:
        tab_name: Name of tab to test
        debug: Enable debug output
        visual_mode: Show UI interactions (True) or run headless (False)

    Usage:
        results = run_tab_test('construct', visual_mode=True)  # See the test run
    """
    runner = OptimizedTestRunner(debug=debug, visual_mode=visual_mode)
    return runner.run_specific_tab(tab_name)


# Command line interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Optimized TKA E2E Test Runner")
    parser.add_argument("--tab", type=str, help="Run specific tab test only")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument(
        "--headless", action="store_true", help="Run in headless mode (no UI)"
    )

    args = parser.parse_args()

    visual_mode = (
        not args.headless
    )  # Visual by default, headless only if explicitly requested

    if args.tab:
        results = run_tab_test(args.tab, debug=args.debug, visual_mode=visual_mode)
    else:
        results = run_optimized_e2e_tests(debug=args.debug, visual_mode=visual_mode)

    # Exit with appropriate code
    sys.exit(0 if results["overall_success"] else 1)
