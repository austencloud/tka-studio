#!/usr/bin/env python3
"""
GraphEditorSignalCoordinator Unit Tests
======================================

Unit tests for the GraphEditorSignalCoordinator component testing signal
connections, data flow coordination, and component communication.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))

from tests.fixtures.graph_editor import (
    create_sample_beat_data,
    create_sample_sequence_data,
    MockDataFlowService,
    MockHotkeyService,
)


@pytest.mark.unit
class TestGraphEditorSignalCoordinatorInitialization:
    """Test SignalCoordinator initialization and setup."""

    def test_initialization(self, qapp):
        """Test SignalCoordinator initializes correctly."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Verify initial state
        assert signal_coordinator._graph_editor == mock_graph_editor
        assert signal_coordinator._data_flow_service is None
        assert signal_coordinator._hotkey_service is None
        assert signal_coordinator._layout_manager is None
        assert signal_coordinator._state_manager is None

        # Clean up
        signal_coordinator.deleteLater()

    def test_signals_exist(self, qapp):
        """Test that all required signals are defined."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Verify signals exist
        assert hasattr(signal_coordinator, "beat_modified")
        assert hasattr(signal_coordinator, "arrow_selected")
        assert hasattr(signal_coordinator, "visibility_changed")

        # Clean up
        signal_coordinator.deleteLater()


@pytest.mark.unit
class TestGraphEditorSignalCoordinatorDependencies:
    """Test dependency injection and setup."""

    def test_set_dependencies(self, qapp):
        """Test setting dependencies after initialization."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Create mock dependencies
        mock_data_flow = MockDataFlowService()
        mock_hotkey = MockHotkeyService()
        mock_layout = Mock()
        mock_state = Mock()

        # Set dependencies
        signal_coordinator.set_dependencies(
            mock_data_flow, mock_hotkey, mock_layout, mock_state
        )

        # Verify dependencies are set
        assert signal_coordinator._data_flow_service == mock_data_flow
        assert signal_coordinator._hotkey_service == mock_hotkey
        assert signal_coordinator._layout_manager == mock_layout
        assert signal_coordinator._state_manager == mock_state

        # Clean up
        signal_coordinator.deleteLater()


@pytest.mark.unit
class TestGraphEditorSignalCoordinatorDataFlowSignals:
    """Test data flow service signal handling."""

    def test_beat_data_updated_handling(self, qapp, sample_beat_data):
        """Test handling of beat data updated signals."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Create mock dependencies
        mock_data_flow = MockDataFlowService()
        mock_state = Mock()

        signal_coordinator.set_dependencies(
            mock_data_flow, Mock(), Mock(), mock_state  # hotkey  # layout
        )

        # Simulate beat data update
        signal_coordinator._on_beat_data_updated(sample_beat_data, 0)

        # Verify state manager was called
        mock_state.set_selected_beat_data.assert_called_once_with(sample_beat_data, 0)

        # Clean up
        signal_coordinator.deleteLater()

    def test_pictograph_refresh_handling(self, qapp, sample_beat_data):
        """Test handling of pictograph refresh signals."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        mock_graph_editor._pictograph_container = Mock()
        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Create mock dependencies
        mock_data_flow = MockDataFlowService()

        signal_coordinator.set_dependencies(
            mock_data_flow, Mock(), Mock(), Mock()  # hotkey  # layout  # state
        )

        # Simulate pictograph refresh
        signal_coordinator._on_pictograph_refresh_needed(sample_beat_data)

        # Verify pictograph container refresh was called
        mock_graph_editor._pictograph_container.refresh_display.assert_called_once_with(
            sample_beat_data
        )

        # Clean up
        signal_coordinator.deleteLater()

    def test_sequence_modified_handling(self, qapp):
        """Test handling of sequence modified signals."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Create mock dependencies
        mock_data_flow = MockDataFlowService()
        mock_state = Mock()
        mock_state.get_selected_beat.return_value = None  # No selected beat

        signal_coordinator.set_dependencies(
            mock_data_flow, Mock(), Mock(), mock_state  # hotkey  # layout  # state
        )

        # Simulate sequence modification
        sample_sequence = create_sample_sequence_data()
        signal_coordinator._on_sequence_modified(sample_sequence)

        # Should not raise exception
        # (This is a placeholder for future sequence handling logic)

        # Clean up
        signal_coordinator.deleteLater()


@pytest.mark.unit
class TestGraphEditorSignalCoordinatorHotkeySignals:
    """Test hotkey service signal handling."""

    def test_arrow_moved_handling(self, qapp):
        """Test handling of arrow moved signals."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Create mock dependencies
        mock_hotkey = MockHotkeyService()

        signal_coordinator.set_dependencies(
            Mock(), mock_hotkey, Mock(), Mock()  # data_flow  # layout  # state
        )

        # Simulate arrow movement
        signal_coordinator._on_arrow_moved("blue", 10, 20)

        # Should not raise exception
        # (This is a placeholder for future arrow movement handling)

        # Clean up
        signal_coordinator.deleteLater()

    def test_rotation_override_handling(self, qapp):
        """Test handling of rotation override signals."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Create mock dependencies
        mock_hotkey = MockHotkeyService()

        signal_coordinator.set_dependencies(
            Mock(), mock_hotkey, Mock(), Mock()  # data_flow  # layout  # state
        )

        # Simulate rotation override
        signal_coordinator._on_rotation_override("blue")

        # Should not raise exception
        # (This is a placeholder for future rotation handling)

        # Clean up
        signal_coordinator.deleteLater()


@pytest.mark.unit
class TestGraphEditorSignalCoordinatorUISignals:
    """Test UI component signal handling."""

    def test_beat_modified_emission(self, qapp, signal_spy, sample_beat_data):
        """Test beat modified signal emission."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Connect signal spy
        signal_coordinator.beat_modified.connect(signal_spy)

        # Emit beat modified signal
        signal_coordinator.emit_beat_modified(sample_beat_data)

        # Verify signal was emitted
        assert signal_spy.was_called_with(sample_beat_data)

        # Clean up
        signal_coordinator.deleteLater()

    def test_arrow_selected_emission(self, qapp, signal_spy):
        """Test arrow selected signal emission."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Connect signal spy
        signal_coordinator.arrow_selected.connect(signal_spy)

        # Emit arrow selected signal
        signal_coordinator.emit_arrow_selected("blue")

        # Verify signal was emitted
        assert signal_spy.was_called_with("blue")

        # Clean up
        signal_coordinator.deleteLater()

    def test_visibility_changed_emission(self, qapp, signal_spy):
        """Test visibility changed signal emission."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Connect signal spy
        signal_coordinator.visibility_changed.connect(signal_spy)

        # Emit visibility changed signal
        signal_coordinator.emit_visibility_changed(True)

        # Verify signal was emitted
        assert signal_spy.was_called_with(True)

        # Clean up
        signal_coordinator.deleteLater()


@pytest.mark.unit
class TestGraphEditorSignalCoordinatorUtilities:
    """Test utility methods."""

    def test_reconnect_ui_component_signals(self, qapp):
        """Test reconnecting UI component signals."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Should not raise exception
        signal_coordinator.reconnect_ui_component_signals()

        # Clean up
        signal_coordinator.deleteLater()

    def test_refresh_display(self, qapp):
        """Test display refresh functionality."""
        from presentation.components.graph_editor.managers.signal_coordinator import (
            GraphEditorSignalCoordinator,
        )

        mock_graph_editor = Mock()
        mock_graph_editor._graph_service = Mock()
        mock_graph_editor._graph_service.get_selected_beat.return_value = None

        signal_coordinator = GraphEditorSignalCoordinator(mock_graph_editor)

        # Create mock state manager
        mock_state = Mock()
        mock_state.get_selected_beat.return_value = None

        signal_coordinator.set_dependencies(
            Mock(), Mock(), Mock(), mock_state  # data_flow  # hotkey  # layout
        )

        # Should not raise exception
        signal_coordinator._refresh_display()

        # Clean up
        signal_coordinator.deleteLater()
