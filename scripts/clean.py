#!/usr/bin/env python3
"""
Clean script for TKA monorepo.
This script cleans up build artifacts, cache files, and temporary files.
"""

import os
import shutil
import sys
from pathlib import Path


def clean_directory(path, patterns, description):
    """Clean files/directories matching patterns in the given path."""
    path = Path(path)
    if not path.exists():
        return

    print(f"🧹 Cleaning {description} in {path}...")
    cleaned_count = 0

    for pattern in patterns:
        for item in path.rglob(pattern):
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                    print(f"   🗑️  Removed directory: {item.relative_to(path)}")
                else:
                    item.unlink()
                    print(f"   🗑️  Removed file: {item.relative_to(path)}")
                cleaned_count += 1
            except Exception as e:
                print(f"   ⚠️  Could not remove {item}: {e}")

    if cleaned_count == 0:
        print(f"   ✅ No {description} found")
    else:
        print(f"   ✅ Cleaned {cleaned_count} items")


def clean_monorepo():
    """Clean the entire monorepo."""
    root = Path(__file__).parent.parent
    print(f"🧹 Cleaning TKA monorepo at: {root.absolute()}")

    # Python cache and build artifacts
    print("\n🐍 Cleaning Python artifacts...")
    python_patterns = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".pytest_cache",
        "*.egg-info",
        "build",
        "dist",
        ".coverage",
        "coverage.xml",
        ".mypy_cache",
        ".tox",
    ]

    # Clean Python artifacts in desktop app
    desktop_path = root / "apps" / "desktop"
    if desktop_path.exists():
        clean_directory(desktop_path, python_patterns, "Python artifacts")

    # Clean Python artifacts in packages
    packages_path = root / "packages"
    if packages_path.exists():
        clean_directory(packages_path, python_patterns, "Python artifacts")

    # Node.js cache and build artifacts
    print("\n📦 Cleaning Node.js artifacts...")
    node_patterns = [
        "node_modules",
        ".npm",
        ".yarn",
        "dist",
        "build",
        ".svelte-kit",
        ".next",
        ".nuxt",
        "coverage",
        ".nyc_output",
        "*.tsbuildinfo",
    ]

    # Clean Node.js artifacts in web apps
    web_apps = ["web", "landing", "animator"]
    for app in web_apps:
        app_path = root / "apps" / app
        if app_path.exists():
            clean_directory(app_path, node_patterns, f"Node.js artifacts ({app})")

    # Clean Node.js artifacts in packages
    if packages_path.exists():
        clean_directory(packages_path, node_patterns, "Node.js artifacts")

    # Clean root node_modules
    root_node_modules = root / "node_modules"
    if root_node_modules.exists():
        print(f"\n🗑️  Removing root node_modules...")
        try:
            shutil.rmtree(root_node_modules)
            print("   ✅ Root node_modules removed")
        except Exception as e:
            print(f"   ⚠️  Could not remove root node_modules: {e}")

    # Test artifacts
    print("\n🧪 Cleaning test artifacts...")
    test_patterns = [
        "test-results",
        "playwright-report",
        ".playwright",
        "screenshots",
        "videos",
    ]

    for app in web_apps:
        app_path = root / "apps" / app
        if app_path.exists():
            clean_directory(app_path, test_patterns, f"test artifacts ({app})")

    # Log files and temporary files
    print("\n📝 Cleaning logs and temporary files...")
    temp_patterns = ["*.log", "*.tmp", ".DS_Store", "Thumbs.db", "*.swp", "*.swo", "*~"]

    clean_directory(root, temp_patterns, "temporary files")

    # IDE and editor files
    print("\n💻 Cleaning IDE artifacts...")
    ide_patterns = [".vscode/settings.json.bak", ".idea", "*.sublime-workspace", ".vs"]

    clean_directory(root, ide_patterns, "IDE artifacts")

    print("\n🎉 Cleanup complete!")
    print("\n💡 To rebuild everything:")
    print("   python scripts/setup.py        # Reinstall dependencies")
    print("   python scripts/dev.py build    # Build all applications")


if __name__ == "__main__":
    try:
        clean_monorepo()
    except KeyboardInterrupt:
        print("\n🛑 Cleanup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        sys.exit(1)
