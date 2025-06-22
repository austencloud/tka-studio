#!/usr/bin/env python3
"""
Comprehensive automated testing script that runs different test suites
and provides detailed reporting.
"""

import subprocess
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class TestResult:
    name: str
    passed: bool
    duration: float
    output: str
    error_output: str
    test_count: int = 0
    failure_count: int = 0


class AutomatedTestRunner:
    """Runs automated tests with comprehensive reporting."""

    def __init__(self):
        self.results: List[TestResult] = []
        self.start_time = datetime.now()

    def run_test_suite(
        self, name: str, command: List[str], critical: bool = False
    ) -> TestResult:
        """Run a test suite and capture results."""
        print(f"\nRunning {name}...")
        print(f"   Command: {' '.join(command)}")

        start_time = time.time()
        result = subprocess.run(
            command, capture_output=True, text=True, cwd=Path.cwd(), check=False
        )
        duration = time.time() - start_time

        test_result = TestResult(
            name=name,
            passed=result.returncode == 0,
            duration=duration,
            output=result.stdout,
            error_output=result.stderr,
        )

        # Extract test counts from pytest output
        if "pytest" in command[0] or (len(command) > 1 and "pytest" in command[1]):
            test_result.test_count, test_result.failure_count = (
                self.parse_pytest_output(result.stdout)
            )

        self.results.append(test_result)

        if test_result.passed:
            print(f"   PASSED {name} ({duration:.1f}s)")
            if test_result.test_count > 0:
                print(
                    f"      Tests: {test_result.test_count}, Failures: {test_result.failure_count}"
                )
        else:
            print(f"   FAILED {name} ({duration:.1f}s)")
            if critical:
                print("   CRITICAL TEST FAILURE!")
            if test_result.error_output:
                print(f"      Error: {test_result.error_output[:200]}...")

        return test_result

    def parse_pytest_output(self, output: str) -> tuple[int, int]:
        """Parse pytest output to extract test counts."""
        lines = output.split("\n")
        for line in lines:
            if "passed" in line and ("failed" in line or "error" in line):
                # Look for lines like "5 passed, 2 failed in 1.23s"
                parts = line.split()
                passed_count = 0
                failed_count = 0

                for i, part in enumerate(parts):
                    if part == "passed" and i > 0:
                        try:
                            passed_count = int(parts[i - 1])
                        except ValueError:
                            pass
                    elif part == "failed" and i > 0:
                        try:
                            failed_count = int(parts[i - 1])
                        except ValueError:
                            pass

                return passed_count + failed_count, failed_count
            elif "passed in" in line:
                # Look for lines like "5 passed in 1.23s"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "passed" and i > 0:
                        try:
                            return int(parts[i - 1]), 0
                        except ValueError:
                            pass

        return 0, 0

    def run_all_tests(self):
        """Run all automated test suites."""
        print("Starting Automated Test Suite")
        print("=" * 50)

        # Critical tests that must always pass
        critical_tests = [
            {
                "name": "Regression Tests (Critical)",
                "command": [
                    "python",
                    "-m",
                    "pytest",
                    "tests/regression/bugs/",
                    "-v",
                    "--tb=short",
                ],
                "critical": True,
            },
            {
                "name": "Specification Tests (Core Behavior)",
                "command": [
                    "python",
                    "-m",
                    "pytest",
                    "tests/specification/",
                    "-v",
                    "--tb=short",
                ],
                "critical": True,
            },
        ]

        # Important but not critical tests
        important_tests = [
            {
                "name": "Unit Tests",
                "command": [
                    "python",
                    "-m",
                    "pytest",
                    "tests/unit/",
                    "-x",
                    "--tb=short",
                ],
                "critical": False,
            }
        ]

        # Run critical tests first
        critical_failures = 0
        for test_config in critical_tests:
            result = self.run_test_suite(**test_config)
            if not result.passed:
                critical_failures += 1

        # If critical tests fail, stop here
        if critical_failures > 0:
            print(f"\nCRITICAL: {critical_failures} test suites FAILED!")
            print("Stopping execution - fix critical issues first")
            self.generate_report()
            return False

        # Run important tests
        for test_config in important_tests:
            self.run_test_suite(**test_config)

        # Generate final report
        self.generate_report()
        return self.all_tests_passed()

    def all_tests_passed(self) -> bool:
        """Check if all tests passed."""
        return all(result.passed for result in self.results)

    def generate_report(self):
        """Generate a comprehensive test report."""
        total_duration = (datetime.now() - self.start_time).total_seconds()
        total_tests = sum(r.test_count for r in self.results)
        total_failures = sum(r.failure_count for r in self.results)
        passed_suites = sum(1 for r in self.results if r.passed)

        print("\n" + "=" * 60)
        print("AUTOMATED TEST REPORT")
        print("=" * 60)
        print(f"Total Duration: {total_duration:.1f}s")
        print(f"Test Suites: {len(self.results)}")
        print(f"Passed Suites: {passed_suites}/{len(self.results)}")
        print(f"Total Tests: {total_tests}")
        print(f"Total Failures: {total_failures}")

        print("\nSuite Results:")
        for result in self.results:
            status = "PASS" if result.passed else "FAIL"
            print(
                f"  {status} {result.name}: {result.test_count} tests, {result.failure_count} failures ({result.duration:.1f}s)"
            )

        if not self.all_tests_passed():
            print("\nFAILURES DETECTED:")
            for result in self.results:
                if not result.passed:
                    print(f"\nFAILED: {result.name}")
                    if result.error_output:
                        print(f"   Error: {result.error_output[:300]}...")
                    if "FAILED" in result.output:
                        # Extract failed test names
                        failed_tests = [
                            line
                            for line in result.output.split("\n")
                            if "FAILED" in line
                        ]
                        for failed_test in failed_tests[:5]:  # Show first 5 failures
                            print(f"   {failed_test}")

        # Save detailed report to file
        self.save_detailed_report()

        overall_status = (
            "ALL TESTS PASSED" if self.all_tests_passed() else "SOME TESTS FAILED"
        )
        print(f"\nOverall Status: {overall_status}")

    def save_detailed_report(self):
        """Save detailed report to JSON file."""
        report_data = {
            "timestamp": self.start_time.isoformat(),
            "total_duration": (datetime.now() - self.start_time).total_seconds(),
            "overall_passed": self.all_tests_passed(),
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "duration": r.duration,
                    "test_count": r.test_count,
                    "failure_count": r.failure_count,
                    "output": r.output,
                    "error_output": r.error_output,
                }
                for r in self.results
            ],
        }

        reports_dir = Path("test_reports")
        reports_dir.mkdir(exist_ok=True)

        report_file = (
            reports_dir
            / f"test_report_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

        print(f"Detailed report saved: {report_file}")


def main():
    """Main entry point."""
    runner = AutomatedTestRunner()
    success = runner.run_all_tests()

    # Exit with appropriate code for CI/CD systems
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
