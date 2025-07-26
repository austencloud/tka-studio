#!/usr/bin/env python3
"""
Graph Editor Test Configuration
==============================

Provides pytest fixtures and configuration for graph editor testing.
Follows TKA testing protocols and architectural patterns.
"""

import sys
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock, Mock

import pytest

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))

from desktop.modern.core.application.application_factory import ApplicationFactory

# Import TKA testing infrastructure
from desktop.modern.core.testing.ai_agent_helpers import TKAAITestHelper

from .mock_beat_data import (
    GraphEditorTestData,
    create_complex_beat,
    create_regular_beat,
    create_sample_beat_data,
    create_sample_sequence_data,
    create_start_position_beat,
)

# Import mock infrastructure
from .mock_services import (
    MockDataFlowService,
    MockGraphEditorService,
    MockHotkeyService,
    create_all_mock_services,
)


@pytest.fixture(scope="session")
def qapp():
    """
    Create session-scoped QApplication for Qt tests.

    This follows pytest-qt best practices:
    - Session scope prevents multiple QApplication instances
    - Proper cleanup prevents memory leaks
    - Compatible with pytest-qt fixtures
    """
    import gc

    from PyQt6.QtCore import QTimer
    from PyQt6.QtWidgets import QApplication

    # Check if QApplication already exists
    app = QApplication.instance()
    if app is None:
        # Create new QApplication with minimal arguments
        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)
        created_app = True
    else:
        created_app = False

    yield app

    # Cleanup: Process pending events and clean up Qt objects
    if created_app:
        # Process any remaining events
        app.processEvents()

        # Close all windows
        for widget in app.allWidgets():
            if widget.isWindow():
                widget.close()

        # Process events again to handle window closing
        app.processEvents()

        # Force garbage collection
        gc.collect()

        # Quit the application
        app.quit()


@pytest.fixture
def tka_test_helper():
    """Provide TKA AI test helper for comprehensive testing."""
    return TKAAITestHelper(use_test_mode=True)


@pytest.fixture
def test_di_container():
    """Provide test DI container with services."""
    return ApplicationFactory.create_test_app()


@pytest.fixture
def mock_graph_service():
    """Provide mock graph editor service."""
    return MockGraphEditorService()


@pytest.fixture
def mock_data_flow_service():
    """Provide mock data flow service."""
    return MockDataFlowService()


@pytest.fixture
def mock_hotkey_service():
    """Provide mock hotkey service."""
    return MockHotkeyService()


@pytest.fixture
def all_mock_services():
    """Provide all mock services for graph editor."""
    return create_all_mock_services()


@pytest.fixture
def sample_beat_data():
    """Provide sample beat data for testing."""
    return create_sample_beat_data()


@pytest.fixture
def sample_sequence_data():
    """Provide sample sequence data for testing."""
    return create_sample_sequence_data()


@pytest.fixture
def start_position_beat():
    """Provide start position beat for testing."""
    return create_start_position_beat()


@pytest.fixture
def regular_beat():
    """Provide regular beat for testing."""
    return create_regular_beat()


@pytest.fixture
def complex_beat():
    """Provide complex beat for testing."""
    return create_complex_beat()


@pytest.fixture
def basic_test_data():
    """Provide basic test data collection."""
    return GraphEditorTestData.get_basic_test_data()


@pytest.fixture
def complex_test_data():
    """Provide complex test data collection."""
    return GraphEditorTestData.get_complex_test_data()


@pytest.fixture
def edge_case_data():
    """Provide edge case test data collection."""
    return GraphEditorTestData.get_edge_case_data()


@pytest.fixture
def comprehensive_test_data():
    """Provide comprehensive test data for all scenarios."""
    return {
        **GraphEditorTestData.get_basic_test_data(),
        **GraphEditorTestData.get_complex_test_data(),
        **GraphEditorTestData.get_edge_case_data(),
    }


@pytest.fixture
def mock_parent_widget(qapp):
    """Provide mock parent widget for component testing."""
    from PyQt6.QtWidgets import QWidget

    parent = QWidget()
    parent.container = Mock()  # Mock DI container
    yield parent

    # Proper Qt widget cleanup
    parent.close()
    parent.deleteLater()
    qapp.processEvents()  # Process deletion events


@pytest.fixture
def mock_workbench(qapp, all_mock_services):
    """Provide mock workbench for integration testing."""
    from PyQt6.QtWidgets import QWidget

    workbench = Mock()
    workbench.container = Mock()

    # Configure container to return mock services
    def mock_resolve(interface):
        service_map = {
            "IGraphEditorService": all_mock_services["graph_service"],
            "IDataFlowService": all_mock_services["data_flow_service"],
            "IHotkeyService": all_mock_services["hotkey_service"],
        }
        return service_map.get(interface.__name__, Mock())

    workbench.container.resolve.side_effect = mock_resolve
    return workbench


@pytest.fixture
def signal_spy():
    """Provide signal spy utility for testing signal emissions."""

    class SignalSpy:
        def __init__(self):
            self.calls = []

        def __call__(self, *args, **kwargs):
            self.calls.append({"args": args, "kwargs": kwargs})

        def call_count(self):
            return len(self.calls)

        def was_called(self):
            return len(self.calls) > 0

        def was_called_with(self, *expected_args, **expected_kwargs):
            for call in self.calls:
                if call["args"] == expected_args and call["kwargs"] == expected_kwargs:
                    return True
            return False

        def reset(self):
            self.calls.clear()

    return SignalSpy()


@pytest.fixture
def reset_mocks():
    """Reset all mocks before each test (manual use only)."""
    yield
    # Reset after test - simplified to avoid dependency issues


# Note: pytest configuration functions are defined in the main conftest.py
# to avoid conflicts and duplication
