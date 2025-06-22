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
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget

# Setup logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Global QApplication instance for tests
_app_instance = None


def get_test_app():
    """Get or create a QApplication instance for testing."""
    global _app_instance
    if _app_instance is None:
        if QApplication.instance() is None:
            _app_instance = QApplication(sys.argv)
        else:
            _app_instance = QApplication.instance()
    return _app_instance


class MockTKAIntegration:
    """Mock TKA integration for testing."""

    def __init__(self):
        self.applications = [
            MockAppData("app1", "TKA Desktop", "Main TKA application", "core"),
            MockAppData("app2", "TKA Web", "Web-based TKA interface", "web"),
            MockAppData("app3", "TKA Launcher", "Application launcher", "utility"),
        ]

    def get_applications(self):
        return self.applications

    def launch_application(self, app_id):
        logger.info(f"Mock launching application: {app_id}")
        return True


class MockAppData:
    """Mock application data for testing."""

    def __init__(self, app_id, title, description, category):
        self.id = app_id
        self.title = title
        self.description = description
        self.category = MockCategory(category)


class MockCategory:
    """Mock category for application data."""

    def __init__(self, value):
        self.value = value


class LauncherTestCase:
    """Base test case class for launcher components."""

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
            QTimer.singleShot(10, lambda: None)
            loop_count += 1

        return received[0] if received else None

    def create_mock_widget(self, parent=None):
        """Create a mock widget for testing."""
        widget = QWidget(parent)
        widget.setFixedSize(300, 200)
        return widget


def assert_widget_properties(widget, expected_properties):
    """Assert that a widget has expected properties."""
    for prop_name, expected_value in expected_properties.items():
        actual_value = getattr(widget, prop_name, None)
        if callable(actual_value):
            actual_value = actual_value()

        assert actual_value == expected_value, (
            f"Widget property {prop_name} expected {expected_value}, "
            f"got {actual_value}"
        )
