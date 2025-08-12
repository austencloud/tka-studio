"""
Graph Editor Data Flow Service

Handles the complete beat selection → modification → propagation flow for the graph editor.
This service bridges graph editor changes to beat repository and UI components with real-time propagation.
"""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

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
        self._current_sequence: SequenceData | None = None
        self._current_beat_index: int | None = None
        self._sequence_service: ISequenceManager | None = None

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

    def get_current_sequence(self) -> SequenceData | None:
        """Get the current sequence"""
        return self._current_sequence

    def get_current_beat_index(self) -> int | None:
        """Get the current beat index"""
        return self._current_beat_index
