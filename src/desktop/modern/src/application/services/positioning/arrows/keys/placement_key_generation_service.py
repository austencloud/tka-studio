"""
Placement Key Generation Service - Legacy Port

Faithful port of the legacy PlacementKeyGenerator for generating placement keys
used in special placement lookups.

This service provides the exact same logic as the legacy system:
- Motion end orientation key generation
- Letter suffix generation (with TYPE3/TYPE5 dash logic)
- Key middle generation (layer1/layer2/layer3 with alpha/beta/gamma)
- Key selection logic

Ported from legacy placement logic for exact parity.
"""

import logging
from typing import Optional

from domain.models.core_models import MotionData, Orientation
from domain.models.pictograph_models import ArrowData, PictographData
from domain.models.letter_type_classifier import LetterTypeClassifier
from application.services.validation.pictograph_checker_service import (
    PictographCheckerService,
)

logger = logging.getLogger(__name__)


class PlacementKeyGenerationService:
    """
    Service for generating placement keys used in special placement lookups.

    This is a faithful port of the legacy PlacementKeyGenerator class."""

    def __init__(self):
        """Initialize the placement key generation service."""

    def _get_motion_end_ori_key(
        self, has_hybrid_orientation: bool, motion_end_ori: str
    ) -> str:
        """
        Generate motion end orientation key component.

        Legacy logic:
        - If hybrid orientation and end_ori is IN/OUT -> "radial_"
        - If hybrid orientation and end_ori is CLOCK/COUNTER -> "nonradial_"
        - Otherwise -> ""
        """
        if has_hybrid_orientation and motion_end_ori in ["IN", "OUT"]:
            return "radial_"
        elif has_hybrid_orientation and motion_end_ori in ["CLOCK", "COUNTER"]:
            return "nonradial_"
        else:
            return ""

    def _get_letter_suffix(self, letter: Optional[str]) -> str:
        """
        Generate letter suffix component.

        Legacy logic:
        - For TYPE3 and TYPE5 letters: "_{letter[:-1]}_dash" (removes dash, adds "_dash")
        - For other letters: "_{letter}"
        - No letter: ""
        """
        if not letter:
            return ""

        # Check if letter is TYPE3 or TYPE5 using the letter type classifier
        letter_type = LetterTypeClassifier.get_letter_type(letter)

        if letter_type in ["Type3", "Type5"]:
            # Remove the dash and add "_dash" suffix
            return f"_{letter[:-1]}_dash"
        else:
            return f"_{letter}"

    def _get_key_middle(
        self,
        has_radial_props: bool,
        has_nonradial_props: bool,
        has_hybrid_orientation: bool,
        has_alpha_props: bool,
        has_beta_props: bool,
        has_gamma_props: bool,
    ) -> str:
        """
        Generate key middle component.

        Legacy logic:
        - has_radial_props -> "layer1"
        - has_nonradial_props -> "layer2"
        - has_hybrid_orientation -> "layer3"
        - Otherwise -> ""

        Then append:
        - has_alpha_props -> "_alpha"
        - has_beta_props -> "_beta"
        - has_gamma_props -> "_gamma"
        """
        if has_radial_props:
            key_middle = "layer1"
        elif has_nonradial_props:
            key_middle = "layer2"
        elif has_hybrid_orientation:
            key_middle = "layer3"
        else:
            return ""

        if has_alpha_props:
            key_middle += "_alpha"
        elif has_beta_props:
            key_middle += "_beta"
        elif has_gamma_props:
            key_middle += "_gamma"

        return key_middle

    def generate_key(
        self,
        arrow_data: ArrowData,
        pictograph_data: PictographData,
        default_placements: dict,
    ) -> str:
        """
        Generate placement key for special placement lookup.

        This is the main method that combines all components to create the placement key.
        Faithful port of legacy generate_key() method.

        Args:
            arrow_data: Arrow data with motion and color info
            pictograph_data: Pictograph context with letter
            default_placements: Available placement keys to choose from

        Returns:
            Placement key string
        """  # Use the pictograph checker to determine properties (like legacy check_manager)
        pictograph_checker = PictographCheckerService(pictograph_data)
        has_beta_props = pictograph_checker.ends_with_beta()
        has_alpha_props = pictograph_checker.ends_with_alpha()
        has_gamma_props = pictograph_checker.ends_with_gamma()
        has_hybrid_orientation = pictograph_checker.ends_with_layer3()
        has_radial_props = pictograph_checker.ends_with_radial_ori()
        has_nonradial_props = pictograph_checker.ends_with_nonradial_ori()

        # Get motion end orientation
        motion_end_ori = self._get_motion_end_orientation(arrow_data.motion_data)

        # Get motion type
        motion_type = self._get_motion_type_string(arrow_data.motion_data)

        # Build key components following legacy logic
        key_suffix = "_to_"

        motion_end_ori_key = self._get_motion_end_ori_key(
            has_hybrid_orientation, motion_end_ori
        )

        letter_suffix = self._get_letter_suffix(pictograph_data.letter)

        key_middle = self._get_key_middle(
            has_radial_props,
            has_nonradial_props,
            has_hybrid_orientation,
            has_alpha_props,
            has_beta_props,
            has_gamma_props,
        )

        # Combine components following legacy logic
        key = motion_type + (
            key_suffix + motion_end_ori_key + key_middle if key_middle else ""
        )
        key_with_letter = f"{key}{letter_suffix}"

        # Select final key using legacy selection logic
        return self._select_key(key_with_letter, key, motion_type, default_placements)

    def _select_key(
        self, key_with_letter: str, key: str, motion_type: str, default_placements: dict
    ) -> str:
        """
        Select the final key to use from available options.

        Legacy selection priority:
        1. key_with_letter (if exists in default_placements)
        2. key (if exists in default_placements)
        3. motion_type (fallback)
        """
        if key_with_letter in default_placements:
            return key_with_letter
        elif key in default_placements:
            return key
        else:
            return motion_type

    def _get_motion_end_orientation(self, motion_data: MotionData) -> str:
        """Extract motion end orientation as string."""
        if not motion_data:
            return "IN"  # Default

        # Calculate end orientation similar to legacy
        from ..calculation.orientation_calculator import OrientationCalculator

        orientation_service = OrientationCalculator()

        start_ori = getattr(motion_data, "start_ori", Orientation.IN)
        if isinstance(start_ori, str):
            start_ori = getattr(Orientation, start_ori.upper(), Orientation.IN)

        end_ori = orientation_service.calculate_end_orientation(motion_data, start_ori)
        return end_ori.value

    def _get_motion_type_string(self, motion_data: MotionData) -> str:
        """Extract motion type as string."""
        if not motion_data or not motion_data.motion_type:
            return "static"  # Default fallback

        return motion_data.motion_type.value
