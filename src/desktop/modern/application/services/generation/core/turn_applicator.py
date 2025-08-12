"""
Turn Applicator - Practical Generation Architecture

Handles turn application using the ACTUAL legacy turn logic.
Fixed to match how the legacy TurnIntensityManager really works.
"""

from __future__ import annotations

import logging
import random

from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData


logger = logging.getLogger(__name__)


class TurnApplicator:
    """
    Turn application using REAL legacy turn logic.

    FIXED: Now uses the actual legacy turn allocation algorithm
    instead of my completely wrong assumptions.
    """

    def apply_turns_to_pictograph(
        self,
        pictograph: PictographData,
        blue_turns: int | float | str,
        red_turns: int | float | str,
    ) -> PictographData:
        """
        Apply specific turn values to a pictograph.

        Args:
            pictograph: The pictograph to apply turns to
            blue_turns: Turn value for blue prop (from legacy allocation)
            red_turns: Turn value for red prop (from legacy allocation)

        Returns:
            PictographData with turns applied
        """
        try:
            # Apply turns to motions
            updated_motions = {}

            if "blue" in pictograph.motions:
                blue_motion = pictograph.motions["blue"]
                updated_blue = self._apply_turns_to_motion(blue_motion, blue_turns)
                updated_motions["blue"] = updated_blue

            if "red" in pictograph.motions:
                red_motion = pictograph.motions["red"]
                updated_red = self._apply_turns_to_motion(red_motion, red_turns)
                updated_motions["red"] = updated_red

            # Create new pictograph with updated motions
            return PictographData(
                letter=pictograph.letter,
                start_position=pictograph.start_position,
                end_position=pictograph.end_position,
                beat=pictograph.beat,
                motions=updated_motions,
                metadata=pictograph.metadata,
            )

        except Exception as e:
            logger.exception(f"Failed to apply turns: {e}")
            return pictograph  # Return original on error

    def allocate_turns_for_sequence(
        self, sequence_length: int, level: int, turn_intensity: float
    ) -> tuple[list[int | float | str], list[int | float | str]]:
        """
        Allocate turns for entire sequence using REAL legacy logic.

        This is the ACTUAL algorithm from legacy TurnIntensityManager.
        """
        # Determine possible turns based on level (EXACT legacy logic)
        if level == 2:
            possible_turns = [0, 1, 2, 3]
        elif level == 3:
            possible_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3, "fl"]
        else:
            # Level 1 or other levels: no turns
            return ([0] * sequence_length, [0] * sequence_length)

        blue_turns = []
        red_turns = []

        for _i in range(sequence_length):
            # Filter possible turns by turn_intensity (EXACT legacy logic)
            valid_turns = [
                t
                for t in possible_turns
                if t == "fl" or (isinstance(t, (int, float)) and t <= turn_intensity)
            ]

            # Random selection from valid turns (EXACT legacy logic)
            blue_turn = random.choice(valid_turns)
            red_turn = random.choice(valid_turns)

            blue_turns.append(blue_turn)
            red_turns.append(red_turn)

        logger.debug(f"Allocated turns for level {level}: {len(blue_turns)} beats")
        return blue_turns, red_turns

    def _apply_turns_to_motion(self, motion: MotionData, turns: float) -> MotionData:
        """
        Apply turns to a motion data object.

        Args:
            motion: Original motion data
            turns: Number of turns to apply

        Returns:
            MotionData with turns applied
        """
        try:
            # Create new motion with turns
            return MotionData(
                motion_type=motion.motion_type,
                prop_rot_dir=motion.prop_rot_dir,
                start_loc=motion.start_loc,
                end_loc=motion.end_loc,
                turns=turns,
            )
        except Exception as e:
            logger.exception(f"Failed to apply turns to motion: {e}")
            return motion  # Return original on error
