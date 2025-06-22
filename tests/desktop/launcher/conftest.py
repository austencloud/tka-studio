"""
Launcher-specific test configuration.

Provides fixtures and utilities for launcher application testing.
This module handles PyQt6 imports safely to avoid crashes during test discovery.
"""

import os
import sys
import pytest
from unittest.mock import Mock

# Set Qt platform to minimal for headless testing
os.environ.setdefault("QT_QPA_PLATFORM", "minimal")


def pytest_configure(config):
    """Configure pytest for launcher tests."""
    # Add markers
    config.addinivalue_line("markers", "qt: tests that require Qt")
    config.addinivalue_line("markers", "launcher: launcher-specific tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to handle Qt availability."""
    qt_available = True
    try:
        # Try importing PyQt6 in a safer way
        import sys

        if sys.platform == "win32":
            # Set Qt platform before importing on Windows
            import os

            os.environ.setdefault("QT_QPA_PLATFORM", "minimal")
        import PyQt6.QtWidgets
    except ImportError:
        qt_available = False
    except Exception:
        # Any other exception (like DLL loading errors) means Qt isn't available
        qt_available = False

    if not qt_available:
        skip_qt = pytest.mark.skip(
            reason="PyQt6 not available or Qt environment not suitable"
        )
        for item in items:
            if "qt" in item.keywords or any(
                marker.name == "qt" for marker in item.iter_markers()
            ):
                item.add_marker(skip_qt)


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for testing."""
    try:
        import sys

        if sys.platform == "win32":
            import os

            os.environ.setdefault("QT_QPA_PLATFORM", "minimal")

        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        yield app
    except ImportError:
        pytest.skip("PyQt6 not available")
    except Exception as e:
        pytest.skip(f"Qt environment not suitable: {e}")


@pytest.fixture
def mock_launcher_window():
    """Mock launcher window for testing."""
    return Mock()


@pytest.fixture
def mock_app_grid():
    """Mock application grid for testing."""
    return Mock()


@pytest.fixture
def sample_app_data():
    """Sample application data for testing."""
    return [
        {
            "id": "tka_desktop",
            "name": "TKA Desktop",
            "description": "Main TKA application",
            "category": "core",
            "icon_path": "icons/desktop.png",
        },
        {
            "id": "tka_web",
            "name": "TKA Web",
            "description": "Web-based interface",
            "category": "web",
            "icon_path": "icons/web.png",
        },
    ]
