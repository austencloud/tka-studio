#!/usr/bin/env python3
"""
Main entry point for The Kinetic Constructor (TKA).

This script provides a unified entry point that always launches the Modern Launcher,
which gives access to all TKA applications and development tools:

- TKA Desktop (Modern)
- TKA Desktop (Legacy)
- Web Applications
- Development Tools
- Test Suites
- Settings and Utilities

Usage:
    python main.py                    # Launch TKA Modern Launcher (recommended)
    python main.py --legacy           # Show deprecation warning, then launch Modern Launcher
    python main.py --modern           # Show deprecation warning, then launch Modern Launcher
    python main.py --dev              # Show deprecation warning, then launch Modern Launcher
"""

import os
import sys
import argparse
from pathlib import Path


def setup_monorepo_paths():
    """Ensure the working directory and Python paths are set correctly for the monorepo."""
    # Get the directory where this script is located (TKA root)
    script_dir = Path(__file__).parent.absolute()

    # Change working directory to TKA root if we're not already there
    if Path.cwd() != script_dir:
        os.chdir(script_dir)

    # Add TKA root to Python path if not already there
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))


def start_launcher():
    """Launch the TKA Unified Launcher interface."""
    try:
        # Import and setup the unified launcher
        launcher_path = Path(__file__).parent / "launcher"
        if str(launcher_path) not in sys.path:
            sys.path.insert(0, str(launcher_path))

        # Change to launcher directory
        original_cwd = Path.cwd()
        os.chdir(launcher_path)

        try:
            from main import main as launcher_main

            return launcher_main()
        finally:
            # Restore original working directory
            os.chdir(original_cwd)

    except ImportError as e:
        print(f"Error importing TKA Unified Launcher: {e}")
        print("Please ensure the TKA Unified Launcher is properly set up.")
        return 1


def launch_dev_tools():
    """Launch TKA development tools."""
    try:
        desktop_path = Path(__file__).parent / "src" / "desktop"

        if str(desktop_path) not in sys.path:
            sys.path.insert(0, str(desktop_path))

        # Change to desktop directory
        original_cwd = Path.cwd()
        os.chdir(desktop_path)

        try:
            import dev_setup

            return dev_setup.main()
        finally:
            # Restore original working directory
            os.chdir(original_cwd)

    except ImportError as dev_error:
        print(f"Error importing development tools: {dev_error}")
        print("Please ensure the TKA Desktop development tools are properly set up.")
        return 1


def main():
    """Main entry point - always launch the Modern Launcher."""
    # setup_monorepo_paths()
    return start_launcher()


if __name__ == "__main__":
    sys.exit(main())
