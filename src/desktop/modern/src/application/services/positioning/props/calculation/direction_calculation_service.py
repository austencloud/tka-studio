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

from domain.models.core_models import (
    MotionData,
    BeatData,
    Location,
    Orientation,
)


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
        # Replicate the get_dir_for_non_shift method exactly
        location = motion.end_loc

        # Determine if prop is radial or nonradial based on end orientation
        # Validated logic: RADIAL = IN/OUT, NONRADIAL = CLOCK/COUNTER
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
