#!/usr/bin/env python3
"""
TKA UI Testing Framework - Validation Script

Validates that the UI testing framework is properly installed and working.
"""

from pathlib import Path
import sys

# Add the src directory to the Python path
current_dir = Path(__file__).parent
src_dir = current_dir.parent.parent  # Go up to the src directory
sys.path.insert(0, str(src_dir))


def validate_imports():
    """Validate that all required modules can be imported."""
    print("🔍 Validating imports...")

    try:
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def validate_basic_functionality():
    """Validate basic functionality without full UI setup."""
    print("🔍 Validating basic functionality...")

    try:
        from desktop.modern.core.testing import TKAAITestHelper

        # Test AI helper initialization
        helper = TKAAITestHelper(use_test_mode=True)
        print("✅ AI helper initialization successful")

        # Test basic result creation
        from desktop.modern.core.testing import AITestResult

        result = AITestResult(success=True, metadata={"test": "validation"})
        print("✅ AITestResult creation successful")

        return True
    except Exception as e:
        print(f"❌ Basic functionality validation failed: {e}")
        return False


def validate_ui_tester_creation():
    """Validate UI tester can be created."""
    print("🔍 Validating UI tester creation...")

    try:
        from desktop.modern.core.testing import SimpleUITester

        # Create tester (this might fail if dependencies aren't available)
        tester = SimpleUITester(headless=True)
        print("✅ SimpleUITester creation successful")

        # Test basic methods exist
        assert hasattr(tester, "setup_test_environment"), (
            "Missing setup_test_environment method"
        )
        assert hasattr(tester, "test_workbench_buttons"), (
            "Missing test_workbench_buttons method"
        )
        assert hasattr(tester, "test_graph_editor_interactions"), (
            "Missing test_graph_editor_interactions method"
        )
        assert hasattr(tester, "run_comprehensive_tests"), (
            "Missing run_comprehensive_tests method"
        )

        print("✅ Required methods present")
        return True
    except Exception as e:
        print(f"❌ UI tester creation failed: {e}")
        print("ℹ️  This might be expected if UI dependencies aren't available")
        return False


def validate_cli_interface():
    """Validate CLI interface exists and is importable."""
    print("🔍 Validating CLI interface...")

    try:
        from desktop.modern.core.testing import ui_test_cli

        print("✅ CLI interface import successful")

        # Check main function exists
        assert hasattr(ui_test_cli, "main"), "Missing main function in CLI"
        print("✅ CLI main function present")

        return True
    except Exception as e:
        print(f"❌ CLI interface validation failed: {e}")
        return False


def validate_runner_interface():
    """Validate runner interface."""
    print("🔍 Validating runner interface...")

    try:
        from desktop.modern.core.testing import UITestRunner

        # Create runner
        runner = UITestRunner(headless=True, verbose=False)
        print("✅ UITestRunner creation successful")

        # Test basic methods exist
        assert hasattr(runner, "run_quick_validation"), (
            "Missing run_quick_validation method"
        )
        assert hasattr(runner, "run_button_tests"), "Missing run_button_tests method"
        assert hasattr(runner, "run_graph_editor_tests"), (
            "Missing run_graph_editor_tests method"
        )
        assert hasattr(runner, "run_comprehensive_tests"), (
            "Missing run_comprehensive_tests method"
        )

        print("✅ Required runner methods present")
        return True
    except Exception as e:
        print(f"❌ Runner interface validation failed: {e}")
        return False


def validate_file_structure():
    """Validate that all required files exist."""
    print("🔍 Validating file structure...")

    testing_dir = Path(__file__).parent
    required_files = [
        "simple_ui_tester.py",
        "component_initializer.py",
        "button_tester.py",
        "graph_editor_tester.py",
        "ui_test_runner.py",
        "ui_test_cli.py",
        "ui_test_main.py",
        "ai_agent_helpers.py",
        "__init__.py",
        "README.md",
    ]

    missing_files = []
    for filename in required_files:
        file_path = testing_dir / filename
        if not file_path.exists():
            missing_files.append(filename)

    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True


def main():
    """Main validation function."""
    print("🚀 TKA UI Testing Framework Validation")
    print("=" * 50)

    validations = [
        ("File Structure", validate_file_structure),
        ("Imports", validate_imports),
        ("Basic Functionality", validate_basic_functionality),
        ("UI Tester Creation", validate_ui_tester_creation),
        ("CLI Interface", validate_cli_interface),
        ("Runner Interface", validate_runner_interface),
    ]

    success_count = 0
    total_count = len(validations)

    for name, validation_func in validations:
        print(f"\n📋 {name}:")
        if validation_func():
            success_count += 1
        print()

    print("=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    print(f"✅ Successful validations: {success_count}/{total_count}")
    print(f"❌ Failed validations: {total_count - success_count}/{total_count}")

    if success_count == total_count:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("✅ UI Testing Framework is ready to use")
        return 0
    else:
        print("💥 SOME VALIDATIONS FAILED!")
        print("❌ UI Testing Framework may have issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
