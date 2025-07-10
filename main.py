#!/usr/bin/env python3
"""
TKA (The Kinetic Alphabet) - Main Application Entry Point

This is the main entry point for the TKA application.
It launches the modern desktop application.
"""

import sys
from pathlib import Path

# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(modern_src_path))

# Import and run the modern application
from src.desktop.modern.main import main as modern_main


def main():
    """Main entry point for TKA application."""
    try:
        # Launch the modern TKA application
        modern_main()
    except Exception as e:
        print(f"Error launching TKA application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
