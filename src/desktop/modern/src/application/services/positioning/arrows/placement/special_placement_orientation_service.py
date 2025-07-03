"""
Special Placement Orientation Service

Generates orientation keys for special placement data structure navigation.
This is different from placement key generation - it creates keys like "from_layer1",
"from_layer2" that determine which subfolder to look in for special placements.

Faithful port of the orientation key generation logic from legacy special placement system.
"""

import logging
from typing import Optional

from domain.models.core_models import MotionData, Orientation
from domain.models.pictograph_models import PictographData
from application.services.validation.pictograph_checker_service import (
    PictographCheckerService,
)

logger = logging.getLogger(__name__)


class SpecialPlacementOrientationService:
    """
    Service for generating orientation keys used in special placement lookups.

    This determines which subfolder to look in for special placements:
    - from_layer1: Both arrows start from layer 1 (in/out orientations)
    - from_layer2: Both arrows start from layer 2 (clock/counter orientations)
    - from_layer3_blue1_red2: Blue starts from layer 1, red from layer 2
    - from_layer3_blue2_red1: Blue starts from layer 2, red from layer 1
    """

    def generate_orientation_key(
        self, motion_data: MotionData, pictograph_data: PictographData
    ) -> str:
        """
        Generate orientation key for special placement lookup.

        This determines which subfolder to look in for special placements.
        Based on the legacy orientation key generation logic.

        Args:
            motion_data: Motion data with orientations
            pictograph_data: Pictograph context for letter-specific checks

        Returns:
            Orientation key string (e.g., "from_layer1", "from_layer2")
        """
        # Use pictograph checker to determine layer properties
        checker = PictographCheckerService(pictograph_data)

        # Check what layer properties this pictograph has
        has_radial_props = checker.ends_with_radial_ori()
        has_nonradial_props = checker.ends_with_nonradial_ori()
        has_hybrid_orientation = checker.ends_with_layer3()

        logger.debug(f"Orientation analysis:")
        logger.debug(f"  Has radial props: {has_radial_props}")
        logger.debug(f"  Has non-radial props: {has_nonradial_props}")
        logger.debug(f"  Has hybrid orientation: {has_hybrid_orientation}")

        # Generate orientation key based on layer analysis
        if has_radial_props and not has_nonradial_props:
            # Pure layer 1 (radial orientations)
            ori_key = "from_layer1"
        elif has_nonradial_props and not has_radial_props:
            # Pure layer 2 (non-radial orientations)
            ori_key = "from_layer2"
        elif has_hybrid_orientation:
            # Layer 3 (mixed orientations) - need to determine which arrow is which layer
            ori_key = self._generate_layer3_key(pictograph_data)
        else:
            # Default fallback - analyze motion data directly
            ori_key = self._analyze_motion_orientations(motion_data)

        logger.debug(f"Generated orientation key: {ori_key}")
        return ori_key

    def _generate_layer3_key(self, pictograph_data: PictographData) -> str:
        """
        Generate layer 3 orientation key based on which arrow is in which layer.

        Args:
            pictograph_data: Pictograph with blue and red arrows

        Returns:
            Layer 3 orientation key (e.g., "from_layer3_blue1_red2")
        """
        blue_arrow = pictograph_data.arrows.get("blue")
        red_arrow = pictograph_data.arrows.get("red")

        if not blue_arrow or not red_arrow:
            logger.warning("Missing arrow data for layer 3 analysis")
            return "from_layer3"

        # Analyze orientations of each arrow
        blue_layer = self._get_arrow_layer(blue_arrow.motion_data)
        red_layer = self._get_arrow_layer(red_arrow.motion_data)

        logger.debug(f"Layer analysis: blue={blue_layer}, red={red_layer}")

        if blue_layer == 1 and red_layer == 2:
            return "from_layer3_blue1_red2"
        elif blue_layer == 2 and red_layer == 1:
            return "from_layer3_blue2_red1"
        else:
            # Default layer 3 key
            return "from_layer3"

    def _get_arrow_layer(self, motion_data: Optional[MotionData]) -> int:
        """
        Determine which layer an arrow belongs to based on its orientations.

        Args:
            motion_data: Motion data with orientation info

        Returns:
            Layer number (1 for radial, 2 for non-radial)
        """
        if not motion_data:
            return 1  # Default to layer 1

        # Check end orientation to determine layer
        end_ori = getattr(motion_data, "end_ori", Orientation.IN)

        if end_ori in [Orientation.IN, Orientation.OUT]:
            return 1  # Layer 1 (radial)
        elif end_ori in [Orientation.CLOCK, Orientation.COUNTER]:
            return 2  # Layer 2 (non-radial)
        else:
            return 1  # Default to layer 1

    def _analyze_motion_orientations(self, motion_data: MotionData) -> str:
        """
        Fallback method to analyze motion data directly when pictograph analysis fails.

        Args:
            motion_data: Motion data to analyze

        Returns:
            Orientation key based on motion analysis
        """
        if not motion_data:
            return "from_layer1"  # Default

        # Check end orientation
        end_ori = getattr(motion_data, "end_ori", Orientation.IN)

        if end_ori in [Orientation.IN, Orientation.OUT]:
            return "from_layer1"
        elif end_ori in [Orientation.CLOCK, Orientation.COUNTER]:
            return "from_layer2"
        else:
            return "from_layer1"  # Default fallback
