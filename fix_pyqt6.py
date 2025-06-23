#!/usr/bin/env python3
"""
PyQt6 Installation Diagnostic and Fix Tool
==========================================

This script diagnoses and fixes PyQt6 installation issues.
"""

import sys
import subprocess
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n--- {description} ---")
    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            print("✅ SUCCESS")
            if result.stdout.strip():
                print(result.stdout)
            return True
        else:
            print("❌ FAILED")
            if result.stderr.strip():
                print("Error:", result.stderr)
            if result.stdout.strip():
                print("Output:", result.stdout)
            return False

    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 ERROR: {e}")
        return False


def diagnose_pyqt6():
    """Diagnose current PyQt6 state."""
    print("🔍 DIAGNOSING PYQT6 INSTALLATION")
    print("=" * 50)

    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")

    # Check if PyQt6 is installed
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import PyQt6; print(f'PyQt6 version: {PyQt6.QtCore.qVersion()}'); print(f'Location: {PyQt6.__file__}')",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            print("✅ PyQt6 is installed:")
            print(result.stdout)
        else:
            print("❌ PyQt6 import failed:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Cannot check PyQt6: {e}")

    # Check pip list for Qt packages
    print(f"\n📦 Checking installed Qt packages...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list"], capture_output=True, text=True
    )
    if result.returncode == 0:
        qt_packages = [
            line
            for line in result.stdout.split("\n")
            if any(qt in line.lower() for qt in ["pyqt", "pyside", "qt"])
        ]
        if qt_packages:
            print("Qt-related packages found:")
            for pkg in qt_packages:
                print(f"  {pkg}")
        else:
            print("No Qt packages found")

    # Check for conflicting installations
    print(f"\n⚠️  Checking for conflicts...")
    conflicts = []

    try:
        import PyQt6

        conflicts.append("PyQt6")
    except:
        pass

    try:
        import PySide6

        conflicts.append("PySide6")
    except:
        pass

    try:
        import PyQt5

        conflicts.append("PyQt5")
    except:
        pass

    if len(conflicts) > 1:
        print(f"⚠️  Multiple Qt frameworks detected: {conflicts}")
        print("This can cause DLL conflicts!")
    else:
        print(f"Qt frameworks: {conflicts}")


def fix_pyqt6():
    """Fix PyQt6 installation."""
    print("\n🔧 FIXING PYQT6 INSTALLATION")
    print("=" * 50)

    # Step 1: Uninstall all Qt packages
    print("Step 1: Removing all Qt packages...")
    qt_packages = [
        "PyQt6",
        "PyQt6-Qt6",
        "PyQt6-sip",
        "PySide6",
        "PyQt5",
        "PyQt5-Qt5",
        "PyQt5-sip",
    ]

    for package in qt_packages:
        run_command(
            [sys.executable, "-m", "pip", "uninstall", package, "-y"],
            f"Uninstalling {package}",
        )

    # Step 2: Clear pip cache
    print("\nStep 2: Clearing pip cache...")
    run_command([sys.executable, "-m", "pip", "cache", "purge"], "Clearing pip cache")

    # Step 3: Update pip
    print("\nStep 3: Updating pip...")
    run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], "Updating pip"
    )

    # Step 4: Install fresh PyQt6
    print("\nStep 4: Installing fresh PyQt6...")
    success = run_command(
        [sys.executable, "-m", "pip", "install", "PyQt6", "--no-cache-dir"],
        "Installing PyQt6",
    )

    if not success:
        print("\n🔄 Trying alternative installation methods...")

        # Try with --force-reinstall
        success = run_command(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "PyQt6",
                "--force-reinstall",
                "--no-cache-dir",
            ],
            "Force reinstalling PyQt6",
        )

        if not success:
            # Try specific version
            success = run_command(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "PyQt6==6.6.1",
                    "--no-cache-dir",
                ],
                "Installing specific PyQt6 version",
            )

    return success


def test_pyqt6():
    """Test PyQt6 installation."""
    print("\n🧪 TESTING PYQT6 INSTALLATION")
    print("=" * 50)

    test_script = """
import sys
try:
    print("Testing PyQt6 imports...")
    
    # Test basic import
    import PyQt6
    print(f"✅ PyQt6 imported successfully")
    print(f"Location: {PyQt6.__file__}")
    
    # Test QtCore
    from PyQt6.QtCore import Qt, QTimer
    print("✅ PyQt6.QtCore imported successfully")
    
    # Test QtWidgets
    from PyQt6.QtWidgets import QApplication, QWidget
    print("✅ PyQt6.QtWidgets imported successfully")
    
    # Test basic functionality
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    widget = QWidget()
    print("✅ QWidget created successfully")
    
    print("🎉 PyQt6 is working correctly!")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ PyQt6 test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""

    try:
        result = subprocess.run(
            [sys.executable, "-c", test_script],
            capture_output=True,
            text=True,
            timeout=30,
        )

        print("Test output:")
        print(result.stdout)

        if result.stderr:
            print("Error output:")
            print(result.stderr)

        if result.returncode == 0:
            print("✅ PyQt6 test PASSED")
            return True
        else:
            print("❌ PyQt6 test FAILED")
            return False

    except Exception as e:
        print(f"💥 Test execution failed: {e}")
        return False


def main():
    """Main diagnostic and fix routine."""
    print("PyQt6 Installation Fix Tool")
    print("=" * 50)

    # Step 1: Diagnose
    diagnose_pyqt6()

    # Step 2: Ask user if they want to fix
    print(f"\n❓ Do you want to fix the PyQt6 installation? (y/n): ", end="")
    try:
        response = input().lower().strip()
    except:
        response = "y"  # Default to yes in automated environments

    if response in ["y", "yes", ""]:
        # Step 3: Fix
        success = fix_pyqt6()

        if success:
            # Step 4: Test
            test_success = test_pyqt6()

            if test_success:
                print(f"\n🎉 SUCCESS! PyQt6 is now working correctly.")
                print(f"You can now run pytest with GUI tests:")
                print(f"  pytest")
                print(f"  pytest -k 'not legacy'  # Skip legacy tests")
            else:
                print(f"\n❌ PyQt6 installation completed but tests still fail.")
                print(f"You may need to:")
                print(f"  1. Restart your terminal/IDE")
                print(f"  2. Check for Windows Visual C++ Redistributables")
                print(f"  3. Try a different PyQt6 version")
        else:
            print(f"\n❌ Failed to fix PyQt6 installation.")
            print(f"Manual steps to try:")
            print(f"  1. pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y")
            print(f"  2. pip install PyQt6 --no-cache-dir")
            print(f"  3. Restart terminal")
    else:
        print(f"\n⏭️  Skipping fix. You can run non-GUI tests with:")
        print(f"  pytest test_basic_setup.py")
        print(f"  pytest src/desktop/modern/tests/unit/core/")


if __name__ == "__main__":
    main()
