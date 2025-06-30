#!/usr/bin/env python3
"""
Graph Editor Validation Tests
============================

Tests for the validation utilities and error handling in graph editor components.
"""


import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

# Add modern source to path
modern_src = Path(__file__).parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src))



@pytest.mark.unit
class TestValidationUtilities:
    """Test validation utility functions."""

    def test_validate_beat_data_valid(self, sample_beat_data):
        """Test validation of valid beat data."""
        from presentation.components.graph_editor.utils.validation import (
            validate_beat_data,
        )

        result = validate_beat_data(sample_beat_data)

        assert result.is_valid is True
        assert not result.has_errors
        assert len(result.errors) == 0

    def test_validate_beat_data_none_allowed(self):
        """Test validation of None beat data when allowed."""
        from presentation.components.graph_editor.utils.validation import (
            validate_beat_data,
        )

        result = validate_beat_data(None, allow_none=True)

        assert result.is_valid is True
        assert not result.has_errors

    def test_validate_beat_data_none_not_allowed(self):
        """Test validation of None beat data when not allowed."""
        from presentation.components.graph_editor.utils.validation import (
            validate_beat_data,
        )

        result = validate_beat_data(None, allow_none=False)

        assert result.is_valid is False
        assert result.has_errors
        assert len(result.errors) == 1
        assert "cannot be None" in result.errors[0].message

    def test_validate_sequence_data_valid(self, sample_sequence_data):
        """Test validation of valid sequence data."""
        from presentation.components.graph_editor.utils.validation import (
            validate_sequence_data,
        )

        result = validate_sequence_data(sample_sequence_data)

        assert result.is_valid is True
        assert not result.has_errors

    def test_validate_beat_index_valid(self):
        """Test validation of valid beat index."""
        from presentation.components.graph_editor.utils.validation import (
            validate_beat_index,
        )

        result = validate_beat_index(0, sequence_length=5)

        assert result.is_valid is True
        assert not result.has_errors

    def test_validate_beat_index_out_of_bounds(self):
        """Test validation of out-of-bounds beat index."""
        from presentation.components.graph_editor.utils.validation import (
            validate_beat_index,
        )

        result = validate_beat_index(10, sequence_length=5)

        assert result.is_valid is False
        assert result.has_errors
        assert "exceeds sequence length" in result.errors[0].message

    def test_validate_arrow_id_valid(self):
        """Test validation of valid arrow ID."""
        from presentation.components.graph_editor.utils.validation import (
            validate_arrow_id,
        )

        result = validate_arrow_id("blue")

        assert result.is_valid is True
        assert not result.has_errors

    def test_validate_arrow_id_invalid(self):
        """Test validation of invalid arrow ID."""
        from presentation.components.graph_editor.utils.validation import (
            validate_arrow_id,
        )

        result = validate_arrow_id("green")

        assert result.is_valid is False
        assert result.has_errors
        assert "must be one of" in result.errors[0].message


@pytest.mark.unit
class TestStateManagerValidation:
    """Test validation in StateManager methods."""

    def test_set_visibility_invalid_type(self, qapp):
        """Test set_visibility with invalid type raises ValidationError."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )
        from presentation.components.graph_editor.utils.validation import (
            ValidationError,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Should raise ValidationError for non-boolean
        with pytest.raises(ValidationError) as exc_info:
            state_manager.set_visibility("true")  # String instead of bool

        assert "must be a boolean" in str(exc_info.value)
        assert exc_info.value.field == "is_visible"

        # Clean up
        state_manager.deleteLater()

    def test_set_current_sequence_invalid_data(self, qapp):
        """Test set_current_sequence with invalid sequence data."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )
        from presentation.components.graph_editor.utils.validation import (
            ValidationError,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Create invalid sequence data (missing required attributes)
        invalid_sequence = Mock()
        invalid_sequence.name = ""  # Empty name should trigger validation error

        # Should raise ValidationError for invalid sequence
        with pytest.raises(ValidationError) as exc_info:
            state_manager.set_current_sequence(invalid_sequence)

        assert "Invalid sequence data" in str(exc_info.value)

        # Clean up
        state_manager.deleteLater()

    def test_set_selected_beat_invalid_index(self, qapp, sample_beat_data):
        """Test set_selected_beat with invalid beat index."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )
        from presentation.components.graph_editor.utils.validation import (
            ValidationError,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # No sequence set, so any positive index should be invalid
        with pytest.raises(ValidationError) as exc_info:
            state_manager.set_selected_beat(sample_beat_data, 0)

        assert "Invalid beat index" in str(exc_info.value)
        assert "exceeds sequence length" in str(exc_info.value)

        # Clean up
        state_manager.deleteLater()

    def test_validation_logging(self, qapp, caplog):
        """Test that validation errors are properly logged."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )
        from presentation.components.graph_editor.utils.validation import (
            ValidationError,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Trigger validation error
        with pytest.raises(ValidationError):
            state_manager.set_visibility("invalid")

        # Check that error was logged
        assert "Validation failed" in caplog.text
        assert "is_visible" in caplog.text

        # Clean up
        state_manager.deleteLater()


@pytest.mark.unit
class TestValidationErrorHandling:
    """Test error handling and recovery mechanisms."""

    def test_validation_error_context(self):
        """Test ValidationError includes proper context."""
        from presentation.components.graph_editor.utils.validation import (
            ValidationError,
        )

        context = {"operation": "test", "component": "StateManager"}
        error = ValidationError("Test error", "test_field", "test_value", context)

        assert error.message == "Test error"
        assert error.field == "test_field"
        assert error.value == "test_value"
        assert error.context == context

        # Test string representation includes all information
        error_str = str(error)
        assert "Test error" in error_str
        assert "test_field" in error_str
        assert "test_value" in error_str
        assert "operation=test" in error_str

    def test_validation_result_error_accumulation(self):
        """Test ValidationResult properly accumulates errors."""
        from presentation.components.graph_editor.utils.validation import (
            ValidationResult,
        )

        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        # Add errors
        result.add_error("First error", "field1", "value1")
        result.add_error("Second error", "field2", "value2")

        assert result.is_valid is False
        assert result.has_errors is True
        assert len(result.errors) == 2
        assert result.errors[0].message == "First error"
        assert result.errors[1].message == "Second error"

    def test_validation_result_warning_handling(self):
        """Test ValidationResult properly handles warnings."""
        from presentation.components.graph_editor.utils.validation import (
            ValidationResult,
        )

        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        # Add warnings
        result.add_warning("First warning")
        result.add_warning("Second warning")

        assert result.is_valid is True  # Warnings don't affect validity
        assert result.has_warnings is True
        assert len(result.warnings) == 2
        assert "First warning" in result.warnings
        assert "Second warning" in result.warnings


@pytest.mark.unit
class TestErrorRecoveryMechanisms:
    """Test error recovery and fallback mechanisms."""

    def test_state_recovery_initialization(self, qapp):
        """Test that StateManager initializes with recovery mechanisms."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Check recovery attributes are initialized
        assert hasattr(state_manager, "_recovery_attempts")
        assert hasattr(state_manager, "_max_recovery_attempts")
        assert hasattr(state_manager, "_fallback_state_enabled")
        assert hasattr(state_manager, "_last_known_good_state")

        assert state_manager._recovery_attempts == 0
        assert state_manager._max_recovery_attempts == 3
        assert state_manager._fallback_state_enabled is True

        # Clean up
        state_manager.deleteLater()

    def test_save_known_good_state(self, qapp, sample_sequence_data, sample_beat_data):
        """Test saving known good state."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Set some state
        state_manager.set_visibility(True, emit_signal=False)
        state_manager.set_current_sequence(sample_sequence_data, emit_signal=False)
        state_manager.set_selected_beat(sample_beat_data, 0, emit_signal=False)

        # Save known good state should be called automatically during validation
        assert state_manager._last_known_good_state is not None
        assert state_manager._last_known_good_state["is_visible"] is True
        assert (
            state_manager._last_known_good_state["current_sequence"]
            == sample_sequence_data
        )

        # Clean up
        state_manager.deleteLater()

    def test_fallback_recovery_toggle(self, qapp):
        """Test enabling/disabling fallback recovery."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Initially enabled
        assert state_manager._fallback_state_enabled is True

        # Disable fallback recovery
        state_manager.enable_fallback_recovery(False)
        assert state_manager._fallback_state_enabled is False

        # Re-enable fallback recovery
        state_manager.enable_fallback_recovery(True)
        assert state_manager._fallback_state_enabled is True

        # Clean up
        state_manager.deleteLater()

    def test_recovery_attempt_counter(self, qapp):
        """Test recovery attempt counter management."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Initially zero
        assert state_manager._recovery_attempts == 0

        # Simulate recovery attempts
        state_manager._recovery_attempts = 2
        assert state_manager._recovery_attempts == 2

        # Reset counter
        state_manager.reset_recovery_attempts()
        assert state_manager._recovery_attempts == 0

        # Clean up
        state_manager.deleteLater()

    def test_safe_state_reset(self, qapp, sample_sequence_data, sample_beat_data):
        """Test reset to safe state functionality."""
        from presentation.components.graph_editor.managers.state_manager import (
            GraphEditorStateManager,
        )

        mock_graph_editor = Mock()
        state_manager = GraphEditorStateManager(mock_graph_editor)

        # Set some state
        state_manager.set_visibility(True, emit_signal=False)
        state_manager.set_current_sequence(sample_sequence_data, emit_signal=False)
        state_manager.set_selected_beat(sample_beat_data, 0, emit_signal=False)

        # Reset to safe state
        state_manager._reset_to_safe_state()

        # Verify all state is reset
        assert state_manager._is_visible is False
        assert state_manager._current_sequence is None
        assert state_manager._selected_beat is None
        assert state_manager._selected_beat_index is None
        assert state_manager._selected_arrow_id is None
        assert state_manager._state_consistent is True
        assert state_manager._last_validation_error is None

        # Clean up
        state_manager.deleteLater()
