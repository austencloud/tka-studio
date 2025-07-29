#!/usr/bin/env python3
"""
TKA - Main Application Entry Point

Minimal entry point that delegates to focused, single-responsibility components.
The main window class has been extracted to presentation/main_window.py for better organization.
"""

# CRITICAL: Path setup MUST be first - before any other imports
import sys
from pathlib import Path

# Check if tka_paths has already been imported (e.g., from root main.py)
if "tka_paths" not in sys.modules:
    # Only do manual path setup if tka_paths hasn't been imported
    # Get the TKA project root (3 levels up from this file)
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[2]  # main.py -> modern -> desktop -> TKA

    # Define the same paths as root main.py - MUST match exactly
    src_paths = [
        project_root
        / "src"
        / "desktop"
        / "modern"
        / "src",  # Modern src (highest priority)
        project_root / "src" / "desktop",  # Desktop directory
        project_root / "src",  # Shared src (lowest priority)
        project_root / "launcher",
        project_root / "packages",
    ]

    # Add paths in reverse order since insert(0) puts them at the beginning
    for path in reversed(src_paths):
        if path.exists() and str(path) not in sys.path:
            sys.path.insert(0, str(path))

    print(
        f"[PATH_SETUP] Added {len([p for p in src_paths if p.exists()])} paths for VS Code debugger compatibility"
    )
    print(f"[PATH_SETUP] First 5 sys.path entries:")
    for i, path in enumerate(sys.path[:5]):
        print(f"  {i}: {path}")

# Now safe to import everything else
import logging

# Import the focused startup components
from desktop.modern.core.startup import ApplicationBootstrapper, ConfigurationManager

# Import the extracted main window class
from desktop.modern.presentation.main_window import TKAMainWindow


def main():
    """
    Main entry point with support for different application modes.

    Refactored to use focused, single-responsibility components for better maintainability.
    """
    logger = logging.getLogger(__name__)

    try:
        # Load configuration using ConfigurationManager
        config_manager = ConfigurationManager()
        config = config_manager.load_configuration()

        # Bootstrap application using ApplicationBootstrapper
        bootstrapper = ApplicationBootstrapper()
        result = bootstrapper.bootstrap_application(config)

        # Return result for test modes, or exit code for UI modes
        return result if result is not None else 0

    except Exception as e:
        logger.error(f"Failed to start TKA application: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
