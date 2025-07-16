#!/usr/bin/env python3
"""
TKA Test Runner Validation Script
================================

Comprehensive validation script to verify the test runner achieves 100% test execution capability.
This script validates all aspects of the enhanced test runner solution.

Usage:
    python validate_test_runner.py
"""

import subprocess
import sys
import time
from pathlib import Path


def run_command(cmd, timeout=60):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=Path(__file__).parent,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"


def validate_test_discovery():
    """Validate test discovery functionality."""
    print("🔍 Validating test discovery...")

    returncode, stdout, stderr = run_command("python tka_test_runner.py --discover")

    if returncode != 0:
        print(f"❌ Test discovery failed: {stderr}")
        return False

    # Check if tests were discovered
    if "Found" in stdout and "test files" in stdout:
        # Extract number of tests found
        lines = stdout.split("\n")
        for line in lines:
            if "Found" in line and "test files" in line:
                # More robust parsing
                words = line.split()
                for i, word in enumerate(words):
                    if word == "Found" and i + 1 < len(words):
                        try:
                            test_count = int(words[i + 1])
                            print(
                                f"✅ Test discovery successful: {test_count} tests found"
                            )
                            return test_count > 0
                        except ValueError:
                            continue

    print("❌ Test discovery output format unexpected")
    return False


def validate_unit_tests():
    """Validate unit test execution."""
    print("🧪 Validating unit test execution...")

    returncode, stdout, stderr = run_command("python tka_test_runner.py --unit --fast")

    if returncode != 0:
        print(f"⚠️  Unit tests completed with issues (expected for some tests)")

    # Check if tests were executed
    if "TEST RESULTS" in stdout:
        print("✅ Unit test execution successful")
        return True

    print("❌ Unit test execution failed")
    return False


def validate_error_handling():
    """Validate error handling and continue-on-error functionality."""
    print("🛡️ Validating error handling...")

    returncode, stdout, stderr = run_command(
        "python tka_test_runner.py --integration --continue-on-error", timeout=120
    )

    # For error handling validation, we expect some tests might fail but execution should continue
    if "TEST RESULTS" in stdout:
        print(
            "✅ Error handling validation successful (execution continued despite errors)"
        )
        return True

    print("❌ Error handling validation failed")
    return False


def validate_gui_availability():
    """Validate GUI interface availability."""
    print("🖥️ Validating GUI interface availability...")

    try:
        # Try to import the GUI module
        from tka_gui_enhanced import TKATestRunnerGUI

        print("✅ GUI interface available")
        return True
    except ImportError as e:
        print(f"❌ GUI interface not available: {e}")
        return False


def validate_comprehensive_execution():
    """Validate comprehensive test execution capability."""
    print("🚀 Validating comprehensive test execution...")

    # Test with a reasonable subset to avoid long execution times
    returncode, stdout, stderr = run_command(
        "python tka_test_runner.py --unit --continue-on-error", timeout=180
    )

    if "TEST RESULTS" in stdout:
        # Extract results
        lines = stdout.split("\n")
        total_tests = 0
        passed_tests = 0

        for line in lines:
            if "Total Tests:" in line:
                total_tests = int(line.split(":")[1].strip())
            elif "Passed:" in line:
                passed_tests = int(line.split(":")[1].strip())

        if total_tests > 0:
            success_rate = (passed_tests / total_tests) * 100
            print(
                f"✅ Comprehensive execution successful: {passed_tests}/{total_tests} tests ({success_rate:.1f}% success rate)"
            )
            return True

    print("❌ Comprehensive execution validation failed")
    return False


def main():
    """Main validation function."""
    print("🧪 TKA Test Runner Validation")
    print("=" * 50)

    validations = [
        ("Test Discovery", validate_test_discovery),
        ("Unit Test Execution", validate_unit_tests),
        ("Error Handling", validate_error_handling),
        ("GUI Availability", validate_gui_availability),
        ("Comprehensive Execution", validate_comprehensive_execution),
    ]

    results = []

    for name, validator in validations:
        print(f"\n📋 {name}")
        print("-" * 30)

        start_time = time.time()
        try:
            success = validator()
            execution_time = time.time() - start_time
            results.append((name, success, execution_time))

            if success:
                print(f"✅ {name} PASSED ({execution_time:.2f}s)")
            else:
                print(f"❌ {name} FAILED ({execution_time:.2f}s)")

        except Exception as e:
            execution_time = time.time() - start_time
            results.append((name, False, execution_time))
            print(f"❌ {name} ERROR: {str(e)} ({execution_time:.2f}s)")

    # Summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)

    passed_count = sum(1 for _, success, _ in results if success)
    total_count = len(results)
    total_time = sum(time for _, _, time in results)

    for name, success, exec_time in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name:25} {status:10} ({exec_time:.2f}s)")

    print("-" * 50)
    print(f"Overall Result: {passed_count}/{total_count} validations passed")
    print(f"Total Time: {total_time:.2f} seconds")

    if passed_count == total_count:
        print("\n🎉 ALL VALIDATIONS PASSED!")
        print("✅ TKA Test Runner is ready for 100% test execution!")
        print("\nQuick Start:")
        print("  python tka_test_runner.py --gui         # Launch GUI interface")
        print("  python tka_test_runner.py --discover    # Discover all tests")
        print("  python tka_test_runner.py               # Run all tests")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} validations failed.")
        print("Please review the failed validations above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
