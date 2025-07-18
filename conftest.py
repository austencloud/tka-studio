"""
TKA Test Configuration
======================

Minimal conftest.py that relies on proper package installation
instead of sys.path manipulation.
"""

import pytest
import warnings
from pathlib import Path


def pytest_configure(config):
    """Configure pytest with comprehensive markers."""
    markers = [
        "unit: Unit tests (fast, isolated)",
        "integration: Integration tests",
        "modern: Modern codebase tests",
        "legacy: Legacy codebase tests", 
        "launcher: Launcher tests",
        "slow: Tests taking >5 seconds",
        "broken: Known broken tests",
        "gui: GUI tests requiring display",
        "skip_if_no_pyqt6: Skip if PyQt6 unavailable",
    ]

    for marker in markers:
        config.addinivalue_line("markers", marker)


def pytest_sessionstart(session):
    """Session start with minimal diagnostics."""
    if session.config.option.verbose >= 1:
        print("🚀 TKA Test Suite Starting")
        print("✅ Using editable package installation")


@pytest.fixture(scope="session")
def tka_root():
    """Provide the TKA project root directory."""
    return Path(__file__).parent.absolute()


@pytest.fixture(scope="session") 
def qt_app():
    """Provide a QApplication instance for GUI tests."""
    try:
        from PyQt6.QtWidgets import QApplication
        import sys
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        yield app
        
        # Clean up
        if app:
            app.quit()
            
    except ImportError:
        pytest.skip("PyQt6 not available")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add markers based on test file location
        test_path = str(item.fspath)
        
        if "launcher/tests" in test_path:
            item.add_marker(pytest.mark.launcher)
        elif "src/desktop/modern/tests" in test_path:
            item.add_marker(pytest.mark.modern)
        elif "src/desktop/legacy/tests" in test_path:
            item.add_marker(pytest.mark.legacy)
        elif "tests/unit" in test_path:
            item.add_marker(pytest.mark.unit)
        elif "tests/integration" in test_path:
            item.add_marker(pytest.mark.integration)
        
        # Mark GUI tests
        if any(gui_keyword in test_path.lower() for gui_keyword in ["gui", "widget", "window", "qt"]):
            item.add_marker(pytest.mark.gui)


# Suppress specific warnings that are not actionable
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
warnings.filterwarnings("ignore", message=".*distutils.*")
