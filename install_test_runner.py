#!/usr/bin/env python3
"""
TKA Test Runner Installation Script
==================================

This script installs the required dependencies for the TKA Test Runner
and validates the installation.

Usage:
    python install_test_runner.py
    python install_test_runner.py --validate-only
"""

import argparse
import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """Install required dependencies for the test runner."""
    print("📦 Installing TKA Test Runner dependencies...")

    try:
        # Install pytest-qt and pytest-xvfb
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "pytest-qt==4.4.0",
                "pytest-xvfb==3.0.0",
            ],
            check=True,
        )

        print("✅ Dependencies installed successfully")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def validate_installation():
    """Validate that all required components are available."""
    print("🔍 Validating TKA Test Runner installation...")

    validation_results = []

    # Check Python version
    if sys.version_info >= (3, 8):
        validation_results.append(
            (
                "Python version",
                True,
                f"{sys.version_info.major}.{sys.version_info.minor}",
            )
        )
    else:
        validation_results.append(("Python version", False, "Requires Python 3.8+"))

    # Check pytest
    try:
        import pytest

        validation_results.append(("pytest", True, pytest.__version__))
    except ImportError:
        validation_results.append(("pytest", False, "Not installed"))

    # Check pytest-qt (check if pytest recognizes qt options)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--help"],
            capture_output=True,
            text=True,
        )
        if "--no-qt-log" in result.stdout:
            validation_results.append(("pytest-qt", True, "Available"))
        else:
            validation_results.append(("pytest-qt", False, "Not detected"))
    except Exception:
        validation_results.append(("pytest-qt", False, "Check failed"))

    # Check PyQt6
    try:
        from PyQt6.QtWidgets import QApplication

        validation_results.append(("PyQt6", True, "Available"))
    except ImportError:
        validation_results.append(("PyQt6", False, "Not available (GUI disabled)"))

    # Check test runner files
    project_root = Path(__file__).parent
    test_runner_file = project_root / "tka_test_runner.py"
    gui_file = project_root / "tka_test_gui.py"

    validation_results.append(
        ("Test Runner", test_runner_file.exists(), str(test_runner_file))
    )
    validation_results.append(("GUI Interface", gui_file.exists(), str(gui_file)))

    # Check pytest configuration
    pytest_ini = project_root / "pytest.ini"
    validation_results.append(("pytest.ini", pytest_ini.exists(), str(pytest_ini)))

    # Print validation results
    print("\n📋 Validation Results:")
    print("=" * 60)

    all_passed = True
    for component, passed, details in validation_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{component:20} {status:10} {details}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("🎉 All validations passed! TKA Test Runner is ready to use.")
        print("\nQuick start:")
        print("  python tka_test_runner.py --discover    # Discover tests")
        print("  python tka_test_runner.py               # Run all tests")
        print("  python tka_test_runner.py --gui         # Launch GUI")
    else:
        print("⚠️  Some validations failed. Please address the issues above.")

    return all_passed


def create_quick_start_script():
    """Create a quick start script for easy access."""
    project_root = Path(__file__).parent

    # Create batch file for Windows
    batch_content = f"""@echo off
cd /d "{project_root}"
python tka_test_runner.py %*
"""

    batch_file = project_root / "run_tests.bat"
    try:
        batch_file.write_text(batch_content)
        print(f"✅ Created quick start script: {batch_file}")
    except Exception as e:
        print(f"⚠️  Could not create batch file: {e}")

    # Create shell script for Unix-like systems
    shell_content = f"""#!/bin/bash
cd "{project_root}"
python tka_test_runner.py "$@"
"""

    shell_file = project_root / "run_tests.sh"
    try:
        shell_file.write_text(shell_content)
        shell_file.chmod(0o755)  # Make executable
        print(f"✅ Created quick start script: {shell_file}")
    except Exception as e:
        print(f"⚠️  Could not create shell script: {e}")


def main():
    """Main installation script."""
    parser = argparse.ArgumentParser(description="Install TKA Test Runner")
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate installation, don't install",
    )

    args = parser.parse_args()

    print("🧪 TKA Test Runner Installation")
    print("=" * 50)

    if args.validate_only:
        success = validate_installation()
    else:
        # Install dependencies
        install_success = install_dependencies()

        if install_success:
            # Validate installation
            success = validate_installation()

            if success:
                # Create quick start scripts
                create_quick_start_script()
        else:
            success = False

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
