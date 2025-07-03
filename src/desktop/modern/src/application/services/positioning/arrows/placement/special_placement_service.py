"""
Special Placement Service for Modern Arrow Positioning

This service implements special placement logic using the same JSON configuration data.
It provides pixel-perfect special placement adjustments for specific pictograph configurations.

IMPLEMENTS SPECIAL PLACEMENT PIPELINE:
- Loads special placement JSON files from data/arrow_placement directory
- Generates orientation keys (ori_key) for motion classification
- Applies letter-specific, turn-specific, and motion-type-specific adjustments
- Handles complex placement rules for specific pictograph patterns

PROVIDES:
- Complete special placement compatibility
- JSON configuration data loading and caching
- Orientation key generation matching validated logic
- Special adjustment calculation with fallback to default
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from PyQt6.QtCore import QPointF

from domain.models.core_models import (
    MotionData,
    Orientation,
)
from domain.models.pictograph_models import ArrowData, PictographData


class SpecialPlacementService:
    """
    Service for loading and applying special placement adjustments from JSON configuration.

    This service replicates the special placement strategy by:
    1. Loading special placement JSON files organized by grid mode and orientation key
    2. Generating orientation keys based on motion data
    3. Looking up letter-specific, turn-specific adjustments
    4. Applying motion-type-specific placement rules
    """

    def __init__(self):
        start_time = time.time()
        logger = logging.getLogger(__name__)

        self.special_placements: Dict[str, Dict[str, Dict[str, Any]]] = {}

        # Eager load special placements during initialization
        self._load_special_placements()

        load_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        total_placements = sum(
            len(subfolder_data)
            for mode_data in self.special_placements.values()
            for subfolder_data in mode_data.values()
        )
        logger.info(
            f"Special Placement Service initialized: {total_placements} placements loaded in {load_time:.1f}ms"
        )

    def get_special_adjustment(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Optional[QPointF]:
        """
        Get special adjustment for arrow based on special placement logic.

        Args:
            arrow_data: Arrow data containing motion information
            pictograph_data: Pictograph data containing letter and context

        Returns:
            QPointF with special adjustment or None if no special placement found
        """

        if not arrow_data.motion_data or not pictograph_data.letter:
            return None

        motion = arrow_data.motion_data
        letter = pictograph_data.letter

        # Generate orientation key using validated logic
        ori_key = self._generate_orientation_key(motion, pictograph_data)

        # Get grid mode (default to diamond)
        grid_mode = getattr(pictograph_data, "grid_mode", "diamond")

        # Generate turns tuple for lookup
        turns_tuple = self._generate_turns_tuple(pictograph_data)

        # Look up special placement data
        letter_data = (
            self.special_placements.get(grid_mode, {}).get(ori_key, {}).get(letter, {})
        )

        if not letter_data:
            return None

        # Get turn-specific data
        turn_data = letter_data.get(turns_tuple, {})

        if not turn_data:
            return None

        # First, try direct color-based coordinate lookup (most common case)
        color_key = arrow_data.color.lower()  # "blue" or "red"

        if color_key in turn_data:
            adjustment_values = turn_data[color_key]
            if isinstance(adjustment_values, list) and len(adjustment_values) == 2:
                result = QPointF(adjustment_values[0], adjustment_values[1])
                return result

        # Second, try motion-type-specific adjustment (for letters like I)
        motion_type_key = (
            motion.motion_type.value.lower()
        )  # "pro", "anti", "float", etc.

        if motion_type_key in turn_data:
            adjustment_values = turn_data[motion_type_key]
            if isinstance(adjustment_values, list) and len(adjustment_values) == 2:
                result = QPointF(adjustment_values[0], adjustment_values[1])
                return result

        # Third, check for special placement boolean flags (swap rules)
        # Note: Boolean flags like "swap_beta_*" are for PROP SWAPPING, not arrow adjustments
        # The arrow placement service should ignore these and return None
        # The prop placement system will handle these flags separately
        for _, value in turn_data.items():
            if isinstance(value, bool) and value is True:
                # Boolean flags are for prop swapping, not arrow placement
                # Return None so the arrow uses default positioning
                return None

        return None

    def _load_special_placements(self) -> None:
        """Load special placement data from JSON configuration files."""
        try:
            # Define the supported modes and subfolders matching the data structure
            supported_modes = ["diamond", "box"]
            subfolders = [
                "from_layer1",
                "from_layer2",
                "from_layer3_blue1_red2",
                "from_layer3_blue2_red1",
            ]

            for mode in supported_modes:
                self.special_placements[mode] = {}

                for subfolder in subfolders:
                    self.special_placements[mode][subfolder] = {}

                    # Build path to special placement directory
                    directory = (
                        Path("data") / "arrow_placement" / mode / "special" / subfolder
                    )

                    if not directory.exists():
                        continue

                    # Load all placement JSON files in this directory
                    for file_path in directory.glob("*_placements.json"):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                self.special_placements[mode][subfolder].update(data)
                        except Exception:
                            pass

        except Exception:
            self.special_placements = {}

    def _generate_orientation_key(
        self, motion: MotionData, pictograph_data: PictographData
    ) -> str:
        """
        Generate orientation key matching the ori_key_generator logic.

        This determines which subfolder of special placements to use:
        - from_layer1: Basic orientations
        - from_layer2: Layer 2 orientations
        - from_layer3_blue1_red2: Mixed orientations with blue on layer 1, red on layer 2
        - from_layer3_blue2_red1: Mixed orientations with blue on layer 2, red on layer 1
        """
        try:
            blue_arrow = pictograph_data.arrows.get("blue")
            red_arrow = pictograph_data.arrows.get("red")

            if (
                blue_arrow
                and red_arrow
                and blue_arrow.motion_data
                and red_arrow.motion_data
            ):
                blue_motion = blue_arrow.motion_data
                red_motion = red_arrow.motion_data

                blue_end_ori = getattr(blue_motion, "end_ori", Orientation.IN)
                red_end_ori = getattr(red_motion, "end_ori", Orientation.IN)

                blue_layer = (
                    1 if blue_end_ori in [Orientation.IN, Orientation.OUT] else 2
                )
                red_layer = 1 if red_end_ori in [Orientation.IN, Orientation.OUT] else 2

                if blue_layer == 1 and red_layer == 1:
                    return "from_layer1"
                elif blue_layer == 2 and red_layer == 2:
                    return "from_layer2"
                elif blue_layer == 1 and red_layer == 2:
                    return "from_layer3_blue1_red2"
                elif blue_layer == 2 and red_layer == 1:
                    return "from_layer3_blue2_red1"
                else:
                    return "from_layer1"

        except Exception:
            pass

        return "from_layer1"

    def _generate_turns_tuple(self, pictograph_data: PictographData) -> str:
        """
        Generate turns tuple string matching the turns_tuple_generator logic.

        This creates a string representation of the turn values for lookup in JSON data.
        Format: "(blue_turns, red_turns)" e.g., "(0, 1.5)", "(1, 0.5)"
        """
        try:
            blue_arrow = pictograph_data.arrows.get("blue")
            red_arrow = pictograph_data.arrows.get("red")

            if (
                blue_arrow
                and red_arrow
                and blue_arrow.motion_data
                and red_arrow.motion_data
            ):
                blue_motion = blue_arrow.motion_data
                red_motion = red_arrow.motion_data

                blue_turns = getattr(blue_motion, "turns", 0)
                red_turns = getattr(red_motion, "turns", 0)

                blue_str = (
                    str(int(blue_turns))
                    if blue_turns == int(blue_turns)
                    else str(blue_turns)
                )
                red_str = (
                    str(int(red_turns))
                    if red_turns == int(red_turns)
                    else str(red_turns)
                )

                return f"({blue_str}, {red_str})"

            return "(0, 0)"

        except Exception:
            return "(0, 0)"
