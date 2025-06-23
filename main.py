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


def launch_desktop_launcher():
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


def launch_modern_direct():
    """Launch the modern TKA Desktop application directly."""
    try:
        modern_desktop_path = Path(__file__).parent / "src" / "desktop" / "modern"

        if str(modern_desktop_path) not in sys.path:
            sys.path.insert(0, str(modern_desktop_path))

        # Change to modern desktop directory
        original_cwd = Path.cwd()
        os.chdir(modern_desktop_path)

        try:
            from main import main as modern_main

            return modern_main()
        finally:
            # Restore original working directory
            os.chdir(original_cwd)

    except ImportError as modern_error:
        print(f"Error importing Modern main: {modern_error}")
        print("Please ensure the TKA Desktop modern application is properly set up.")
        return 1


def launch_legacy_direct():
    """Launch the legacy TKA Desktop application directly."""
    try:
        print("🏛️ Launching TKA Desktop (Legacy Version)")

        legacy_desktop_path = Path(__file__).parent / "src" / "desktop" / "legacy"

        if str(legacy_desktop_path) not in sys.path:
            sys.path.insert(0, str(legacy_desktop_path))

        # Change to legacy desktop directory
        original_cwd = Path.cwd()
        os.chdir(legacy_desktop_path)

        try:
            from main import main as legacy_main

            return legacy_main()
        finally:
            # Restore original working directory
            os.chdir(original_cwd)

    except ImportError as legacy_error:
        print(f"Error importing Legacy main: {legacy_error}")
        print("Please ensure the TKA Desktop legacy application is properly set up.")
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
    parser = argparse.ArgumentParser(
        description="TKA - The Kinetic Constructor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
TKA uses a unified Modern Launcher interface for all applications and tools.
        """,
    )

    # Keep legacy arguments for backward compatibility but route everything to launcher
    parser.add_argument(
        "--modern",
        action="store_true",
        help="Launch modern TKA Desktop directly (legacy - use launcher instead)",
    )
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Launch legacy TKA Desktop directly (legacy - use launcher instead)",
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Launch TKA development tools (legacy - use launcher instead)",
    )

    args = parser.parse_args()

    # Setup monorepo environment
    setup_monorepo_paths()

    # Show deprecation warnings for direct launch arguments
    if args.modern:
        print(
            "⚠️  Direct --modern launch is deprecated. Use the Modern Launcher to access TKA Desktop (Modern)."
        )
    elif args.legacy:
        print(
            "⚠️  Direct --legacy launch is deprecated. Use the Modern Launcher to access TKA Desktop (Legacy)."
        )
    elif args.dev:
        print(
            "⚠️  Direct --dev launch is deprecated. Use the Modern Launcher to access Development Tools."
        )

    # Always launch the Modern Launcher - it provides access to everything
    print("🚀 Launching TKA Modern Launcher...")
    return launch_desktop_launcher()


if __name__ == "__main__":
    sys.exit(main())
