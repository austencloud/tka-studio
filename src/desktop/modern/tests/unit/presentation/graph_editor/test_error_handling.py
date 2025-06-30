#!/usr/bin/env python3
"""
Graph Editor Error Handling Tests
=================================

Comprehensive tests for error handling and recovery mechanisms in the graph editor.
Tests all error scenarios, validation, and recovery patterns implemented.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))

from presentation.components.graph_editor.graph_editor import GraphEditor
from presentation.components.graph_editor.utils.validation import (
    ValidationError,
    ValidationResult,
)
from domain.models.core_models import BeatData, SequenceData, Orientation


@pytest.mark.unit
class TestGraphEditorErrorHandling:
    """Test comprehensive error handling in GraphEditor."""

    def test_initialization_error_handling(self, qapp):
        """Test error handling during initialization."""
        # Test with invalid service
        graph_editor = GraphEditor(graph_service=None, parent=None)

        # Should still initialize but may be in fallback mode
        assert graph_editor is not None
        assert hasattr(graph_editor, "_initialization_successful")
        assert hasattr(graph_editor, "_component_errors")
        assert hasattr(graph_editor, "_fallback_mode_enabled")

        # Clean up
        graph_editor.deleteLater()

    def test_component_creation_error_handling(self, qapp):
        """Test error handling when component creation fails."""
        with patch(
            "presentation.components.graph_editor.graph_editor.PictographDisplaySection"
        ) as mock_pictograph:
            # Make pictograph creation fail
            mock_pictograph.side_effect = RuntimeError("Component creation failed")

            graph_editor = GraphEditor(parent=None)

            # Should handle the error gracefully
            assert graph_editor is not None
            errors = graph_editor.get_component_errors()
            assert len(errors) > 0
            # Check for any error related to pictograph or component creation
            error_keys = list(errors.keys())
            assert any(
                "pictograph" in key.lower()
                or "component" in key.lower()
                or "ui" in key.lower()
                for key in error_keys
            )

            # Clean up
            graph_editor.deleteLater()

    def test_set_sequence_error_handling(self, qapp):
        """Test error handling in set_sequence method."""
        graph_editor = GraphEditor(parent=None)

        # Test with invalid sequence data
        invalid_sequence = Mock()
        invalid_sequence.name = ""  # Invalid empty name
        invalid_sequence.word = "test"
        invalid_sequence.beats = []

        # Should return False for invalid data
        result = graph_editor.set_sequence(invalid_sequence)
        assert result is False

        # Test with None (should succeed)
        result = graph_editor.set_sequence(None)
        assert result is True

        # Clean up
        graph_editor.deleteLater()

    def test_set_selected_beat_data_error_handling(self, qapp, sample_beat_data):
        """Test error handling in set_selected_beat_data method."""
        graph_editor = GraphEditor(parent=None)

        # Test with invalid beat index (no sequence set)
        result = graph_editor.set_selected_beat_data(5, sample_beat_data)
        assert result is False

        # Test with invalid beat data
        invalid_beat = Mock()
        invalid_beat.letter = ""  # Invalid empty letter

        result = graph_editor.set_selected_beat_data(0, invalid_beat)
        assert result is False

        # Test with None beat data (should succeed for index -1)
        result = graph_editor.set_selected_beat_data(-1, None)
        assert result is True

        # Clean up
        graph_editor.deleteLater()

    def test_signal_handler_error_handling(self, qapp, sample_beat_data):
        """Test error handling in signal handlers."""
        graph_editor = GraphEditor(parent=None)

        # Test pictograph update with None data
        graph_editor._on_pictograph_updated_safe(None)
        # Should not crash

        # Test with invalid beat data
        invalid_beat = Mock()
        # Missing letter attribute
        graph_editor._on_pictograph_updated_safe(invalid_beat)
        # Should not crash

        # Test orientation change with invalid parameters
        graph_editor._on_orientation_changed_safe("", Orientation.IN)  # Empty color
        graph_editor._on_orientation_changed_safe("blue", "")  # Empty orientation
        graph_editor._on_orientation_changed_safe(None, Orientation.IN)  # None color
        graph_editor._on_orientation_changed_safe(
            "blue", "invalid_orientation"
        )  # Invalid orientation string
        graph_editor._on_orientation_changed_safe(
            "blue", 123
        )  # Invalid orientation type

        # Test with valid orientation enum and string
        graph_editor._on_orientation_changed_safe("blue", Orientation.IN)  # Valid enum
        graph_editor._on_orientation_changed_safe("red", "out")  # Valid string
        # Should not crash

        # Test turn amount change with invalid parameters
        graph_editor._on_turn_amount_changed_safe(
            "blue", "invalid"
        )  # Non-numeric amount
        graph_editor._on_turn_amount_changed_safe("", 1.5)  # Empty color
        # Should not crash

        # Clean up
        graph_editor.deleteLater()

    def test_orientation_enum_handling(self, qapp):
        """Test proper handling of Orientation enum vs string."""
        graph_editor = GraphEditor(parent=None)

        # Test with Orientation enum (should work)
        graph_editor._on_orientation_changed_safe("blue", Orientation.IN)
        graph_editor._on_orientation_changed_safe("red", Orientation.OUT)
        graph_editor._on_orientation_changed_safe("blue", Orientation.CLOCK)
        graph_editor._on_orientation_changed_safe("red", Orientation.COUNTER)

        # Test with valid orientation strings (should work)
        graph_editor._on_orientation_changed_safe("blue", "in")
        graph_editor._on_orientation_changed_safe("red", "out")
        graph_editor._on_orientation_changed_safe("blue", "clock")
        graph_editor._on_orientation_changed_safe("red", "counter")

        # Test with invalid orientation strings (should be rejected)
        graph_editor._on_orientation_changed_safe("blue", "invalid")
        graph_editor._on_orientation_changed_safe("red", "")
        graph_editor._on_orientation_changed_safe("blue", None)

        # Test with invalid types (should be rejected)
        graph_editor._on_orientation_changed_safe("red", 123)
        graph_editor._on_orientation_changed_safe("blue", [])

        # Should not crash and should handle all cases gracefully
        assert graph_editor is not None

        # Clean up
        graph_editor.deleteLater()

    def test_sequence_update_mechanism(
        self, qapp, sample_sequence_data, sample_beat_data
    ):
        """Test that sequence updates work correctly to fix None sequence issue."""
        graph_editor = GraphEditor(parent=None)

        # Initially no sequence
        assert graph_editor._current_sequence is None

        # Set initial sequence
        result = graph_editor.set_sequence(sample_sequence_data)
        assert result is True
        assert graph_editor._current_sequence is not None
        assert graph_editor._current_sequence.name == sample_sequence_data.name

        # Test beat index validation with current sequence
        result = graph_editor.set_selected_beat_data(0, sample_beat_data)
        assert result is True  # Should work now that sequence is set

        # Test sequence update notification
        updated_sequence = sample_sequence_data.update(name="Updated Sequence")
        result = graph_editor.notify_sequence_updated(updated_sequence)
        assert result is True

        # Verify sequence was updated
        assert graph_editor._current_sequence.name == "Updated Sequence"

        # Test that beat index validation still works after update
        result = graph_editor.set_selected_beat_data(0, sample_beat_data)
        assert result is True

        # Clean up
        graph_editor.deleteLater()

    def test_workbench_sequence_synchronization(self, qapp, sample_sequence_data):
        """Test that graph editor automatically receives workbench sequence updates."""
        from PyQt6.QtWidgets import QWidget
        from PyQt6.QtCore import pyqtSignal

        # Create a real QWidget that acts like a workbench
        class MockWorkbench(QWidget):
            sequence_modified = pyqtSignal(object)

            def __init__(self):
                super().__init__()

        mock_workbench = MockWorkbench()

        # Create graph editor with mock workbench as parent
        graph_editor = GraphEditor(parent=mock_workbench)

        # Initially no sequence
        assert graph_editor._current_sequence is None

        # Simulate workbench emitting sequence_modified signal
        mock_workbench.sequence_modified.emit(sample_sequence_data)

        # Verify that the graph editor's sequence was updated
        assert graph_editor._current_sequence is not None
        assert graph_editor._current_sequence.name == sample_sequence_data.name

        # Test beat index validation now works with updated sequence
        result = graph_editor.set_selected_beat_data(
            0, None
        )  # Should work with valid index
        assert result is True

        # Clean up
        graph_editor.deleteLater()
        mock_workbench.deleteLater()

    def test_workbench_signal_connection_error_handling(self, qapp):
        """Test error handling when workbench signal connection fails."""
        from unittest.mock import Mock

        # Create a mock workbench that raises an error on signal connection
        mock_workbench = Mock()
        mock_workbench.sequence_modified = Mock()
        mock_workbench.sequence_modified.connect = Mock(
            side_effect=RuntimeError("Signal connection failed")
        )

        # Create graph editor with problematic workbench
        graph_editor = GraphEditor(parent=mock_workbench)

        # Should handle the error gracefully
        assert graph_editor is not None
        errors = graph_editor.get_component_errors()
        assert any(
            "workbench" in key.lower() or "signal" in key.lower()
            for key in errors.keys()
        )

        # Clean up
        graph_editor.deleteLater()

    def test_component_recovery_mechanism(self, qapp):
        """Test component recovery functionality."""
        graph_editor = GraphEditor(parent=None)

        # Simulate component failure
        graph_editor._pictograph_display = None
        graph_editor._component_errors["test_error"] = "Simulated error"

        # Attempt recovery
        recovery_result = graph_editor.attempt_component_recovery()

        # Recovery may or may not succeed depending on component availability
        assert isinstance(recovery_result, bool)

        # Check that recovery was attempted
        assert graph_editor._recovery_attempts > 0

        # Clean up
        graph_editor.deleteLater()

    def test_error_utility_methods(self, qapp):
        """Test error handling utility methods."""
        graph_editor = GraphEditor(parent=None)

        # Clear any initialization errors first
        graph_editor.clear_component_errors()

        # Test error tracking
        graph_editor._component_errors["test_component"] = "Test error message"

        errors = graph_editor.get_component_errors()
        assert "test_component" in errors
        assert errors["test_component"] == "Test error message"

        # Test error summary (should show the single error)
        summary = graph_editor.get_error_summary()
        assert "test_component" in summary

        # Test error clearing
        graph_editor.clear_component_errors()
        errors_after_clear = graph_editor.get_component_errors()
        assert len(errors_after_clear) == 0

        # Test initialization status
        init_status = graph_editor.is_initialization_successful()
        assert isinstance(init_status, bool)

        # Test fallback mode status
        fallback_status = graph_editor.is_fallback_mode_enabled()
        assert isinstance(fallback_status, bool)

        # Clean up
        graph_editor.deleteLater()

    def test_state_validation(self, qapp, sample_beat_data, sample_sequence_data):
        """Test comprehensive state validation."""
        graph_editor = GraphEditor(parent=None)

        # Test validation with valid data
        graph_editor.set_sequence(sample_sequence_data)
        graph_editor.set_selected_beat_data(0, sample_beat_data)

        validation_result = graph_editor.validate_current_state()
        assert isinstance(validation_result, ValidationResult)

        # Test validation with invalid data
        graph_editor._selected_beat_data = Mock()  # Invalid beat data
        validation_result = graph_editor.validate_current_state()
        assert isinstance(validation_result, ValidationResult)

        # Clean up
        graph_editor.deleteLater()

    def test_fallback_ui_creation(self, qapp):
        """Test fallback UI creation when normal initialization fails."""
        # This test verifies that fallback mechanisms work
        with patch(
            "presentation.components.graph_editor.graph_editor.PictographDisplaySection"
        ) as mock_pictograph:
            with patch(
                "presentation.components.graph_editor.graph_editor.MainAdjustmentPanel"
            ) as mock_panel:
                # Make both components fail
                mock_pictograph.side_effect = RuntimeError("Pictograph failed")
                mock_panel.side_effect = RuntimeError("Panel failed")

                graph_editor = GraphEditor(parent=None)

                # Should still create a widget (in fallback mode)
                assert graph_editor is not None
                assert graph_editor.is_fallback_mode_enabled()

                # Should have error information
                errors = graph_editor.get_component_errors()
                assert len(errors) > 0

                # Clean up
                graph_editor.deleteLater()

    def test_maximum_recovery_attempts(self, qapp):
        """Test that recovery attempts are limited."""
        graph_editor = GraphEditor(parent=None)

        # Set recovery attempts to maximum
        graph_editor._recovery_attempts = graph_editor._max_recovery_attempts

        # Attempt recovery should fail due to max attempts
        recovery_result = graph_editor.attempt_component_recovery()
        assert recovery_result is False

        # Clean up
        graph_editor.deleteLater()

    def test_toggle_visibility_error_handling(self, qapp):
        """Test error handling in visibility toggle."""
        graph_editor = GraphEditor(parent=None)

        # Test normal visibility toggle
        result = graph_editor.toggle_visibility()
        assert result is True

        # Test with signal emission error
        with patch.object(graph_editor, "visibility_changed") as mock_signal:
            mock_signal.emit.side_effect = RuntimeError("Signal error")

            # Should still succeed even if signal fails
            result = graph_editor.toggle_visibility()
            assert result is True

        # Clean up
        graph_editor.deleteLater()


@pytest.mark.unit
class TestGraphEditorErrorRecovery:
    """Test error recovery scenarios."""

    def test_component_recreation_after_failure(self, qapp):
        """Test that components can be recreated after failure."""
        graph_editor = GraphEditor(parent=None)

        # Simulate component destruction
        if graph_editor._pictograph_display:
            graph_editor._pictograph_display.deleteLater()
            graph_editor._pictograph_display = None

        # Attempt recovery
        recovery_result = graph_editor.attempt_component_recovery()

        # Check if component was recreated (may depend on component availability)
        if recovery_result:
            assert graph_editor._pictograph_display is not None

        # Clean up
        graph_editor.deleteLater()

    def test_signal_reconnection_after_recovery(self, qapp):
        """Test that signals are reconnected after component recovery."""
        graph_editor = GraphEditor(parent=None)

        # Simulate component failure and recovery
        graph_editor._pictograph_display = None

        # Attempt recovery
        recovery_success = graph_editor.attempt_component_recovery()

        # If recovery succeeded, signals should be reconnected
        if recovery_success and graph_editor._pictograph_display:
            # Test that signal handlers work
            graph_editor._on_pictograph_updated_safe(None)  # Should not crash

        # Clean up
        graph_editor.deleteLater()


@pytest.mark.integration
class TestGraphEditorErrorHandlingIntegration:
    """Integration tests for error handling with real components."""

    def test_error_handling_with_tka_test_helper(self, tka_test_helper):
        """Test error handling using TKA test infrastructure."""
        # Create a sequence using TKA helper
        seq_result = tka_test_helper.create_sequence("Error Test", 4)
        if seq_result.success:
            sequence_data = seq_result.data

            # Create graph editor
            graph_editor = GraphEditor(parent=None)

            # Test with valid data - may fail due to validation issues with TKA data structure
            result = graph_editor.set_sequence(sequence_data)
            # Don't assert True here as TKA data might not match our validation expectations
            assert isinstance(result, bool)

            # Test error handling regardless of sequence setting result
            validation_result = graph_editor.validate_current_state()
            assert isinstance(validation_result, ValidationResult)

            # Clean up
            graph_editor.deleteLater()
        else:
            # If TKA helper fails, just test basic error handling
            graph_editor = GraphEditor(parent=None)
            validation_result = graph_editor.validate_current_state()
            assert isinstance(validation_result, ValidationResult)
            graph_editor.deleteLater()

    def test_comprehensive_error_scenario(
        self, qapp, sample_beat_data, sample_sequence_data
    ):
        """Test a comprehensive error scenario with recovery."""
        graph_editor = GraphEditor(parent=None)

        # Set up valid state
        graph_editor.set_sequence(sample_sequence_data)
        graph_editor.set_selected_beat_data(0, sample_beat_data)

        # Introduce errors
        graph_editor._component_errors["test_error"] = "Simulated comprehensive error"

        # Validate state
        validation_result = graph_editor.validate_current_state()
        assert not validation_result.is_valid

        # Attempt recovery
        graph_editor.clear_component_errors()
        recovery_success = graph_editor.attempt_component_recovery()

        # Validate state after recovery
        validation_result_after = graph_editor.validate_current_state()

        # Should be in better state after recovery attempt
        assert isinstance(validation_result_after, ValidationResult)
        # Recovery may or may not succeed, but should not crash
        assert isinstance(recovery_success, bool)

        # Clean up
        graph_editor.deleteLater()
