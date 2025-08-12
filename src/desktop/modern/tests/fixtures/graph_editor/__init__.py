"""
Graph Editor Test Fixtures Package
=================================

Provides comprehensive fixtures and mock services for testing graph editor components.

Available fixtures:
- mock_services: Mock implementations of graph editor services
- mock_beat_data: Sample beat and sequence data for testing

Usage:
    from tests.fixtures.graph_editor import create_all_mock_services
    from tests.fixtures.graph_editor.mock_beat_data import create_sample_beat_data
"""

from .mock_services import (
    MockGraphEditorService,
    MockDataFlowService,
    MockHotkeyService,
    create_mock_graph_editor_service,
    create_mock_data_flow_service,
    create_mock_hotkey_service,
    create_all_mock_services,
)

from .mock_beat_data import (
    create_sample_beat_data,
    create_sample_sequence_data,
    create_start_position_beat,
    create_regular_beat,
    create_complex_beat,
    create_empty_sequence,
    GraphEditorTestData,
    pytest_sample_beat_data,
    pytest_sample_sequence_data,
    pytest_graph_editor_test_data,
)

__all__ = [
    # Mock services
    "MockGraphEditorService",
    "MockDataFlowService", 
    "MockHotkeyService",
    "create_mock_graph_editor_service",
    "create_mock_data_flow_service",
    "create_mock_hotkey_service",
    "create_all_mock_services",
    # Mock data
    "create_sample_beat_data",
    "create_sample_sequence_data",
    "create_start_position_beat",
    "create_regular_beat",
    "create_complex_beat",
    "create_empty_sequence",
    "GraphEditorTestData",
    "pytest_sample_beat_data",
    "pytest_sample_sequence_data",
    "pytest_graph_editor_test_data",
]
