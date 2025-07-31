#!/usr/bin/env python3
"""
Complete TKA Test Suite Validator
=================================

Executes ALL 387 tests with segmentation fault avoidance and provides
comprehensive categorization and analysis.
"""

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import subprocess
import time
from typing import Dict, List, Optional


@dataclass
class TestResult:
    """Individual test execution result."""

    test_id: str
    file_path: str
    test_name: str
    status: str  # PASS, FAIL_IMPORT, FAIL_LOGIC, COLLECTION_ERROR, SKIP, SEGFAULT
    execution_time: float
    error_message: Optional[str] = None
    error_type: Optional[str] = None


class CompleteTestValidator:
    """Validates all tests in the TKA test suite with segfault avoidance."""

    def __init__(self, tka_root: Path):
        self.tka_root = tka_root
        self.results: List[TestResult] = []

        # Define test categories to run separately to avoid resource conflicts
        self.test_categories = {
            "core_services": "tests/unit/services/",
            "cross_platform": "tests/cross_platform/",
            "interface_coverage": "tests/interface_coverage/",
            "interface_completeness": "tests/interface_completeness/",
            "service_implementation": "tests/service_implementation/",
            "integration_workflows": "tests/integration/test_interface_workflows.py",
            "integration_menu": "tests/integration/test_menu_bar_layout.py",
            "launcher_tests": "launcher/tests/",  # Run separately to avoid segfaults
            "modern_unit_core": "src/desktop/modern/tests/unit/core/",
            "modern_unit_interfaces": "src/desktop/modern/tests/unit/interfaces/",
            "modern_unit_presentation": "src/desktop/modern/tests/unit/presentation/",
            "modern_integration": "src/desktop/modern/tests/integration/",
            "modern_spec_core": "src/desktop/modern/tests/specification/core/",
            "modern_spec_domain": "src/desktop/modern/tests/specification/domain/",
            "modern_application": "src/desktop/modern/tests/application/",
            "modern_framework": "src/desktop/modern/tests/framework/",
            "modern_improved_arch": "src/desktop/modern/tests/improved_architecture/",
            "modern_root_tests": "src/desktop/modern/tests/test_*.py",
        }

    def discover_tests_in_category(self, category: str, path: str) -> List[str]:
        """Discover all test items in a specific category."""
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", path, "--collect-only", "-q"],
                cwd=self.tka_root,
                capture_output=True,
                text=True,
                timeout=60,
            )

            test_items = []
            lines = result.stdout.split("\n")

            for line in lines:
                line = line.strip()
                if (
                    "::" in line
                    and not line.startswith("=")
                    and not line.startswith("<")
                ):
                    # Extract test identifier
                    if not line.startswith("ERROR") and not line.startswith("FAILED"):
                        test_items.append(line)

            return test_items

        except Exception as e:
            print(f"❌ Error discovering tests in {category}: {e}")
            return []

    def execute_test_category(self, category: str, path: str) -> List[TestResult]:
        """Execute all tests in a category and return results."""
        print(f"\n🔍 Executing category: {category} ({path})")

        # Discover tests first
        test_items = self.discover_tests_in_category(category, path)
        if not test_items:
            print(f"⚪ No tests found in {category}")
            return []

        print(f"📊 Found {len(test_items)} tests in {category}")

        category_results = []

        # For launcher tests, run them separately to avoid segfaults
        if category == "launcher_tests":
            return self._execute_launcher_tests_safely(test_items)

        # For other categories, run them normally
        start_time = time.time()

        try:
            result = subprocess.run(
                ["python", "-m", "pytest", path, "-v", "--tb=short"],
                cwd=self.tka_root,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes max per category
            )

            execution_time = time.time() - start_time

            # Parse results for each test
            category_results = self._parse_category_results(
                test_items,
                result.stdout + result.stderr,
                execution_time / len(test_items),
            )

        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            # Mark all tests as timeout
            for test_item in test_items:
                category_results.append(
                    TestResult(
                        test_id=test_item,
                        file_path=test_item.split("::")[0],
                        test_name="::".join(test_item.split("::")[1:]),
                        status="FAIL_LOGIC",
                        execution_time=execution_time / len(test_items),
                        error_message="Category execution timeout",
                        error_type="TimeoutError",
                    )
                )
        except Exception as e:
            # Mark all tests as errors
            for test_item in test_items:
                category_results.append(
                    TestResult(
                        test_id=test_item,
                        file_path=test_item.split("::")[0],
                        test_name="::".join(test_item.split("::")[1:]),
                        status="COLLECTION_ERROR",
                        execution_time=0.0,
                        error_message=str(e),
                        error_type=type(e).__name__,
                    )
                )

        return category_results

    def _execute_launcher_tests_safely(self, test_items: List[str]) -> List[TestResult]:
        """Execute launcher tests individually to avoid segfaults."""
        print("🛡️ Executing launcher tests individually to avoid segfaults...")

        results = []

        for i, test_item in enumerate(test_items, 1):
            print(f"  [{i}/{len(test_items)}] {test_item}")

            start_time = time.time()

            try:
                result = subprocess.run(
                    ["python", "-m", "pytest", test_item, "-v", "--tb=short"],
                    cwd=self.tka_root,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

                execution_time = time.time() - start_time

                # Parse individual result
                test_result = self._parse_individual_test_result(
                    test_item,
                    result.stdout + result.stderr,
                    execution_time,
                    result.returncode,
                )
                results.append(test_result)

            except subprocess.TimeoutExpired:
                execution_time = time.time() - start_time
                results.append(
                    TestResult(
                        test_id=test_item,
                        file_path=test_item.split("::")[0],
                        test_name="::".join(test_item.split("::")[1:]),
                        status="FAIL_LOGIC",
                        execution_time=execution_time,
                        error_message="Test execution timeout",
                        error_type="TimeoutError",
                    )
                )
            except Exception as e:
                execution_time = time.time() - start_time
                results.append(
                    TestResult(
                        test_id=test_item,
                        file_path=test_item.split("::")[0],
                        test_name="::".join(test_item.split("::")[1:]),
                        status="COLLECTION_ERROR",
                        execution_time=execution_time,
                        error_message=str(e),
                        error_type=type(e).__name__,
                    )
                )

        return results

    def _parse_category_results(
        self, test_items: List[str], output: str, avg_time: float
    ) -> List[TestResult]:
        """Parse category execution results."""
        results = []

        for test_item in test_items:
            # Determine status based on output
            if f"{test_item} PASSED" in output:
                status = "PASS"
                error_message = None
                error_type = None
            elif f"{test_item} FAILED" in output:
                status = "FAIL_LOGIC"
                error_message = self._extract_failure_message(output, test_item)
                error_type = "AssertionError"
            elif f"{test_item} SKIPPED" in output:
                status = "SKIP"
                error_message = "Test skipped"
                error_type = None
            elif "ModuleNotFoundError" in output or "ImportError" in output:
                status = "FAIL_IMPORT"
                error_message = self._extract_import_error(output)
                error_type = "ImportError"
            elif "ERROR collecting" in output:
                status = "COLLECTION_ERROR"
                error_message = self._extract_collection_error(output)
                error_type = "CollectionError"
            else:
                # Default to logic failure if we can't determine
                status = "FAIL_LOGIC"
                error_message = "Unknown test failure"
                error_type = "UnknownError"

            results.append(
                TestResult(
                    test_id=test_item,
                    file_path=test_item.split("::")[0],
                    test_name="::".join(test_item.split("::")[1:]),
                    status=status,
                    execution_time=avg_time,
                    error_message=error_message,
                    error_type=error_type,
                )
            )

        return results

    def _parse_individual_test_result(
        self, test_item: str, output: str, execution_time: float, return_code: int
    ) -> TestResult:
        """Parse individual test result."""
        if return_code == 0 and "PASSED" in output:
            status = "PASS"
            error_message = None
            error_type = None
        elif "SKIPPED" in output:
            status = "SKIP"
            error_message = "Test skipped"
            error_type = None
        elif "ModuleNotFoundError" in output or "ImportError" in output:
            status = "FAIL_IMPORT"
            error_message = self._extract_import_error(output)
            error_type = "ImportError"
        elif "ERROR collecting" in output:
            status = "COLLECTION_ERROR"
            error_message = self._extract_collection_error(output)
            error_type = "CollectionError"
        else:
            status = "FAIL_LOGIC"
            error_message = self._extract_failure_message(output, test_item)
            error_type = "AssertionError"

        return TestResult(
            test_id=test_item,
            file_path=test_item.split("::")[0],
            test_name="::".join(test_item.split("::")[1:]),
            status=status,
            execution_time=execution_time,
            error_message=error_message,
            error_type=error_type,
        )

    def _extract_import_error(self, output: str) -> str:
        """Extract import error message."""
        lines = output.split("\n")
        for line in lines:
            if "ModuleNotFoundError:" in line or "ImportError:" in line:
                return line.strip()
        return "Import error (details not found)"

    def _extract_collection_error(self, output: str) -> str:
        """Extract collection error message."""
        lines = output.split("\n")
        for line in lines:
            if "ERROR collecting" in line:
                return line.strip()
        return "Collection error (details not found)"

    def _extract_failure_message(self, output: str, test_item: str) -> str:
        """Extract test failure message."""
        lines = output.split("\n")
        for line in lines:
            if "FAILED" in line and test_item in line:
                return line.strip()
        return "Test failed (details not found)"

    def validate_all_tests(self) -> Dict:
        """Execute comprehensive validation of all tests."""
        print("🚀 Starting Complete Test Suite Validation")
        print("=" * 60)

        total_start_time = time.time()

        for category, path in self.test_categories.items():
            category_results = self.execute_test_category(category, path)
            self.results.extend(category_results)

            # Print immediate summary
            passed = len([r for r in category_results if r.status == "PASS"])
            total = len(category_results)
            if total > 0:
                print(
                    f"✅ {category}: {passed}/{total} passed ({passed / total * 100:.1f}%)"
                )
            else:
                print(f"⚪ {category}: No tests found")

        total_execution_time = time.time() - total_start_time

        # Generate summary
        summary = self._generate_summary(total_execution_time)
        return summary

    def _generate_summary(self, total_time: float) -> Dict:
        """Generate comprehensive summary."""
        total_tests = len(self.results)
        passed = len([r for r in self.results if r.status == "PASS"])
        failed_import = len([r for r in self.results if r.status == "FAIL_IMPORT"])
        failed_logic = len([r for r in self.results if r.status == "FAIL_LOGIC"])
        collection_errors = len(
            [r for r in self.results if r.status == "COLLECTION_ERROR"]
        )
        skipped = len([r for r in self.results if r.status == "SKIP"])

        return {
            "total_tests": total_tests,
            "passed": passed,
            "failed_import": failed_import,
            "failed_logic": failed_logic,
            "collection_errors": collection_errors,
            "skipped": skipped,
            "total_execution_time": total_time,
            "success_rate": (passed / total_tests * 100) if total_tests > 0 else 0,
            "detailed_results": [asdict(r) for r in self.results],
        }

    def print_comprehensive_summary(self, summary: Dict):
        """Print comprehensive validation summary."""
        print("\n" + "=" * 60)
        print("🎯 COMPLETE TEST SUITE VALIDATION RESULTS")
        print("=" * 60)

        print(f"📊 TOTAL TESTS: {summary['total_tests']}")
        print(f"   ✅ PASSED: {summary['passed']} ({summary['success_rate']:.1f}%)")
        print(f"   ❌ IMPORT ERRORS: {summary['failed_import']}")
        print(f"   ❌ LOGIC FAILURES: {summary['failed_logic']}")
        print(f"   ❌ COLLECTION ERRORS: {summary['collection_errors']}")
        print(f"   ⏭️ SKIPPED: {summary['skipped']}")
        print(f"⏱️ TOTAL TIME: {summary['total_execution_time']:.2f} seconds")

        # Show breakdown by category
        print("\n📋 CATEGORY BREAKDOWN:")
        category_stats = {}
        for result in self.results:
            category = self._get_category_from_path(result.file_path)
            if category not in category_stats:
                category_stats[category] = {"total": 0, "passed": 0}
            category_stats[category]["total"] += 1
            if result.status == "PASS":
                category_stats[category]["passed"] += 1

        for category, stats in category_stats.items():
            rate = stats["passed"] / stats["total"] * 100 if stats["total"] > 0 else 0
            print(f"   {category}: {stats['passed']}/{stats['total']} ({rate:.1f}%)")

    def _get_category_from_path(self, file_path: str) -> str:
        """Get category name from file path."""
        if "tests/unit/services" in file_path:
            return "core_services"
        elif "tests/cross_platform" in file_path:
            return "cross_platform"
        elif "launcher/tests" in file_path:
            return "launcher_tests"
        elif "src/desktop/modern/tests/unit/core" in file_path:
            return "modern_unit_core"
        elif "src/desktop/modern/tests/unit/interfaces" in file_path:
            return "modern_unit_interfaces"
        elif "tests/interface" in file_path:
            return "interface_tests"
        elif "tests/integration" in file_path:
            return "integration_tests"
        else:
            return "other"


def main():
    """Main validation function."""
    tka_root = Path()

    validator = CompleteTestValidator(tka_root)
    summary = validator.validate_all_tests()
    validator.print_comprehensive_summary(summary)

    # Save detailed results
    with open("complete_test_validation_results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n📄 Detailed results saved to: complete_test_validation_results.json")

    return summary


if __name__ == "__main__":
    main()
