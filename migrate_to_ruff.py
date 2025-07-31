#!/usr/bin/env python3
"""
TKA Ruff Migration Script
Helps migrate from Black + isort + Pylint to Ruff
"""

from pathlib import Path
import subprocess
import sys


def run_command(cmd, description):
    """Run a command and handle errors gracefully."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False


def main():
    """Main migration function."""
    print("🚀 TKA Ruff Migration Script")
    print("=" * 50)

    # Check if we're in the TKA directory
    if not Path("pyproject.toml").exists():
        print(
            "❌ Error: pyproject.toml not found. Please run this script from the TKA root directory."
        )
        return False

    # 1. Install Ruff in the virtual environment
    venv_python = Path(".venv/Scripts/python.exe")
    if venv_python.exists():
        python_cmd = str(venv_python)
        pip_cmd = f"{python_cmd} -m pip"
    else:
        print("⚠️  Virtual environment not found at .venv/Scripts/python.exe")
        print("   Using system Python instead")
        python_cmd = "python"
        pip_cmd = "pip"

    # Install Ruff
    success = run_command(f"{pip_cmd} install ruff>=0.1.0", "Installing Ruff")

    if not success:
        print(
            "❌ Failed to install Ruff. Please install manually with: pip install ruff"
        )
        return False

    # 2. Uninstall old tools (optional)
    print("\n📦 Optional: Remove old linting tools to save space")
    old_tools = ["black", "isort", "pylint"]
    for tool in old_tools:
        run_command(f"{pip_cmd} uninstall {tool} -y", f"Removing {tool}")

    # 3. Run Ruff check to see current issues
    print("\n🔍 Running Ruff check to see current code status...")
    run_command(f"{python_cmd} -m ruff check .", "Checking code with Ruff")

    # 4. Run Ruff format to format all code
    print("\n🎨 Formatting all Python code with Ruff...")
    run_command(f"{python_cmd} -m ruff format .", "Formatting code with Ruff")

    # 5. Fix auto-fixable issues
    print("\n🔧 Auto-fixing issues where possible...")
    run_command(f"{python_cmd} -m ruff check . --fix", "Auto-fixing issues with Ruff")

    # 6. Install pre-commit hooks
    print("\n🪝 Setting up pre-commit hooks...")
    run_command(f"{pip_cmd} install pre-commit", "Installing pre-commit")

    run_command(f"{python_cmd} -m pre_commit install", "Installing pre-commit hooks")

    # 7. Clean up old configuration files (optional)
    old_configs = [".pylintrc", "setup.cfg", ".flake8"]
    for config in old_configs:
        if Path(config).exists():
            print(f"\n🗑️  Found old config file: {config}")
            response = input(f"   Delete {config}? [y/N]: ").strip().lower()
            if response == "y":
                Path(config).unlink()
                print(f"   ✅ Deleted {config}")
            else:
                print(f"   ⏭️  Keeping {config}")

    print("\n" + "=" * 50)
    print("🎉 Migration completed!")
    print("\n📋 What's changed:")
    print("   • Ruff installed (replaces Black + isort + Pylint)")
    print("   • VS Code settings updated for better performance")
    print("   • pyproject.toml configured with Ruff rules")
    print("   • Pre-commit hooks set up")
    print("\n🔧 Next steps:")
    print("   1. Restart VS Code")
    print("   2. Install the Ruff VS Code extension: 'charliermarsh.ruff'")
    print("   3. Run: ruff check . --fix")
    print("   4. Run: ruff format .")
    print("   5. Check for any remaining issues")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
