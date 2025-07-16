#!/usr/bin/env python3
"""
TKA Comprehensive Test Runner
============================

A bulletproof test execution system for the TKA PyQt6 project that:
- Discovers ALL tests across the entire codebase
- Runs tests with a single command
- Provides both CLI and optional GUI interfaces
- Optimized for <5 second execution
- Works reliably with PyQt6 applications

Usage:
    python tka_test_runner.py                    # Run all tests (CLI)
    python tka_test_runner.py --gui              # Run with GUI interface
    python tka_test_runner.py --discover         # Just discover tests
    python tka_test_runner.py --fast             # Run only fast tests
    python tka_test_runner.py --unit             # Run only unit tests
    python tka_test_runner.py --integration      # Run only integration tests
    python tka_test_runner.py --parallel         # Run tests in parallel
    python tka_test_runner.py --help             # Show help

Research Citations:
- pytest-qt documentation: https://pytest-qt.readthedocs.io/
- PyQt6 testing best practices: https://doc.qt.io/qt-6/qttest-index.html
- pytest configuration: https://docs.pytest.org/en/stable/reference/customize.html
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class TestResult:
    """Container for test execution results."""

    success: bool
    total_tests: int
    passed: int
    failed: int
    skipped: int
    execution_time: float
    errors: List[str]
    output: str


@dataclass
class TestFile:
    """Container for discovered test file information."""

    path: Path
    relative_path: str
    category: str
    estimated_time: float
    priority: int


class TKATestDiscovery:
    """
    Universal test discovery engine that finds ALL tests across the codebase.

    Based on research of pytest best practices and TKA project structure.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.test_patterns = ["test_*.py", "*_test.py"]

        # Define search directories based on project structure analysis
        self.search_dirs = [
            "src/desktop/modern/tests",
            "src/desktop/legacy/tests",
            "launcher/tests",
            "tests",
            "src/web/shared/di/tests",  # TypeScript tests converted to Python
            ".",  # Root level test files
        ]

        # Test categorization for better organization
        self.categories = {
            "unit": ["unit", "test_unit"],
            "integration": ["integration", "test_integration"],
            "specification": ["specification", "test_specification"],
            "end_to_end": ["end_to_end", "e2e", "test_e2e"],
            "regression": ["regression", "test_regression"],
            "framework": ["framework", "test_framework"],
            "gui": ["gui", "ui", "test_gui", "test_ui"],
            "services": ["services", "test_services"],
            "components": ["components", "test_components"],
            "positioning": ["positioning", "test_positioning"],
            "other": [],  # Default category
        }

    def discover_all_tests(self) -> List[TestFile]:
        """
        Discover ALL test files across the entire codebase.

        Returns comprehensive list of test files with metadata.
        """
        discovered_tests = []

        for search_dir in self.search_dirs:
            dir_path = self.project_root / search_dir
            if dir_path.exists():
                discovered_tests.extend(self._scan_directory(dir_path))

        # Remove duplicates and sort by priority
        unique_tests = self._deduplicate_tests(discovered_tests)
        return sorted(unique_tests, key=lambda t: (t.priority, t.relative_path))

    def _scan_directory(self, directory: Path) -> List[TestFile]:
        """Recursively scan directory for test files."""
        tests = []

        try:
            for pattern in self.test_patterns:
                for test_file in directory.rglob(pattern):
                    if test_file.is_file() and self._is_valid_test_file(test_file):
                        tests.append(self._create_test_file_info(test_file))
        except (OSError, PermissionError) as e:
            print(f"Warning: Could not scan {directory}: {e}")

        return tests

    def _is_valid_test_file(self, file_path: Path) -> bool:
        """Check if file is a valid Python test file."""
        if not file_path.suffix == ".py":
            return False

        # Skip files in virtual environments or node_modules
        path_parts = file_path.parts
        skip_dirs = {".venv", "venv", "node_modules", "__pycache__", ".git"}
        if any(part in skip_dirs for part in path_parts):
            return False

        return True

    def _create_test_file_info(self, file_path: Path) -> TestFile:
        """Create TestFile object with metadata."""
        relative_path = str(file_path.relative_to(self.project_root))
        category = self._categorize_test(relative_path)
        estimated_time = self._estimate_execution_time(file_path)
        priority = self._calculate_priority(category, file_path)

        return TestFile(
            path=file_path,
            relative_path=relative_path,
            category=category,
            estimated_time=estimated_time,
            priority=priority,
        )

    def _categorize_test(self, relative_path: str) -> str:
        """Categorize test based on path and filename."""
        path_lower = relative_path.lower()

        for category, keywords in self.categories.items():
            if any(keyword in path_lower for keyword in keywords):
                return category

        return "other"

    def _estimate_execution_time(self, file_path: Path) -> float:
        """Estimate test execution time based on file analysis."""
        try:
            content = file_path.read_text(encoding="utf-8")

            # Simple heuristics for time estimation
            if "slow" in content.lower() or "time.sleep" in content:
                return 5.0
            elif "integration" in content.lower() or "e2e" in content.lower():
                return 2.0
            elif "gui" in content.lower() or "qt" in content.lower():
                return 1.5
            else:
                return 0.5
        except (OSError, UnicodeDecodeError):
            return 1.0  # Default estimate

    def _calculate_priority(self, category: str, file_path: Path) -> int:
        """Calculate test priority (lower number = higher priority)."""
        priority_map = {
            "unit": 1,
            "integration": 2,
            "services": 3,
            "components": 4,
            "gui": 5,
            "regression": 6,
            "specification": 7,
            "end_to_end": 8,
            "framework": 9,
            "other": 10,
        }

        base_priority = priority_map.get(category, 10)

        # Boost priority for critical files
        if "critical" in str(file_path).lower():
            base_priority -= 1

        return max(1, base_priority)

    def _deduplicate_tests(self, tests: List[TestFile]) -> List[TestFile]:
        """Remove duplicate test files based on path."""
        seen_paths = set()
        unique_tests = []

        for test in tests:
            if test.path not in seen_paths:
                seen_paths.add(test.path)
                unique_tests.append(test)

        return unique_tests


class TKATestExecutor:
    """
    High-performance test executor optimized for PyQt6 applications.

    Implements best practices from pytest-qt documentation and PyQt6 testing guides.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.setup_environment()

    def setup_environment(self):
        """Setup environment for reliable PyQt6 testing."""
        # Set up Python path for TKA project
        essential_paths = [
            str(self.project_root),
            str(self.project_root / "src"),
            str(self.project_root / "src" / "desktop" / "modern" / "src"),
            str(self.project_root / "src" / "desktop" / "modern"),
            str(self.project_root / "src" / "desktop" / "legacy" / "src"),
            str(self.project_root / "src" / "desktop" / "legacy"),
            str(self.project_root / "launcher"),
            str(self.project_root / "packages"),
        ]

        # Update PYTHONPATH
        current_path = os.environ.get("PYTHONPATH", "")
        new_paths = [p for p in essential_paths if Path(p).exists()]

        if current_path:
            os.environ["PYTHONPATH"] = os.pathsep.join(new_paths + [current_path])
        else:
            os.environ["PYTHONPATH"] = os.pathsep.join(new_paths)

        # Set Qt platform for headless testing (research-based)
        if not os.environ.get("QT_QPA_PLATFORM"):
            os.environ["QT_QPA_PLATFORM"] = "offscreen"

    def run_all_tests(
        self, tests: List[TestFile], parallel: bool = False, fast_only: bool = False
    ) -> TestResult:
        """
        Execute all discovered tests with optimizations.

        Args:
            tests: List of test files to execute
            parallel: Whether to run tests in parallel
            fast_only: Whether to run only fast tests (<2 seconds)

        Returns:
            TestResult with comprehensive execution information
        """
        if fast_only:
            tests = [t for t in tests if t.estimated_time < 2.0]

        start_time = time.time()

        if parallel and len(tests) > 1:
            result = self._run_parallel_tests(tests)
        else:
            result = self._run_sequential_tests(tests)

        result.execution_time = time.time() - start_time
        return result

    def _run_sequential_tests(self, tests: List[TestFile]) -> TestResult:
        """Run tests sequentially using pytest."""
        test_paths = [str(test.path) for test in tests]

        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "--tb=short",
            "-v",
            "--disable-warnings",
            "--continue-on-collection-errors",
        ] + test_paths

        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            return self._parse_pytest_output(result)

        except subprocess.TimeoutExpired:
            return TestResult(
                success=False,
                total_tests=len(tests),
                passed=0,
                failed=len(tests),
                skipped=0,
                execution_time=300.0,
                errors=["Test execution timed out after 5 minutes"],
                output="Timeout",
            )
        except Exception as e:
            return TestResult(
                success=False,
                total_tests=len(tests),
                passed=0,
                failed=len(tests),
                skipped=0,
                execution_time=0.0,
                errors=[f"Execution error: {str(e)}"],
                output="",
            )

    def _run_parallel_tests(self, tests: List[TestFile]) -> TestResult:
        """Run tests in parallel for faster execution."""
        # Group tests by category to avoid conflicts
        test_groups = self._group_tests_for_parallel(tests)

        all_results = []
        with ThreadPoolExecutor(max_workers=min(4, len(test_groups))) as executor:
            futures = {
                executor.submit(self._run_test_group, group): group
                for group in test_groups
            }

            for future in as_completed(futures):
                try:
                    result = future.result()
                    all_results.append(result)
                except Exception as e:
                    # Handle individual group failures
                    group = futures[future]
                    all_results.append(
                        TestResult(
                            success=False,
                            total_tests=len(group),
                            passed=0,
                            failed=len(group),
                            skipped=0,
                            execution_time=0.0,
                            errors=[f"Group execution error: {str(e)}"],
                            output="",
                        )
                    )

        return self._merge_results(all_results)

    def _group_tests_for_parallel(self, tests: List[TestFile]) -> List[List[TestFile]]:
        """Group tests to avoid conflicts in parallel execution."""
        # Group by category to prevent Qt application conflicts
        groups = {}
        for test in tests:
            category = test.category
            if category not in groups:
                groups[category] = []
            groups[category].append(test)

        return list(groups.values())

    def _run_test_group(self, test_group: List[TestFile]) -> TestResult:
        """Run a group of tests sequentially."""
        return self._run_sequential_tests(test_group)

    def _parse_pytest_output(self, result: subprocess.CompletedProcess) -> TestResult:
        """Parse pytest output to extract test results."""
        output = result.stdout + result.stderr

        # Simple parsing - could be enhanced with pytest JSON output
        passed = output.count(" PASSED")
        failed = output.count(" FAILED") + output.count(" ERROR")
        skipped = output.count(" SKIPPED")
        total = passed + failed + skipped

        # Extract errors from output
        errors = []
        if result.returncode != 0:
            error_lines = [
                line
                for line in output.split("\n")
                if "ERROR" in line or "FAILED" in line
            ]
            errors = error_lines[:10]  # Limit to first 10 errors

        return TestResult(
            success=result.returncode == 0,
            total_tests=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            execution_time=0.0,  # Will be set by caller
            errors=errors,
            output=output,
        )

    def _merge_results(self, results: List[TestResult]) -> TestResult:
        """Merge multiple test results into one."""
        total_tests = sum(r.total_tests for r in results)
        passed = sum(r.passed for r in results)
        failed = sum(r.failed for r in results)
        skipped = sum(r.skipped for r in results)

        all_errors = []
        for r in results:
            all_errors.extend(r.errors)

        combined_output = "\n".join(r.output for r in results if r.output)

        return TestResult(
            success=all(r.success for r in results),
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            skipped=skipped,
            execution_time=0.0,  # Will be set by caller
            errors=all_errors,
            output=combined_output,
        )


def main():
    """Main entry point for the TKA Test Runner."""
    parser = argparse.ArgumentParser(
        description="TKA Comprehensive Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument("--gui", action="store_true", help="Launch GUI interface")
    parser.add_argument(
        "--discover", action="store_true", help="Just discover tests, don't run them"
    )
    parser.add_argument(
        "--fast", action="store_true", help="Run only fast tests (<2 seconds)"
    )
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument(
        "--integration", action="store_true", help="Run only integration tests"
    )
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument(
        "--output", choices=["json", "text"], default="text", help="Output format"
    )

    args = parser.parse_args()

    # Get project root
    project_root = Path(__file__).parent.absolute()

    # Initialize discovery engine
    discovery = TKATestDiscovery(project_root)

    print("🔍 Discovering tests across TKA codebase...")
    tests = discovery.discover_all_tests()

    # Filter tests based on arguments
    if args.unit:
        tests = [t for t in tests if t.category == "unit"]
    elif args.integration:
        tests = [t for t in tests if t.category == "integration"]

    print(f"📋 Found {len(tests)} test files")

    if args.discover:
        # Just show discovered tests
        for test in tests:
            print(f"  {test.category:12} {test.relative_path}")
        return 0

    if args.gui:
        # Launch GUI interface
        try:
            from tka_test_gui import main as gui_main

            return gui_main()
        except ImportError as e:
            print(f"❌ GUI interface not available: {e}")
            print("   Make sure PyQt6 is installed: pip install PyQt6")
            return 1

    # Run tests
    print("🚀 Running tests...")
    executor = TKATestExecutor(project_root)
    result = executor.run_all_tests(tests, parallel=args.parallel, fast_only=args.fast)

    # Output results
    if args.output == "json":
        print(
            json.dumps(
                {
                    "success": result.success,
                    "total_tests": result.total_tests,
                    "passed": result.passed,
                    "failed": result.failed,
                    "skipped": result.skipped,
                    "execution_time": result.execution_time,
                    "errors": result.errors,
                },
                indent=2,
            )
        )
    else:
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS")
        print("=" * 60)
        print(f"Total Tests: {result.total_tests}")
        print(f"Passed:      {result.passed}")
        print(f"Failed:      {result.failed}")
        print(f"Skipped:     {result.skipped}")
        print(f"Success:     {'✅ YES' if result.success else '❌ NO'}")
        print(f"Time:        {result.execution_time:.2f} seconds")

        if result.errors:
            print(f"\n❌ Errors ({len(result.errors)}):")
            for error in result.errors[:5]:  # Show first 5 errors
                print(f"  • {error}")
            if len(result.errors) > 5:
                print(f"  ... and {len(result.errors) - 5} more")

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
