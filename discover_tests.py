#!/usr/bin/env python3
"""
Test Discovery Script - See how many tests pytest finds
"""

import subprocess
import sys
from pathlib import Path


def discover_tests():
    """Discover all tests without running them."""
    print("🔍 Discovering all tests in TKA project...")

    # Use pytest's collect-only option to see what tests would be run
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--collect-only",
        "-q",  # Quiet mode to reduce output
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, cwd="F:/CODE/TKA"
        )

        if result.returncode == 0:
            output = result.stdout
            lines = output.strip().split("\n")

            # Count tests
            test_count = 0
            for line in lines:
                if (
                    "::test_" in line
                    or line.strip().endswith(" PASSED")
                    or line.strip().endswith(" FAILED")
                ):
                    test_count += 1

            # Look for summary line
            summary_line = [
                line for line in lines if "collected" in line and "item" in line
            ]

            print("📊 Test Discovery Results:")
            print("=" * 50)

            if summary_line:
                print(summary_line[0])
            else:
                print(f"Estimated tests found: {test_count}")

            # Show breakdown by directory
            print("\n📁 Test Files Found:")
            test_files = [line for line in lines if line.startswith("<Module")]
            for file_line in test_files[:20]:  # Show first 20
                print(f"  {file_line}")

            if len(test_files) > 20:
                print(f"  ... and {len(test_files) - 20} more test files")

            return True

        else:
            print("❌ Test discovery failed:")
            print("STDERR:", result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("⏰ Test discovery timed out")
        return False
    except Exception as e:
        print(f"💥 Error during test discovery: {e}")
        return False


def quick_test_run():
    """Run a quick subset of tests to verify setup."""
    print("\n🏃‍♂️ Running quick test subset...")

    cmd = [sys.executable, "-m", "pytest", "test_basic_setup.py", "-v", "--tb=short"]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, cwd="F:/CODE/TKA"
        )

        if result.returncode == 0:
            print("✅ Quick tests passed!")
            return True
        else:
            print("❌ Quick tests failed:")
            print(result.stdout[-500:])
            return False

    except Exception as e:
        print(f"💥 Error running quick tests: {e}")
        return False


if __name__ == "__main__":
    print("TKA Test Discovery & Quick Run")
    print("=" * 50)

    # Step 1: Discover tests
    discovery_ok = discover_tests()

    # Step 2: Quick test run
    if discovery_ok:
        quick_ok = quick_test_run()

        if quick_ok:
            print(f"\n🎉 Ready to run all tests!")
            print("Commands you can now use:")
            print("  pytest                    # Run all tests")
            print("  pytest -k modern         # Run only modern tests")
            print("  pytest -k 'not legacy'   # Skip legacy tests")
            print("  pytest --maxfail=5       # Stop after 5 failures")
            print("  pytest -m unit           # Run only unit tests")
        else:
            print(f"\n⚠️  Basic setup has issues - fix before running all tests")
    else:
        print(f"\n❌ Test discovery failed - check configuration")
