#!/usr/bin/env python3
"""
Setup script for TKA Automated Testing Pipeline
"""

import subprocess
import sys
from pathlib import Path
import shutil


def install_dependencies():
    """Install required dependencies for automated testing."""
    print("Installing dependencies...")

    dependencies = [
        "pre-commit",
        "watchdog",
        "schedule",
        "pytest",
        "pytest-cov",
        "pytest-xdist",
        "pytest-qt",
    ]

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install"] + dependencies, check=True
        )
        print("[PASS] Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Failed to install dependencies: {e}")
        return False


def setup_pre_commit():
    """Setup pre-commit hooks."""
    print("Setting up pre-commit hooks...")

    try:
        subprocess.run(["pre-commit", "install"], check=True)
        print("[PASS] Pre-commit hooks installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Failed to install pre-commit hooks: {e}")
        return False


def setup_git_hooks():
    """Setup Git hooks."""
    print("Setting up Git hooks...")

    project_root = Path.cwd()
    git_dir = project_root / ".git"

    if not git_dir.exists():
        print("[FAIL] No .git directory found. Make sure you're in a Git repository.")
        return False

    hooks_dir = git_dir / "hooks"
    if not hooks_dir.exists():
        print("[FAIL] Git hooks directory not found.")
        return False

    # Copy post-merge hook
    source_hook = project_root / "scripts" / "git-hooks" / "post-merge"
    target_hook = hooks_dir / "post-merge"

    try:
        if source_hook.exists():
            shutil.copy2(source_hook, target_hook)
            # Make it executable (Unix/Linux/Mac)
            target_hook.chmod(0o755)
            print("[PASS] Post-merge hook installed")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to setup Git hooks: {e}")
        return False


def create_test_directories():
    """Create necessary test directories."""
    print("Creating test directories...")

    test_dirs = [
        "tests/unit",
        "tests/integration",
        "tests/regression/bugs",
        "tests/specification",
    ]

    success = True
    for dir_path in test_dirs:
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            # Create __init__.py files
            init_file = Path(dir_path) / "__init__.py"
            if not init_file.exists():
                init_file.write_text("")
            print(f"[PASS] Created: {dir_path}")
        except Exception as e:
            print(f"[FAIL] Failed to create {dir_path}: {e}")
            success = False

    return success


def create_placeholder_tests():
    """Create placeholder test files."""
    print("Creating placeholder test files...")

    test_files = {
        "tests/unit/test_placeholder.py": '''"""Unit test placeholder."""
import pytest

def test_placeholder():
    """Placeholder unit test."""
    assert True
''',
        "tests/integration/test_placeholder.py": '''"""Integration test placeholder."""
import pytest

def test_placeholder():
    """Placeholder integration test."""
    assert True
''',
        "tests/regression/bugs/test_placeholder.py": '''"""Regression test placeholder."""
import pytest

def test_placeholder():
    """Placeholder regression test."""
    assert True
''',
        "tests/specification/test_placeholder.py": '''"""Specification test placeholder."""
import pytest

def test_placeholder():
    """Placeholder specification test."""
    assert True
''',
    }

    success = True
    for file_path, content in test_files.items():
        try:
            test_file = Path(file_path)
            if not test_file.exists():
                test_file.write_text(content)
                print(f"[PASS] Created: {file_path}")
        except Exception as e:
            print(f"[FAIL] Failed to create {file_path}: {e}")
            success = False

    return success


def create_vscode_tasks():
    """Create VS Code tasks configuration."""
    print("Creating VS Code tasks...")

    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Run All Tests",
                "type": "shell",
                "command": "python",
                "args": ["scripts/simple_test_runner.py"],
                "group": "test",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "new",
                },
            },
            {
                "label": "Start Test Watcher",
                "type": "shell",
                "command": "python",
                "args": ["scripts/test_watcher.py"],
                "group": "test",
                "isBackground": True,
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "new",
                },
            },
            {
                "label": "Health Monitor",
                "type": "shell",
                "command": "python",
                "args": ["scripts/health_monitor.py"],
                "group": "test",
                "isBackground": True,
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "new",
                },
            },
        ],
    }

    try:
        import json

        tasks_file = vscode_dir / "tasks.json"
        with open(tasks_file, "w") as f:
            json.dump(tasks_config, f, indent=2)
        print("[PASS] VS Code tasks configuration created")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to create VS Code tasks: {e}")
        return False


def main():
    """Main setup function."""
    print("TKA Automated Testing Setup")
    print("=" * 40)

    setup_steps = [
        ("Install Dependencies", install_dependencies),
        ("Create Test Directories", create_test_directories),
        ("Create Placeholder Tests", create_placeholder_tests),
        ("Setup Pre-commit Hooks", setup_pre_commit),
        ("Setup Git Hooks", setup_git_hooks),
        ("Create VS Code Tasks", create_vscode_tasks),
    ]

    success_count = 0
    total_steps = len(setup_steps)

    for step_name, step_func in setup_steps:
        print(f"\n{step_name}...")
        if step_func():
            success_count += 1

    print("\n" + "=" * 40)
    print(f"Setup Complete: {success_count}/{total_steps} steps successful")

    if success_count == total_steps:
        print("[PASS] All setup steps completed successfully!")
        print("\nNext steps:")
        print("1. Run: python scripts/validate_test_automation.py")
        print("2. Start test watcher: python scripts/test_watcher.py")
        print("3. Run tests: python scripts/simple_test_runner.py")
        return True
    else:
        print("[FAIL] Some setup steps failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
