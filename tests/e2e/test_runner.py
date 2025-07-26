"""
E2E Test Runner for TKA Application

Provides a unified interface for running all end-to-end tests
with proper test isolation, reporting, and error handling.
"""

import logging
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Type

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from base_e2e_test import BaseE2ETest

logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """Container for test execution results."""

    test_name: str
    success: bool
    duration: float
    error_message: str = ""


class E2ETestRunner:
    """
    Runner for executing end-to-end tests with proper isolation and reporting.

    Features:
    - Test isolation to prevent interference between tests
    - Comprehensive result reporting
    - Error handling and cleanup
    - Configurable test execution order
    """

    def __init__(self):
        self.test_results: List[TestResult] = []
        self.total_start_time = 0

    def register_test(self, test_class: Type[BaseE2ETest]) -> None:
        """Register a test class to be executed."""
        # Tests are discovered automatically, but this could be used
        # for explicit test registration in the future
        pass

    def run_all_tests(self) -> bool:
        """Run all available E2E tests."""
        logger.info("RUNNER: Starting E2E test suite execution...")
        self.total_start_time = time.time()

        # Discover and run tests
        test_modules = self._discover_test_modules()

        if not test_modules:
            logger.warning("WARNING: No test modules found")
            return False

        logger.info(f"RUNNER: Found {len(test_modules)} test modules")

        # Execute each test module
        for module_name, test_function in test_modules.items():
            self._run_single_test(module_name, test_function)

        # Generate final report
        self._generate_final_report()

        # Return overall success
        return all(result.success for result in self.test_results)

    def run_specific_test(self, test_name: str) -> bool:
        """Run a specific test by name."""
        logger.info(f"RUNNER: Running specific test: {test_name}")
        self.total_start_time = time.time()

        test_modules = self._discover_test_modules()

        if test_name not in test_modules:
            logger.error(f"ERROR: Test '{test_name}' not found")
            logger.info(f"Available tests: {list(test_modules.keys())}")
            return False

        test_function = test_modules[test_name]
        self._run_single_test(test_name, test_function)

        self._generate_final_report()

        return len(self.test_results) > 0 and self.test_results[0].success

    def _discover_test_modules(self) -> Dict[str, callable]:
        """Discover all test modules in the e2e directory."""
        test_modules = {}

        # Get current directory
        e2e_dir = Path(__file__).parent

        # Look for test files
        for test_file in e2e_dir.glob("test_*.py"):
            if test_file.name == "test_runner.py":
                continue

            module_name = test_file.stem

            try:
                # Import the module
                import importlib.util

                spec = importlib.util.spec_from_file_location(module_name, test_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Look for a run function with multiple naming patterns
                possible_function_names = [
                    f"run_{module_name.replace('test_', '')}",
                    f"run_{module_name.replace('test_', '')}_test",
                    f"run_{module_name}",
                ]

                function_found = False
                for func_name in possible_function_names:
                    if hasattr(module, func_name):
                        test_modules[module_name] = getattr(module, func_name)
                        logger.info(
                            f"DISCOVERED: {module_name} with function {func_name}"
                        )
                        function_found = True
                        break

                if not function_found:
                    logger.warning(f"WARNING: No run function found in {module_name}")

            except Exception as e:
                logger.error(f"ERROR: Failed to import {module_name}: {e}")

        return test_modules

    def _run_single_test(self, test_name: str, test_function: callable):
        """Run a single test with proper isolation and error handling."""
        logger.info(f"RUNNER: Executing test: {test_name}")

        start_time = time.time()
        success = False
        error_message = ""

        try:
            # Execute the test function
            success = test_function()

        except Exception as e:
            logger.error(f"ERROR: Test {test_name} raised exception: {e}")
            import traceback

            traceback.print_exc()
            error_message = str(e)
            success = False

        finally:
            # Calculate duration
            duration = time.time() - start_time

            # Store result
            result = TestResult(
                test_name=test_name,
                success=success,
                duration=duration,
                error_message=error_message,
            )
            self.test_results.append(result)

            # Log immediate result
            status = "PASSED" if success else "FAILED"
            logger.info(f"RESULT: {test_name} {status} in {duration:.2f}s")

            # Wait between tests to ensure proper cleanup
            time.sleep(1)

    def _generate_final_report(self):
        """Generate and display the final test report."""
        total_duration = time.time() - self.total_start_time

        logger.info("=" * 60)
        logger.info("E2E TEST SUITE RESULTS")
        logger.info("=" * 60)

        passed_count = sum(1 for result in self.test_results if result.success)
        failed_count = len(self.test_results) - passed_count

        logger.info(f"Total Tests: {len(self.test_results)}")
        logger.info(f"Passed: {passed_count}")
        logger.info(f"Failed: {failed_count}")
        logger.info(f"Total Duration: {total_duration:.2f}s")
        logger.info("")

        # Individual test results
        for result in self.test_results:
            status = "PASS" if result.success else "FAIL"
            logger.info(f"{status:4} | {result.test_name:30} | {result.duration:6.2f}s")
            if result.error_message:
                logger.info(f"     | Error: {result.error_message}")

        logger.info("=" * 60)

        # Overall result
        if failed_count == 0:
            logger.info("🎉 ALL TESTS PASSED!")
        else:
            logger.info(f"❌ {failed_count} TEST(S) FAILED")

    def get_results(self) -> List[TestResult]:
        """Get the test results."""
        return self.test_results.copy()


def main():
    """Main entry point for the E2E test runner."""
    import argparse

    parser = argparse.ArgumentParser(description="TKA E2E Test Runner")
    parser.add_argument(
        "--test",
        type=str,
        help="Run a specific test by name (e.g., test_start_position_transfer)",
    )
    parser.add_argument("--list", action="store_true", help="List available tests")

    args = parser.parse_args()

    runner = E2ETestRunner()

    if args.list:
        # List available tests
        test_modules = runner._discover_test_modules()
        print("Available E2E tests:")
        for test_name in test_modules.keys():
            print(f"  - {test_name}")
        return

    if args.test:
        # Run specific test
        success = runner.run_specific_test(args.test)
    else:
        # Run all tests
        success = runner.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
