"""
BeatSequenceService - Focused Service for Sequence Manipulation

Single Responsibility: Adding, removing, and updating beats within sequences.
Extracted from SequenceBeatOperations God Object.
"""

from __future__ import annotations

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


class BeatSequenceService:
    """
    Service focused solely on sequence manipulation operations.

    Responsibilities:
    - Adding beats to sequences
    - Removing beats from sequences
    - Updating beat properties
    - Managing beat numbering within sequences
    """

    def add_beat(self, sequence: SequenceData, beat: BeatData) -> SequenceData:
        """
        Add a beat to the end of the sequence.

        Args:
            sequence: The sequence to add to
            beat: The beat to add

        Returns:
            New sequence with beat added
        """
        if sequence is None:
            sequence = SequenceData.empty()

        return sequence.add_beat(beat)

    def remove_beat(self, sequence: SequenceData, index: int) -> SequenceData:
        """
        Remove a single beat from the sequence.

        Args:
            sequence: The sequence to remove from
            index: Index of beat to remove

        Returns:
            New sequence with beat removed

        Raises:
            ValueError: If index is invalid
        """
        if not sequence or index < 0 or index >= len(sequence.beats):
            raise ValueError(f"Invalid beat index: {index}")

        updated_beats = list(sequence.beats)
        updated_beats.pop(index)

        # Renumber remaining beats
        for i, beat in enumerate(updated_beats):
            updated_beats[i] = beat.update(beat_number=i + 1)

        return sequence.update(beats=updated_beats)

    def delete_beat_and_following(
        self, sequence: SequenceData, index: int
    ) -> SequenceData:
        """
        Delete beat and all following beats from the sequence (legacy behavior).

        Args:
            sequence: The sequence to modify
            index: Index of the beat to delete (and all following)

        Returns:
            Updated sequence with beat and following beats removed

        Raises:
            ValueError: If index is invalid
        """
        if not sequence or index < 0 or index >= len(sequence.beats):
            raise ValueError(f"Invalid beat index: {index}")

        # Keep only beats before the deletion point
        remaining_beats = list(sequence.beats[:index])

        return sequence.update(beats=remaining_beats)

    def update_beat_turns(
        self, sequence: SequenceData, beat_index: int, color: str, new_turns: int
    ) -> SequenceData:
        """
        Update the number of turns for a specific beat's motion.

        Args:
            sequence: The sequence containing the beat
            beat_index: Index of the beat to update
            color: Color/side of the motion to update
            new_turns: New number of turns

        Returns:
            Updated sequence with modified beat

        Raises:
            ValueError: If beat_index is invalid or color not found
        """
        if not sequence or beat_index >= len(sequence.beats):
            raise ValueError(f"Invalid beat index: {beat_index}")

        beat = sequence.beats[beat_index]

        if not beat.has_pictograph or color.lower() not in beat.pictograph_data.motions:
            raise ValueError(f"Invalid color '{color}' or missing motion data")

        # Update the motion
        motion = beat.pictograph_data.motions[color.lower()]
        updated_motion = motion.update(turns=new_turns)

        # Update the pictograph data
        updated_motions = {
            **beat.pictograph_data.motions,
            color.lower(): updated_motion,
        }
        updated_pictograph = beat.pictograph_data.update(motions=updated_motions)
        updated_beat = beat.update(pictograph_data=updated_pictograph)

        # Update sequence
        new_beats = sequence.beats.copy()
        new_beats[beat_index] = updated_beat

        return sequence.update(beats=new_beats)

    def update_beat_orientation(
        self, sequence: SequenceData, beat_index: int, color: str, new_orientation: int
    ) -> SequenceData:
        """
        Update the orientation for a specific beat's motion.

        Args:
            sequence: The sequence containing the beat
            beat_index: Index of the beat to update
            color: Color/side of the motion to update
            new_orientation: New orientation value

        Returns:
            Updated sequence with modified beat

        Raises:
            ValueError: If beat_index is invalid or color not found
        """
        if not sequence or beat_index >= len(sequence.beats):
            raise ValueError(f"Invalid beat index: {beat_index}")

        beat = sequence.beats[beat_index]

        if not beat.has_pictograph or color.lower() not in beat.pictograph_data.motions:
            raise ValueError(f"Invalid color '{color}' or missing motion data")

        # Update the motion
        motion = beat.pictograph_data.motions[color.lower()]
        updated_motion = motion.update(
            start_ori=new_orientation, end_ori=new_orientation
        )

        # Update the pictograph data
        updated_motions = {
            **beat.pictograph_data.motions,
            color.lower(): updated_motion,
        }
        updated_pictograph = beat.pictograph_data.update(motions=updated_motions)
        updated_beat = beat.update(pictograph_data=updated_pictograph)

        # Update sequence
        new_beats = sequence.beats.copy()
        new_beats[beat_index] = updated_beat

        return sequence.update(beats=new_beats)
