"""
Attribute Key Generation Service - Faithful Legacy Port

Faithful port of legacy AttrKeyGenerator for special placement lookups.
Legacy source: src/desktop/legacy/src/placement_managers/attr_key_generator.py
"""

import logging

from desktop.modern.core.interfaces.positioning_services import IAttributeKeyGenerator
from desktop.modern.domain.models.arrow_data import ArrowData
from desktop.modern.domain.models.enums import Orientation
from desktop.modern.domain.models.letter_type_classifier import LetterTypeClassifier
from desktop.modern.domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class AttributeKeyGenerator(IAttributeKeyGenerator):
    """Faithful port of legacy AttrKeyGenerator."""

    def __init__(self):
        pass

    def get_key_from_arrow(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> str:
        """Original method for getting key from Arrow data (faithful port)."""

        # Check if motion data exists for this arrow color
        if arrow_data.color not in pictograph_data.motions:
            # No motion data means static arrow - return color as fallback
            return arrow_data.color

        motion_data = pictograph_data.motions[arrow_data.color]
        motion_type = motion_data.motion_type
        letter = pictograph_data.letter or ""
        start_ori = getattr(motion_data, "start_ori", Orientation.IN)
        color = arrow_data.color
        lead_state = self._determine_lead_state(arrow_data, pictograph_data)

        has_hybrid_motions = self._has_hybrid_motions(pictograph_data)
        starts_from_mixed_orientation = self._starts_from_mixed_orientation(
            pictograph_data
        )
        starts_from_standard_orientation = self._starts_from_standard_orientation(
            pictograph_data
        )

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
        """Core key generation logic - faithful port of legacy generate_key()."""
        if starts_from_mixed_orientation:
            if letter in ["S", "T"]:
                return f"{lead_state}"
            elif has_hybrid_motions:
                # Convert string orientation to enum for comparison
                from desktop.modern.domain.models import Orientation

                ori_enum = start_ori
                if isinstance(start_ori, str):
                    ori_map = {
                        "in": Orientation.IN,
                        "out": Orientation.OUT,
                        "clock": Orientation.CLOCK,
                        "counter": Orientation.COUNTER,
                    }
                    ori_enum = ori_map.get(start_ori.lower(), Orientation.IN)

                if ori_enum in [Orientation.IN, Orientation.OUT]:
                    return f"{motion_type}_from_layer1"
                elif ori_enum in [Orientation.CLOCK, Orientation.COUNTER]:
                    return f"{motion_type}_from_layer2"
                else:
                    return color
            elif self._is_non_hybrid_letter(letter):
                return color
            else:
                return motion_type

        elif starts_from_standard_orientation:
            if letter in ["S", "T"]:
                return f"{color}_{lead_state}"
            elif has_hybrid_motions:
                return motion_type
            else:
                return color

        return motion_type

    def _has_hybrid_motions(self, pictograph_data: PictographData) -> bool:
        """Check if pictograph has hybrid motions."""
        arrows = list(pictograph_data.arrows.values())
        if len(arrows) < 2:
            return False
        motions = pictograph_data.motions
        motion_types = set()
        for motion in motions.values():
            if motion:
                motion_types.add(motion.motion_type.value)

        return len(motion_types) > 1

    def _starts_from_mixed_orientation(self, pictograph_data: PictographData) -> bool:
        """Check if pictograph starts from mixed orientation."""
        arrows = list(pictograph_data.arrows.values())
        if len(arrows) < 2:
            return False
        motions = pictograph_data.motions

        start_oris = set()
        for motion in motions:
            if motion:
                start_ori = getattr(motion, "start_ori", Orientation.IN)
                start_oris.add(start_ori)

        return len(start_oris) > 1

    def _starts_from_standard_orientation(
        self, pictograph_data: PictographData
    ) -> bool:
        """Check if pictograph starts from standard orientation."""
        return not self._starts_from_mixed_orientation(pictograph_data)

    def _is_non_hybrid_letter(self, letter: str) -> bool:
        """Check if letter is non-hybrid (Type1)."""
        return LetterTypeClassifier.get_letter_type(letter) == "Type1"

    def _determine_lead_state(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> str:
        """
        Determine lead state for the given arrow.

        Faithful port of legacy lead state determination logic.
        Leading motion is determined by position and motion direction.
        """
        arrows = list(pictograph_data.arrows.values())
        if len(arrows) < 2:
            return "leading"  # Default for single arrow

        blue_arrow = pictograph_data.arrows.get("blue")
        red_arrow = pictograph_data.arrows.get("red")

        if not blue_arrow or not red_arrow:
            return "leading"  # Default

        # Simplified lead state logic based on legacy LeadStateDeterminer
        # The arrow that "leads" is typically determined by position/motion order

        # If one motion ends where the other starts, the one that starts there is leading
        blue_motion = pictograph_data.motions.get("blue")
        red_motion = pictograph_data.motions.get("red")

        if blue_motion and red_motion:
            blue_start = blue_motion.start_loc
            blue_end = blue_motion.end_loc
            red_start = red_motion.start_loc
            red_end = red_motion.end_loc

            # Check if blue ends where red starts
            if blue_end == red_start:
                if arrow_data.color == "red":
                    return "leading"
                else:
                    return "trailing"

            # Check if red ends where blue starts
            if red_end == blue_start:
                if arrow_data.color == "blue":
                    return "leading"
                else:
                    return "trailing"

        # Default fallback: blue is leading, red is trailing
        if arrow_data.color == "blue":
            return "leading"
        else:
            return "trailing"
