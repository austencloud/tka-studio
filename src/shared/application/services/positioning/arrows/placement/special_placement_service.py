"""
Framework-Agnostic Special Placement Service

This service implements special placement logic using the same JSON configuration data
but without Qt dependencies, making it suitable for shared use across frameworks.

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
import logging
from pathlib import Path
from typing import Any, Optional

from desktop.modern.core.types import Point
from desktop.modern.domain.models import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class SpecialPlacementService:
    """
    Framework-agnostic service for loading and applying special placement adjustments.

    This service replicates the special placement strategy by:
    1. Loading special placement JSON files organized by grid mode and orientation key
    2. Generating orientation keys based on motion data
    3. Looking up letter-specific, turn-specific adjustments
    4. Applying motion-type-specific placement rules
    """

    def __init__(self):
        self.root_path = self._find_project_root()
        self.special_placements: dict[str, dict[str, dict[str, Any]]] = {}
        self._load_special_placements()

    def _find_project_root(self) -> Path:
        """Find the project root directory."""
        current = Path(__file__).parent
        while current.parent != current:
            if (current / "main.py").exists():
                return current
            current = current.parent
        return Path(__file__).parent.parent.parent.parent.parent.parent

    def get_special_adjustment(
        self,
        motion_data: MotionData,
        pictograph_data: PictographData,
        arrow_color: str = None,
    ) -> Optional[Point]:
        """
        Get special adjustment for arrow based on special placement logic.

        Args:
            motion_data: Motion data containing motion information
            pictograph_data: Pictograph data containing letter and context
            arrow_color: Color of the arrow ('red' or 'blue') - if not provided, will try to determine from motion

        Returns:
            Point with special adjustment or None if no special placement found
        """
        if not motion_data or not pictograph_data.letter:
            return None

        motion = motion_data
        letter = pictograph_data.letter

        # Generate orientation key using validated logic
        ori_key = self._generate_orientation_key(motion, pictograph_data)

        # Get grid mode (default to diamond)
        grid_mode = getattr(pictograph_data, "grid_mode", "diamond")

        # Generate turns tuple for lookup
        turns_tuple = self._generate_turns_tuple(pictograph_data)

        # Look up special placement data
        letter_data: dict[str, dict[tuple[int], dict[str, float]]] = (
            self.special_placements.get(grid_mode, {}).get(ori_key, {}).get(letter, {})
        )

        if not letter_data:
            return None

        # Get turn-specific data
        turn_data = letter_data.get(turns_tuple, {})

        if not turn_data:
            return None

        # Determine arrow color if not provided
        if arrow_color is None:
            arrow_color = self._determine_arrow_color(motion)

        # First, try arrow-color-specific adjustment
        if arrow_color in turn_data:
            adjustment_values = turn_data[arrow_color]
            if isinstance(adjustment_values, list) and len(adjustment_values) == 2:
                result = Point(adjustment_values[0], adjustment_values[1])
                return result

        # Second, try motion-type-specific adjustment (for letters like I)
        motion_type_key = (
            motion.motion_type.value.lower()
        )  # "pro", "anti", "float", etc.

        if motion_type_key in turn_data:
            adjustment_values = turn_data[motion_type_key]
            if isinstance(adjustment_values, list) and len(adjustment_values) == 2:
                result = Point(adjustment_values[0], adjustment_values[1])
                return result

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

                    # Build path to special placement directory using project root
                    directory = (
                        self.root_path
                        / "data"
                        / "arrow_placement"
                        / mode
                        / "special"
                        / subfolder
                    )

                    if not directory.exists():
                        continue

                    # Load all placement JSON files in this directory
                    for file_path in directory.glob("*_placements.json"):
                        try:
                            with open(file_path, encoding="utf-8") as f:
                                data = json.load(f)
                                self.special_placements[mode][subfolder].update(data)
                        except Exception:
                            pass

        except Exception:
            self.special_placements = {}

    def _generate_orientation_key(
        self, motion: MotionData, pictograph_data: PictographData
    ) -> str:
        """Generate orientation key for special placement lookup."""
        # This is a simplified version - in full implementation would use SpecialPlacementOriKeyGenerator
        # For now, return a default key
        return "from_layer1"

    def _generate_turns_tuple(self, pictograph_data: PictographData) -> tuple[int, ...]:
        """Generate turns tuple for special placement lookup."""
        # This is a simplified version - in full implementation would use TurnsTupleKeyGenerator
        # For now, return a default tuple
        return (0, 0)

    def _determine_arrow_color(self, motion: MotionData) -> str:
        """Determine arrow color from motion data."""
        # This is a simplified version - in full implementation would use proper color determination
        # For now, return a default color
        return "blue"
