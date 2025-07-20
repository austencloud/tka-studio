#!/usr/bin/env python3
"""
TKA (The Kinetic Alphabet) - Main Application Entry Point
"""

import sys
from pathlib import Path

# Add necessary paths to Python path
project_root = Path(__file__).parent
src_paths = [
    project_root / "src",
    project_root / "src" / "desktop" / "modern" / "src",
    project_root / "launcher",
    project_root / "packages",
]

for path in src_paths:
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))


def main():
    """Main entry point for TKA application."""
    try:
        # Import after path setup
        from src.desktop.modern.main import main as modern_main

        # Launch the modern TKA application
        modern_main()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Available paths:")
        for path in sys.path[:5]:
            print(f"  {path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching TKA application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
