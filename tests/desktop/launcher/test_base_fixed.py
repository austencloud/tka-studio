#!/usr/bin/env python3
"""
Base test utilities for TKA Launcher testing.
"""

import logging
import sys
from pathlib import Path
from typing import Any, List, Optional
from unittest.mock import MagicMock, Mock

import pytest

# Setup logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def _ensure_qt_application():
    """Ensure QApplication instance exists for tests."""
    try:
        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        return app
    except ImportError:
        pytest.skip("PyQt6 not available")


# Global QApplication instance for tests
_app_instance = None


def get_test_app():
    """Get or create a QApplication instance for testing."""
    global _app_instance
    if _app_instance is None:
        _app_instance = _ensure_qt_application()
    return _app_instance


class MockTKAIntegration:
    """Mock TKA integration for testing."""

    def __init__(self):
        self.applications = [
            MockAppData("app1", "TKA Desktop", "Main TKA application", "core"),
            MockAppData("app2", "TKA Web", "Web-based TKA interface", "web"),
            MockAppData("app3", "TKA Launcher", "Application launcher", "utility"),
        ]


class MockAppData:
    """Mock application data for testing."""

    def __init__(self, id: str, name: str, description: str, category: str):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.icon_path = f"icons/{id}.png"
        self.executable_path = f"bin/{id}"


class TestHelperMixin:
    """Base test helper mixin for launcher tests."""

    def setup_method(self):
        """Setup method run before each test."""
        self.app = get_test_app()
        self.tka_integration = MockTKAIntegration()

    def teardown_method(self):
        """Cleanup method run after each test."""
        # Process any pending events
        if self.app:
            self.app.processEvents()

    def wait_for_signal(self, signal, timeout=1000):
        """Wait for a signal to be emitted within timeout."""
        received = []
        signal.connect(lambda *args: received.append(args))

        loop_count = 0
        max_loops = timeout // 10

        while not received and loop_count < max_loops:
            self.app.processEvents()
            try:
                from PyQt6.QtCore import QTimer

                QTimer.singleShot(10, lambda: None)
            except ImportError:
                pass
            loop_count += 1

        return received[0] if received else None

    def create_mock_widget(self, parent=None):
        """Create a mock widget for testing."""
        try:
            from PyQt6.QtWidgets import QWidget

            widget = QWidget(parent)
            widget.setFixedSize(300, 200)
            return widget
        except ImportError:
            pytest.skip("PyQt6 not available")


def assert_widget_properties(widget, expected_properties):
    """Assert that a widget has expected properties."""
    for prop_name, expected_value in expected_properties.items():
        actual_value = getattr(widget, prop_name, None)
        if callable(actual_value):
            actual_value = actual_value()

        assert (
            actual_value == expected_value
        ), f"Property {prop_name}: expected {expected_value}, got {actual_value}"


def wait_for_condition(condition_func, timeout=1000, interval=10):
    """Wait for a condition to become true."""
    app = get_test_app()
    elapsed = 0

    while elapsed < timeout:
        if condition_func():
            return True
        app.processEvents()
        elapsed += interval

    return False


@pytest.fixture
def test_app():
    """Pytest fixture for QApplication."""
    return get_test_app()


@pytest.fixture
def mock_tka_integration():
    """Pytest fixture for mock TKA integration."""
    return MockTKAIntegration()
