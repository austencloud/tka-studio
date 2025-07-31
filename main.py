#!/usr/bin/env python3
"""
TKA (The Kinetic Alphabet) - Main Application Entry Point
"""

import os
import sys

# Use the existing universal path management system
from src.infrastructure.paths import tka_paths


def main():
    """Main entry point for TKA application."""
    try:
        # Get TKA root and change to it
        tka_root = tka_paths.find_tka_root()
        os.chdir(tka_root)

        # Import after path setup - modern main.py is in src/desktop/modern/
        # Add the modern directory to path and import the modern main
        modern_path = str(tka_root / "src" / "desktop" / "modern")
        sys.path.insert(0, modern_path)

        # Import the modern main module
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "modern_main", tka_root / "src" / "desktop" / "modern" / "main.py"
        )
        modern_main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modern_main_module)
        modern_main = modern_main_module.main

        # Launch the modern TKA application
        modern_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📁 Available paths:")
        for i, path in enumerate(sys.path[:10]):
            print(f"  {i}: {path}")
        print(f"📂 Current working directory: {os.getcwd()}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching TKA application: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
