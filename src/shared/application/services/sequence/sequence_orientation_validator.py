"""
Sequence Orientation Validation Manager

Modern service for validating and ensuring orientation continuity in sequences.
This service analyzes the current sequence state, validates orientation continuity
between pictographs, and ensures correct orientation transitions based on motion types.

This addresses the critical bug where the option picker incorrectly assumes all options
start from "in" orientation instead of dynamically determining starting orientation
from the actual sequence context.
"""

import logging
from typing import Optional

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import Orientation
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


class SequenceOrientationValidator:
    """
    Service for validating and managing orientation continuity in sequences.

    Modern implementation that:
    1. Analyzes current sequence state to extract actual end orientations
    2. Validates orientation continuity between consecutive pictographs
    3. Ensures correct orientation transitions based on motion types
    4. Provides accurate starting orientations for new pictograph options
    """

    def __init__(self):
        """Initialize the sequence orientation validator."""
        self._default_orientations = {"blue": Orientation.IN, "red": Orientation.OUT}

    def get_sequence_end_orientations(
        self, sequence: SequenceData
    ) -> dict[str, Orientation]:
        """
        Extract the actual end orientations from the last valid beat in the sequence.

        This is the core method that fixes the bug where options incorrectly
        assume "in" orientation instead of using the actual sequence context.

        Args:
            sequence: The current sequence data

        Returns:
            Dictionary mapping color to actual end orientation from sequence
        """
        # DEBUG: Add logging to trace sequence data (simplified)
        if sequence and sequence.beats:
            logger.debug(f"Processing sequence with {len(sequence.beats)} beats")
        else:
            logger.debug("No sequence or beats found")
            logger.debug("No sequence or beats found")

        if not sequence or not sequence.beats:
            logger.debug("No sequence or beats found, using default orientations")
            logger.debug(
                f"Returning default orientations: {self._default_orientations}"
            )
            return self._default_orientations.copy()

        # Find the last valid beat (non-blank, non-placeholder)
        last_valid_beat = self._get_last_valid_beat(sequence)
        if not last_valid_beat:
            logger.debug("No valid last beat found, using default orientations")
            return self._default_orientations.copy()

        # Extract end orientations from the last valid beat
        end_orientations = self._extract_beat_end_orientations(last_valid_beat)

        logger.debug(
            f"Extracted end orientations from sequence: "
            f"blue={end_orientations['blue'].value}, red={end_orientations['red'].value}"
        )

        return end_orientations

    def validate_sequence_orientation_continuity(
        self, sequence: SequenceData
    ) -> tuple[bool, list[str]]:
        """
        Validate that orientations flow correctly throughout the entire sequence.

        Args:
            sequence: The sequence to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        if not sequence or not sequence.beats:
            return True, []

        errors = []
        regular_beats = [
            beat
            for beat in sequence.beats
            if not beat.is_blank and beat.beat_number > 0
        ]

        if len(regular_beats) < 2:
            return True, []  # Need at least 2 beats to check continuity

        # Check continuity between consecutive beats
        for i in range(1, len(regular_beats)):
            previous_beat = regular_beats[i - 1]
            current_beat = regular_beats[i]

            continuity_errors = self._validate_beat_continuity(
                previous_beat, current_beat
            )
            errors.extend(continuity_errors)

        is_valid = len(errors) == 0
        if not is_valid:
            logger.warning(
                f"Sequence orientation continuity validation failed: {errors}"
            )

        return is_valid, errors

    def calculate_option_start_orientations(
        self, sequence: SequenceData, options: list[PictographData]
    ) -> list[PictographData]:
        """
        Update pictograph options with correct start orientations based on sequence context.

        This is the main method that fixes the option picker bug by ensuring
        options start with the correct orientations from the sequence context.

        Args:
            sequence: The current sequence data
            options: List of pictograph options to update

        Returns:
            List of updated pictograph options with correct start orientations
        """
        if not options:
            return options

        # Get the actual end orientations from the sequence
        sequence_end_orientations = self.get_sequence_end_orientations(sequence)
        logger.debug(
            f"Sequence end orientations: Blue={sequence_end_orientations['blue']}, Red={sequence_end_orientations['red']}"
        )

        updated_options = []
        for i, option in enumerate(options):
            updated_option = self._update_option_start_orientations(
                option, sequence_end_orientations
            )
            updated_options.append(updated_option)

            # Debug first option only
            if i == 0:
                blue_motion = updated_option.motions.get("blue")
                red_motion = updated_option.motions.get("red")
                blue_start = blue_motion.start_ori if blue_motion else "None"
                red_start = red_motion.start_ori if red_motion else "None"
                logger.debug(
                    f"First option ({updated_option.letter}): Blue={blue_start}, Red={red_start}"
                )

        logger.debug(f"Updated start orientations for {len(updated_options)} options")
        return updated_options

    def _get_last_valid_beat(self, sequence: SequenceData) -> Optional[BeatData]:
        """
        Get the last valid beat from sequence, excluding blank beats and placeholders.
        """
        if not sequence.beats:
            return None

        # Check beats from last to first
        for beat in reversed(sequence.beats):
            if not beat.is_blank and beat.beat_number > 0:
                return beat

        return None

    def _extract_beat_end_orientations(self, beat: BeatData) -> dict[str, Orientation]:
        """
        Extract end orientations from a beat's pictograph data.

        Returns:
            Dictionary mapping color to end orientation
        """
        end_orientations = self._default_orientations.copy()

        if not beat.pictograph_data or not beat.pictograph_data.motions:
            return end_orientations

        # Extract end orientations from motion data
        for color in ["blue", "red"]:
            if color in beat.pictograph_data.motions:
                motion = beat.pictograph_data.motions[color]
                if motion and hasattr(motion, "end_ori"):
                    end_orientations[color] = motion.end_ori

        return end_orientations

    def _validate_beat_continuity(
        self, previous_beat: BeatData, current_beat: BeatData
    ) -> list[str]:
        """
        Validate orientation continuity between two consecutive beats.

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        if not previous_beat.pictograph_data or not current_beat.pictograph_data:
            return errors

        prev_motions = previous_beat.pictograph_data.motions
        curr_motions = current_beat.pictograph_data.motions

        for color in ["blue", "red"]:
            if color in prev_motions and color in curr_motions:
                prev_motion = prev_motions[color]
                curr_motion = curr_motions[color]

                if prev_motion and curr_motion:
                    prev_end_ori = getattr(prev_motion, "end_ori", None)
                    curr_start_ori = getattr(curr_motion, "start_ori", None)

                    if (
                        prev_end_ori
                        and curr_start_ori
                        and prev_end_ori != curr_start_ori
                    ):
                        errors.append(
                            f"Orientation discontinuity in {color} between beats "
                            f"{previous_beat.beat_number} and {current_beat.beat_number}: "
                            f"{prev_end_ori.value} -> {curr_start_ori.value}"
                        )

        return errors

    def _update_option_start_orientations(
        self, option: PictographData, sequence_end_orientations: dict[str, Orientation]
    ) -> PictographData:
        """
        Update a single pictograph option with correct start orientations.
        Also calculates correct end orientations and updates prop orientations.

        FIXED: Following legacy pattern - props use motion END orientations.
        """
        updated_motions = {}
        updated_props = {}

        # Import orientation calculator for end orientation calculation
        from shared.application.services.positioning.arrows.calculation.orientation_calculator import (
            OrientationCalculator,
        )

        orientation_calculator = OrientationCalculator()

        # Update motion start orientations and calculate end orientations
        for color in ["blue", "red"]:
            motion_start_ori = sequence_end_orientations[color]

            if color in option.motions:
                original_motion = option.motions[color]

                # Update motion with correct start orientation
                motion_with_start = original_motion.update(start_ori=motion_start_ori)

                # Calculate correct end orientation based on motion type and turns
                calculated_end_ori = orientation_calculator.calculate_end_orientation(
                    motion_with_start, motion_start_ori
                )

                # Update motion with both correct start and calculated end orientations
                updated_motion = motion_with_start.update(end_ori=calculated_end_ori)
                updated_motions[color] = updated_motion

                # FIXED: Update prop orientation to match motion END orientation (legacy pattern)
                if color in option.props:
                    original_prop = option.props[color]
                    # Prop uses motion's END orientation (not start)
                    from dataclasses import replace

                    updated_prop = replace(
                        original_prop, orientation=calculated_end_ori
                    )
                    updated_props[color] = updated_prop

                    logger.debug(
                        f"Updated {color} prop orientation: {motion_start_ori} → {calculated_end_ori}"
                    )
                else:
                    updated_props[color] = option.props.get(color)
            else:
                updated_motions[color] = option.motions.get(color)
                updated_props[color] = option.props.get(color)

        # Create updated pictograph with corrected orientations
        from dataclasses import replace

        return replace(option, motions=updated_motions, props=updated_props)

    def validate_and_fix_sequence_orientations(
        self, sequence: SequenceData
    ) -> tuple[SequenceData, list[str]]:
        """
        Validate sequence orientation continuity and fix any issues found.

        This method can be used to repair sequences with orientation discontinuities.

        Args:
            sequence: The sequence to validate and fix

        Returns:
            Tuple of (fixed_sequence, list_of_fixes_applied)
        """
        if not sequence or not sequence.beats:
            return sequence, []

        fixes_applied = []
        updated_beats = []

        regular_beats = [
            beat
            for beat in sequence.beats
            if not beat.is_blank and beat.beat_number > 0
        ]

        if len(regular_beats) < 2:
            return sequence, []  # Nothing to fix

        # Process beats to ensure continuity
        updated_beats.append(regular_beats[0])  # First beat is reference

        for i in range(1, len(regular_beats)):
            previous_beat = updated_beats[-1]
            current_beat = regular_beats[i]

            # Check if current beat needs orientation fixes
            fixed_beat, beat_fixes = self._fix_beat_orientations(
                previous_beat, current_beat
            )
            updated_beats.append(fixed_beat)
            fixes_applied.extend(beat_fixes)

        # Reconstruct sequence with fixed beats
        from dataclasses import replace

        fixed_sequence = replace(sequence, beats=updated_beats)

        return fixed_sequence, fixes_applied

    def _fix_beat_orientations(
        self, previous_beat: BeatData, current_beat: BeatData
    ) -> tuple[BeatData, list[str]]:
        """
        Fix orientation continuity issues in a single beat.

        Returns:
            Tuple of (fixed_beat, list_of_fixes_applied)
        """
        fixes_applied = []

        if not previous_beat.pictograph_data or not current_beat.pictograph_data:
            return current_beat, fixes_applied

        prev_motions = previous_beat.pictograph_data.motions
        curr_motions = current_beat.pictograph_data.motions
        updated_motions = curr_motions.copy()

        for color in ["blue", "red"]:
            if color in prev_motions and color in curr_motions:
                prev_motion = prev_motions[color]
                curr_motion = curr_motions[color]

                if prev_motion and curr_motion:
                    prev_end_ori = getattr(prev_motion, "end_ori", None)
                    curr_start_ori = getattr(curr_motion, "start_ori", None)

                    if (
                        prev_end_ori
                        and curr_start_ori
                        and prev_end_ori != curr_start_ori
                    ):
                        # Fix the discontinuity by updating current beat's start orientation
                        fixed_motion = curr_motion.update(start_ori=prev_end_ori)

                        # Recalculate end orientation with the fixed start
                        from shared.application.services.positioning.arrows.calculation.orientation_calculator import (
                            OrientationCalculator,
                        )

                        orientation_calculator = OrientationCalculator()
                        calculated_end_ori = (
                            orientation_calculator.calculate_end_orientation(
                                fixed_motion, prev_end_ori
                            )
                        )

                        final_motion = fixed_motion.update(end_ori=calculated_end_ori)
                        updated_motions[color] = final_motion

                        fixes_applied.append(
                            f"Fixed {color} orientation discontinuity in beat {current_beat.beat_number}: "
                            f"{curr_start_ori.value} -> {prev_end_ori.value}"
                        )

        # Update pictograph data with fixed motions
        if updated_motions != curr_motions:
            from dataclasses import replace

            updated_pictograph = replace(
                current_beat.pictograph_data, motions=updated_motions
            )
            fixed_beat = replace(current_beat, pictograph_data=updated_pictograph)
            return fixed_beat, fixes_applied

        return current_beat, fixes_applied
