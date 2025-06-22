#!/usr/bin/env python3
"""
Validate TKA test organization and automation setup.
"""

import subprocess
import sys
from pathlib import Path


def check_file_exists(file_path, description):
    """Check if a file exists and report result."""
    path = Path(file_path)
    exists = path.exists()
    status = "[PASS]" if exists else "[FAIL]"
    print(f"{status} {description}: {file_path}")
    return exists


def check_directory_exists(dir_path, description):
    """Check if a directory exists and report result."""
    path = Path(dir_path)
    exists = path.exists() and path.is_dir()
    status = "[PASS]" if exists else "[FAIL]"
    print(f"{status} {description}: {dir_path}")
    return exists


def check_command_available(command, description):
    """Check if a command is available."""
    try:
        result = subprocess.run(
            [command, "--version"], capture_output=True, text=True, check=False
        )
        available = result.returncode == 0
        status = "[PASS]" if available else "[FAIL]"
        print(f"{status} {description}: {command}")
        return available
    except FileNotFoundError:
        print(f"[FAIL] {description}: {command} (not found)")
        return False


def main():
    """Validate the automated testing setup."""
    print("Validating TKA Automated Testing Setup")
    print("=" * 50)

    checks_passed = 0
    total_checks = 0

    # Check core test directories
    test_dirs = [
        ("tests/regression/bugs", "Regression tests directory"),
        ("tests/specification", "Specification tests directory"),
        ("tests/unit", "Unit tests directory"),
        ("tests/integration", "Integration tests directory"),
    ]

    print("\nTest Directory Structure:")
    for dir_path, description in test_dirs:
        if check_directory_exists(dir_path, description):
            checks_passed += 1
        total_checks += 1
    # Check automation scripts
    automation_scripts = [
        ("scripts/test_watcher.py", "Test watcher script"),
        ("scripts/simple_test_runner.py", "Simple test runner"),
        ("scripts/notification_system.py", "Notification system"),
        ("scripts/health_monitor.py", "Health monitor"),
        ("scripts/setup_automated_testing.py", "Setup script"),
    ]

    print("\nAutomation Scripts:")
    for script_path, description in automation_scripts:
        if check_file_exists(script_path, description):
            checks_passed += 1
        total_checks += 1

    # Check configuration files
    config_files = [
        (".pre-commit-config.yaml", "Pre-commit configuration"),
        ("scripts/notification_config.json", "Notification configuration"),
        ("pytest.ini", "Pytest configuration"),
        (".github/workflows/automated-testing.yml", "GitHub Actions workflow"),
    ]

    print("\nConfiguration Files:")
    for config_path, description in config_files:
        if check_file_exists(config_path, description):
            checks_passed += 1
        total_checks += 1

    # Check Git hooks
    git_hooks = [
        ("scripts/git-hooks/post-merge", "Post-merge hook source"),
        (".git/hooks/post-merge", "Post-merge hook installed"),
    ]

    print("\nGit Hooks:")
    for hook_path, description in git_hooks:
        if check_file_exists(hook_path, description):
            checks_passed += 1
        total_checks += 1

    # Check command availability
    commands = [
        ("python", "Python interpreter"),
        ("pytest", "Pytest test runner"),
        ("pre-commit", "Pre-commit tool"),
    ]

    print("\nCommand Availability:")
    for command, description in commands:
        if check_command_available(command, description):
            checks_passed += 1
        total_checks += 1

    # Summary
    print("\n" + "=" * 50)
    print(f"Validation Results: {checks_passed}/{total_checks} checks passed")

    if checks_passed == total_checks:
        print("[PASS] All checks passed! Automated testing is ready to use.")
        print("\nNext Steps:")
        print("1. Run: python scripts/test_watcher.py")
        print("2. Edit some code and save to see automatic testing")
        print("3. Run: python scripts/simple_test_runner.py for comprehensive testing")
        return True
    else:
        missing_checks = total_checks - checks_passed
        print(f"[FAIL] {missing_checks} checks failed. Run setup script to fix:")
        print("   python scripts/setup_automated_testing.py")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
