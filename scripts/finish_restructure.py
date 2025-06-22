#!/usr/bin/env python3
"""
Finish the monorepo restructuring by copying remaining directories.
"""

import os
import shutil
import sys
from pathlib import Path


def copy_directory_contents(src, dst, exclude_dirs=None, exclude_files=None):
    """Copy directory contents while excluding certain directories and files."""
    if exclude_dirs is None:
        exclude_dirs = {
            ".git",
            "__pycache__",
            "node_modules",
            ".pytest_cache",
            ".svelte-kit",
        }
    if exclude_files is None:
        exclude_files = {"*.pyc", "*.pyo"}

    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.exists():
        print(f"⚠️  Source {src} does not exist")
        return False

    # Create destination directory
    dst_path.mkdir(parents=True, exist_ok=True)

    for item in src_path.iterdir():
        if item.is_dir():
            if item.name in exclude_dirs:
                print(f"⏭️  Skipping excluded directory: {item}")
                continue

            dst_item = dst_path / item.name
            try:
                if dst_item.exists():
                    shutil.rmtree(dst_item)
                shutil.copytree(
                    item, dst_item, ignore=shutil.ignore_patterns("*.pyc", "*.pyo")
                )
                print(f"✅ Copied directory: {item} → {dst_item}")
            except Exception as e:
                print(f"❌ Failed to copy directory {item}: {e}")
        else:
            if any(item.match(pattern) for pattern in exclude_files):
                continue

            dst_item = dst_path / item.name
            try:
                shutil.copy2(item, dst_item)
                print(f"✅ Copied file: {item} → {dst_item}")
            except Exception as e:
                print(f"❌ Failed to copy file {item}: {e}")

    return True


def main():
    """Finish the restructuring process."""
    print("🔧 Finishing monorepo restructuring...")

    # Copy desktop app contents
    print("\n📱 Copying desktop app...")
    if copy_directory_contents("tka-desktop", "apps/desktop"):
        print("✅ Desktop app copied successfully")
    else:
        print("❌ Failed to copy desktop app")

    # Copy web app contents
    print("\n🌐 Copying web app...")
    if copy_directory_contents("tka-web/tka-web-app", "apps/web"):
        print("✅ Web app copied successfully")
    else:
        print("❌ Failed to copy web app")

    print("\n🎉 Restructuring completion finished!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
