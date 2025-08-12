"""
BeatCreationService - Focused Service for Beat Creation

Single Responsibility: Creating new beats from pictographs and calculating beat numbers.
Extracted from SequenceBeatOperations God Object.
"""

from __future__ import annotations

from typing import Optional

from shared.application.services.sequence.beat_factory import BeatFactory

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData


class BeatCreationService:
    """
    Service focused solely on creating new beats.

    Responsibilities:
    - Creating beats from pictographs
    - Calculating next beat numbers
    - Managing beat numbering logic
    """

    def create_beat_from_pictograph(
        self,
        pictograph_data: PictographData,
        current_sequence: Optional[SequenceData] = None,
    ) -> BeatData:
        """
        Create a new beat from pictograph data.

        Args:
            pictograph_data: The pictograph to embed in the beat
            current_sequence: Current sequence to calculate beat number from

        Returns:
            New BeatData with proper beat number
        """
        beat_number = self.calculate_next_beat_number(current_sequence)

        return BeatFactory.create_from_pictograph(
            pictograph_data=pictograph_data, beat_number=beat_number
        )

    def calculate_next_beat_number(
        self, current_sequence: Optional[SequenceData]
    ) -> int:
        """
        Calculate the next beat number for a new beat.

        Args:
            current_sequence: The current sequence state

        Returns:
            Next beat number to use
        """
        if not current_sequence or not current_sequence.beats:
            # Empty sequence, first beat is beat 1
            return 1

        # Check if first beat is a start position (beat_number=0)
        has_start_position = (
            current_sequence.beats[0].metadata.get("is_start_position", False)
            and current_sequence.beats[0].beat_number == 0
        )

        if has_start_position:
            # Regular beats start from 1, so beat_number = number of non-start-position beats + 1
            regular_beats_count = len(current_sequence.beats) - 1
            return regular_beats_count + 1
        # No start position, so beat_number = total beats + 1
        return len(current_sequence.beats) + 1
