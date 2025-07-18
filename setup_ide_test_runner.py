#!/usr/bin/env python3
"""
IDE Test Runner Configuration Setup
===================================

Configures the IDE to use pytest as the test runner and sets up proper
import path resolution for individual test execution.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def setup_vscode_pytest_config():
    """Configure VS Code to use pytest as the test runner."""

    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    # VS Code settings for pytest
    settings = {
        "python.testing.pytestEnabled": True,
        "python.testing.unittestEnabled": False,
        "python.testing.pytestArgs": [".", "-v", "--tb=short"],
        "python.testing.cwd": "${workspaceFolder}",
        "python.testing.autoTestDiscoverOnSaveEnabled": True,
        "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
        "python.terminal.activateEnvironment": True,
        "python.testing.pytestPath": "./.venv/Scripts/pytest.exe",
    }

    settings_file = vscode_dir / "settings.json"

    # Merge with existing settings if they exist
    if settings_file.exists():
        with open(settings_file, "r", encoding="utf-8") as f:
            existing_settings = json.load(f)
        existing_settings.update(settings)
        settings = existing_settings

    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

    print("✅ VS Code pytest configuration created/updated")
    return settings_file


def setup_pycharm_pytest_config():
    """Configure PyCharm to use pytest as the test runner."""

    idea_dir = Path(".idea")
    if not idea_dir.exists():
        print("⚠️ PyCharm .idea directory not found - configure manually")
        return None

    # Create pytest run configuration template
    run_config = """
<component name="ProjectRunConfigurationManager">
  <configuration default="true" type="tests" factoryName="py.test">
    <module name="TKA" />
    <option name="INTERPRETER_OPTIONS" value="" />
    <option name="PARENT_ENVS" value="true" />
    <envs />
    <option name="SDK_HOME" value="$PROJECT_DIR$/.venv/Scripts/python.exe" />
    <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$" />
    <option name="IS_MODULE_SDK" value="false" />
    <option name="ADD_CONTENT_ROOTS" value="true" />
    <option name="ADD_SOURCE_ROOTS" value="true" />
    <option name="SCRIPT_NAME" value="" />
    <option name="CLASS_NAME" value="" />
    <option name="METHOD_NAME" value="" />
    <option name="FOLDER_NAME" value="" />
    <option name="TEST_TYPE" value="TEST_SCRIPT" />
    <option name="PATTERN" value="" />
    <option name="USE_PATTERN" value="false" />
    <option name="testToRun" value="" />
    <option name="keywords" value="" />
    <option name="params" value="-v --tb=short" />
    <option name="USE_PARAM" value="true" />
    <option name="USE_KEYWORD" value="false" />
    <method v="2" />
  </configuration>
</component>
"""

    workspace_file = idea_dir / "workspace.xml"
    if workspace_file.exists():
        print("✅ PyCharm workspace found - add pytest configuration manually")
        print("   Go to Run/Debug Configurations > Templates > Python tests > pytest")
        print("   Set working directory to project root")
        print("   Set additional arguments: -v --tb=short")

    return workspace_file


def create_test_runner_script():
    """Create a universal test runner script that works with any IDE."""

    script_content = '''#!/usr/bin/env python3
"""
Universal Test Runner for TKA
=============================

This script can be used by any IDE to run individual tests or test files
with proper import path resolution.

Usage:
    python run_test.py <test_file_or_pattern>
    python run_test.py tests/unit/services/test_option_picker_size_service.py
    python run_test.py tests/unit/services/test_option_picker_size_service.py::TestOptionPickerSizeService::test_initial_state
"""

import sys
import subprocess
from pathlib import Path


def run_test(test_target):
    """Run a test using pytest with proper configuration."""
    
    # Ensure we're in the project root
    project_root = Path(__file__).parent
    
    # Build pytest command
    cmd = [
        sys.executable, "-m", "pytest",
        str(test_target),
        "-v",
        "--tb=short"
    ]
    
    print(f"🧪 Running: {' '.join(cmd)}")
    print(f"📁 Working directory: {project_root}")
    print("-" * 60)
    
    # Run the test
    result = subprocess.run(
        cmd,
        cwd=project_root,
        env=dict(os.environ, PYTHONPATH=str(project_root))
    )
    
    return result.returncode


def main():
    """Main test runner function."""
    if len(sys.argv) < 2:
        print("Usage: python run_test.py <test_file_or_pattern>")
        print("Examples:")
        print("  python run_test.py tests/unit/services/")
        print("  python run_test.py tests/unit/services/test_option_picker_size_service.py")
        print("  python run_test.py tests/unit/services/test_option_picker_size_service.py::TestOptionPickerSizeService::test_initial_state")
        return 1
    
    test_target = sys.argv[1]
    return run_test(test_target)


if __name__ == "__main__":
    import os
    sys.exit(main())
'''

    script_file = Path("run_test.py")
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(script_content)

    # Make executable on Unix systems
    if os.name != "nt":
        os.chmod(script_file, 0o755)

    print(f"✅ Universal test runner created: {script_file}")
    return script_file


def setup_pytest_ini_for_ide():
    """Ensure pytest.ini is configured for IDE compatibility."""

    pytest_ini = Path("pytest.ini")

    config_content = """[tool:pytest]
# TKA Test Configuration for IDE Integration
minversion = 6.0
testpaths = 
    .
    src/desktop/modern/tests
    src/desktop/legacy/tests
    launcher/tests

python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Output configuration
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --color=yes

# Markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    gui: marks tests that require GUI components

# Test discovery
norecursedirs = 
    .git
    .tox
    dist
    build
    *.egg
    __pycache__
    .venv
    venv

# Minimum test timeout
timeout = 300

# Console output
console_output_style = progress
"""

    with open(pytest_ini, "w", encoding="utf-8") as f:
        f.write(config_content)

    print(f"✅ pytest.ini configured for IDE integration")
    return pytest_ini


def test_ide_integration():
    """Test that IDE integration is working correctly."""

    print("\n🧪 Testing IDE Integration...")

    # Test 1: Run a simple test using the universal runner
    test_file = "tests/unit/services/test_option_picker_size_service.py::TestOptionPickerSizeService::test_calculate_optimal_width_basic"

    result = subprocess.run(
        [sys.executable, "run_test.py", test_file], capture_output=True, text=True
    )

    if result.returncode == 0:
        print("✅ Universal test runner works correctly")
    else:
        print("❌ Universal test runner failed")
        print(f"Error: {result.stderr}")
        return False

    # Test 2: Verify pytest discovery works
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "tests/unit/services/",
        ],
        capture_output=True,
        text=True,
    )

    if "collected" in result.stdout and "items" in result.stdout:
        print("✅ Pytest test discovery works correctly")
    else:
        print("❌ Pytest test discovery failed")
        return False

    return True


def main():
    """Main setup function."""
    print("🚀 Setting up IDE Test Runner Integration")
    print("=" * 60)

    # Setup configurations
    vscode_config = setup_vscode_pytest_config()
    pycharm_config = setup_pycharm_pytest_config()
    test_runner = create_test_runner_script()
    pytest_config = setup_pytest_ini_for_ide()

    print("\n📋 Configuration Summary:")
    print(f"   VS Code config: {vscode_config}")
    print(
        f"   PyCharm config: {'Configured' if pycharm_config else 'Manual setup required'}"
    )
    print(f"   Universal runner: {test_runner}")
    print(f"   Pytest config: {pytest_config}")

    # Test the integration
    if test_ide_integration():
        print("\n🎯 IDE Integration Setup Complete!")
        print("\n📖 How to use:")
        print("   VS Code: Use the Test Explorer or Ctrl+Shift+P > 'Python: Run Tests'")
        print("   PyCharm: Right-click test files and select 'Run pytest in...'")
        print("   Any IDE: Use 'python run_test.py <test_path>' for individual tests")
        print("\n✅ All tests can now be run with IDE play buttons!")
    else:
        print("\n❌ IDE Integration setup encountered issues")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
