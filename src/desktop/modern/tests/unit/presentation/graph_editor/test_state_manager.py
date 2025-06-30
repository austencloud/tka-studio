#!/usr/bin/env python3
"""
GraphEditorStateManager Unit Tests
=================================

Unit tests for the GraphEditorStateManager component testing state management,
validation, and signal emission in isolation.
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
    create_start_position_beat,
    create_regular_beat,
)


@pytest.mark.unit
class TestGraphEditorStateManagerInitialization:
    """Test StateManager initialization and setup."""

    def test_initialization(self, qapp):
        """Test StateManager initializes with correct default state."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Verify initial state
        assert state_manager._is_visible is False
        assert state_manager._current_sequence is None
        assert state_manager._selected_beat is None
        assert state_manager._selected_beat_index is None
        assert state_manager._selected_arrow_id is None
        assert state_manager._state_consistent is True
        assert state_manager._last_validation_error is None

        # Clean up
        state_manager.deleteLater()

    def test_signals_exist(self, qapp):
        """Test that all required signals are defined."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Verify signals exist
        assert hasattr(state_manager, "visibility_changed")
        assert hasattr(state_manager, "sequence_changed")
        assert hasattr(state_manager, "selected_beat_changed")
        assert hasattr(state_manager, "selected_arrow_changed")

        # Clean up
        state_manager.deleteLater()


@pytest.mark.unit
class TestGraphEditorStateManagerVisibility:
    """Test visibility state management."""

    def test_set_visibility_true(self, qapp, signal_spy):
        """Test setting visibility to True."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)
        state_manager.visibility_changed.connect(signal_spy)

        # Set visibility to True
        state_manager.set_visibility(True)

        # Verify state and signal
        assert state_manager.is_visible() is True
        assert signal_spy.was_called_with(True)

        # Clean up
        state_manager.deleteLater()

    def test_set_visibility_false(self, qapp, signal_spy):
        """Test setting visibility to False."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)
        state_manager.visibility_changed.connect(signal_spy)

        # Set visibility to True first, then False to trigger signal
        state_manager.set_visibility(
            True, emit_signal=False
        )  # Set initial state without signal
        signal_spy.reset()  # Clear any previous calls

        # Set visibility to False
        state_manager.set_visibility(False)

        # Verify state and signal
        assert state_manager.is_visible() is False
        assert signal_spy.was_called_with(False)

        # Clean up
        state_manager.deleteLater()

    def test_set_visibility_no_signal(self, qapp, signal_spy):
        """Test setting visibility without emitting signal."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)
        state_manager.visibility_changed.connect(signal_spy)

        # Set visibility without signal
        state_manager.set_visibility(True, emit_signal=False)

        # Verify state changed but no signal
        assert state_manager.is_visible() is True
        assert not signal_spy.was_called()

        # Clean up
        state_manager.deleteLater()


@pytest.mark.unit
class TestGraphEditorStateManagerSequence:
    """Test sequence state management."""

    def test_set_sequence_data(self, qapp, signal_spy, sample_sequence_data):
        """Test setting sequence data."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)
        state_manager.sequence_changed.connect(signal_spy)

        # Set sequence data
        state_manager.set_current_sequence(sample_sequence_data)

        # Verify state and signal
        assert state_manager.get_current_sequence() == sample_sequence_data
        assert state_manager.has_sequence() is True
        assert signal_spy.was_called_with(sample_sequence_data)

        # Clean up
        state_manager.deleteLater()

    def test_set_sequence_data_none(self, qapp, signal_spy, sample_sequence_data):
        """Test setting sequence data to None."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)
        state_manager.sequence_changed.connect(signal_spy)

        # Set sequence data first, then None to trigger signal
        state_manager.set_current_sequence(sample_sequence_data, emit_signal=False)
        signal_spy.reset()

        # Set sequence data to None
        state_manager.set_current_sequence(None)

        # Verify state and signal
        assert state_manager.get_current_sequence() is None
        assert state_manager.has_sequence() is False
        assert signal_spy.was_called_with(None)

        # Clean up
        state_manager.deleteLater()


@pytest.mark.unit
class TestGraphEditorStateManagerBeat:
    """Test beat state management."""

    def test_set_selected_beat_data(
        self, qapp, signal_spy, sample_beat_data, sample_sequence_data
    ):
        """Test setting selected beat data."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)
        state_manager.selected_beat_changed.connect(signal_spy)

        # Set sequence first to provide valid context for beat index
        state_manager.set_current_sequence(sample_sequence_data, emit_signal=False)
        signal_spy.reset()

        # Set selected beat data
        state_manager.set_selected_beat_data(sample_beat_data, 0)

        # Verify state and signal
        assert state_manager.get_selected_beat() == sample_beat_data
        assert state_manager.get_selected_beat_index() == 0
        assert state_manager.has_selected_beat() is True
        assert signal_spy.was_called()  # Signal was emitted

        # Clean up
        state_manager.deleteLater()

    def test_set_selected_beat_data_none(self, qapp, signal_spy):
        """Test setting selected beat data to None."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)
        state_manager.selected_beat_changed.connect(signal_spy)

        # Set selected beat data to None (with valid None index)
        state_manager.set_selected_beat_data(None, None)

        # Verify state - signal may not be emitted if state doesn't change
        assert state_manager.get_selected_beat() is None
        assert state_manager.get_selected_beat_index() is None
        assert state_manager.has_selected_beat() is False
        # Note: Signal may not be emitted if state doesn't change from initial None state

        # Clean up
        state_manager.deleteLater()


@pytest.mark.unit
class TestGraphEditorStateManagerArrow:
    """Test arrow state management."""

    def test_set_selected_arrow_id(self, qapp, signal_spy):
        """Test setting selected arrow ID."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)
        state_manager.selected_arrow_changed.connect(signal_spy)

        # Set selected arrow ID
        state_manager.set_selected_arrow_id("blue")

        # Verify state and signal
        assert state_manager.get_selected_arrow_id() == "blue"
        assert state_manager.has_selected_arrow() is True
        assert signal_spy.was_called_with("blue")

        # Clean up
        state_manager.deleteLater()

    def test_set_selected_arrow_id_none(self, qapp, signal_spy):
        """Test setting selected arrow ID to None."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)
        state_manager.selected_arrow_changed.connect(signal_spy)

        # Set arrow ID first, then None (Note: None doesn't emit signal in StateManager)
        state_manager.set_selected_arrow_id("blue", emit_signal=False)
        signal_spy.reset()

        # Set selected arrow ID to None
        state_manager.set_selected_arrow_id(None)

        # Verify state (Note: signal is NOT emitted for None values)
        assert state_manager.get_selected_arrow_id() is None
        assert state_manager.has_selected_arrow() is False
        assert not signal_spy.was_called()  # No signal emitted for None

        # Clean up
        state_manager.deleteLater()


@pytest.mark.unit
class TestGraphEditorStateManagerValidation:
    """Test state validation functionality."""

    def test_state_validation_consistent(
        self, qapp, sample_beat_data, sample_sequence_data
    ):
        """Test state validation with consistent state."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Set consistent state
        state_manager.set_current_sequence(sample_sequence_data)
        state_manager.set_selected_beat_data(sample_beat_data, 0)

        # Validate state
        is_valid = state_manager.force_state_validation()

        # Verify validation passes
        assert is_valid is True
        assert state_manager.is_state_consistent() is True

        # Clean up
        state_manager.deleteLater()

    def test_get_state_summary(self, qapp, sample_beat_data, sample_sequence_data):
        """Test getting state summary."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Set state
        state_manager.set_visibility(True)
        state_manager.set_current_sequence(sample_sequence_data)
        state_manager.set_selected_beat_data(sample_beat_data, 0)
        state_manager.set_selected_arrow_id("blue")

        # Get state summary
        summary = state_manager.get_state_summary()

        # Verify summary
        assert summary["is_visible"] is True
        assert summary["has_sequence"] is True
        assert summary["has_selected_beat"] is True
        assert summary["selected_beat_index"] == 0
        assert summary["has_selected_arrow"] is True
        assert summary["selected_arrow_id"] == "blue"
        assert summary["state_consistent"] is True

        # Clean up
        state_manager.deleteLater()

    def test_reset_all_state(
        self, qapp, signal_spy, sample_beat_data, sample_sequence_data
    ):
        """Test resetting all state."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Connect signals
        state_manager.visibility_changed.connect(signal_spy)
        state_manager.sequence_changed.connect(signal_spy)
        state_manager.selected_beat_changed.connect(signal_spy)

        # Set some state
        state_manager.set_visibility(True)
        state_manager.set_current_sequence(sample_sequence_data)
        state_manager.set_selected_beat_data(sample_beat_data, 0)

        # Reset spy
        signal_spy.reset()

        # Reset all state
        state_manager.reset_all_state()

        # Verify state is reset
        assert state_manager.is_visible() is False
        assert state_manager.get_current_sequence() is None
        assert state_manager.get_selected_beat() is None
        assert state_manager.get_selected_beat_index() is None  # Reset sets to None
        assert state_manager.get_selected_arrow_id() is None

        # Verify signals were emitted
        assert (
            signal_spy.call_count() >= 3
        )  # At least visibility, sequence, beat signals

        # Clean up
        state_manager.deleteLater()
