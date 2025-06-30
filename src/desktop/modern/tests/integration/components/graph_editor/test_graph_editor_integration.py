#!/usr/bin/env python3
"""
GraphEditor Integration Tests
============================

Integration tests for the complete GraphEditor component testing component
interactions, signal flow, and end-to-end workflows.
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
    create_start_position_beat,
    create_regular_beat,
)


@pytest.mark.integration
class TestGraphEditorComponentIntegration:
    """Test integration between GraphEditor components."""

    def test_complete_initialization_workflow(self, qapp, all_mock_services):
        """Test complete GraphEditor initialization with all components."""
        from presentation.components.graph_editor import GraphEditor

        # Create GraphEditor with mock services
        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"],
            parent=None,
            workbench_width=800,
            workbench_height=600,
        )

        # Verify initialization completed
        assert graph_editor is not None
        assert graph_editor._graph_service is not None

        # Verify component references exist (may be None initially)
        assert hasattr(graph_editor, "_pictograph_display")
        assert hasattr(graph_editor, "_adjustment_panel")

        # Clean up
        graph_editor.deleteLater()

    def test_beat_data_flow_integration(
        self, qapp, all_mock_services, sample_beat_data, signal_spy
    ):
        """Test beat data flow through all components."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Connect to beat modified signal
        graph_editor.beat_modified.connect(signal_spy)

        # Set beat data
        graph_editor.set_selected_beat_data(0, sample_beat_data)

        # Verify state was updated
        assert graph_editor._selected_beat_data == sample_beat_data
        assert graph_editor._selected_beat_index == 0

        # Clean up
        graph_editor.deleteLater()

    def test_sequence_data_flow_integration(
        self, qapp, all_mock_services, sample_sequence_data
    ):
        """Test sequence data flow through all components."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Set sequence data
        graph_editor.set_sequence(sample_sequence_data)

        # Verify state was updated
        assert graph_editor._current_sequence == sample_sequence_data

        # Clean up
        graph_editor.deleteLater()

    def test_visibility_state_integration(self, qapp, all_mock_services, signal_spy):
        """Test visibility state changes through all components."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Connect to visibility changed signal
        graph_editor.visibility_changed.connect(signal_spy)

        # Test show/hide
        graph_editor.show()
        graph_editor.hide()

        # Should not raise exceptions

        # Clean up
        graph_editor.deleteLater()


@pytest.mark.integration
class TestGraphEditorServiceIntegration:
    """Test integration with graph editor services."""

    def test_graph_service_integration(self, qapp, all_mock_services, sample_beat_data):
        """Test integration with graph editor service."""
        from presentation.components.graph_editor import GraphEditor

        mock_service = all_mock_services["graph_service"]

        graph_editor = GraphEditor(graph_service=mock_service, parent=None)

        # Set beat data (should interact with service)
        graph_editor.set_selected_beat_data(0, sample_beat_data)

        # Verify service interaction
        assert graph_editor._graph_service == mock_service

        # Clean up
        graph_editor.deleteLater()

    def test_service_method_delegation(self, qapp, all_mock_services):
        """Test that GraphEditor properly delegates to services."""
        from presentation.components.graph_editor import GraphEditor

        mock_service = all_mock_services["graph_service"]

        graph_editor = GraphEditor(graph_service=mock_service, parent=None)

        # Verify service is available for delegation
        assert graph_editor._graph_service is not None

        # Clean up
        graph_editor.deleteLater()


@pytest.mark.integration
class TestGraphEditorSignalFlowIntegration:
    """Test signal flow integration across components."""

    def test_beat_modification_signal_flow(
        self, qapp, all_mock_services, sample_beat_data, signal_spy
    ):
        """Test beat modification signal flow through components."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Connect signal spy
        graph_editor.beat_modified.connect(signal_spy)

        # Simulate beat modification (would normally come from UI components)
        # For now, just verify signal infrastructure exists
        assert hasattr(graph_editor, "beat_modified")

        # Clean up
        graph_editor.deleteLater()

    def test_arrow_selection_signal_flow(self, qapp, all_mock_services, signal_spy):
        """Test arrow selection signal flow through components."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Connect signal spy
        graph_editor.arrow_selected.connect(signal_spy)

        # Verify signal infrastructure exists
        assert hasattr(graph_editor, "arrow_selected")

        # Clean up
        graph_editor.deleteLater()


@pytest.mark.integration
class TestGraphEditorErrorHandling:
    """Test error handling in integrated scenarios."""

    def test_none_beat_data_handling(self, qapp, all_mock_services):
        """Test handling of None beat data across components."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Should handle None beat data gracefully (signal signature now fixed)
        graph_editor.set_selected_beat_data(-1, None)

        # Verify state
        assert graph_editor._selected_beat_data is None
        assert graph_editor._selected_beat_index == -1

        # Clean up
        graph_editor.deleteLater()

    def test_none_sequence_data_handling(self, qapp, all_mock_services):
        """Test handling of None sequence data across components."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Should handle None sequence data gracefully
        graph_editor.set_sequence(None)

        # Verify state
        assert graph_editor._current_sequence is None

        # Clean up
        graph_editor.deleteLater()

    def test_invalid_beat_index_handling(
        self, qapp, all_mock_services, sample_beat_data
    ):
        """Test handling of invalid beat indices."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Should handle invalid indices gracefully
        graph_editor.set_selected_beat_data(-1, sample_beat_data)
        graph_editor.set_selected_beat_data(999, sample_beat_data)

        # Should not raise exceptions

        # Clean up
        graph_editor.deleteLater()


@pytest.mark.integration
class TestGraphEditorStateConsistency:
    """Test state consistency across component interactions."""

    def test_beat_and_sequence_consistency(
        self, qapp, all_mock_services, sample_sequence_data
    ):
        """Test consistency between beat and sequence state."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Set sequence first
        graph_editor.set_sequence(sample_sequence_data)

        # Set beat from sequence
        if sample_sequence_data.beats:
            first_beat = sample_sequence_data.beats[0]
            graph_editor.set_selected_beat_data(0, first_beat)

            # Verify consistency
            assert graph_editor._current_sequence == sample_sequence_data
            assert graph_editor._selected_beat_data == first_beat
            assert graph_editor._selected_beat_index == 0

        # Clean up
        graph_editor.deleteLater()

    def test_state_reset_consistency(
        self, qapp, all_mock_services, sample_beat_data, sample_sequence_data
    ):
        """Test state consistency after reset operations."""
        from presentation.components.graph_editor import GraphEditor

        graph_editor = GraphEditor(
            graph_service=all_mock_services["graph_service"], parent=None
        )

        # Set initial state
        graph_editor.set_sequence(sample_sequence_data)
        graph_editor.set_selected_beat_data(0, sample_beat_data)

        # Reset with None values
        graph_editor.set_sequence(None)
        graph_editor.set_selected_beat_data(-1, None)  # Signal signature now fixed

        # Verify consistent reset state
        assert graph_editor._current_sequence is None
        assert graph_editor._selected_beat_data is None
        assert graph_editor._selected_beat_index == -1

        # Clean up
        graph_editor.deleteLater()
