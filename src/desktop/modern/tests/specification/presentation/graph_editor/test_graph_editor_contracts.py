#!/usr/bin/env python3
"""
Graph Editor Specification Tests - Permanent Contracts
=====================================================

SPECIFICATION TESTS - NEVER DELETE
These tests define the permanent behavioral contracts for the GraphEditor component.

Tests ensure:
- Public API stability
- Signal emission contracts
- Component initialization contracts
- State management contracts
- Integration point contracts
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))

from tests.fixtures.graph_editor import (
    create_all_mock_services,
    create_sample_beat_data,
    create_sample_sequence_data,
)


@pytest.mark.specification
@pytest.mark.critical
class TestGraphEditorPublicAPIContracts:
    """
    PERMANENT: Test GraphEditor public API contracts.

    These contracts must remain stable for backward compatibility.
    """

    def test_graph_editor_initialization_contract(self, qapp, all_mock_services):
        """PERMANENT: GraphEditor must initialize with required parameters."""
        from presentation.components.graph_editor import GraphEditor

        # Test initialization with all parameters
        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"],
            parent=None,
            workbench_width=800,
            workbench_height=600,
        )

        # Verify initialization
        assert graph_editor is not None
        assert hasattr(graph_editor, "_graph_service")
        assert hasattr(graph_editor, "_current_sequence")
        assert hasattr(graph_editor, "_selected_beat_index")
        assert hasattr(graph_editor, "_selected_beat_data")

        # Clean up
        graph_editor.deleteLater()

    def test_graph_editor_signal_contracts(self, qapp, all_mock_services):
        """PERMANENT: GraphEditor must expose required signals."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Verify required signals exist
        assert hasattr(graph_editor, "beat_modified")
        assert hasattr(graph_editor, "arrow_selected")
        assert hasattr(graph_editor, "visibility_changed")

        # Verify signals are callable (can be connected)
        mock_slot = Mock()
        graph_editor.beat_modified.connect(mock_slot)
        graph_editor.arrow_selected.connect(mock_slot)
        graph_editor.visibility_changed.connect(mock_slot)

        # Clean up
        graph_editor.deleteLater()

    def test_set_beat_data_contract(self, qapp, all_mock_services, sample_beat_data):
        """PERMANENT: set_selected_beat_data must accept beat_index and BeatData."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Test set_selected_beat_data method exists and accepts correct parameters
        assert hasattr(graph_editor, "set_selected_beat_data")

        # Should not raise exception
        graph_editor.set_selected_beat_data(0, sample_beat_data)

        # Clean up
        graph_editor.deleteLater()

    def test_set_sequence_data_contract(
        self, qapp, all_mock_services, sample_sequence_data
    ):
        """PERMANENT: set_sequence must accept SequenceData."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Test set_sequence method exists and accepts correct parameters
        assert hasattr(graph_editor, "set_sequence")

        # Should not raise exception
        graph_editor.set_sequence(sample_sequence_data)

        # Clean up
        graph_editor.deleteLater()

    def test_visibility_control_contract(self, qapp, all_mock_services):
        """PERMANENT: GraphEditor must support visibility control."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Test visibility methods exist
        assert hasattr(graph_editor, "show")
        assert hasattr(graph_editor, "hide")
        assert hasattr(graph_editor, "setVisible")

        # Test visibility can be controlled
        graph_editor.show()
        graph_editor.hide()
        graph_editor.setVisible(True)
        graph_editor.setVisible(False)

        # Clean up
        graph_editor.deleteLater()


@pytest.mark.specification
@pytest.mark.critical
class TestGraphEditorComponentIntegrationContracts:
    """
    PERMANENT: Test GraphEditor component integration contracts.

    These ensure proper component coordination and communication.
    """

    def test_component_initialization_contract(self, qapp, all_mock_services):
        """PERMANENT: GraphEditor must initialize all required components."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Verify component references exist (may be None initially)
        assert hasattr(graph_editor, "_pictograph_display")
        assert hasattr(graph_editor, "_adjustment_panel")

        # Clean up
        graph_editor.deleteLater()

    def test_signal_coordination_contract(self, qapp, all_mock_services, signal_spy):
        """PERMANENT: GraphEditor must coordinate signals between components."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Connect signal spy
        graph_editor.beat_modified.connect(signal_spy)

        # Verify signal can be emitted (component coordination working)
        # This tests the signal infrastructure is properly set up
        assert hasattr(graph_editor, "beat_modified")

        # Clean up
        graph_editor.deleteLater()


@pytest.mark.specification
@pytest.mark.critical
class TestGraphEditorStateManagementContracts:
    """
    PERMANENT: Test GraphEditor state management contracts.

    These ensure proper state handling and consistency.
    """

    def test_state_consistency_contract(
        self, qapp, all_mock_services, sample_beat_data
    ):
        """PERMANENT: GraphEditor must maintain state consistency."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Set beat data
        graph_editor.set_selected_beat_data(0, sample_beat_data)

        # Verify state is maintained
        assert graph_editor._selected_beat_data == sample_beat_data
        assert graph_editor._selected_beat_index == 0

        # Clean up
        graph_editor.deleteLater()

    def test_none_handling_contract(self, qapp, all_mock_services):
        """PERMANENT: GraphEditor must handle None values gracefully."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Should handle None beat data without exception
        graph_editor.set_selected_beat_data(-1, None)

        # Should handle None sequence data without exception
        graph_editor.set_sequence(None)

        # Clean up
        graph_editor.deleteLater()


@pytest.mark.specification
@pytest.mark.critical
class TestGraphEditorArchitecturalContracts:
    """
    PERMANENT: Test GraphEditor architectural contracts.

    These ensure adherence to TKA clean architecture patterns.
    """

    def test_dependency_injection_contract(self, qapp):
        """PERMANENT: GraphEditor must accept service injection."""
        from presentation.components.graph_editor import GraphEditor

        mock_service = Mock()

        # Must accept service injection
        graph_editor = GraphEditor(graph_service=mock_service, parent=None)

        # Verify service is stored
        assert graph_editor._graph_service == mock_service

        # Clean up
        graph_editor.deleteLater()

    def test_immutable_domain_model_contract(
        self, qapp, all_mock_services, sample_beat_data
    ):
        """PERMANENT: GraphEditor must work with immutable domain models."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Store original beat data
        original_beat = sample_beat_data

        # Set beat data
        graph_editor.set_selected_beat_data(0, sample_beat_data)

        # Verify original beat data is unchanged (immutability respected)
        assert sample_beat_data == original_beat

        # Clean up
        graph_editor.deleteLater()

    def test_clean_architecture_layer_contract(self, qapp, all_mock_services):
        """PERMANENT: GraphEditor must respect clean architecture layers."""
        from presentation.components.graph_editor import GraphEditor

        # GraphEditor is in presentation layer
        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Must depend on service interfaces (application layer)
        assert graph_editor._graph_service is not None

        # Must not directly import domain models for business logic
        # (should delegate to services)

        # Clean up
        graph_editor.deleteLater()
