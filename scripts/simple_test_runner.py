#!/usr/bin/env python3
"""
Simple automated testing script for TKA.
"""

import subprocess
import sys
from pathlib import Path


def run_test_category(name, command):
    """Run a test category and report results."""
    print(f"\n=== Running {name} ===")
    print(f"Command: {' '.join(command)}")

    try:
        result = subprocess.run(command, check=False, cwd=Path.cwd())

        if result.returncode == 0:
            print(f"PASSED: {name}")
            return True
        else:
            print(f"FAILED: {name}")
            return False

    except Exception as e:
        print(f"ERROR running {name}: {e}")
        return False


def main():
    """Run automated tests."""
    print("TKA Automated Testing")
    print("=" * 40)

    # Define test categories
    test_categories = [
        (
            "Regression Tests",
            ["python", "-m", "pytest", "tests/regression/bugs/", "-v"],
        ),
        (
            "Specification Tests",
            ["python", "-m", "pytest", "tests/specification/", "-v"],
        ),
        ("Unit Tests", ["python", "-m", "pytest", "tests/unit/", "-v"]),
    ]

    results = []

    # Run each category
    for name, command in test_categories:
        passed = run_test_category(name, command)
        results.append((name, passed))

    # Report overall results
    print("\n" + "=" * 40)
    print("FINAL RESULTS:")

    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\nALL TESTS PASSED!")
        return True
    else:
        print("\nSOME TESTS FAILED!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
