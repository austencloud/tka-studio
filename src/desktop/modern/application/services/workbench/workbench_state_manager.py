"""
Workbench State Manager - Framework-Agnostic Business Logic

Manages workbench-specific state including sequence, start position, and operation states.
Coordinates with SequenceStateTracker and provides workbench-specific state logic.

Following established patterns:
- Framework-agnostic (no Qt dependencies)
- Single responsibility (state management only)
- Event-driven coordination
- Clean separation from presentation
"""

import logging
from typing import Optional

from desktop.modern.core.interfaces.workbench_services import (
    IWorkbenchStateManager,
    StateChangeResult,
    WorkbenchState,
)
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


# Note: WorkbenchState and StateChangeResult are now imported from the interface


class WorkbenchStateManager(IWorkbenchStateManager):
    """
    Framework-agnostic workbench state management.

    Responsibilities:
    - Track workbench-specific state (sequence, start position, restoration flags)
    - Coordinate with SequenceStateTracker for persistence
    - Provide state validation and consistency checks
    - Calculate derived state (button enablement, operation availability)
    - Manage restoration state to prevent auto-save loops
    """

    def __init__(self, sequence_state_tracker=None):
        """
        Initialize workbench state manager.

        Args:
            sequence_state_tracker: Optional injected SequenceStateTracker
        """
        self._sequence_state_tracker = sequence_state_tracker

        # Current workbench state
        self._current_sequence: Optional[SequenceData] = None
        self._start_position_data: Optional[BeatData] = None
        self._current_state = WorkbenchState.EMPTY

        # Restoration state management
        self._is_restoring = False
        self._restoration_complete = False

        logger.debug("WorkbenchStateManager initialized")

    # State Management
    def set_sequence(
        self, sequence: Optional[SequenceData], from_restoration: bool = False
    ) -> StateChangeResult:
        """
        Set current sequence and update workbench state.

        Args:
            sequence: New sequence data (None to clear)
            from_restoration: Whether this is from session restoration

        Returns:
            StateChangeResult with change details
        """

        previous_state = self._current_state
        previous_sequence = self._current_sequence

        # Update restoration flag if needed
        if from_restoration:
            self._is_restoring = True

        # Set new sequence
        self._current_sequence = sequence




        # Calculate new state
        new_state = self._calculate_workbench_state()
        state_changed = new_state != previous_state
        sequence_changed = sequence != previous_sequence

        if sequence_changed:
            logger.debug(
                f"Sequence changed: {sequence.length if sequence else 0} beats"
            )

        if state_changed:
            self._current_state = new_state
            logger.debug(f"Workbench state changed: {previous_state} -> {new_state}")

        # Coordinate with SequenceStateTracker if available and not restoring
        if self._sequence_state_tracker and not self._is_restoring:
            self._sequence_state_tracker.set_sequence_direct(sequence)

        return (
            StateChangeResult.create_sequence_changed(previous_state, new_state)
            if (state_changed or sequence_changed)
            else StateChangeResult.create_no_change(new_state)
        )

    def set_start_position(
        self, start_position: Optional[BeatData], from_restoration: bool = False
    ) -> StateChangeResult:
        """
        Set start position and update workbench state.

        Args:
            start_position: New start position data (None to clear)
            from_restoration: Whether this is from session restoration

        Returns:
            StateChangeResult with change details
        """
        previous_state = self._current_state
        previous_start_position = self._start_position_data

        # Update restoration flag if needed
        if from_restoration:
            self._is_restoring = True

        # Set new start position
        self._start_position_data = start_position

        # Calculate new state
        new_state = self._calculate_workbench_state()
        state_changed = new_state != previous_state
        start_position_changed = start_position != previous_start_position

        if state_changed:
            self._current_state = new_state
            logger.debug(f"Workbench state changed: {previous_state} -> {new_state}")

        if start_position_changed:
            logger.debug(
                f"Start position changed: {start_position.letter if start_position else 'None'}"
            )

        # Coordinate with SequenceStateTracker if available and not restoring
        if self._sequence_state_tracker and not self._is_restoring:
            self._sequence_state_tracker.set_start_position_direct(start_position)

        # Return appropriate result based on what actually changed
        if state_changed or start_position_changed:
            return StateChangeResult.create_start_position_changed(
                previous_state, new_state
            )
        else:
            return StateChangeResult.create_no_change(new_state)

    def clear_all_state(self) -> StateChangeResult:
        """Clear all workbench state."""
        previous_state = self._current_state

        self._current_sequence = None
        self._start_position_data = None
        self._current_state = WorkbenchState.EMPTY
        self._is_restoring = False
        self._restoration_complete = False

        logger.debug("All workbench state cleared")

        # Coordinate with SequenceStateTracker if available
        if self._sequence_state_tracker:
            self._sequence_state_tracker.set_sequence_direct(None)
            self._sequence_state_tracker.set_start_position_direct(None)

        return StateChangeResult.create_both_changed(
            previous_state, WorkbenchState.EMPTY
        )

    # State Queries
    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get current sequence."""
        return self._current_sequence

    def get_start_position(self) -> Optional[BeatData]:
        """Get current start position."""
        return self._start_position_data

    def get_workbench_state(self) -> WorkbenchState:
        """Get current workbench state."""
        return self._current_state

    def has_sequence(self) -> bool:
        """Check if workbench has a sequence."""
        return (
            self._current_sequence is not None and len(self._current_sequence.beats) > 0
        )

    def has_start_position(self) -> bool:
        """Check if workbench has a start position."""
        return self._start_position_data is not None

    def is_empty(self) -> bool:
        """Check if workbench is completely empty."""
        return self._current_state == WorkbenchState.EMPTY

    def is_restoring(self) -> bool:
        """Check if workbench is in restoration mode."""
        return self._is_restoring

    def is_restoration_complete(self) -> bool:
        """Check if restoration has completed."""
        return self._restoration_complete

    # Derived State Calculations
    def should_enable_sequence_operations(self) -> bool:
        """Check if sequence operations should be enabled."""
        return self.has_sequence()

    def should_enable_export_operations(self) -> bool:
        """Check if export operations should be enabled."""
        return self.has_sequence()

    def should_enable_transform_operations(self) -> bool:
        """Check if transform operations should be enabled."""
        return self.has_sequence()

    def should_enable_clear_operation(self) -> bool:
        """Check if clear operation should be enabled."""
        return not self.is_empty()

    def should_prevent_auto_save(self) -> bool:
        """Check if auto-save should be prevented (during restoration)."""
        return self._is_restoring

    def get_complete_sequence_with_start_position(self) -> Optional[SequenceData]:
        """Get sequence with start position included if both exist."""
        if not self._current_sequence:
            return None

        if self._start_position_data:
            return self._current_sequence.update(
                start_position=self._start_position_data
            )

        return self._current_sequence

    # Restoration Management
    def begin_restoration(self) -> None:
        """Begin restoration mode."""
        self._is_restoring = True
        self._restoration_complete = False
        logger.debug("Restoration mode activated")

    def complete_restoration(self) -> None:
        """Complete restoration mode."""
        self._is_restoring = False
        self._restoration_complete = True
        logger.debug("Restoration mode completed")

    def reset_restoration_state(self) -> None:
        """Reset restoration state."""
        self._is_restoring = False
        self._restoration_complete = False
        logger.debug("Restoration state reset")

    # Internal Methods
    def _calculate_workbench_state(self) -> WorkbenchState:
        """Calculate workbench state based on current data."""
        if self._is_restoring:
            return WorkbenchState.RESTORING

        has_seq = self.has_sequence()
        has_start = self.has_start_position()

        if has_seq and has_start:
            return WorkbenchState.BOTH_SET
        elif has_seq:
            return WorkbenchState.SEQUENCE_LOADED
        elif has_start:
            return WorkbenchState.START_POSITION_SET
        else:
            return WorkbenchState.EMPTY

    # State Validation
    def validate_state_consistency(self) -> tuple[bool, list[str]]:
        """
        Validate current state consistency.

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        # Check sequence validity
        if self._current_sequence:
            if self._current_sequence.length == 0:
                issues.append("Sequence exists but has zero length")

        # Check start position validity
        if self._start_position_data:
            if not hasattr(self._start_position_data, "letter"):
                issues.append("Start position data missing required fields")

        # Check state calculation consistency
        calculated_state = self._calculate_workbench_state()
        if calculated_state != self._current_state and not self._is_restoring:
            issues.append(
                f"State mismatch: stored={self._current_state}, calculated={calculated_state}"
            )

        return len(issues) == 0, issues

    # Debug and Diagnostics
    def get_state_summary(self) -> dict:
        """Get comprehensive state summary for debugging."""
        is_valid, issues = self.validate_state_consistency()

        return {
            "workbench_state": self._current_state.value,
            "has_sequence": self.has_sequence(),
            "sequence_length": (
                self._current_sequence.length if self._current_sequence else 0
            ),
            "has_start_position": self.has_start_position(),
            "start_position_letter": (
                self._start_position_data.letter if self._start_position_data else None
            ),
            "is_restoring": self._is_restoring,
            "restoration_complete": self._restoration_complete,
            "is_empty": self.is_empty(),
            "state_valid": is_valid,
            "validation_issues": issues,
            "operations_enabled": {
                "sequence_ops": self.should_enable_sequence_operations(),
                "export_ops": self.should_enable_export_operations(),
                "transform_ops": self.should_enable_transform_operations(),
                "clear_op": self.should_enable_clear_operation(),
            },
        }
