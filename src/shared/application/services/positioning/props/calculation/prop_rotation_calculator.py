"""
Prop Rotation Calculator Service

Pure service for calculating prop rotation angles.
Extracted from PropManagementService to follow single responsibility principle.

PROVIDES:
- Prop rotation angle calculations
- Orientation-based rotation mapping
- Location-specific angle calculations
- End orientation calculations for rotation
"""

from abc import ABC, abstractmethod

from desktop.modern.domain.models import MotionData, Orientation
from desktop.modern.domain.models.enums import Location


class IPropRotationCalculator(ABC):
    """Interface for prop rotation calculation operations."""

    @abstractmethod
    def calculate_prop_rotation_angle(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> float:
        """Calculate rotation angle for prop."""

    @abstractmethod
    def get_rotation_angle_map(self) -> dict[Orientation, dict[Location, float]]:
        """Get rotation angle mapping for orientations and locations."""


class PropRotationCalculator(IPropRotationCalculator):
    """
    Pure service for prop rotation calculations.

    Handles calculation of prop rotation angles based on motion data,
    end orientations, and location-specific rotation requirements.
    """

    def __init__(self):
        """Initialize with rotation angle mapping."""
        self._angle_map = self._build_rotation_angle_map()

    def calculate_prop_rotation_angle(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> float:
        """Calculate prop rotation angle based on motion data and orientation."""
        location = motion_data.end_loc

        # Calculate end orientation for this motion
        end_orientation = self._calculate_end_orientation(
            motion_data, start_orientation
        )

        # Get rotation angle from mapping
        orientation_map = self._angle_map.get(
            end_orientation, self._angle_map[Orientation.IN]
        )
        rotation_angle = orientation_map.get(location, 0)
        return float(rotation_angle)

    def get_rotation_angle_map(self) -> dict[Orientation, dict[Location, float]]:
        """Get rotation angle mapping for orientations and locations."""
        return self._angle_map.copy()

    def _build_rotation_angle_map(self) -> dict[Orientation, dict[Location, float]]:
        """Build rotation angle mapping for diamond grid orientations."""
        return {
            Orientation.IN: {
                Location.NORTH: 90,
                Location.SOUTH: 270,
                Location.WEST: 0,
                Location.EAST: 180,
            },
            Orientation.OUT: {
                Location.NORTH: 270,
                Location.SOUTH: 90,
                Location.WEST: 180,
                Location.EAST: 0,
            },
        }

    def _calculate_end_orientation(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """Calculate end orientation for rotation calculations using legacy logic."""
        from desktop.modern.domain.models import MotionType

        motion_type = motion_data.motion_type
        turns = motion_data.turns

        # Handle valid turn values according to legacy logic
        valid_turns = {0, 0.5, 1, 1.5, 2, 2.5, 3}
        if turns not in valid_turns:
            return start_orientation

        # Handle whole turns (0, 1, 2, 3)
        if turns in {0, 1, 2, 3}:
            if motion_type in [MotionType.PRO, MotionType.STATIC]:
                return (
                    start_orientation
                    if turns % 2 == 0
                    else self._switch_orientation(start_orientation)
                )
            elif motion_type in [MotionType.ANTI, MotionType.DASH]:
                return (
                    self._switch_orientation(start_orientation)
                    if turns % 2 == 0
                    else start_orientation
                )

        # Handle half turns (0.5, 1.5, 2.5) - these always switch orientation
        elif turns in {0.5, 1.5, 2.5}:
            return self._switch_orientation(start_orientation)

        return start_orientation

    def _switch_orientation(self, orientation: Orientation) -> Orientation:
        """Switch between IN and OUT orientations."""
        return Orientation.OUT if orientation == Orientation.IN else Orientation.IN
