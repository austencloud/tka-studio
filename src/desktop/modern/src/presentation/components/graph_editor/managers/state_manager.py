"""
Graph Editor State Manager - Simplified
=======================================

Manages state for the graph editor component with simple, direct state management.
Removed over-engineered immutable patterns in favor of straightforward state tracking.
"""

import logging
from typing import TYPE_CHECKING, Optional

from domain.models.beat_data import BeatData
from domain.models.sequence_models import SequenceData
from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor

logger = logging.getLogger(__name__)


class GraphEditorStateManager(QObject):
    """
    Simple state manager for the graph editor.

    Manages core state variables with straightforward getters/setters and
    signal emissions. No over-engineering, just clean state management.

    Responsibilities:
    - Track current sequence and selected beat data
    - Emit signals when state changes
    - Provide simple state access methods
    """

    # Signals for state changes
    visibility_changed = pyqtSignal(bool)  # is_visible
    sequence_changed = pyqtSignal(object)  # SequenceData or None
    selected_beat_changed = pyqtSignal(object, int)  # BeatData or None, beat_index
    selected_arrow_changed = pyqtSignal(str)  # arrow_id

    def __init__(self, graph_editor: "GraphEditor", parent: Optional[QObject] = None):
        super().__init__(parent)
        self._graph_editor = graph_editor

        # Core state variables - simple and direct
        self._is_visible = False
        self._current_sequence: Optional[SequenceData] = None
        self._selected_beat: Optional[BeatData] = None
        self._selected_beat_index: Optional[int] = None
        self._selected_arrow_id: Optional[str] = None

        logger.info("Simple StateManager initialized")

    # Visibility State
    def set_visibility(self, is_visible: bool, emit_signal: bool = True) -> None:
        """Set visibility state with optional signal emission."""
        if self._is_visible != is_visible:
            self._is_visible = is_visible
            if emit_signal:
                self.visibility_changed.emit(is_visible)
            logger.debug(f"Visibility set to: {is_visible}")

    def get_visibility(self) -> bool:
        """Get current visibility state."""
        return self._is_visible

    # Sequence State
    def set_sequence(
        self, sequence: Optional[SequenceData], emit_signal: bool = True
    ) -> None:
        """Set current sequence with optional signal emission."""
        if self._current_sequence != sequence:
            self._current_sequence = sequence
            if emit_signal:
                self.sequence_changed.emit(sequence)
            logger.debug(f"Sequence set: {sequence.name if sequence else 'None'}")

    def get_sequence(self) -> Optional[SequenceData]:
        """Get current sequence."""
        return self._current_sequence

    # Selected Beat State
    def set_selected_beat(
        self,
        beat: Optional[BeatData],
        beat_index: Optional[int] = None,
        emit_signal: bool = True,
    ) -> None:
        """Set selected beat data with optional signal emission."""
        changed = self._selected_beat != beat or self._selected_beat_index != beat_index

        if changed:
            self._selected_beat = beat
            self._selected_beat_index = beat_index
            if emit_signal:
                self.selected_beat_changed.emit(beat, beat_index or -1)
            logger.debug(
                f"Selected beat set: index={beat_index}, beat={beat.letter if beat else 'None'}"
            )

    def get_selected_beat(self) -> Optional[BeatData]:
        """Get currently selected beat."""
        return self._selected_beat

    def get_selected_beat_index(self) -> Optional[int]:
        """Get currently selected beat index."""
        return self._selected_beat_index

    # Selected Arrow State
    def set_selected_arrow(
        self, arrow_id: Optional[str], emit_signal: bool = True
    ) -> None:
        """Set selected arrow ID with optional signal emission."""
        if self._selected_arrow_id != arrow_id:
            self._selected_arrow_id = arrow_id
            if emit_signal and arrow_id:
                self.selected_arrow_changed.emit(arrow_id)
            logger.debug(f"Selected arrow set: {arrow_id}")

    def get_selected_arrow(self) -> Optional[str]:
        """Get currently selected arrow ID."""
        return self._selected_arrow_id

    # Utility Methods
    def clear_selection(self, emit_signals: bool = True) -> None:
        """Clear all selection state."""
        self.set_selected_beat(None, None, emit_signals)
        self.set_selected_arrow(None, emit_signals)
        logger.debug("Selection cleared")

    def get_state_summary(self) -> str:
        """Get a human-readable summary of current state."""
        sequence_name = (
            self._current_sequence.name if self._current_sequence else "None"
        )
        beat_info = (
            f"beat {self._selected_beat_index}"
            if self._selected_beat_index is not None
            else "no beat"
        )
        arrow_info = self._selected_arrow_id if self._selected_arrow_id else "no arrow"

        return f"Sequence: {sequence_name}, Selected: {beat_info}, Arrow: {arrow_info}, Visible: {self._is_visible}"

    def is_beat_selected(self) -> bool:
        """Check if a beat is currently selected."""
        return self._selected_beat is not None and self._selected_beat_index is not None

    def is_arrow_selected(self) -> bool:
        """Check if an arrow is currently selected."""
        return self._selected_arrow_id is not None

    def has_sequence(self) -> bool:
        """Check if a sequence is currently loaded."""
        return self._current_sequence is not None

    # Simple validation - no over-engineering
    def validate_beat_index(self, beat_index: int) -> bool:
        """Simple validation for beat index."""
        if not self._current_sequence:
            return False
        return 0 <= beat_index < len(self._current_sequence.beats)

    def get_beat_count(self) -> int:
        """Get the number of beats in current sequence."""
        return len(self._current_sequence.beats) if self._current_sequence else 0
