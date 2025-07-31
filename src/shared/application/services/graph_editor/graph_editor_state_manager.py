"""
Graph Editor State Service - Pure Business Logic

Extracted from presentation layer to handle all graph editor state management
without any Qt dependencies.
"""

from typing import Optional

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


class GraphEditorStateManager:
    """
    Pure business service for graph editor state management.

    Handles all state transitions, validations, and business rules
    without any presentation layer dependencies.
    """

    def __init__(self):
        """Initialize empty state."""
        self._current_sequence: Optional[SequenceData] = None
        self._selected_beat: Optional[BeatData] = None
        self._selected_beat_index: Optional[int] = None
        self._selected_arrow_id: Optional[str] = None

    def set_sequence(self, sequence: Optional[SequenceData]) -> bool:
        """
        Set current sequence.

        Returns:
            bool: True if sequence actually changed, False otherwise
        """
        if self._current_sequence != sequence:
            self._current_sequence = sequence
            # Clear selection when sequence changes
            self._selected_beat = None
            self._selected_beat_index = None
            self._selected_arrow_id = None
            return True
        return False

    def get_sequence(self) -> Optional[SequenceData]:
        """Get current sequence."""
        return self._current_sequence

    def set_selected_beat(
        self, beat: Optional[BeatData], beat_index: Optional[int] = None
    ) -> bool:
        """
        Set selected beat with validation.

        Returns:
            bool: True if selection actually changed, False otherwise
        """
        # Validate beat index if provided
        if beat_index is not None and not self.validate_beat_index(beat_index):
            return False

        changed = self._selected_beat != beat or self._selected_beat_index != beat_index

        if changed:
            self._selected_beat = beat
            self._selected_beat_index = beat_index
            # Clear arrow selection when beat selection changes
            self._selected_arrow_id = None
            return True
        return False

    def get_selected_beat(self) -> Optional[BeatData]:
        """Get currently selected beat."""
        return self._selected_beat

    def get_selected_beat_index(self) -> Optional[int]:
        """Get currently selected beat index."""
        return self._selected_beat_index

    def set_selected_arrow(self, arrow_id: Optional[str]) -> bool:
        """
        Set selected arrow.

        Returns:
            bool: True if selection actually changed, False otherwise
        """
        if self._selected_arrow_id != arrow_id:
            self._selected_arrow_id = arrow_id
            return True
        return False

    def get_selected_arrow(self) -> Optional[str]:
        """Get currently selected arrow ID."""
        return self._selected_arrow_id

    def clear_selection(self) -> bool:
        """
        Clear all selection state.

        Returns:
            bool: True if anything was actually cleared, False if already clear
        """
        had_selection = (
            self._selected_beat is not None
            or self._selected_beat_index is not None
            or self._selected_arrow_id is not None
        )

        self._selected_beat = None
        self._selected_beat_index = None
        self._selected_arrow_id = None

        return had_selection

    def validate_beat_index(self, beat_index: int) -> bool:
        """
        Validate beat index against current sequence.

        Args:
            beat_index: Index to validate

        Returns:
            bool: True if index is valid for current sequence
        """
        if not self._current_sequence:
            return False
        return 0 <= beat_index < len(self._current_sequence.beats)

    def get_beat_count(self) -> int:
        """Get the number of beats in current sequence."""
        return len(self._current_sequence.beats) if self._current_sequence else 0

    def is_beat_selected(self) -> bool:
        """Check if a beat is currently selected."""
        return self._selected_beat is not None and self._selected_beat_index is not None

    def is_arrow_selected(self) -> bool:
        """Check if an arrow is currently selected."""
        return self._selected_arrow_id is not None

    def has_sequence(self) -> bool:
        """Check if a sequence is currently loaded."""
        return self._current_sequence is not None

    def get_state_summary(self) -> dict:
        """
        Get a summary of current state for debugging.

        Returns:
            dict: State summary with all current values
        """
        return {
            "sequence_name": (
                self._current_sequence.name if self._current_sequence else None
            ),
            "selected_beat_index": self._selected_beat_index,
            "selected_beat_letter": (
                self._selected_beat.letter if self._selected_beat else None
            ),
            "selected_arrow": self._selected_arrow_id,
            "has_sequence": self.has_sequence(),
            "beat_count": self.get_beat_count(),
        }
