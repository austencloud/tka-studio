"""
Graph Editor State Manager - Qt Presentation Adapter

Thin adapter that delegates business logic to GraphEditorStateService
while handling Qt-specific concerns (signals, UI state).
"""

import logging
from typing import TYPE_CHECKING, Optional

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData
from shared.application.services.graph_editor.graph_editor_state_manager import (
    GraphEditorStateManager as GraphEditorStateService,
)

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor

logger = logging.getLogger(__name__)


class GraphEditorStateManager(QObject):
    """
    Qt presentation adapter for graph editor state management.

    Handles Qt signals and UI state while delegating all business logic
    to the GraphEditorStateService.
    """

    # Qt signals for state changes
    visibility_changed = pyqtSignal(bool)  # is_visible
    sequence_changed = pyqtSignal(object)  # SequenceData or None
    selected_beat_changed = pyqtSignal(object, int)  # BeatData or None, beat_index
    selected_arrow_changed = pyqtSignal(str)  # arrow_id

    def __init__(
        self,
        graph_editor: "GraphEditor",
        state_service: Optional[GraphEditorStateService] = None,
        parent: Optional[QObject] = None,
    ):
        super().__init__(parent)
        self._graph_editor = graph_editor

        # Use injected service or create fallback for backward compatibility
        self._state_service = state_service or GraphEditorStateService()

        # Qt-specific state (presentation only)
        self._is_visible = False

        logger.info("Graph Editor State Manager initialized with service delegation")

    # Visibility management (pure Qt presentation concern)
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

    # Sequence management (delegate to service)
    def set_sequence(
        self, sequence: Optional[SequenceData], emit_signal: bool = True
    ) -> None:
        """Set current sequence with optional signal emission."""
        if self._state_service.set_sequence(sequence):
            if emit_signal:
                self.sequence_changed.emit(sequence)
            logger.debug(f"Sequence set: {sequence.name if sequence else 'None'}")

    def get_sequence(self) -> Optional[SequenceData]:
        """Get current sequence."""
        return self._state_service.get_sequence()

    # Beat selection management (delegate to service)
    def set_selected_beat(
        self,
        beat: Optional[BeatData],
        beat_index: Optional[int] = None,
        emit_signal: bool = True,
    ) -> None:
        """Set selected beat data with optional signal emission."""
        if self._state_service.set_selected_beat(beat, beat_index):
            if emit_signal:
                self.selected_beat_changed.emit(beat, beat_index or -1)
            logger.debug(
                f"Selected beat set: index={beat_index}, beat={beat.letter if beat else 'None'}"
            )

    def get_selected_beat(self) -> Optional[BeatData]:
        """Get currently selected beat."""
        return self._state_service.get_selected_beat()

    def get_selected_beat_index(self) -> Optional[int]:
        """Get currently selected beat index."""
        return self._state_service.get_selected_beat_index()

    # Arrow selection management (delegate to service)
    def set_selected_arrow(
        self, arrow_id: Optional[str], emit_signal: bool = True
    ) -> None:
        """Set selected arrow ID with optional signal emission."""
        if self._state_service.set_selected_arrow(arrow_id):
            if emit_signal and arrow_id:
                self.selected_arrow_changed.emit(arrow_id)
            logger.debug(f"Selected arrow set: {arrow_id}")

    def get_selected_arrow(self) -> Optional[str]:
        """Get currently selected arrow ID."""
        return self._state_service.get_selected_arrow()

    # Utility methods (delegate to service)
    def clear_selection(self, emit_signals: bool = True) -> None:
        """Clear all selection state."""
        if self._state_service.clear_selection():
            if emit_signals:
                self.selected_beat_changed.emit(None, -1)
                self.selected_arrow_changed.emit("")
            logger.debug("Selection cleared")

    def get_state_summary(self) -> str:
        """Get a human-readable summary of current state."""
        state = self._state_service.get_state_summary()
        return f"Sequence: {state['sequence_name']}, Selected: beat {state['selected_beat_index']}, Arrow: {state['selected_arrow']}, Visible: {self._is_visible}"

    def is_beat_selected(self) -> bool:
        """Check if a beat is currently selected."""
        return self._state_service.is_beat_selected()

    def is_arrow_selected(self) -> bool:
        """Check if an arrow is currently selected."""
        return self._state_service.is_arrow_selected()

    def has_sequence(self) -> bool:
        """Check if a sequence is currently loaded."""
        return self._state_service.has_sequence()

    def validate_beat_index(self, beat_index: int) -> bool:
        """Validate beat index using service."""
        return self._state_service.validate_beat_index(beat_index)

    def get_beat_count(self) -> int:
        """Get the number of beats in current sequence."""
        return self._state_service.get_beat_count()
