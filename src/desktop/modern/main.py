#!/usr/bin/env python3
"""
TKA - Main Application Entry Point

Minimal entry point that delegates to focused, single-responsibility components.
The main window class has been extracted to presentation/main_window.py for better organization.
"""

# CRITICAL: Path setup MUST be first - before any other imports
from __future__ import annotations

from pathlib import Path
import sys

# Fix VS Code debugger Unicode encoding issue
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
except (AttributeError, OSError):
    # Fallback for older Python versions or restricted environments
    pass


# Check if tka_paths has already been imported (e.g., from root main.py)
if "tka_paths" not in sys.modules:
    # Only do manual path setup if tka_paths hasn't been imported
    # Get the TKA project root (3 levels up from this file)
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[3]  # main.py -> modern -> desktop -> src -> TKA

    # Define the correct paths for the TKA project
    src_paths = [
        project_root / "src",  # Main src directory (highest priority)
        project_root / "src" / "desktop",  # Desktop directory
        project_root / "launcher",
        project_root / "packages",
    ]

    # Add paths in reverse order since insert(0) puts them at the beginning
    for path in reversed(src_paths):
        if path.exists() and str(path) not in sys.path:
            sys.path.insert(0, str(path))

# Now safe to import everything else
import logging

# Import the focused startup components
from desktop.modern.core.startup import ConfigurationManager

# Import the extracted main window class
from desktop.modern.presentation.main_window import TKAMainWindow


def _position_window_on_secondary_monitor(window):
    """
    Position window on secondary monitor if available, otherwise primary.

    This restores the legacy behavior that was removed during simplification.
    """
    from PyQt6.QtGui import QGuiApplication

    screens = QGuiApplication.screens()

    # Use secondary monitor if available, otherwise primary (legacy behavior)
    target_screen = screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()

    if not target_screen:
        return  # Fallback to default positioning

    # Log which screen we're using
    target_screen.name() if hasattr(target_screen, "name") else "Unknown"
    "secondary" if len(screens) > 1 else "primary"

    # Calculate window dimensions (90% of screen size, centered)
    available_geometry = target_screen.availableGeometry()
    window_width = int(available_geometry.width() * 0.9)
    window_height = int(available_geometry.height() * 0.9)
    x = available_geometry.x() + int((available_geometry.width() - window_width) / 2)
    y = available_geometry.y() + int((available_geometry.height() - window_height) / 2)

    # Apply geometry
    window.setGeometry(x, y, window_width, window_height)
    window.setMinimumSize(1400, 900)


def create_application():
    """
    Create application for testing - returns (app, main_window) tuple.

    Returns:
        tuple: (QApplication, TKAMainWindow)
    """
    from PyQt6.QtWidgets import QApplication

    from desktop.modern.core.application.application_factory import ApplicationFactory

    # Create Qt application
    app = QApplication.instance() or QApplication([])

    # Create container in production mode
    container = ApplicationFactory.create_app("production")

    # Create main window
    window = TKAMainWindow(container)

    return app, window


def main():
    """
    Main entry point - simple and direct.
    """
    logger = logging.getLogger(__name__)

    try:
        # Load configuration
        config_manager = ConfigurationManager()
        config = config_manager.load_configuration()

        if config.mode == "test":
            # Test mode: just create container and return it
            from desktop.modern.core.application.application_factory import (
                ApplicationFactory,
            )

            container = ApplicationFactory.create_app(config.mode)
            return container

        # UI mode: create Qt app and main window
        # Suppress Qt layout warnings that are harmless but noisy
        import os

        from PyQt6.QtWidgets import QApplication

        from desktop.modern.core.application.application_factory import (
            ApplicationFactory,
        )

        os.environ["QT_LOGGING_RULES"] = "qt.qpa.xcb.warning=false"

        app = QApplication.instance() or QApplication([])
        container = ApplicationFactory.create_app(config.mode)

        # Create main window
        window = TKAMainWindow(container)

        # Position window on secondary monitor if available (restored legacy behavior)
        _position_window_on_secondary_monitor(window)

        window.show()
        return app.exec()

    except Exception as e:
        logger.exception(f"Failed to start TKA application: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
