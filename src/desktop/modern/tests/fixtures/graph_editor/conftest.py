#!/usr/bin/env python3
"""
Graph Editor Test Configuration
==============================

Provides pytest fixtures and configuration for graph editor testing.
Follows TKA testing protocols and architectural patterns.
"""
from __future__ import annotations

from pathlib import Path
import sys
from unittest.mock import Mock

import pytest


# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))

# Import TKA testing infrastructure
from core.application.application_factory import ApplicationFactory
from core.testing.ai_agent_helpers import TKAAITestHelper

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


@pytest.fixture
def qapp():
    """Create QApplication for Qt tests."""
    from PyQt6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app
    # Don't quit the app as it might be used by other tests


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
    parent.deleteLater()


@pytest.fixture
def mock_workbench(qapp, all_mock_services):
    """Provide mock workbench for integration testing."""

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


@pytest.fixture(autouse=True)
def reset_mocks(all_mock_services):
    """Auto-reset all mocks before each test."""
    yield
    # Reset after test
    for service in all_mock_services.values():
        if hasattr(service, "reset_calls"):
            service.reset_calls()


# Note: pytest configuration functions are defined in the main conftest.py
# to avoid conflicts and duplication
