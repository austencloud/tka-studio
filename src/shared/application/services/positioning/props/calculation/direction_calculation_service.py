"""
Direction Calculation Service

Pure service for calculating prop separation directions.
Extracted from PropManagementService to follow single responsibility principle.

PROVIDES:
- Separation direction calculations based on motion and grid mode
- Orientation-based direction mapping
- Grid mode detection (diamond vs box)
- Complex direction logic replication from BetaPropDirectionCalculator
"""

from abc import ABC, abstractmethod
from enum import Enum

from desktop.modern.domain.models import BeatData, Location, MotionData, Orientation


class SeparationDirection(Enum):
    """Separation directions for prop positioning."""

    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    DOWNRIGHT = "downright"
    UPLEFT = "upleft"
    DOWNLEFT = "downleft"
    UPRIGHT = "upright"


class IDirectionCalculationService(ABC):
    """Interface for direction calculation operations."""

    @abstractmethod
    def calculate_separation_direction(
        self, motion: MotionData, beat_data: BeatData, color: str
    ) -> SeparationDirection:
        """Calculate the direction props should be separated."""

    @abstractmethod
    def calculate_end_orientation(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for placement calculations."""

    @abstractmethod
    def detect_grid_mode(self, location: Location) -> str:
        """Detect grid mode (diamond or box) based on location."""


class DirectionCalculationService(IDirectionCalculationService):
    """
    Pure service for direction calculation operations.

    Handles complex direction calculations without external dependencies.
    Replicates BetaPropDirectionCalculator logic exactly for correct positioning.
    """

    def __init__(self):
        """Initialize direction calculation service."""
        # Direction constants for backward compatibility
        self.LEFT = "left"
        self.RIGHT = "right"
        self.UP = "up"
        self.DOWN = "down"
        self.UPLEFT = "upleft"
        self.UPRIGHT = "upright"
        self.DOWNLEFT = "downleft"
        self.DOWNRIGHT = "downright"

    def calculate_separation_direction(
        self, motion: MotionData, beat_data: BeatData, color: str
    ) -> SeparationDirection:
        """
        Calculate the direction props should be separated.

        CRITICAL: This replicates the BetaPropDirectionCalculator logic exactly.
        DO NOT SIMPLIFY - this complex logic was carefully crafted for correct arrow positioning.
        """
        # SPECIAL CASE: Letter I positioning
        # Letter I uses PRO/ANTI motion type logic instead of location-based logic
        if beat_data.letter == "I":
            return self._calculate_letter_I_direction(motion, beat_data, color)

        # Use standard direction calculation for all other letters
        return self._calculate_standard_direction(motion, beat_data, color)

    def calculate_end_orientation(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for placement calculations."""
        motion_type = motion_data.motion_type
        turns = motion_data.turns

        if turns in {0, 1, 2, 3}:
            if motion_type.value in ["pro", "static"]:
                return (
                    start_orientation
                    if int(turns) % 2 == 0
                    else self._switch_orientation(start_orientation)
                )
            elif motion_type.value in ["anti", "dash"]:
                return (
                    self._switch_orientation(start_orientation)
                    if int(turns) % 2 == 0
                    else start_orientation
                )

        return start_orientation

    def detect_grid_mode(self, location: Location) -> str:
        """Detect grid mode (diamond or box) based on location."""
        if location.value in ["n", "s", "e", "w"]:
            return "diamond"
        else:
            return "box"

    def is_radial_orientation(self, orientation) -> bool:
        """Check if orientation is radial (in/out) vs nonradial (clock/counter)."""
        if isinstance(orientation, Orientation):
            return orientation in [Orientation.IN, Orientation.OUT]
        elif isinstance(orientation, str):
            return orientation.lower() in ["in", "out"]
        else:
            return False

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

    def _switch_orientation(self, orientation: Orientation) -> Orientation:
        """Switch between IN and OUT orientations."""
        return Orientation.OUT if orientation == Orientation.IN else Orientation.IN

    def _calculate_letter_I_direction(
        self, motion: MotionData, beat_data: BeatData, color: str
    ) -> SeparationDirection:
        """
        Calculate direction for letter I using PRO/ANTI motion type logic.

        This replicates the legacy reposition_I method:
        1. Identify which motion is PRO and which is ANTI
        2. Calculate direction for PRO motion
        3. ANTI motion moves in opposite direction
        """
        from desktop.modern.domain.models.enums import MotionType

        # Get both motions from beat data
        red_motion = (
            beat_data.red_motion
            if hasattr(beat_data, "red_motion")
            else beat_data.pictograph_data.motions.get("red")
        )
        blue_motion = (
            beat_data.blue_motion
            if hasattr(beat_data, "blue_motion")
            else beat_data.pictograph_data.motions.get("blue")
        )

        if not red_motion or not blue_motion:
            # Fallback to standard logic if we can't get both motions
            return self._calculate_standard_direction(motion, beat_data, color)

        # Identify PRO and ANTI motions
        pro_motion = None
        anti_motion = None
        pro_color = None
        anti_color = None

        if red_motion.motion_type == MotionType.PRO:
            pro_motion = red_motion
            pro_color = "red"
            anti_motion = blue_motion
            anti_color = "blue"
        elif blue_motion.motion_type == MotionType.PRO:
            pro_motion = blue_motion
            pro_color = "blue"
            anti_motion = red_motion
            anti_color = "red"

        if not pro_motion or not anti_motion:
            # If it's not a PRO/ANTI combination, fall back to standard logic
            return self._calculate_standard_direction(motion, beat_data, color)

        # Calculate direction for PRO motion using standard logic
        pro_direction = self._calculate_standard_direction(
            pro_motion, beat_data, pro_color
        )

        # Return the calculated direction for PRO or its opposite for ANTI
        if color == pro_color:
            return pro_direction
        else:
            return self.get_opposite_direction(pro_direction)

    def _calculate_standard_direction(
        self, motion: MotionData, beat_data: BeatData, color: str
    ) -> SeparationDirection:
        """
        Calculate direction using the standard location-based logic.
        This is the original logic extracted for reuse in letter I handling.
        """
        location = motion.end_loc

        # Determine if prop is radial or nonradial based on end orientation
        is_radial = motion.end_ori in [Orientation.IN, Orientation.OUT]

        # Determine grid mode based on location
        grid_mode = self.detect_grid_mode(location)

        if grid_mode == "diamond":
            if is_radial:
                # Diamond layer reposition map for RADIAL
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
                # Diamond layer reposition map for NONRADIAL
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
                # Box layer reposition map for RADIAL
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
                # Box layer reposition map for NONRADIAL
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
