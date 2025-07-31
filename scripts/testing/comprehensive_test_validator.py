#!/usr/bin/env python3
"""
Comprehensive TKA Test Suite Validator
=====================================

Executes ALL 382 tests individually and categorizes their status.
Provides detailed analysis of pass/fail/error states with specific diagnostics.
"""

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import subprocess
import time
from typing import Optional


@dataclass
class TestResult:
    """Individual test execution result."""

    test_id: str
    file_path: str
    test_name: str
    status: str  # PASS, FAIL_IMPORT, FAIL_LOGIC, COLLECTION_ERROR, SKIP
    execution_time: float
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    output: Optional[str] = None


class ComprehensiveTestValidator:
    """Validates all tests in the TKA test suite."""

    def __init__(self, tka_root: Path):
        self.tka_root = tka_root
        self.results: list[TestResult] = []
        self.summary = {
            "total_tests": 0,
            "passed": 0,
            "failed_import": 0,
            "failed_logic": 0,
            "collection_errors": 0,
            "skipped": 0,
            "total_execution_time": 0.0,
        }

    def discover_all_tests(self) -> list[str]:
        """Discover all test items using pytest."""
        print("🔍 Discovering all tests...")

        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "--collect-only", "-q", "--tb=no"],
                cwd=self.tka_root,
                capture_output=True,
                text=True,
                timeout=120,
            )

            # Parse the output to extract test items
            test_items = []
            lines = result.stdout.split("\n")

            for line in lines:
                # Look for test items in the format: path::class::method or path::function
                if (
                    "::" in line
                    and not line.startswith("=")
                    and not line.startswith("<")
                ):
                    # Clean up the line and extract test identifier
                    clean_line = line.strip()
                    if clean_line and not clean_line.startswith("ERROR"):
                        test_items.append(clean_line)

            print(f"📊 Discovered {len(test_items)} test items")
            return test_items

        except Exception as e:
            print(f"❌ Error discovering tests: {e}")
            return []

    def execute_single_test(self, test_item: str) -> TestResult:
        """Execute a single test and categorize the result."""
        print(f"🧪 Testing: {test_item}")

        # Parse test item to extract file path and test name
        parts = test_item.split("::")
        file_path = parts[0]
        test_name = "::".join(parts[1:]) if len(parts) > 1 else "unknown"

        start_time = time.time()

        try:
            # Execute the specific test
            result = subprocess.run(
                ["python", "-m", "pytest", test_item, "-v", "--tb=short"],
                cwd=self.tka_root,
                capture_output=True,
                text=True,
                timeout=60,
            )

            execution_time = time.time() - start_time

            # Analyze the result
            return self._analyze_test_result(
                test_item, file_path, test_name, result, execution_time
            )

        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return TestResult(
                test_id=test_item,
                file_path=file_path,
                test_name=test_name,
                status="FAIL_LOGIC",
                execution_time=execution_time,
                error_message="Test execution timeout (>60s)",
                error_type="TimeoutError",
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult(
                test_id=test_item,
                file_path=file_path,
                test_name=test_name,
                status="COLLECTION_ERROR",
                execution_time=execution_time,
                error_message=str(e),
                error_type=type(e).__name__,
            )

    def _analyze_test_result(
        self,
        test_item: str,
        file_path: str,
        test_name: str,
        result: subprocess.CompletedProcess,
        execution_time: float,
    ) -> TestResult:
        """Analyze subprocess result and categorize the test outcome."""

        output = result.stdout + result.stderr

        # Check for collection errors first
        if "ERRORS" in output and "ERROR collecting" in output:
            error_msg = self._extract_collection_error(output)
            return TestResult(
                test_id=test_item,
                file_path=file_path,
                test_name=test_name,
                status="COLLECTION_ERROR",
                execution_time=execution_time,
                error_message=error_msg,
                error_type="CollectionError",
                output=output[:500],
            )

        # Check for import errors
        if "ModuleNotFoundError" in output or "ImportError" in output:
            error_msg = self._extract_import_error(output)
            return TestResult(
                test_id=test_item,
                file_path=file_path,
                test_name=test_name,
                status="FAIL_IMPORT",
                execution_time=execution_time,
                error_message=error_msg,
                error_type="ImportError",
                output=output[:500],
            )

        # Check for passed tests
        if result.returncode == 0 and "PASSED" in output:
            return TestResult(
                test_id=test_item,
                file_path=file_path,
                test_name=test_name,
                status="PASS",
                execution_time=execution_time,
            )

        # Check for skipped tests
        if "SKIPPED" in output:
            return TestResult(
                test_id=test_item,
                file_path=file_path,
                test_name=test_name,
                status="SKIP",
                execution_time=execution_time,
                error_message="Test skipped",
            )

        # Everything else is a logic failure
        error_msg = self._extract_failure_error(output)
        return TestResult(
            test_id=test_item,
            file_path=file_path,
            test_name=test_name,
            status="FAIL_LOGIC",
            execution_time=execution_time,
            error_message=error_msg,
            error_type="AssertionError",
            output=output[:500],
        )

    def _extract_collection_error(self, output: str) -> str:
        """Extract collection error message."""
        lines = output.split("\n")
        for i, line in enumerate(lines):
            if "ERROR collecting" in line:
                # Look for the actual error in subsequent lines
                for j in range(i + 1, min(i + 10, len(lines))):
                    if lines[j].strip() and not lines[j].startswith("="):
                        return lines[j].strip()
        return "Collection error (details not found)"

    def _extract_import_error(self, output: str) -> str:
        """Extract import error message."""
        lines = output.split("\n")
        for line in lines:
            if "ModuleNotFoundError:" in line or "ImportError:" in line:
                return line.strip()
        return "Import error (details not found)"

    def _extract_failure_error(self, output: str) -> str:
        """Extract test failure error message."""
        lines = output.split("\n")
        for line in lines:
            if "FAILED" in line or "AssertionError" in line or "Error:" in line:
                return line.strip()
        return "Test failed (details not found)"

    def validate_all_tests(self) -> dict:
        """Execute comprehensive validation of all tests."""
        print("🚀 Starting Comprehensive Test Validation")
        print("=" * 60)

        # Discover all tests
        test_items = self.discover_all_tests()
        self.summary["total_tests"] = len(test_items)

        if not test_items:
            print("❌ No tests discovered!")
            return self.summary

        # Execute each test individually
        total_start_time = time.time()

        for i, test_item in enumerate(test_items, 1):
            print(f"\n[{i}/{len(test_items)}] ", end="")

            result = self.execute_single_test(test_item)
            self.results.append(result)

            # Update summary
            if result.status == "PASS":
                self.summary["passed"] += 1
                print("✅ PASS")
            elif result.status == "FAIL_IMPORT":
                self.summary["failed_import"] += 1
                print(f"❌ IMPORT ERROR: {result.error_message}")
            elif result.status == "FAIL_LOGIC":
                self.summary["failed_logic"] += 1
                print(f"❌ LOGIC ERROR: {result.error_message}")
            elif result.status == "COLLECTION_ERROR":
                self.summary["collection_errors"] += 1
                print(f"❌ COLLECTION ERROR: {result.error_message}")
            elif result.status == "SKIP":
                self.summary["skipped"] += 1
                print("⏭️ SKIPPED")

            # Progress update every 25 tests
            if i % 25 == 0:
                self._print_progress_summary(i, len(test_items))

        self.summary["total_execution_time"] = time.time() - total_start_time

        return self.summary

    def _print_progress_summary(self, current: int, total: int):
        """Print progress summary."""
        print(f"\n📊 Progress: {current}/{total} tests completed")
        print(f"   ✅ Passed: {self.summary['passed']}")
        print(f"   ❌ Import Errors: {self.summary['failed_import']}")
        print(f"   ❌ Logic Errors: {self.summary['failed_logic']}")
        print(f"   ❌ Collection Errors: {self.summary['collection_errors']}")
        print(f"   ⏭️ Skipped: {self.summary['skipped']}")

    def generate_detailed_report(self) -> str:
        """Generate detailed validation report."""
        report = []
        report.append("# TKA Test Suite Comprehensive Validation Report")
        report.append("=" * 60)
        report.append("")

        # Summary statistics
        report.append("## EXECUTIVE SUMMARY")
        report.append(f"- **Total Tests**: {self.summary['total_tests']}")
        report.append(
            f"- **Passed**: {self.summary['passed']} ({self.summary['passed'] / self.summary['total_tests'] * 100:.1f}%)"
        )
        report.append(
            f"- **Import Errors**: {self.summary['failed_import']} ({self.summary['failed_import'] / self.summary['total_tests'] * 100:.1f}%)"
        )
        report.append(
            f"- **Logic Errors**: {self.summary['failed_logic']} ({self.summary['failed_logic'] / self.summary['total_tests'] * 100:.1f}%)"
        )
        report.append(
            f"- **Collection Errors**: {self.summary['collection_errors']} ({self.summary['collection_errors'] / self.summary['total_tests'] * 100:.1f}%)"
        )
        report.append(
            f"- **Skipped**: {self.summary['skipped']} ({self.summary['skipped'] / self.summary['total_tests'] * 100:.1f}%)"
        )
        report.append(
            f"- **Total Execution Time**: {self.summary['total_execution_time']:.2f} seconds"
        )
        report.append("")

        # Detailed breakdowns
        self._add_category_breakdown(report, "IMPORT ERRORS", "FAIL_IMPORT")
        self._add_category_breakdown(report, "COLLECTION ERRORS", "COLLECTION_ERROR")
        self._add_category_breakdown(report, "LOGIC ERRORS", "FAIL_LOGIC")

        return "\n".join(report)

    def _add_category_breakdown(self, report: list[str], title: str, status: str):
        """Add category breakdown to report."""
        category_results = [r for r in self.results if r.status == status]

        if not category_results:
            return

        report.append(f"## {title} ({len(category_results)} tests)")
        report.append("")

        for result in category_results[:20]:  # Show first 20
            report.append(f"- **{result.test_id}**")
            report.append(f"  - Error: {result.error_message}")
            report.append(f"  - Time: {result.execution_time:.2f}s")
            report.append("")

        if len(category_results) > 20:
            report.append(f"... and {len(category_results) - 20} more {title.lower()}")
            report.append("")

    def save_results(self, filename: str = "comprehensive_test_results.json"):
        """Save detailed results to JSON file."""
        data = {
            "summary": self.summary,
            "results": [asdict(result) for result in self.results],
            "timestamp": time.time(),
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"📄 Detailed results saved to: {filename}")


def main():
    """Main validation function."""
    tka_root = Path()

    validator = ComprehensiveTestValidator(tka_root)
    summary = validator.validate_all_tests()

    # Generate and save reports
    report = validator.generate_detailed_report()

    with open("comprehensive_test_validation_report.md", "w", encoding="utf-8") as f:
        f.write(report)

    validator.save_results()

    # Print final summary
    print("\n" + "=" * 60)
    print("🎯 COMPREHENSIVE VALIDATION COMPLETE")
    print("=" * 60)
    print(f"📊 Total Tests: {summary['total_tests']}")
    print(
        f"✅ Passed: {summary['passed']} ({summary['passed'] / summary['total_tests'] * 100:.1f}%)"
    )
    print(
        f"❌ Failed: {summary['failed_import'] + summary['failed_logic'] + summary['collection_errors']} ({(summary['failed_import'] + summary['failed_logic'] + summary['collection_errors']) / summary['total_tests'] * 100:.1f}%)"
    )
    print(f"⏱️ Total Time: {summary['total_execution_time']:.2f} seconds")
    print(
        "📄 Reports saved: comprehensive_test_validation_report.md, comprehensive_test_results.json"
    )


if __name__ == "__main__":
    main()
