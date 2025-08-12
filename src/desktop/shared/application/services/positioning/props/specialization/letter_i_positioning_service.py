"""
Letter I Positioning Service

Specialized service for Letter I PRO/ANTI coordination logic.
Extracted from PropManagementService to follow single responsibility principle.

PROVIDES:
- Letter I specific direction calculations
- PRO/ANTI motion coordination
- Opposite direction mapping
- Special case handling for Letter I positioning
"""

from abc import ABC, abstractmethod

from desktop.modern.domain.models import MotionData, MotionType
from desktop.modern.domain.models.enums import Location, Orientation

from ..calculation.direction_calculation_service import SeparationDirection


class ILetterIPositioningService(ABC):
    """Interface for Letter I positioning operations."""

    @abstractmethod
    def calculate_letter_i_directions(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> tuple[SeparationDirection, SeparationDirection]:
        """Calculate directions for letter I using PRO/ANTI coordination."""

    @abstractmethod
    def calculate_standard_direction(
        self, motion: MotionData, color: str
    ) -> SeparationDirection:
        """Calculate direction using standard location/color mapping."""

    @abstractmethod
    def get_opposite_direction(
        self, direction: SeparationDirection
    ) -> SeparationDirection:
        """Get opposite direction for symmetric positioning."""


class LetterIPositioningService(ILetterIPositioningService):
    """
    Specialized service for Letter I positioning logic.

    Handles the complex PRO/ANTI coordination required for Letter I,
    where PRO and ANTI motions must move in opposite directions.
    """

    def calculate_letter_i_directions(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> tuple[SeparationDirection, SeparationDirection]:
        """
        Calculate directions for letter I using PRO/ANTI coordination.

        This replicates the legacy reposition_I logic:
        1. Find which motion is PRO
        2. Calculate direction for the PRO motion
        3. ANTI motion gets opposite direction

        Returns:
            (blue_direction, red_direction)
        """
        # Identify PRO and ANTI motions
        if red_motion.motion_type == MotionType.PRO:
            pro_motion = red_motion
            pro_color = "red"
            anti_motion = blue_motion
        elif blue_motion.motion_type == MotionType.PRO:
            pro_motion = blue_motion
            pro_color = "blue"
            anti_motion = red_motion
        else:
            # Fallback if neither is PRO (shouldn't happen in letter I)
            # Use standard directions
            blue_direction = self.calculate_standard_direction(blue_motion, "blue")
            red_direction = self.calculate_standard_direction(red_motion, "red")
            return blue_direction, red_direction

        # Calculate direction for PRO motion
        pro_direction = self.calculate_standard_direction(pro_motion, pro_color)

        # ANTI motion gets opposite direction
        anti_direction = self.get_opposite_direction(pro_direction)

        # Return directions in correct order (blue, red)
        if pro_color == "red":
            return anti_direction, pro_direction  # blue=anti, red=pro
        else:
            return pro_direction, anti_direction  # blue=pro, red=anti

    def calculate_standard_direction(
        self, motion: MotionData, color: str
    ) -> SeparationDirection:
        """Calculate direction using standard location/color mapping."""
        location = motion.end_loc
        is_radial = motion.end_ori in [Orientation.IN, Orientation.OUT]

        # Determine grid mode based on location
        if location in [Location.NORTH, Location.EAST, Location.SOUTH, Location.WEST]:
            grid_mode = "diamond"
        else:
            grid_mode = "box"

        if grid_mode == "diamond":
            if is_radial:
                direction_map = {
                    (Location.NORTH, "red"): SeparationDirection.RIGHT,
                    (Location.NORTH, "blue"): SeparationDirection.LEFT,
                    (Location.EAST, "red"): SeparationDirection.DOWN,
                    (Location.EAST, "blue"): SeparationDirection.UP,
                    (Location.SOUTH, "red"): SeparationDirection.LEFT,
                    (Location.SOUTH, "blue"): SeparationDirection.RIGHT,
                    (Location.WEST, "blue"): SeparationDirection.DOWN,
                    (Location.WEST, "red"): SeparationDirection.UP,
                }
            else:
                direction_map = {
                    (Location.NORTH, "red"): SeparationDirection.UP,
                    (Location.NORTH, "blue"): SeparationDirection.DOWN,
                    (Location.SOUTH, "red"): SeparationDirection.UP,
                    (Location.SOUTH, "blue"): SeparationDirection.DOWN,
                    (Location.EAST, "red"): SeparationDirection.RIGHT,
                    (Location.WEST, "blue"): SeparationDirection.LEFT,
                    (Location.WEST, "red"): SeparationDirection.RIGHT,
                    (Location.EAST, "blue"): SeparationDirection.LEFT,
                }
        else:  # box grid
            if is_radial:
                direction_map = {
                    (Location.NORTHEAST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.NORTHEAST, "blue"): SeparationDirection.UPLEFT,
                    (Location.SOUTHEAST, "red"): SeparationDirection.UPRIGHT,
                    (Location.SOUTHEAST, "blue"): SeparationDirection.DOWNLEFT,
                    (Location.SOUTHWEST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.SOUTHWEST, "blue"): SeparationDirection.UPLEFT,
                    (Location.NORTHWEST, "red"): SeparationDirection.UPRIGHT,
                    (Location.NORTHWEST, "blue"): SeparationDirection.DOWNLEFT,
                }
            else:
                direction_map = {
                    (Location.NORTHEAST, "red"): SeparationDirection.UPRIGHT,
                    (Location.NORTHEAST, "blue"): SeparationDirection.DOWNLEFT,
                    (Location.SOUTHEAST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.SOUTHEAST, "blue"): SeparationDirection.UPLEFT,
                    (Location.SOUTHWEST, "red"): SeparationDirection.UPRIGHT,
                    (Location.SOUTHWEST, "blue"): SeparationDirection.DOWNLEFT,
                    (Location.NORTHWEST, "red"): SeparationDirection.DOWNRIGHT,
                    (Location.NORTHWEST, "blue"): SeparationDirection.UPLEFT,
                }

        return direction_map.get((location, color), SeparationDirection.RIGHT)

    def get_opposite_direction(
        self, direction: SeparationDirection
    ) -> SeparationDirection:
        """Get opposite direction for symmetric positioning."""
        opposite_map = {
            SeparationDirection.LEFT: SeparationDirection.RIGHT,
            SeparationDirection.RIGHT: SeparationDirection.LEFT,
            SeparationDirection.UP: SeparationDirection.DOWN,
            SeparationDirection.DOWN: SeparationDirection.UP,
            SeparationDirection.UPLEFT: SeparationDirection.DOWNRIGHT,
            SeparationDirection.UPRIGHT: SeparationDirection.DOWNLEFT,
            SeparationDirection.DOWNLEFT: SeparationDirection.UPRIGHT,
            SeparationDirection.DOWNRIGHT: SeparationDirection.UPLEFT,
        }
        return opposite_map.get(direction, direction)
