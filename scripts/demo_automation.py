#!/usr/bin/env python3
"""
Demo script to show automated testing in action.
"""

import time
import subprocess
from pathlib import Path


def create_test_file():
    """Create a test file to trigger the watcher."""
    test_file = Path("demo_test.py")
    test_content = '''
def test_demo():
    """Demo test that will trigger automation."""
    assert True

def test_failing_demo():
    """Demo test that will fail."""
    assert False, "This test is designed to fail for demo purposes"
'''

    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)

    print(f"📝 Created demo test file: {test_file}")
    return test_file


def run_demo():
    """Run a demo of the automated testing system."""
    print("🎭 TKA Automated Testing Demo")
    print("=" * 40)

    # Show current setup status
    print("\n1. Checking automation setup...")
    result = subprocess.run(
        ["python", "scripts/validate_test_automation.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        print("✅ Automation setup is complete!")
    else:
        print(
            "⚠️ Some setup steps are missing. Run: python scripts/setup_automated_testing.py"
        )

    # Run tests to show current status
    print("\n2. Running existing tests...")
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/regression/bugs/", "-v"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        print("✅ All regression tests are passing!")
    else:
        print("❌ Some tests are failing:")
        print(result.stdout[-200:])  # Show last 200 chars

    # Show automation features
    print("\n3. Available automation features:")
    print("   📁 File Watcher: python scripts/test_watcher.py")
    print("   🧪 Test Runner: python scripts/run_automated_tests.py")
    print("   🔔 Notifications: Configured in scripts/notification_config.json")
    print("   💚 Health Monitor: python scripts/health_monitor.py")
    print("   ⚙️ VS Code Tasks: Ctrl+Shift+P → 'Tasks: Run Task'")

    print("\n4. Quick test:")
    print("   Running a subset of tests to show the system...")
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/regression/bugs/test_placeholder.py", "-v"],
        capture_output=True,
        text=True,
        check=False,
    )
    print(f"   Result: {'✅ PASSED' if result.returncode == 0 else '❌ FAILED'}")

    print("\n🎯 Demo Complete!")
    print("Next steps:")
    print("1. Run: python scripts/test_watcher.py (in a separate terminal)")
    print("2. Edit any Python file and save it")
    print("3. Watch the automated tests run!")


if __name__ == "__main__":
    run_demo()
