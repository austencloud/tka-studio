import logging
from typing import Optional, TYPE_CHECKING
from PyQt6.QtCore import QObject, pyqtSignal

from domain.models.core_models import SequenceData, BeatData
from ..utils.validation import (
    validate_beat_data,
    validate_sequence_data,
    validate_beat_index,
    ValidationError,
)
from ..utils.logging import (
    create_component_logger,
    log_method_call,
    log_validation_errors,
)

logger = logging.getLogger(__name__)
component_logger = create_component_logger("StateManager")

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor


class GraphEditorStateManager(QObject):
    """
    Manages all state for the graph editor component.

    Responsibilities:
    - Current sequence management
    - Selected beat tracking
    - Selected arrow tracking
    - Visibility state management
    - State validation and consistency
    - State change notifications
    """

    # Signals for state changes
    visibility_changed = pyqtSignal(bool)  # is_visible
    sequence_changed = pyqtSignal(object)  # SequenceData or None
    selected_beat_changed = pyqtSignal(object, int)  # BeatData or None, beat_index
    selected_arrow_changed = pyqtSignal(str)  # arrow_id

    def __init__(self, graph_editor: "GraphEditor", parent: Optional[QObject] = None):
        super().__init__(parent)
        self._graph_editor = graph_editor

        # Core state variables
        self._is_visible = False
        self._current_sequence: Optional[SequenceData] = None
        self._selected_beat: Optional[BeatData] = None
        self._selected_beat_index: Optional[int] = None
        self._selected_arrow_id: Optional[str] = None

        # State validation flags
        self._state_consistent = True
        self._last_validation_error: Optional[str] = None

        # Error recovery mechanisms
        self._recovery_attempts = 0
        self._max_recovery_attempts = 3
        self._fallback_state_enabled = True
        self._last_known_good_state = None

        component_logger.info("StateManager initialized with error recovery enabled")

    # Visibility State
    def set_visibility(self, is_visible: bool, emit_signal: bool = True) -> None:
        """
        Set the visibility state with input validation.

        Args:
            is_visible: New visibility state
            emit_signal: Whether to emit the visibility_changed signal

        Raises:
            ValidationError: If is_visible is not a boolean
        """
        # Input validation
        if not isinstance(is_visible, bool):
            error_msg = f"Visibility must be a boolean, got {type(is_visible).__name__}: {is_visible}"
            component_logger.validation_error("is_visible", is_visible, error_msg)
            raise ValidationError(error_msg, "is_visible", is_visible)

        # Log method call
        component_logger.method_call(
            "set_visibility", {"is_visible": is_visible, "emit_signal": emit_signal}
        )

        if self._is_visible != is_visible:
            old_visibility = self._is_visible
            self._is_visible = is_visible

            # Log state change
            component_logger.state_change(
                old_visibility, is_visible, {"emit_signal": emit_signal}
            )
            logger.debug("State: Visibility changed to %s", is_visible)

            if emit_signal:
                self.visibility_changed.emit(is_visible)

    def is_visible(self) -> bool:
        """Get the current visibility state"""
        return self._is_visible

    def toggle_visibility(self) -> bool:
        """
        Toggle the visibility state.

        Returns:
            bool: New visibility state
        """
        new_state = not self._is_visible
        self.set_visibility(new_state)
        return new_state

    # Error Recovery Methods
    def _save_known_good_state(self) -> None:
        """Save current state as a known good state for recovery."""
        try:
            self._last_known_good_state = {
                "is_visible": self._is_visible,
                "current_sequence": self._current_sequence,
                "selected_beat": self._selected_beat,
                "selected_beat_index": self._selected_beat_index,
                "selected_arrow_id": self._selected_arrow_id,
            }
            component_logger.debug(
                "Saved known good state",
                {
                    "sequence_name": (
                        self._current_sequence.name if self._current_sequence else None
                    ),
                    "beat_index": self._selected_beat_index,
                },
            )
        except Exception as e:
            component_logger.error("Failed to save known good state", exception=e)

    def _attempt_state_recovery(self) -> bool:
        """
        Attempt to recover from an invalid state.

        Returns:
            True if recovery was successful, False otherwise
        """
        if self._recovery_attempts >= self._max_recovery_attempts:
            component_logger.error(
                "Maximum recovery attempts exceeded",
                {
                    "attempts": self._recovery_attempts,
                    "max_attempts": self._max_recovery_attempts,
                },
            )
            return False

        self._recovery_attempts += 1
        component_logger.warning(
            f"Attempting state recovery (attempt {self._recovery_attempts})"
        )

        try:
            # Strategy 1: Restore last known good state
            if self._last_known_good_state and self._fallback_state_enabled:
                component_logger.info("Restoring last known good state")
                self._restore_known_good_state()
                return True

            # Strategy 2: Reset to safe default state
            component_logger.info("Resetting to safe default state")
            self._reset_to_safe_state()
            return True

        except Exception as e:
            component_logger.error("State recovery failed", exception=e)
            return False

    def _restore_known_good_state(self) -> None:
        """Restore the last known good state."""
        if not self._last_known_good_state:
            raise ValueError("No known good state available for restoration")

        state = self._last_known_good_state
        self._is_visible = state["is_visible"]
        self._current_sequence = state["current_sequence"]
        self._selected_beat = state["selected_beat"]
        self._selected_beat_index = state["selected_beat_index"]
        self._selected_arrow_id = state["selected_arrow_id"]

        # Emit signals to notify components of state restoration
        self.visibility_changed.emit(self._is_visible)
        self.sequence_changed.emit(self._current_sequence)
        self.selected_beat_changed.emit(
            self._selected_beat, self._selected_beat_index or -1
        )
        if self._selected_arrow_id:
            self.selected_arrow_changed.emit(self._selected_arrow_id)

    def _reset_to_safe_state(self) -> None:
        """Reset to a safe default state."""
        component_logger.info("Resetting to safe default state")

        # Clear all state to safe defaults
        self._is_visible = False
        self._current_sequence = None
        self._selected_beat = None
        self._selected_beat_index = None
        self._selected_arrow_id = None

        # Reset validation flags
        self._state_consistent = True
        self._last_validation_error = None

        # Emit signals to notify components
        self.visibility_changed.emit(False)
        self.sequence_changed.emit(None)
        self.selected_beat_changed.emit(None, -1)

    def enable_fallback_recovery(self, enabled: bool = True) -> None:
        """Enable or disable fallback state recovery."""
        self._fallback_state_enabled = enabled
        component_logger.info(
            f"Fallback recovery {'enabled' if enabled else 'disabled'}"
        )

    def reset_recovery_attempts(self) -> None:
        """Reset the recovery attempt counter."""
        self._recovery_attempts = 0
        component_logger.debug("Recovery attempt counter reset")

    # Sequence State
    def set_current_sequence(
        self, sequence: Optional[SequenceData], emit_signal: bool = True
    ) -> None:
        """
        Set the current sequence with comprehensive validation.

        Args:
            sequence: New sequence data
            emit_signal: Whether to emit the sequence_changed signal

        Raises:
            ValidationError: If sequence data is invalid
        """
        # Input validation
        validation_result = validate_sequence_data(
            sequence, allow_none=True, context={"operation": "set_current_sequence"}
        )
        if validation_result.has_errors:
            log_validation_errors(
                component_logger, validation_result, "set_current_sequence"
            )
            raise ValidationError(
                f"Invalid sequence data: {validation_result.errors[0].message}",
                "sequence",
                sequence,
            )

        # Log warnings if any
        if validation_result.has_warnings:
            for warning in validation_result.warnings:
                component_logger.warning(
                    f"Sequence validation warning: {warning}",
                    {"sequence_name": sequence.name if sequence else None},
                )

        # Log method call
        component_logger.method_call(
            "set_current_sequence",
            {
                "sequence_name": sequence.name if sequence else None,
                "emit_signal": emit_signal,
            },
        )

        if self._current_sequence != sequence:
            old_sequence = self._current_sequence
            self._current_sequence = sequence

            # Log state change
            component_logger.state_change(
                old_sequence.name if old_sequence else None,
                sequence.name if sequence else None,
                {"emit_signal": emit_signal},
            )
            logger.debug("State: Sequence changed to %s", sequence)

            # Validate sequence change doesn't break beat selection
            if sequence is None:
                self.clear_selected_beat(emit_signal=False)

            if emit_signal:
                self.sequence_changed.emit(sequence)

            self._validate_state()

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence"""
        return self._current_sequence

    def has_sequence(self) -> bool:
        """Check if a sequence is currently set"""
        return self._current_sequence is not None

    # Beat State
    def set_selected_beat(
        self,
        beat_data: Optional[BeatData],
        beat_index: Optional[int] = None,
        emit_signal: bool = True,
    ) -> None:
        """
        Set the selected beat and its index with comprehensive validation.

        Args:
            beat_data: Beat data to select
            beat_index: Index of the beat in the sequence
            emit_signal: Whether to emit the selected_beat_changed signal

        Raises:
            ValidationError: If beat data or index is invalid
        """
        # Input validation for beat data
        validation_result = validate_beat_data(
            beat_data,
            allow_none=True,
            context={"operation": "set_selected_beat", "beat_index": beat_index},
        )
        if validation_result.has_errors:
            log_validation_errors(
                component_logger, validation_result, "set_selected_beat"
            )
            raise ValidationError(
                f"Invalid beat data: {validation_result.errors[0].message}",
                "beat_data",
                beat_data,
            )

        # Input validation for beat index
        if beat_index is not None:
            sequence_length = (
                len(self._current_sequence.beats) if self._current_sequence else 0
            )
            index_validation = validate_beat_index(
                beat_index,
                sequence_length,
                allow_negative=True,
                context={
                    "operation": "set_selected_beat",
                    "sequence_length": sequence_length,
                },
            )
            if index_validation.has_errors:
                log_validation_errors(
                    component_logger, index_validation, "set_selected_beat"
                )
                raise ValidationError(
                    f"Invalid beat index: {index_validation.errors[0].message}",
                    "beat_index",
                    beat_index,
                )

        # Log method call
        component_logger.method_call(
            "set_selected_beat",
            {
                "beat_letter": beat_data.letter if beat_data else None,
                "beat_index": beat_index,
                "emit_signal": emit_signal,
            },
        )

        state_changed = (
            self._selected_beat != beat_data or self._selected_beat_index != beat_index
        )

        if state_changed:
            old_beat = self._selected_beat
            old_index = self._selected_beat_index

            self._selected_beat = beat_data
            self._selected_beat_index = beat_index

            # Log state change
            component_logger.state_change(
                f"{old_beat.letter if old_beat else None}@{old_index}",
                f"{beat_data.letter if beat_data else None}@{beat_index}",
                {"emit_signal": emit_signal},
            )
            logger.debug(
                "State: Selected beat changed to index %s: %s", beat_index, beat_data
            )

            if emit_signal:
                self.selected_beat_changed.emit(beat_data, beat_index or -1)

            self._validate_state()

    def set_selected_beat_data(
        self, beat_data: Optional[BeatData], beat_index: Optional[int] = None
    ) -> None:
        """
        Convenience method to set beat data (preserves index if not provided).

        Args:
            beat_data: Beat data to set
            beat_index: Beat index (optional, preserves current if None)
        """
        index_to_use = (
            beat_index if beat_index is not None else self._selected_beat_index
        )
        self.set_selected_beat(beat_data, index_to_use)

    def get_selected_beat(self) -> Optional[BeatData]:
        """Get the currently selected beat"""
        return self._selected_beat

    def get_selected_beat_index(self) -> Optional[int]:
        """Get the index of the currently selected beat"""
        return self._selected_beat_index

    def has_selected_beat(self) -> bool:
        """Check if a beat is currently selected"""
        return self._selected_beat is not None

    def clear_selected_beat(self, emit_signal: bool = True) -> None:
        """
        Clear the selected beat.

        Args:
            emit_signal: Whether to emit the selected_beat_changed signal
        """
        if self._selected_beat is not None or self._selected_beat_index is not None:
            self._selected_beat = None
            self._selected_beat_index = None

            logger.debug("State: Selected beat cleared")

            if emit_signal:
                self.selected_beat_changed.emit(None, -1)

    # Arrow State
    def set_selected_arrow_id(
        self, arrow_id: Optional[str], emit_signal: bool = True
    ) -> None:
        """
        Set the selected arrow ID.

        Args:
            arrow_id: Arrow ID to select
            emit_signal: Whether to emit the selected_arrow_changed signal
        """
        if self._selected_arrow_id != arrow_id:
            self._selected_arrow_id = arrow_id
            logger.debug("State: Selected arrow changed to %s", arrow_id)

            if emit_signal and arrow_id:
                self.selected_arrow_changed.emit(arrow_id)

    def get_selected_arrow_id(self) -> Optional[str]:
        """Get the currently selected arrow ID"""
        return self._selected_arrow_id

    def has_selected_arrow(self) -> bool:
        """Check if an arrow is currently selected"""
        return self._selected_arrow_id is not None

    def clear_selected_arrow(self, emit_signal: bool = True) -> None:
        """
        Clear the selected arrow.

        Args:
            emit_signal: Whether to emit the selected_arrow_changed signal
        """
        if self._selected_arrow_id is not None:
            old_arrow = self._selected_arrow_id
            self._selected_arrow_id = None
            logger.debug("State: Selected arrow cleared (was %s)", old_arrow)

    # State Management
    def get_state_summary(self) -> dict:
        """
        Get a summary of the current state.

        Returns:
            dict: Current state summary
        """
        return {
            "is_visible": self._is_visible,
            "has_sequence": self.has_sequence(),
            "sequence_id": (
                getattr(self._current_sequence, "id", None)
                if self._current_sequence
                else None
            ),
            "has_selected_beat": self.has_selected_beat(),
            "selected_beat_index": self._selected_beat_index,
            "has_selected_arrow": self.has_selected_arrow(),
            "selected_arrow_id": self._selected_arrow_id,
            "state_consistent": self._state_consistent,
            "last_validation_error": self._last_validation_error,
        }

    def _validate_state(self) -> bool:
        """
        Validate state consistency.

        Returns:
            bool: True if state is consistent
        """
        errors = []

        # Check beat selection consistency
        if self._selected_beat is not None and self._selected_beat_index is None:
            errors.append("Selected beat without beat index")

        if self._selected_beat_index is not None and self._selected_beat is None:
            errors.append("Beat index without selected beat")

        # Check sequence-beat relationship
        if self._selected_beat is not None and self._current_sequence is None:
            errors.append("Selected beat without current sequence")

        # Check index bounds (if sequence has beats)
        if (
            self._current_sequence
            and hasattr(self._current_sequence, "beats")
            and self._selected_beat_index is not None
        ):

            beats_count = len(self._current_sequence.beats)
            if (
                self._selected_beat_index < 0
                or self._selected_beat_index >= beats_count
            ):
                errors.append(
                    f"Beat index {self._selected_beat_index} out of bounds (0-{beats_count-1})"
                )

        # Update validation state
        self._state_consistent = len(errors) == 0
        self._last_validation_error = "; ".join(errors) if errors else None

        if not self._state_consistent:
            component_logger.error(
                "State validation failed",
                {"errors": errors, "validation_error": self._last_validation_error},
            )
            logger.warning("State validation failed: %s", self._last_validation_error)

            # Attempt automatic recovery if enabled
            if self._fallback_state_enabled:
                component_logger.info("Attempting automatic state recovery")
                recovery_success = self._attempt_state_recovery()
                if recovery_success:
                    component_logger.info("State recovery successful")
                    # Re-validate after recovery
                    return self._validate_state()

                component_logger.error(
                    "State recovery failed - manual intervention required"
                )
        else:
            # Save current state as known good state
            self._save_known_good_state()
            # Reset recovery attempts on successful validation
            self.reset_recovery_attempts()

        return self._state_consistent

    def reset_all_state(self) -> None:
        """Reset all state to initial values"""
        logger.debug("State: Resetting all state")

        self._is_visible = False
        self._current_sequence = None
        self._selected_beat = None
        self._selected_beat_index = None
        self._selected_arrow_id = None

        self._state_consistent = True
        self._last_validation_error = None

        # Emit all change signals
        self.visibility_changed.emit(False)
        self.sequence_changed.emit(None)
        self.selected_beat_changed.emit(None, -1)

    def force_state_validation(self) -> bool:
        """
        Force a state validation check.

        Returns:
            bool: True if state is valid
        """
        return self._validate_state()

    def is_state_consistent(self) -> bool:
        """Check if the current state is consistent"""
        return self._state_consistent

    def get_last_validation_error(self) -> Optional[str]:
        """Get the last validation error message"""
        return self._last_validation_error

    # Context and relationship helpers
    def update_data_flow_context(self, data_flow_service) -> None:
        """
        Update data flow service context with current state.

        Args:
            data_flow_service: Data flow service to update
        """
        if (
            self._current_sequence
            and self._selected_beat_index is not None
            and data_flow_service
        ):

            data_flow_service.set_context(
                self._current_sequence, self._selected_beat_index
            )
            logger.debug(
                "Updated data flow context: sequence with beat index %s",
                self._selected_beat_index,
            )

    def sync_with_graph_service(self, graph_service) -> None:
        """
        Synchronize state with graph service.

        Args:
            graph_service: Graph service to synchronize with
        """
        if graph_service:
            # Update service with current state
            if self._current_sequence:
                graph_service.update_graph_display(self._current_sequence)

            if self._selected_beat and self._selected_beat_index is not None:
                graph_service.set_selected_beat(
                    self._selected_beat, self._selected_beat_index
                )

            if self._selected_arrow_id:
                graph_service.set_arrow_selection(self._selected_arrow_id)

            logger.debug("Synchronized state with graph service")
