#!/usr/bin/env python3
"""
TKA Comprehensive Test Runner - Enhanced Edition
===============================================

A bulletproof test execution system for the TKA PyQt6 project that:
- Discovers ALL tests across the entire codebase (100% coverage)
- Runs tests with robust error handling and recovery
- Provides both CLI and GUI interfaces
- Ensures 100% test execution even with individual test failures
- Optimized for PyQt6 applications with proper environment setup

Usage:
    python tka_test_runner.py                    # Run all tests (CLI)
    python tka_test_runner.py --gui              # Run with GUI interface
    python tka_test_runner.py --discover         # Just discover tests
    python tka_test_runner.py --fast             # Run only fast tests
    python tka_test_runner.py --parallel         # Run tests in parallel
    python tka_test_runner.py --continue-on-error # Continue even if tests fail

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
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class TestResult:
    """Enhanced container for test execution results."""

    success: bool
    total_tests: int
    passed: int
    failed: int
    skipped: int
    errors: int
    execution_time: float
    error_details: List[str] = field(default_factory=list)
    output: str = ""
    individual_results: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TestFile:
    """Enhanced container for discovered test file information."""

    path: Path
    relative_path: str
    category: str
    estimated_time: float
    priority: int
    size_bytes: int = 0
    last_modified: float = 0.0


class TKATestDiscovery:
    """
    Enhanced universal test discovery engine with 100% coverage guarantee.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.test_patterns = ["test_*.py", "*_test.py"]

        # Comprehensive search directories - ENHANCED for 100% coverage
        self.search_dirs = [
            "src/desktop/modern/tests",
            "src/desktop/legacy/tests",
            "launcher/tests",
            "tests",
            "src/web/shared/di/tests",
            ".",  # Root level
        ]

        # Additional patterns for comprehensive discovery
        self.additional_patterns = [
            "**/*test*.py",  # Catch any test files with different naming
            "**/test*.py",  # Recursive test files
        ]

        # Exclusion patterns to avoid virtual environments and dependencies
        self.exclusion_patterns = [
            ".venv",
            "venv",
            "node_modules",
            "__pycache__",
            ".git",
            ".pytest_cache",
            "build",
            "dist",
            ".tox",
            "htmlcov",
        ]

        # Enhanced categorization
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
            "other": [],
        }

    def discover_all_tests(
        self, progress_callback: Optional[Callable] = None
    ) -> List[TestFile]:
        """
        Discover ALL test files with progress reporting.
        Guarantees 100% coverage of the codebase.
        """
        discovered_tests = []
        total_dirs = len(self.search_dirs)

        for i, search_dir in enumerate(self.search_dirs):
            if progress_callback:
                progress_callback(f"Scanning {search_dir}...", i / total_dirs * 100)

            dir_path = self.project_root / search_dir
            if dir_path.exists():
                discovered_tests.extend(self._scan_directory_comprehensive(dir_path))

        # Remove duplicates and sort
        unique_tests = self._deduplicate_and_enhance(discovered_tests)

        if progress_callback:
            progress_callback(f"Found {len(unique_tests)} tests", 100)

        return sorted(unique_tests, key=lambda t: (t.priority, t.relative_path))

    def _scan_directory_comprehensive(self, directory: Path) -> List[TestFile]:
        """Comprehensive directory scanning with error recovery."""
        tests = []

        try:
            # Use multiple patterns and methods for maximum coverage
            for pattern in self.test_patterns:
                for test_file in directory.rglob(pattern):
                    if test_file.is_file() and self._is_valid_test_file(test_file):
                        tests.append(self._create_enhanced_test_file_info(test_file))
        except Exception as e:
            print(f"Warning: Error scanning {directory}: {e}")
            # Continue with other directories

        return tests

    def _is_valid_test_file(self, file_path: Path) -> bool:
        """Enhanced validation for test files."""
        if not file_path.suffix == ".py":
            return False

        # Skip problematic directories
        path_parts = file_path.parts
        skip_dirs = {
            ".venv",
            "venv",
            "node_modules",
            "__pycache__",
            ".git",
            ".pytest_cache",
        }
        if any(part in skip_dirs for part in path_parts):
            return False

        # Additional validation: check if file contains test functions
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            return (
                "def test_" in content
                or "class Test" in content
                or "import pytest" in content
                or "@pytest" in content
            )
        except:
            return True  # If we can't read it, assume it's valid

    def _create_enhanced_test_file_info(self, file_path: Path) -> TestFile:
        """Create enhanced TestFile object with comprehensive metadata."""
        relative_path = str(file_path.relative_to(self.project_root))
        category = self._categorize_test(relative_path)
        estimated_time = self._estimate_execution_time(file_path)
        priority = self._calculate_priority(category, file_path)

        # Additional metadata
        size_bytes = 0
        last_modified = 0.0
        try:
            stat = file_path.stat()
            size_bytes = stat.st_size
            last_modified = stat.st_mtime
        except:
            pass

        return TestFile(
            path=file_path,
            relative_path=relative_path,
            category=category,
            estimated_time=estimated_time,
            priority=priority,
            size_bytes=size_bytes,
            last_modified=last_modified,
        )

    def _categorize_test(self, relative_path: str) -> str:
        """Enhanced test categorization."""
        path_lower = relative_path.lower()

        for category, keywords in self.categories.items():
            if any(keyword in path_lower for keyword in keywords):
                return category

        return "other"

    def _estimate_execution_time(self, file_path: Path) -> float:
        """Enhanced time estimation based on file analysis."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            # Count test functions for better estimation
            test_count = content.count("def test_") + content.count("class Test")
            base_time = max(0.1, test_count * 0.2)

            # Adjust based on content
            if any(
                keyword in content.lower()
                for keyword in ["slow", "time.sleep", "integration"]
            ):
                base_time *= 3
            elif any(keyword in content.lower() for keyword in ["gui", "qt", "widget"]):
                base_time *= 2
            elif "mock" in content.lower() or "unit" in content.lower():
                base_time *= 0.5

            return min(base_time, 10.0)  # Cap at 10 seconds
        except:
            return 1.0

    def _calculate_priority(self, category: str, file_path: Path) -> int:
        """Enhanced priority calculation."""
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

        # Boost priority for critical or small files
        if "critical" in str(file_path).lower():
            base_priority -= 1
        try:
            if file_path.stat().st_size < 1000:  # Small files likely run faster
                base_priority -= 1
        except:
            pass

        return max(1, base_priority)

    def _deduplicate_and_enhance(self, tests: List[TestFile]) -> List[TestFile]:
        """Remove duplicates and enhance test information."""
        seen_paths = set()
        unique_tests = []

        for test in tests:
            if test.path not in seen_paths:
                seen_paths.add(test.path)
                unique_tests.append(test)

        return unique_tests


class TKATestExecutor:
    """
    Enhanced test executor with 100% execution guarantee and robust error handling.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.setup_environment()
        self.execution_stats = {
            "total_attempted": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "skipped_runs": 0,
        }

    def setup_environment(self):
        """Enhanced environment setup for reliable PyQt6 testing."""
        # Comprehensive Python path setup
        essential_paths = [
            str(self.project_root),
            str(self.project_root / "src"),
            str(self.project_root / "src" / "desktop" / "modern" / "src"),
            str(self.project_root / "src" / "desktop" / "modern"),
            str(self.project_root / "src" / "desktop" / "legacy" / "src"),
            str(self.project_root / "src" / "desktop" / "legacy"),
            str(self.project_root / "launcher"),
            str(self.project_root / "packages"),
            str(self.project_root / "data"),
        ]

        # Update PYTHONPATH
        existing_paths = os.environ.get("PYTHONPATH", "").split(os.pathsep)
        new_paths = [p for p in essential_paths if Path(p).exists()]
        all_paths = new_paths + [p for p in existing_paths if p and p not in new_paths]
        os.environ["PYTHONPATH"] = os.pathsep.join(all_paths)

        # Qt environment for headless testing
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        os.environ.setdefault("QT_LOGGING_RULES", "*.debug=false")

        # Pytest environment
        os.environ.setdefault("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "0")

    def run_all_tests(
        self,
        tests: List[TestFile],
        parallel: bool = False,
        fast_only: bool = False,
        continue_on_error: bool = True,
        progress_callback: Optional[Callable] = None,
    ) -> TestResult:
        """
        Execute all tests with 100% execution guarantee.

        Args:
            tests: List of test files to execute
            parallel: Whether to run tests in parallel
            fast_only: Whether to run only fast tests
            continue_on_error: Whether to continue when individual tests fail
            progress_callback: Callback for progress updates

        Returns:
            TestResult with comprehensive execution information
        """
        if fast_only:
            tests = [t for t in tests if t.estimated_time < 2.0]

        start_time = time.time()
        self.execution_stats["total_attempted"] = len(tests)

        if progress_callback:
            progress_callback("Starting test execution...", 0, "")

        try:
            if parallel and len(tests) > 1:
                result = self._run_parallel_tests(
                    tests, continue_on_error, progress_callback
                )
            else:
                result = self._run_sequential_tests(
                    tests, continue_on_error, progress_callback
                )

            result.execution_time = time.time() - start_time

            if progress_callback:
                progress_callback("Test execution completed", 100, "")

            return result

        except Exception as e:
            # Even if there's a catastrophic failure, return partial results
            error_result = TestResult(
                success=False,
                total_tests=len(tests),
                passed=self.execution_stats["successful_runs"],
                failed=self.execution_stats["failed_runs"],
                skipped=self.execution_stats["skipped_runs"],
                errors=1,
                execution_time=time.time() - start_time,
                error_details=[f"Executor error: {str(e)}"],
                output=traceback.format_exc(),
            )

            if progress_callback:
                progress_callback("Test execution failed", 100, str(e))

            return error_result

    def _run_sequential_tests(
        self,
        tests: List[TestFile],
        continue_on_error: bool,
        progress_callback: Optional[Callable] = None,
    ) -> TestResult:
        """Run tests sequentially with individual error handling."""
        all_results = []
        total_tests = len(tests)

        for i, test in enumerate(tests):
            if progress_callback:
                progress = int((i / total_tests) * 100)
                progress_callback(
                    f"Running {test.relative_path}", progress, test.relative_path
                )

            try:
                result = self._run_single_test(test)
                all_results.append(result)

                if result.success:
                    self.execution_stats["successful_runs"] += 1
                else:
                    self.execution_stats["failed_runs"] += 1

                # Continue even if this test failed (if continue_on_error is True)
                if not continue_on_error and not result.success:
                    break

            except Exception as e:
                # Individual test execution failed - record and continue
                error_result = TestResult(
                    success=False,
                    total_tests=1,
                    passed=0,
                    failed=1,
                    skipped=0,
                    errors=1,
                    execution_time=0.0,
                    error_details=[f"Test execution error: {str(e)}"],
                    output=traceback.format_exc(),
                )
                all_results.append(error_result)
                self.execution_stats["failed_runs"] += 1

                if not continue_on_error:
                    break

        return self._merge_results(all_results)

    def _run_single_test(self, test: TestFile) -> TestResult:
        """Run a single test file with comprehensive error handling."""
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(test.path),
            "--tb=short",
            "-v",
            "--disable-warnings",
            "--continue-on-collection-errors",
            "--maxfail=1000",  # Don't stop on first failure
        ]

        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=max(30, test.estimated_time * 10),  # Generous timeout
            )

            return self._parse_pytest_output(result, test.relative_path)

        except subprocess.TimeoutExpired:
            return TestResult(
                success=False,
                total_tests=1,
                passed=0,
                failed=1,
                skipped=0,
                errors=1,
                execution_time=test.estimated_time * 10,
                error_details=[
                    f"Test timed out after {test.estimated_time * 10} seconds"
                ],
                output="Timeout",
            )
        except Exception as e:
            return TestResult(
                success=False,
                total_tests=1,
                passed=0,
                failed=1,
                skipped=0,
                errors=1,
                execution_time=0.0,
                error_details=[f"Execution error: {str(e)}"],
                output=traceback.format_exc(),
            )

    def _parse_pytest_output(
        self, result: subprocess.CompletedProcess, test_name: str
    ) -> TestResult:
        """Enhanced pytest output parsing."""
        output = result.stdout + result.stderr

        # Enhanced parsing with multiple patterns
        passed = len([line for line in output.split("\n") if " PASSED" in line])
        failed = len([line for line in output.split("\n") if " FAILED" in line])
        errors = len([line for line in output.split("\n") if " ERROR" in line])
        skipped = len([line for line in output.split("\n") if " SKIPPED" in line])

        total = passed + failed + errors + skipped

        # If no tests were detected, assume collection issues
        if total == 0 and result.returncode != 0:
            failed = 1
            total = 1

        # Extract detailed errors
        error_details = []
        if result.returncode != 0:
            lines = output.split("\n")
            for i, line in enumerate(lines):
                if "FAILED" in line or "ERROR" in line:
                    error_details.append(line.strip())
                    # Add context lines
                    for j in range(1, 4):
                        if i + j < len(lines) and lines[i + j].strip():
                            error_details.append(f"  {lines[i + j].strip()}")

        return TestResult(
            success=result.returncode == 0,
            total_tests=max(total, 1),
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            execution_time=0.0,  # Will be set by caller
            error_details=error_details[:10],  # Limit error details
            output=output,
            individual_results=[
                {
                    "test_name": test_name,
                    "success": result.returncode == 0,
                    "output": output[:1000],  # Truncate long output
                }
            ],
        )

    def _run_parallel_tests(
        self,
        tests: List[TestFile],
        continue_on_error: bool,
        progress_callback: Optional[Callable] = None,
    ) -> TestResult:
        """Run tests in parallel with error isolation."""
        # Group tests to avoid conflicts
        test_groups = self._group_tests_safely(tests)
        all_results = []
        completed = 0
        total_groups = len(test_groups)

        with ThreadPoolExecutor(max_workers=min(4, total_groups)) as executor:
            futures = {
                executor.submit(self._run_test_group, group, continue_on_error): group
                for group in test_groups
            }

            for future in as_completed(futures):
                try:
                    result = future.result()
                    all_results.append(result)
                except Exception as e:
                    # Handle group execution failure
                    group = futures[future]
                    error_result = TestResult(
                        success=False,
                        total_tests=len(group),
                        passed=0,
                        failed=len(group),
                        skipped=0,
                        errors=1,
                        execution_time=0.0,
                        error_details=[f"Group execution error: {str(e)}"],
                        output=traceback.format_exc(),
                    )
                    all_results.append(error_result)

                completed += 1
                if progress_callback:
                    progress = int((completed / total_groups) * 100)
                    progress_callback(
                        f"Completed {completed}/{total_groups} groups", progress, ""
                    )

        return self._merge_results(all_results)

    def _group_tests_safely(self, tests: List[TestFile]) -> List[List[TestFile]]:
        """Group tests to prevent conflicts in parallel execution."""
        # Group by category and estimated time to balance load
        groups = {}
        for test in tests:
            # Create groups that won't conflict
            group_key = f"{test.category}_{int(test.estimated_time)}"
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(test)

        # Split large groups
        final_groups = []
        for group in groups.values():
            if len(group) > 5:  # Split large groups
                for i in range(0, len(group), 5):
                    final_groups.append(group[i : i + 5])
            else:
                final_groups.append(group)

        return final_groups

    def _run_test_group(
        self, test_group: List[TestFile], continue_on_error: bool
    ) -> TestResult:
        """Run a group of tests with error isolation."""
        return self._run_sequential_tests(test_group, continue_on_error, None)

    def _merge_results(self, results: List[TestResult]) -> TestResult:
        """Merge multiple test results into comprehensive summary."""
        if not results:
            return TestResult(
                success=False,
                total_tests=0,
                passed=0,
                failed=0,
                skipped=0,
                errors=1,
                execution_time=0.0,
                error_details=["No test results to merge"],
                output="",
            )

        total_tests = sum(r.total_tests for r in results)
        passed = sum(r.passed for r in results)
        failed = sum(r.failed for r in results)
        skipped = sum(r.skipped for r in results)
        errors = sum(r.errors for r in results)

        all_error_details = []
        all_individual_results = []

        for r in results:
            all_error_details.extend(r.error_details)
            all_individual_results.extend(r.individual_results)

        combined_output = "\n".join(r.output for r in results if r.output)

        return TestResult(
            success=all(r.success for r in results) and failed == 0,
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            execution_time=0.0,  # Will be set by caller
            error_details=all_error_details,
            output=combined_output,
            individual_results=all_individual_results,
        )


def main():
    """Main entry point for the TKA Test Runner."""
    parser = argparse.ArgumentParser(
        description="TKA Comprehensive Test Runner - Enhanced Edition",
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
        "--continue-on-error",
        action="store_true",
        default=True,
        help="Continue execution even if individual tests fail",
    )
    parser.add_argument(
        "--output", choices=["json", "text"], default="text", help="Output format"
    )

    args = parser.parse_args()

    # Get project root
    project_root = Path(__file__).parent.absolute()

    # Initialize discovery engine
    discovery = TKATestDiscovery(project_root)

    try:
        print("🔍 Discovering tests across TKA codebase...")
    except UnicodeEncodeError:
        print("Discovering tests across TKA codebase...")

    tests = discovery.discover_all_tests()

    # Filter tests based on arguments
    if args.unit:
        tests = [t for t in tests if t.category == "unit"]
    elif args.integration:
        tests = [t for t in tests if t.category == "integration"]

    try:
        print(f"📋 Found {len(tests)} test files")
    except UnicodeEncodeError:
        print(f"Found {len(tests)} test files")

    if args.discover:
        # Just show discovered tests
        for test in tests:
            print(f"  {test.category:12} {test.relative_path}")
        return 0

    if args.gui:
        # Launch GUI interface
        try:
            from tka_gui_enhanced import main as gui_main

            return gui_main()
        except ImportError as e:
            print(f"❌ GUI interface not available: {e}")
            print("   Make sure PyQt6 is installed: pip install PyQt6")
            return 1

    # Run tests
    try:
        print("🚀 Running tests...")
    except UnicodeEncodeError:
        print("Running tests...")
    executor = TKATestExecutor(project_root)
    result = executor.run_all_tests(
        tests,
        parallel=args.parallel,
        fast_only=args.fast,
        continue_on_error=args.continue_on_error,
    )

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
                    "errors": result.errors,
                    "execution_time": result.execution_time,
                    "error_details": result.error_details,
                },
                indent=2,
            )
        )
    else:
        print("\n" + "=" * 60)
        try:
            print("📊 TEST RESULTS")
        except UnicodeEncodeError:
            print("TEST RESULTS")
        print("=" * 60)
        print(f"Total Tests: {result.total_tests}")
        print(f"Passed:      {result.passed}")
        print(f"Failed:      {result.failed}")
        print(f"Skipped:     {result.skipped}")
        print(f"Errors:      {result.errors}")
        try:
            print(f"Success:     {'✅ YES' if result.success else '❌ NO'}")
        except UnicodeEncodeError:
            print(f"Success:     {'YES' if result.success else 'NO'}")
        print(f"Time:        {result.execution_time:.2f} seconds")

        if result.error_details:
            try:
                print(f"\n❌ Error Details ({len(result.error_details)}):")
                for error in result.error_details[:10]:  # Show first 10 errors
                    print(f"  • {error}")
            except UnicodeEncodeError:
                print(f"\nError Details ({len(result.error_details)}):")
                for error in result.error_details[:10]:  # Show first 10 errors
                    print(f"  - {error}")
            if len(result.error_details) > 10:
                print(f"  ... and {len(result.error_details) - 10} more")

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
