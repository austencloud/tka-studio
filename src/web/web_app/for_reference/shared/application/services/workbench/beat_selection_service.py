"""
Beat Selection Service - Pure Business Logic

Handles all beat selection logic including multi-selection, keyboard navigation,
and validation without any Qt dependencies.
"""

import logging
from enum import Enum
from typing import NamedTuple

from desktop.modern.core.interfaces.workbench_services import IBeatSelectionService

logger = logging.getLogger(__name__)


class SelectionType(Enum):
    """Types of selection operations."""

    BEAT = "beat"
    START_POSITION = "start_position"
    NONE = "none"


class SelectionChangeResult(NamedTuple):
    """Result of a selection change operation."""

    changed: bool
    selection_type: SelectionType
    selected_index: int | None
    previous_indices: list[int]
    current_indices: list[int]

    @classmethod
    def no_change(cls):
        """Create a no-change result."""
        return cls(False, SelectionType.NONE, None, [], [])

    @classmethod
    def beat_selected(cls, index: int, previous: list[int], current: list[int]):
        """Create a beat selection result."""
        return cls(True, SelectionType.BEAT, index, previous, current)

    @classmethod
    def start_position_selected(cls, previous: list[int]):
        """Create a start position selection result."""
        return cls(True, SelectionType.START_POSITION, -1, previous, [])


class BeatSelectionService(IBeatSelectionService):
    """
    Pure business service for beat selection management.

    Handles selection logic, multi-selection rules, and validation without Qt dependencies.
    """

    # Special index for start position
    START_POSITION_INDEX = -1

    def __init__(self):
        """Initialize the selection service with default values."""
        self._selected_index: int | None = None
        self._selected_indices: list[int] = []
        self._multi_selection_enabled = False
        self._start_position_selected = False
        self._keyboard_navigation_enabled = True
        self._beat_count = 0

        logger.debug("Beat selection service initialized")

    # Configuration
    def set_beat_count(self, count: int) -> None:
        """Set the number of beats available for selection."""
        self._beat_count = max(0, count)
        # Clear invalid selections
        self._selected_indices = [
            idx for idx in self._selected_indices if self._is_valid_beat_index(idx)
        ]
        if self._selected_index is not None and not self._is_valid_beat_index(
            self._selected_index
        ):
            self._selected_index = None
        logger.debug(f"Beat count set to: {count}")

    def get_beat_count(self) -> int:
        """Get the current beat count."""
        return self._beat_count

    def set_multi_selection_enabled(self, enabled: bool) -> SelectionChangeResult:
        """
        Enable or disable multi-selection mode.

        Args:
            enabled: Whether to enable multi-selection

        Returns:
            SelectionChangeResult: Details of any selection changes
        """
        if self._multi_selection_enabled == enabled:
            return SelectionChangeResult.no_change()

        self._multi_selection_enabled = enabled

        # If disabling multi-selection and we have multiple selections, keep only the first
        if not enabled and len(self._selected_indices) > 1:
            if self._selected_indices:
                return self.select_beat(self._selected_indices[0])
            else:
                return self.clear_selection()

        logger.debug(f"Multi-selection enabled: {enabled}")
        return SelectionChangeResult.no_change()

    def set_keyboard_navigation_enabled(self, enabled: bool) -> None:
        """Enable or disable keyboard navigation."""
        self._keyboard_navigation_enabled = enabled
        logger.debug(f"Keyboard navigation enabled: {enabled}")

    # Selection Operations
    def select_beat(self, beat_index: int) -> SelectionChangeResult:
        """
        Select a specific beat.

        Args:
            beat_index: Index of the beat to select

        Returns:
            SelectionChangeResult: Details of the selection change
        """
        if not self._is_valid_beat_index(beat_index):
            logger.warning(f"Invalid beat index: {beat_index}")
            return SelectionChangeResult.no_change()

        previous_indices = self._selected_indices.copy()

        # Clear all previous selections
        self._clear_all_internal_selections()

        # Set new selection
        self._selected_index = beat_index
        self._selected_indices = [beat_index]
        self._start_position_selected = False

        logger.debug(f"Beat selected: {beat_index}")
        return SelectionChangeResult.beat_selected(
            beat_index, previous_indices, self._selected_indices
        )

    def select_start_position(self) -> SelectionChangeResult:
        """
        Select the start position.

        Returns:
            SelectionChangeResult: Details of the selection change
        """
        previous_indices = self._selected_indices.copy()

        # Clear all previous selections
        self._clear_all_internal_selections()

        # Set start position as selected
        self._selected_index = self.START_POSITION_INDEX
        self._selected_indices = []
        self._start_position_selected = True

        logger.debug("Start position selected")
        return SelectionChangeResult.start_position_selected(previous_indices)

    def add_to_selection(self, beat_index: int) -> SelectionChangeResult:
        """
        Add a beat to the current selection (multi-selection mode).

        Args:
            beat_index: Index of the beat to add

        Returns:
            SelectionChangeResult: Details of the selection change
        """
        if not self._multi_selection_enabled:
            # If multi-selection is disabled, just select the beat
            return self.select_beat(beat_index)

        if not self._is_valid_beat_index(beat_index):
            logger.warning(f"Invalid beat index for addition: {beat_index}")
            return SelectionChangeResult.no_change()

        if beat_index in self._selected_indices:
            # Already selected, no change
            return SelectionChangeResult.no_change()

        previous_indices = self._selected_indices.copy()

        # Add to selection
        self._selected_indices.append(beat_index)
        self._start_position_selected = False

        # Update primary selection if this is the first
        if self._selected_index is None:
            self._selected_index = beat_index

        logger.debug(f"Beat added to selection: {beat_index}")
        return SelectionChangeResult.beat_selected(
            self._selected_index, previous_indices, self._selected_indices
        )

    def remove_from_selection(self, beat_index: int) -> SelectionChangeResult:
        """
        Remove a beat from the current selection.

        Args:
            beat_index: Index of the beat to remove

        Returns:
            SelectionChangeResult: Details of the selection change
        """
        if beat_index not in self._selected_indices:
            # Not selected, no change
            return SelectionChangeResult.no_change()

        previous_indices = self._selected_indices.copy()

        # Remove from selection
        self._selected_indices.remove(beat_index)

        # Update primary selection
        if self._selected_index == beat_index:
            self._selected_index = (
                self._selected_indices[0] if self._selected_indices else None
            )

        logger.debug(f"Beat removed from selection: {beat_index}")
        return SelectionChangeResult.beat_selected(
            self._selected_index, previous_indices, self._selected_indices
        )

    def clear_selection(self) -> SelectionChangeResult:
        """
        Clear all selections.

        Returns:
            SelectionChangeResult: Details of the selection change
        """
        if not self._selected_indices and not self._start_position_selected:
            return SelectionChangeResult.no_change()

        previous_indices = self._selected_indices.copy()

        self._clear_all_internal_selections()

        logger.debug("All selections cleared")
        return SelectionChangeResult.beat_selected(None, previous_indices, [])

    # Keyboard Navigation
    def select_next_beat(self) -> SelectionChangeResult:
        """
        Select the next beat (keyboard navigation).

        Returns:
            SelectionChangeResult: Details of the selection change
        """
        if not self._keyboard_navigation_enabled:
            return SelectionChangeResult.no_change()

        if self._selected_index is None:
            # Select first beat if available
            if self._beat_count > 0:
                return self.select_beat(0)
        else:
            # Select next beat
            next_index = self._selected_index + 1
            if next_index < self._beat_count:
                return self.select_beat(next_index)

        return SelectionChangeResult.no_change()

    def select_previous_beat(self) -> SelectionChangeResult:
        """
        Select the previous beat (keyboard navigation).

        Returns:
            SelectionChangeResult: Details of the selection change
        """
        if not self._keyboard_navigation_enabled:
            return SelectionChangeResult.no_change()

        if self._selected_index is None:
            # Select last beat if available
            if self._beat_count > 0:
                return self.select_beat(self._beat_count - 1)
        else:
            # Select previous beat
            prev_index = self._selected_index - 1
            if prev_index >= 0:
                return self.select_beat(prev_index)

        return SelectionChangeResult.no_change()

    # Query Methods
    def get_selected_index(self) -> int | None:
        """Get the primary selected beat index."""
        return self._selected_index

    def get_selected_indices(self) -> list[int]:
        """Get all selected beat indices."""
        return self._selected_indices.copy()

    def is_beat_selected(self, beat_index: int) -> bool:
        """Check if a specific beat is selected."""
        return beat_index in self._selected_indices

    def is_start_position_selected(self) -> bool:
        """Check if the start position is selected."""
        return self._start_position_selected

    def has_selection(self) -> bool:
        """Check if any selection exists."""
        return bool(self._selected_indices) or self._start_position_selected

    def is_multi_selection_enabled(self) -> bool:
        """Check if multi-selection is enabled."""
        return self._multi_selection_enabled

    def is_keyboard_navigation_enabled(self) -> bool:
        """Check if keyboard navigation is enabled."""
        return self._keyboard_navigation_enabled

    def get_selection_count(self) -> int:
        """Get the number of selected beats."""
        return len(self._selected_indices)

    # Validation
    def _is_valid_beat_index(self, beat_index: int) -> bool:
        """Check if beat index is valid."""
        return 0 <= beat_index < self._beat_count

    def validate_selection_state(self) -> bool:
        """
        Validate current selection state consistency.

        Returns:
            bool: True if state is valid, False otherwise
        """
        # Check that all selected indices are valid
        for idx in self._selected_indices:
            if not self._is_valid_beat_index(idx):
                return False

        # Check that primary selection is in the list
        if self._selected_index is not None:
            if (
                self._selected_index != self.START_POSITION_INDEX
                and self._selected_index not in self._selected_indices
            ):
                return False

        # Check that start position selection is consistent
        if self._start_position_selected:
            if (
                self._selected_index != self.START_POSITION_INDEX
                or self._selected_indices
            ):
                return False

        return True

    # Utility Methods
    def _clear_all_internal_selections(self) -> None:
        """Clear all internal selection state."""
        self._selected_index = None
        self._selected_indices = []
        self._start_position_selected = False

    def get_state_summary(self) -> dict:
        """
        Get a summary of current state for debugging.

        Returns:
            dict: Dictionary containing current state information
        """
        return {
            "selected_index": self._selected_index,
            "selected_indices": self._selected_indices.copy(),
            "start_position_selected": self._start_position_selected,
            "multi_selection_enabled": self._multi_selection_enabled,
            "keyboard_navigation_enabled": self._keyboard_navigation_enabled,
            "beat_count": self._beat_count,
            "selection_count": self.get_selection_count(),
            "has_selection": self.has_selection(),
            "state_valid": self.validate_selection_state(),
        }

    # Missing interface methods implementation
    def select_multiple_beats(self, beat_indices: list[int]) -> bool:
        """Select multiple beats (interface implementation)."""
        try:
            # Clear current selection first
            self._selected_beats.clear()

            # Add all valid indices
            valid_indices = []
            for index in beat_indices:
                if self._is_valid_beat_index(index):
                    self._selected_beats.add(index)
                    valid_indices.append(index)

            # Update primary selection to first valid index
            if valid_indices:
                self._primary_selection = valid_indices[0]
                logger.info(f"✅ [SELECTION] Selected multiple beats: {valid_indices}")
                return True
            else:
                logger.warning("❌ [SELECTION] No valid indices in multiple selection")
                return False
        except Exception as e:
            logger.error(f"❌ [SELECTION] Error in select_multiple_beats: {e}")
            return False

    def deselect_all(self) -> None:
        """Deselect all beats (interface implementation)."""
        try:
            previous_count = len(self._selected_beats)
            self._selected_beats.clear()
            self._primary_selection = None
            logger.info(f"✅ [SELECTION] Deselected all beats (was {previous_count})")
        except Exception as e:
            logger.error(f"❌ [SELECTION] Error in deselect_all: {e}")

    def get_selected_beats(self) -> list[int]:
        """Get list of selected beat indices (interface implementation)."""
        return sorted(list(self._selected_beats))

    def get_primary_selection(self) -> int | None:
        """Get primary selected beat index (interface implementation)."""
        return self._primary_selection
