"""
Graph Editor Data Flow Service

Handles the complete beat selection → modification → propagation flow for the graph editor.
This service bridges graph editor changes to beat repository and UI components with real-time propagation.
"""

from dataclasses import replace
from typing import TYPE_CHECKING, Optional

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import MotionType
from desktop.modern.domain.models.sequence_data import SequenceData

if TYPE_CHECKING:
    from desktop.modern.core.interfaces.core_services import ISequenceManager


class GraphEditorDataFlowManager(QObject):
    """Bridges graph editor changes to beat frame and pictograph updates"""

    # Signals for real-time UI updates
    beat_data_updated = pyqtSignal(
        BeatData, int
    )  # beat_data, beat_index (includes pictograph refresh)
    sequence_modified = pyqtSignal(SequenceData)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_sequence: Optional[SequenceData] = None
        self._current_beat_index: Optional[int] = None
        self._sequence_service: Optional[ISequenceManager] = None

    def set_context(self, sequence: SequenceData, beat_index: int):
        """Set current sequence and beat context"""
        self._current_sequence = sequence
        self._current_beat_index = beat_index

    def set_sequence_service(self, sequence_service: "ISequenceManager"):
        """Set the sequence management service for persistence"""
        self._sequence_service = sequence_service

    def process_turn_change(
        self, beat_data: BeatData, arrow_color: str, new_turns: float
    ) -> BeatData:
        """Process turn change and trigger all necessary updates"""
        # 1. Apply the change to beat data
        updated_beat = beat_data

        if arrow_color == "blue" and beat_data.blue_motion:
            updated_motion = replace(beat_data.blue_motion, turns=new_turns)
            updated_beat = beat_data.update(blue_motion=updated_motion)
        elif arrow_color == "red" and beat_data.red_motion:
            updated_motion = replace(beat_data.red_motion, turns=new_turns)
            updated_beat = beat_data.update(red_motion=updated_motion)

        # 2. Update sequence if we have context
        if self._current_sequence and self._current_beat_index is not None:
            beats = list(self._current_sequence.beats)
            if self._current_beat_index < len(beats):
                beats[self._current_beat_index] = updated_beat
                self._current_sequence = self._current_sequence.update(beats=beats)

                # Persist through sequence service if available
                if self._sequence_service:
                    # TODO: Add persistence method to sequence service
                    pass

        # 3. Emit consolidated signal for UI updates (includes pictograph refresh)
        self.beat_data_updated.emit(updated_beat, self._current_beat_index or 0)

        if self._current_sequence:
            self.sequence_modified.emit(self._current_sequence)

        return updated_beat

    def process_orientation_change(
        self, beat_data: BeatData, arrow_color: str, new_orientation: str
    ) -> BeatData:
        """Process orientation change and trigger all necessary updates"""
        # 1. Apply the change to beat data
        updated_beat = beat_data

        try:
            motion_type = MotionType(new_orientation)

            if arrow_color == "blue" and beat_data.blue_motion:
                updated_motion = replace(beat_data.blue_motion, motion_type=motion_type)
                updated_beat = beat_data.update(blue_motion=updated_motion)
            elif arrow_color == "red" and beat_data.red_motion:
                updated_motion = replace(beat_data.red_motion, motion_type=motion_type)
                updated_beat = beat_data.update(red_motion=updated_motion)
        except ValueError:
            # Invalid motion type, return original beat
            return beat_data

        # 2. Update sequence if we have context
        if self._current_sequence and self._current_beat_index is not None:
            beats = list(self._current_sequence.beats)
            if self._current_beat_index < len(beats):
                beats[self._current_beat_index] = updated_beat
                self._current_sequence = self._current_sequence.update(beats=beats)

                # Persist through sequence service if available
                if self._sequence_service:
                    # TODO: Add persistence method to sequence service
                    pass

        # 3. Emit consolidated signal for UI updates (includes pictograph refresh)
        self.beat_data_updated.emit(updated_beat, self._current_beat_index or 0)

        if self._current_sequence:
            self.sequence_modified.emit(self._current_sequence)

        return updated_beat

    def determine_panel_mode(self, beat_data: Optional[BeatData]) -> str:
        """Determine whether to show orientation picker or turns controls"""
        if not beat_data:
            return "orientation"

        # Check if this is start position using multiple indicators for robustness
        is_start = (
            getattr(beat_data, "is_start_position", False)
            or getattr(beat_data, "beat_number", 1) == 0
            or getattr(beat_data, "sequence_position", 1) == 0
            or str(getattr(beat_data, "beat_number", "1")).lower()
            in ["start", "0", "start_pos"]
            or beat_data.metadata.get("is_start_position", False)
        )

        return "orientation" if is_start else "turns"

    def get_current_sequence(self) -> Optional[SequenceData]:
        """Get the current sequence"""
        return self._current_sequence

    def get_current_beat_index(self) -> Optional[int]:
        """Get the current beat index"""
        return self._current_beat_index
