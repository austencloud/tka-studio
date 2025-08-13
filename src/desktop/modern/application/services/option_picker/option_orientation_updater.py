"""
Option Orientation Update Service

Modern service for updating orientations of option beats based on sequence context.
This service handles updating start orientations of option beats based on the end orientations
of the last beat in a sequence, then calculates new end orientations.

This ensures that options display with correct orientations that flow from the sequence context,
rather than using default "in,in" orientations.
"""

import logging
from dataclasses import replace

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


class OptionOrientationUpdater:
    """
    Service for updating orientations of pictograph options based on sequence context.

    Modern implementation that:
    1. Extract end orientations from last beat in sequence
    2. Set those as start orientations for all pictograph options
    3. Update prop orientations to match sequence continuity
    """

    def __init__(self):
        """Initialize the orientation update service."""

    def update_option_orientations(
        self, sequence: SequenceData, options: list[PictographData]
    ) -> list[PictographData]:
        """
        Update orientations for pictograph options based on sequence context.

        Modern implementation that:
        - Extract end orientations from last beat in sequence
        - Set those as start orientations for all pictograph options
        - Update prop orientations to match sequence continuity

        Args:
            sequence: The current sequence data
            options: List of pictograph options to update

        Returns:
            List of updated PictographData objects with corrected orientations
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

        # Update each pictograph option
        updated_options = []
        for option in options:
            updated_option = self._update_single_pictograph_orientation(
                option, last_blue_end_ori, last_red_end_ori
            )
            updated_options.append(updated_option)

        logger.debug(
            f"Updated orientations for {len(updated_options)} pictograph options"
        )
        return updated_options

    def _get_last_valid_beat(self, sequence: SequenceData) -> BeatData | None:
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
    ) -> tuple[str | None, str | None]:
        """
        Extract end orientations from a beat's pictograph data.

        Returns:
            Tuple of (blue_end_ori, red_end_ori) as strings
        """
        blue_end_ori = None
        red_end_ori = None

        # NEW: Get motion data from pictograph_data motions dictionary
        if beat.pictograph_data and beat.pictograph_data.motions:
            if "blue" in beat.pictograph_data.motions:
                blue_motion = beat.pictograph_data.motions["blue"]
                if blue_motion and hasattr(blue_motion, "end_ori"):
                    # FIXED: Convert Orientation enum to string value
                    end_ori = blue_motion.end_ori
                    blue_end_ori = (
                        end_ori.value if hasattr(end_ori, "value") else str(end_ori)
                    )

            if "red" in beat.pictograph_data.motions:
                red_motion = beat.pictograph_data.motions["red"]
                if red_motion and hasattr(red_motion, "end_ori"):
                    # FIXED: Convert Orientation enum to string value
                    end_ori = red_motion.end_ori
                    red_end_ori = (
                        end_ori.value if hasattr(end_ori, "value") else str(end_ori)
                    )

        return blue_end_ori, red_end_ori

    def _update_single_pictograph_orientation(
        self, pictograph: PictographData, blue_start_ori: str, red_start_ori: str
    ) -> PictographData:
        """
        Update orientations for a single pictograph option.

        Modern implementation that:
        1. Sets start orientations from sequence context
        2. Updates prop orientations to match sequence continuity
        """
        updated_props = pictograph.props.copy()

        # Update blue prop orientation
        if "blue" in updated_props:
            blue_prop = updated_props["blue"]
            updated_blue_prop = replace(blue_prop, orientation=blue_start_ori)
            updated_props["blue"] = updated_blue_prop

        # Update red prop orientation
        if "red" in updated_props:
            red_prop = updated_props["red"]
            updated_red_prop = replace(red_prop, orientation=red_start_ori)
            updated_props["red"] = updated_red_prop

        return replace(pictograph, props=updated_props)
