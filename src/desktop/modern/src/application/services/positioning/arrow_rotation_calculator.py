"""
Arrow Rotation Calculator Service

Pure algorithmic service for calculating arrow rotations based on motion data.
Extracted from ArrowManagementService to follow single responsibility principle.

PROVIDES:
- Static arrow rotation calculation
- Pro/Anti arrow rotation calculation  
- Dash arrow rotation calculation
- Float arrow rotation calculation
- Pure algorithms with no Qt dependencies
"""

from typing import Dict
from abc import ABC, abstractmethod

from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)


class IArrowRotationCalculator(ABC):
    """Interface for arrow rotation calculation."""

    @abstractmethod
    def calculate_rotation(self, motion: MotionData, arrow_location: Location) -> float:
        """Calculate arrow rotation based on motion data and location."""
        pass


class ArrowRotationCalculator(IArrowRotationCalculator):
    """
    Pure algorithmic service for arrow rotation calculation.

    Handles all arrow rotation algorithms without Qt dependencies.
    Uses immutable data patterns following TKA architecture.
    """

    def __init__(self):
        """Initialize rotation calculator."""
        pass

    def calculate_rotation(self, motion: MotionData, arrow_location: Location) -> float:
        """Calculate arrow rotation using motion-type-specific algorithms."""
        if motion.motion_type == MotionType.STATIC:
            return self._calculate_static_rotation(arrow_location)
        elif motion.motion_type == MotionType.PRO:
            return self._calculate_pro_rotation(motion, arrow_location)
        elif motion.motion_type == MotionType.ANTI:
            return self._calculate_anti_rotation(motion, arrow_location)
        elif motion.motion_type == MotionType.DASH:
            return self._calculate_dash_rotation(motion, arrow_location)
        elif motion.motion_type == MotionType.FLOAT:
            return self._calculate_float_rotation(motion, arrow_location)
        else:
            return 0

    def _calculate_static_rotation(self, location: Location) -> float:
        """Calculate rotation for static arrows (point inward)."""
        location_angles = {
            Location.NORTH: 180,
            Location.NORTHEAST: 225,
            Location.EAST: 270,
            Location.SOUTHEAST: 315,
            Location.SOUTH: 0,
            Location.SOUTHWEST: 45,
            Location.WEST: 90,
            Location.NORTHWEST: 135,
        }
        return location_angles.get(location, 0)

    def _calculate_pro_rotation(self, motion: MotionData, location: Location) -> float:
        """Calculate rotation for pro arrows."""
        if motion.prop_rot_dir == RotationDirection.CLOCKWISE:
            direction_map = {
                Location.NORTH: 315,
                Location.EAST: 45,
                Location.SOUTH: 135,
                Location.WEST: 225,
                Location.NORTHEAST: 0,
                Location.SOUTHEAST: 90,
                Location.SOUTHWEST: 180,
                Location.NORTHWEST: 270,
            }
        else:  # COUNTER_CLOCKWISE
            direction_map = {
                Location.NORTH: 315,
                Location.EAST: 225,
                Location.SOUTH: 135,
                Location.WEST: 45,
                Location.NORTHEAST: 270,
                Location.SOUTHEAST: 180,
                Location.SOUTHWEST: 90,
                Location.NORTHWEST: 0,
            }
        return direction_map.get(location, 0.0)

    def _calculate_anti_rotation(self, motion: MotionData, location: Location) -> float:
        """Calculate rotation for anti arrows using exact rotation logic."""
        if motion.prop_rot_dir == RotationDirection.CLOCKWISE:
            direction_map = {
                Location.NORTH: 315,
                Location.EAST: 225,
                Location.SOUTH: 135,
                Location.WEST: 45,
                Location.NORTHEAST: 270,
                Location.SOUTHEAST: 180,
                Location.SOUTHWEST: 90,
                Location.NORTHWEST: 0,
            }
        else:  # COUNTER_CLOCKWISE
            direction_map = {
                Location.NORTH: 315,
                Location.EAST: 45,
                Location.SOUTH: 135,
                Location.WEST: 225,
                Location.NORTHEAST: 0,
                Location.SOUTHEAST: 90,
                Location.SOUTHWEST: 180,
                Location.NORTHWEST: 270,
            }
        return direction_map.get(location, 0.0)

    def _calculate_dash_rotation(self, motion: MotionData, location: Location) -> float:
        """Calculate rotation for dash arrows using exact rotation logic."""
        # Handle NO_ROTATION case first (most common for dash)
        if motion.prop_rot_dir == RotationDirection.NO_ROTATION:
            no_rotation_map = {
                (Location.NORTH, Location.SOUTH): 90,
                (Location.EAST, Location.WEST): 180,
                (Location.SOUTH, Location.NORTH): 270,
                (Location.WEST, Location.EAST): 0,
                (Location.SOUTHEAST, Location.NORTHWEST): 225,
                (Location.SOUTHWEST, Location.NORTHEAST): 315,
                (Location.NORTHWEST, Location.SOUTHEAST): 45,
                (Location.NORTHEAST, Location.SOUTHWEST): 135,
            }
            return no_rotation_map.get((motion.start_loc, motion.end_loc), 0)

        # Handle rotation-based dash arrows
        if motion.prop_rot_dir == RotationDirection.CLOCKWISE:
            direction_map = {
                Location.NORTH: 270,
                Location.EAST: 0,
                Location.SOUTH: 90,
                Location.WEST: 180,
                Location.NORTHEAST: 315,
                Location.SOUTHEAST: 45,
                Location.SOUTHWEST: 135,
                Location.NORTHWEST: 225,
            }
        else:  # COUNTER_CLOCKWISE
            direction_map = {
                Location.NORTH: 270,
                Location.EAST: 180,
                Location.SOUTH: 90,
                Location.WEST: 0,
                Location.NORTHEAST: 225,
                Location.SOUTHEAST: 135,
                Location.SOUTHWEST: 45,
                Location.NORTHWEST: 315,
            }
        return direction_map.get(location, 0.0)

    def _calculate_float_rotation(
        self, motion: MotionData, location: Location
    ) -> float:
        """Calculate rotation for float arrows (similar to pro)."""
        return self._calculate_pro_rotation(motion, location)
