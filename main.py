#!/usr/bin/env python3
"""
TKA (The Kinetic Alphabet) - Main Application Entry Point
"""

import os
import sys

# Use the existing universal path management system
import tka_paths


def main():
    """Main entry point for TKA application."""
    try:
        # Get TKA root and change to it
        tka_root = tka_paths.find_tka_root()
        os.chdir(tka_root)

        # Import after path setup - modern main.py is in src/desktop/modern/
        # Since src/desktop/modern is in sys.path, we can import main directly
        sys.path.insert(0, str(tka_root / "src" / "desktop" / "modern"))
        from main import main as modern_main

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
