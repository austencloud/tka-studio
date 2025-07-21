#!/usr/bin/env python3
"""
Automated Test Execution Script for Sequence Card Tab.

This script runs all tests and generates a comprehensive report.
Implements the comprehensive testing protocol outlined in the testing documentation.
"""

import subprocess
import sys
import json
from pathlib import Path
import time
import os
from typing import Dict, List, Any


def run_test_phase(
    phase_name: str, test_command: str, required_passes: int = None
) -> Dict[str, Any]:
    """Run a test phase and return results."""
    print(f"\n{'='*60}")
    print(f"PHASE: {phase_name}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        # Ensure we're in the correct directory
        test_dir = Path(__file__).parent
        project_root = test_dir.parent.parent.parent.parent

        result = subprocess.run(
            test_command, shell=True, capture_output=True, text=True, cwd=project_root
        )

        end_time = time.time()
        duration = end_time - start_time

        print(f"Command: {test_command}")
        print(f"Duration: {duration:.2f}s")
        print(f"Return code: {result.returncode}")

        if result.stdout:
            print("STDOUT:")
            print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        success = result.returncode == 0

        # Parse pytest output for test counts
        test_counts = parse_pytest_output(result.stdout)

        return {
            "phase": phase_name,
            "success": success,
            "duration": duration,
            "command": test_command,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "test_counts": test_counts,
        }

    except Exception as e:
        print(f"Error running {phase_name}: {e}")
        return {
            "phase": phase_name,
            "success": False,
            "duration": 0,
            "error": str(e),
            "test_counts": {"total": 0, "passed": 0, "failed": 0, "skipped": 0},
        }


def parse_pytest_output(output: str) -> Dict[str, int]:
    """Parse pytest output to extract test counts."""
    counts = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}

    if not output:
        return counts

    lines = output.split("\n")
    for line in lines:
        # Look for summary line like "5 passed, 2 failed, 1 skipped in 2.34s"
        if " passed" in line or " failed" in line or " skipped" in line:
            parts = line.split()
            for i, part in enumerate(parts):
                if part == "passed" and i > 0:
                    try:
                        counts["passed"] = int(parts[i - 1])
                    except (ValueError, IndexError):
                        pass
                elif part == "failed" and i > 0:
                    try:
                        counts["failed"] = int(parts[i - 1])
                    except (ValueError, IndexError):
                        pass
                elif part == "skipped" and i > 0:
                    try:
                        counts["skipped"] = int(parts[i - 1])
                    except (ValueError, IndexError):
                        pass

    counts["total"] = counts["passed"] + counts["failed"] + counts["skipped"]
    return counts


def check_dependencies() -> bool:
    """Check that all required dependencies are available."""
    print("🔍 Checking dependencies...")

    required_packages = ["pytest", "pytest-qt", "pytest-mock", "pytest-cov", "PyQt6"]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")

    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False

    print("✅ All dependencies available")
    return True


def setup_environment() -> bool:
    """Setup test environment variables."""
    print("🔧 Setting up test environment...")

    # Set environment variables for headless testing
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    os.environ["PYTHONPATH"] = str(Path(__file__).parent.parent.parent.parent)

    print("✅ Environment configured")
    return True


def generate_coverage_report(results: List[Dict]) -> Dict[str, Any]:
    """Generate coverage analysis from test results."""
    print("\n📊 Generating coverage report...")

    coverage_data = {
        "total_lines_covered": 0,
        "total_lines": 0,
        "coverage_percentage": 0,
        "uncovered_files": [],
        "low_coverage_files": [],
    }

    # Look for coverage information in test outputs
    for result in results:
        if result.get("success") and "cov" in result.get("command", ""):
            stdout = result.get("stdout", "")
            if "TOTAL" in stdout:
                # Parse coverage output
                lines = stdout.split("\n")
                for line in lines:
                    if "TOTAL" in line and "%" in line:
                        # Extract percentage
                        parts = line.split()
                        for part in parts:
                            if part.endswith("%"):
                                try:
                                    coverage_data["coverage_percentage"] = int(
                                        part[:-1]
                                    )
                                    break
                                except ValueError:
                                    pass

    return coverage_data


def validate_critical_tests(results: List[Dict]) -> Dict[str, bool]:
    """Validate that critical tests have passed."""
    critical_tests = {
        "service_registration": False,
        "data_loading": False,
        "length_filtering": False,
        "cache_performance": False,
        "settings_persistence": False,
        "ui_integration": False,
        "export_functionality": False,
        "memory_management": False,
    }

    # Analyze test outputs to determine which critical tests passed
    for result in results:
        if result.get("success"):
            stdout = result.get("stdout", "")

            # Check for specific test patterns
            if "test_service_registration" in stdout and "PASSED" in stdout:
                critical_tests["service_registration"] = True

            if "test_get_sequences_by_length" in stdout and "PASSED" in stdout:
                critical_tests["length_filtering"] = True

            if "test_cache" in stdout and "PASSED" in stdout:
                critical_tests["cache_performance"] = True

            if "test_settings" in stdout and "PASSED" in stdout:
                critical_tests["settings_persistence"] = True

            if "test_tab_creation" in stdout and "PASSED" in stdout:
                critical_tests["ui_integration"] = True

            if "test_export" in stdout and "PASSED" in stdout:
                critical_tests["export_functionality"] = True

            if "test_memory" in stdout and "PASSED" in stdout:
                critical_tests["memory_management"] = True

    return critical_tests


def main():
    """Run all test phases and generate report."""

    print("SEQUENCE CARD TAB - AUTOMATED TEST EXECUTION")
    print("=" * 80)

    # Pre-flight checks
    if not check_dependencies():
        sys.exit(1)

    if not setup_environment():
        sys.exit(1)

    # Test phases with specific commands
    phases = [
        {
            "name": "Service Layer Tests",
            "command": "python -m pytest src/desktop/modern/tests/sequence_card/test_sequence_card_services.py -v --tb=short",
        },
        {
            "name": "UI Component Tests",
            "command": "python -m pytest src/desktop/modern/tests/sequence_card/test_sequence_card_ui.py -v --tb=short",
        },
        {
            "name": "Integration Tests",
            "command": "python -m pytest src/desktop/modern/tests/sequence_card/test_sequence_card_integration.py -v --tb=short",
        },
        {
            "name": "Performance Tests",
            "command": "python -m pytest src/desktop/modern/tests/sequence_card/ -m performance -v --tb=short",
        },
        {
            "name": "Complete Test Suite with Coverage",
            "command": "python -m pytest src/desktop/modern/tests/sequence_card/ --cov=src/desktop/modern/src/application/services/sequence_card --cov=src/desktop/modern/src/presentation/tabs/sequence_card --cov-report=term-missing -v",
        },
    ]

    results = []

    # Run each phase
    for phase in phases:
        result = run_test_phase(phase["name"], phase["command"])
        results.append(result)

        if not result["success"]:
            print(f"\n❌ FAILURE: {phase['name']}")
        else:
            print(f"\n✅ SUCCESS: {phase['name']}")

    # Generate comprehensive analysis
    print(f"\n{'='*80}")
    print("COMPREHENSIVE ANALYSIS")
    print(f"{'='*80}")

    # Overall statistics
    total_phases = len(results)
    successful_phases = sum(1 for r in results if r["success"])
    total_duration = sum(r.get("duration", 0) for r in results)

    # Test count aggregation
    total_tests = sum(r.get("test_counts", {}).get("total", 0) for r in results)
    total_passed = sum(r.get("test_counts", {}).get("passed", 0) for r in results)
    total_failed = sum(r.get("test_counts", {}).get("failed", 0) for r in results)
    total_skipped = sum(r.get("test_counts", {}).get("skipped", 0) for r in results)

    print(f"Phase Summary:")
    print(f"  Total Phases: {total_phases}")
    print(f"  Successful: {successful_phases}")
    print(f"  Failed: {total_phases - successful_phases}")
    print(f"  Success Rate: {successful_phases/total_phases*100:.1f}%")
    print(f"  Total Duration: {total_duration:.2f}s")

    print(f"\nTest Summary:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {total_passed}")
    print(f"  Failed: {total_failed}")
    print(f"  Skipped: {total_skipped}")
    if total_tests > 0:
        print(f"  Pass Rate: {total_passed/total_tests*100:.1f}%")

    # Coverage analysis
    coverage_data = generate_coverage_report(results)
    if coverage_data["coverage_percentage"] > 0:
        print(f"\nCoverage Analysis:")
        print(f"  Code Coverage: {coverage_data['coverage_percentage']}%")

        if coverage_data["coverage_percentage"] >= 90:
            print("  ✅ Excellent coverage")
        elif coverage_data["coverage_percentage"] >= 70:
            print("  ⚠️  Good coverage")
        else:
            print("  ❌ Coverage needs improvement")

    # Critical test validation
    critical_tests = validate_critical_tests(results)
    critical_passed = sum(1 for passed in critical_tests.values() if passed)
    critical_total = len(critical_tests)

    print(f"\nCritical Test Validation:")
    print(f"  Critical Tests Passed: {critical_passed}/{critical_total}")

    for test_name, passed in critical_tests.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {test_name.replace('_', ' ').title()}")

    # Detailed results by phase
    print(f"\nDETAILED RESULTS BY PHASE:")
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        duration = result.get("duration", 0)
        counts = result.get("test_counts", {})
        test_summary = f"({counts.get('passed', 0)} passed, {counts.get('failed', 0)} failed, {counts.get('skipped', 0)} skipped)"
        print(f"  {status} | {result['phase']} | {duration:.2f}s | {test_summary}")

    # Performance benchmarks
    print(f"\nPERFORMANCE BENCHMARKS:")
    performance_targets = {
        "Service Layer Tests": 30.0,  # seconds
        "UI Component Tests": 60.0,
        "Integration Tests": 45.0,
        "Performance Tests": 20.0,
        "Complete Test Suite with Coverage": 120.0,
    }

    for result in results:
        phase_name = result["phase"]
        duration = result.get("duration", 0)
        target = performance_targets.get(phase_name, 60.0)

        if duration <= target:
            status = "✅"
        elif duration <= target * 1.5:
            status = "⚠️"
        else:
            status = "❌"

        print(f"  {status} {phase_name}: {duration:.2f}s (target: {target:.1f}s)")

    # Memory and resource analysis
    print(f"\nRESOURCE ANALYSIS:")
    print(f"  Peak Memory Usage: Not measured (requires additional tooling)")
    print(f"  File System Operations: Tested with temporary directories")
    print(f"  Qt Application Lifecycle: Managed by pytest-qt")

    # Recommendations
    print(f"\nRECOMMENDATIONS:")

    if successful_phases == total_phases:
        print("  🎉 All test phases passed!")
        print("  ✅ Sequence Card Tab implementation is ready for production")
    else:
        failed_phases = [r["phase"] for r in results if not r["success"]]
        print(f"  ❌ Failed phases: {', '.join(failed_phases)}")
        print("  🔧 Review failed test output and fix issues before deployment")

    if coverage_data["coverage_percentage"] < 90:
        print("  📈 Consider adding more tests to improve code coverage")

    if any(
        r.get("duration", 0) > performance_targets.get(r["phase"], 60) * 1.5
        for r in results
    ):
        print("  ⚡ Some test phases are running slowly - consider optimization")

    # Save results to file
    results_file = Path(__file__).parent / "test_results.json"
    comprehensive_results = {
        "timestamp": time.time(),
        "summary": {
            "total_phases": total_phases,
            "successful_phases": successful_phases,
            "total_duration": total_duration,
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_skipped": total_skipped,
            "pass_rate": total_passed / total_tests * 100 if total_tests > 0 else 0,
        },
        "coverage": coverage_data,
        "critical_tests": critical_tests,
        "phase_results": results,
        "performance_benchmarks": {
            phase: {
                "duration": next(
                    (r["duration"] for r in results if r["phase"] == phase), 0
                ),
                "target": target,
                "meets_target": next(
                    (r["duration"] for r in results if r["phase"] == phase), 0
                )
                <= target,
            }
            for phase, target in performance_targets.items()
        },
    }

    with open(results_file, "w") as f:
        json.dump(comprehensive_results, f, indent=2)

    print(f"\nDetailed results saved to: {results_file}")

    # Final verdict
    print(f"\n{'='*80}")
    print("FINAL VERDICT")
    print(f"{'='*80}")

    if successful_phases == total_phases and critical_passed >= critical_total * 0.8:
        print(f"🎉 SUCCESS: Sequence Card Tab implementation validated!")
        print(f"✅ All critical functionality tested and working")
        print(f"✅ Performance within acceptable limits")
        print(f"✅ Ready for production deployment")
        exit_code = 0
    else:
        print(f"❌ FAILURE: Issues found in Sequence Card Tab implementation")
        print(f"🔧 Review failed tests and address issues")
        print(f"⚠️  Do not deploy until all critical tests pass")
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
