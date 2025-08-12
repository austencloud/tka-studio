"""
Modern Attribute Key Generator

Generates attribute keys for arrow positioning using modern data structures.
Replaces the legacy AttrKeyGenerator to work with ArrowData and PictographData.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from desktop.modern.domain.models.arrow_data import ArrowData
    from desktop.modern.domain.models.pictograph_data import PictographData

from desktop.modern.core.interfaces.positioning_services import IAttributeKeyGenerator


logger = logging.getLogger(__name__)


class AttributeKeyGenerator(IAttributeKeyGenerator):
    """
    Modern implementation of attribute key generation for arrow positioning.

    Generates keys used for special placement and default placement lookups.
    Works with modern ArrowData and PictographData objects.
    """

    def get_key_from_arrow(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> str:
        """
        Get attribute key from modern arrow data.

        Args:
            arrow_data: Arrow data containing color and other attributes
            pictograph_data: Pictograph data for context

        Returns:
            Attribute key string for positioning lookups
        """
        try:
            # Extract motion data for this arrow color
            motion_data = pictograph_data.motions.get(arrow_data.color)

            if not motion_data:
                # Fallback to color if no motion data
                logger.debug(
                    f"No motion data for {arrow_data.color}, using color as key"
                )
                return arrow_data.color

            # Extract required attributes
            motion_type = (
                motion_data.motion_type.value
                if hasattr(motion_data.motion_type, "value")
                else str(motion_data.motion_type)
            )
            letter = pictograph_data.letter
            start_ori = (
                motion_data.start_ori.value
                if hasattr(motion_data.start_ori, "value")
                else str(motion_data.start_ori)
            )
            color = arrow_data.color

            # For modern data, we don't have lead_state, so use None
            lead_state = None

            # Determine motion characteristics
            has_hybrid_motions = self._has_hybrid_motions(pictograph_data)
            starts_from_mixed_orientation = self._starts_from_mixed_orientation(
                pictograph_data
            )
            starts_from_standard_orientation = not starts_from_mixed_orientation

            return self.generate_key(
                motion_type=motion_type,
                letter=letter,
                start_ori=start_ori,
                color=color,
                lead_state=lead_state,
                has_hybrid_motions=has_hybrid_motions,
                starts_from_mixed_orientation=starts_from_mixed_orientation,
                starts_from_standard_orientation=starts_from_standard_orientation,
            )

        except Exception as e:
            logger.error(f"Error generating attribute key for {arrow_data.color}: {e}")
            # Fallback to color
            return arrow_data.color

    def generate_key(
        self,
        motion_type: str,
        letter: str,
        start_ori: str,
        color: str,
        lead_state: str,
        has_hybrid_motions: bool,
        starts_from_mixed_orientation: bool,
        starts_from_standard_orientation: bool,
    ) -> str:
        """
        Core key generation logic matching legacy implementation.

        Args:
            motion_type: Motion type string
            letter: Letter string
            start_ori: Start orientation string
            color: Arrow color
            lead_state: Lead state (may be None for modern data)
            has_hybrid_motions: Whether there are hybrid motions
            starts_from_mixed_orientation: Whether starts from mixed orientation
            starts_from_standard_orientation: Whether starts from standard orientation

        Returns:
            Generated attribute key string
        """
        try:
            # Import constants for orientation checking
            from data.constants import CLOCK, COUNTER, IN, OUT

            if starts_from_mixed_orientation:
                if letter in ["S", "T"]:
                    return lead_state if lead_state else color
                elif has_hybrid_motions:
                    if start_ori in [IN, OUT]:
                        return f"{motion_type}_from_layer1"
                    elif start_ori in [CLOCK, COUNTER]:
                        return f"{motion_type}_from_layer2"
                    else:
                        return color
                elif self._is_non_hybrid_letter(letter):
                    return color
                else:
                    return motion_type
            else:
                # Standard orientation - return color for most cases
                return color

        except Exception as e:
            logger.error(f"Error in key generation: {e}")
            # Fallback to color
            return color

    def _has_hybrid_motions(self, pictograph_data: PictographData) -> bool:
        """
        Check if pictograph has hybrid motions.

        Args:
            pictograph_data: Pictograph data to check

        Returns:
            True if has hybrid motions
        """
        try:
            # Check if we have both blue and red motions with different types
            blue_motion = pictograph_data.motions.get("blue")
            red_motion = pictograph_data.motions.get("red")

            if not blue_motion or not red_motion:
                return False

            # Different motion types indicate hybrid
            blue_type = (
                blue_motion.motion_type.value
                if hasattr(blue_motion.motion_type, "value")
                else str(blue_motion.motion_type)
            )
            red_type = (
                red_motion.motion_type.value
                if hasattr(red_motion.motion_type, "value")
                else str(red_motion.motion_type)
            )

            return blue_type != red_type

        except Exception:
            return False

    def _starts_from_mixed_orientation(self, pictograph_data: PictographData) -> bool:
        """
        Check if pictograph starts from mixed orientation.

        Args:
            pictograph_data: Pictograph data to check

        Returns:
            True if starts from mixed orientation
        """
        try:
            from data.constants import IN, OUT

            blue_motion = pictograph_data.motions.get("blue")
            red_motion = pictograph_data.motions.get("red")

            if not blue_motion or not red_motion:
                return False

            blue_start = (
                blue_motion.start_ori.value
                if hasattr(blue_motion.start_ori, "value")
                else str(blue_motion.start_ori)
            )
            red_start = (
                red_motion.start_ori.value
                if hasattr(red_motion.start_ori, "value")
                else str(red_motion.start_ori)
            )

            # Mixed if one is layer1 (IN/OUT) and other is layer2 (CLOCK/COUNTER)
            blue_layer1 = blue_start in [IN, OUT]
            red_layer1 = red_start in [IN, OUT]

            return blue_layer1 != red_layer1

        except Exception:
            return False

    def _is_non_hybrid_letter(self, letter: str) -> bool:
        """
        Check if letter is non-hybrid.

        Args:
            letter: Letter to check

        Returns:
            True if letter is non-hybrid
        """
        # Basic non-hybrid letters (this may need expansion based on actual letter conditions)
        non_hybrid_letters = [
            "A",
            "B",
            "D",
            "E",
            "G",
            "H",
            "J",
            "K",
            "M",
            "N",
            "P",
            "Q",
            "S",
            "T",
        ]
        return letter in non_hybrid_letters
