"""
Option Orientation Update Service

Modern service for updating orientations of option beats based on sequence context.
This service handles updating start orientations of option beats based on the end orientations
of the last beat in a sequence, then calculates new end orientations.

This ensures that options display with correct orientations that flow from the sequence context,
rather than using default "in,in" orientations.
"""

import logging
from typing import List, Optional
from dataclasses import replace

from domain.models.core_models import BeatData, SequenceData, Orientation
from application.services.positioning.arrows.calculation.orientation_calculator import (
    OrientationCalculator,
)

logger = logging.getLogger(__name__)


class OptionOrientationUpdateService:
    """
    Service for updating orientations of option beats based on sequence context.

    Modern implementation that:
    1. Extract end orientations from last beat in sequence
    2. Set those as start orientations for all option beats
    3. Calculate new end orientations using orientation calculator
    """

    def __init__(self, orientation_calculator: Optional[OrientationCalculator] = None):
        """
        Initialize the orientation update service.

        Args:
            orientation_calculator: Calculator for end orientations (optional, will create if None)
        """
        self.orientation_calculator = orientation_calculator or OrientationCalculator()

    def update_option_orientations(
        self, sequence: SequenceData, options: List[BeatData]
    ) -> List[BeatData]:
        """
        Update orientations for option beats based on sequence context.

        Modern implementation that:
        - Extract end orientations from last beat in sequence
        - Set those as start orientations for all options
        - Calculate new end orientations using modern orientation calculator

        Args:
            sequence: The current sequence data
            options: List of option beats to update

        Returns:
            List of updated BeatData objects with corrected orientations
        """
        if not sequence or sequence.length == 0 or not options:
            logger.debug("No sequence or options to update orientations for")
            return options

        # Get the last beat from sequence (excluding placeholders)
        last_beat = self._get_last_valid_beat(sequence)
        if not last_beat:
            logger.debug("No valid last beat found in sequence")
            return options

        # Extract end orientations from last beat
        last_blue_end_ori, last_red_end_ori = self._extract_end_orientations(last_beat)
        if not last_blue_end_ori or not last_red_end_ori:
            logger.debug("Could not extract end orientations from last beat")
            return options

        logger.debug(
            f"Updating {len(options)} options with start orientations: blue={last_blue_end_ori}, red={last_red_end_ori}"
        )

        # Update each option
        updated_options = []
        for option in options:
            updated_option = self._update_single_option_orientation(
                option, last_blue_end_ori, last_red_end_ori
            )
            updated_options.append(updated_option)

        logger.debug(f"Updated orientations for {len(updated_options)} options")
        return updated_options

    def _get_last_valid_beat(self, sequence: SequenceData) -> Optional[BeatData]:
        """
        Get the last valid beat from sequence, excluding blank beats.

        Modern implementation that finds the last beat with actual motion data.
        """
        if not sequence.beats:
            return None

        # Check last beat first
        last_beat = sequence.beats[-1]
        if not last_beat.is_blank:
            return last_beat

        # If last beat is blank, try second to last
        if len(sequence.beats) >= 2:
            second_last = sequence.beats[-2]
            if not second_last.is_blank:
                return second_last

        return None

    def _extract_end_orientations(
        self, beat: BeatData
    ) -> tuple[Optional[str], Optional[str]]:
        """
        Extract end orientations from a beat.

        Returns:
            Tuple of (blue_end_ori, red_end_ori) as strings
        """
        blue_end_ori = None
        red_end_ori = None

        if beat.blue_motion and hasattr(beat.blue_motion, "end_ori"):
            blue_end_ori = beat.blue_motion.end_ori

        if beat.red_motion and hasattr(beat.red_motion, "end_ori"):
            red_end_ori = beat.red_motion.end_ori

        return blue_end_ori, red_end_ori

    def _update_single_option_orientation(
        self, option: BeatData, blue_start_ori: str, red_start_ori: str
    ) -> BeatData:
        """
        Update orientations for a single option beat.

        Modern implementation that:
        1. Sets start orientations from sequence context
        2. Calculates new end orientations using modern orientation calculator
        """
        # Create updated motion data with new start orientations
        updated_blue_motion = None
        updated_red_motion = None

        if option.blue_motion:
            # Calculate new end orientation based on updated start orientation
            start_orientation = self._string_to_orientation(blue_start_ori)
            calculated_end_ori = self.orientation_calculator.calculate_end_orientation(
                option.blue_motion, start_orientation
            )

            # Create updated motion with new orientations
            updated_blue_motion = replace(
                option.blue_motion,
                start_ori=blue_start_ori,
                end_ori=calculated_end_ori.value.lower(),
            )

        if option.red_motion:
            # Calculate new end orientation based on updated start orientation
            start_orientation = self._string_to_orientation(red_start_ori)
            calculated_end_ori = self.orientation_calculator.calculate_end_orientation(
                option.red_motion, start_orientation
            )

            # Create updated motion with new orientations
            updated_red_motion = replace(
                option.red_motion,
                start_ori=red_start_ori,
                end_ori=calculated_end_ori.value.lower(),
            )

        # Return updated BeatData with new motion data
        return replace(
            option, blue_motion=updated_blue_motion, red_motion=updated_red_motion
        )

    def _string_to_orientation(self, ori_str: str) -> Orientation:
        """Convert string orientation to Orientation enum."""
        ori_str = ori_str.lower()
        if ori_str == "in":
            return Orientation.IN
        elif ori_str == "out":
            return Orientation.OUT
        elif ori_str == "clock":
            return Orientation.CLOCK
        elif ori_str == "counter":
            return Orientation.COUNTER
        else:
            logger.warning(f"Unknown orientation string: {ori_str}, defaulting to IN")
            return Orientation.IN
