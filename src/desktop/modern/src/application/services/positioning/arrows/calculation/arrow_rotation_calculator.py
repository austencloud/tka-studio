"""
Arrow Rotation Calculator Service

Pure algorithmic service for calculating arrow rotation angles based on motion data and location.

This service handles:
- Static motion rotation (arrows point inward)
- PRO motion rotation (based on rotation direction and location)
- ANTI motion rotation (based on rotation direction and location)
- DASH motion rotation (handles NO_ROTATION and directional cases)
- FLOAT motion rotation (similar to PRO)

No UI dependencies, completely testable in isolation.
"""

import logging

from core.interfaces.positioning_services import (
    IArrowRotationCalculator,
)
from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)

logger = logging.getLogger(__name__)


class ArrowRotationCalculatorService(IArrowRotationCalculator):
    """
    Pure algorithmic service for calculating arrow rotation angles.

    Implements rotation calculation algorithms without any UI dependencies.
    Each motion type has its own rotation strategy based on proven algorithms.
    """

    def __init__(self):
        """Initialize the rotation calculator with angle mappings."""

        # Static arrow rotation angles (arrows point inward by default)
        self._static_rotation_map = {
            Location.NORTH: 180.0,
            Location.NORTHEAST: 225.0,
            Location.EAST: 270.0,
            Location.SOUTHEAST: 315.0,
            Location.SOUTH: 0.0,
            Location.SOUTHWEST: 45.0,
            Location.WEST: 90.0,
            Location.NORTHWEST: 135.0,
        }

        # PRO rotation angles by rotation direction
        self._pro_clockwise_map = {
            Location.NORTH: 315,
            Location.EAST: 45,
            Location.SOUTH: 135,
            Location.WEST: 225,
            Location.NORTHEAST: 0,
            Location.SOUTHEAST: 90,
            Location.SOUTHWEST: 180,
            Location.NORTHWEST: 270,
        }

        self._pro_counter_clockwise_map = {
            Location.NORTH: 315,
            Location.EAST: 225,
            Location.SOUTH: 135,
            Location.WEST: 45,
            Location.NORTHEAST: 270,
            Location.SOUTHEAST: 180,
            Location.SOUTHWEST: 90,
            Location.NORTHWEST: 0,
        }

        # ANTI rotation angles by rotation direction
        self._anti_clockwise_map = {
            Location.NORTH: 315,
            Location.EAST: 225,
            Location.SOUTH: 135,
            Location.WEST: 45,
            Location.NORTHEAST: 270,
            Location.SOUTHEAST: 180,
            Location.SOUTHWEST: 90,
            Location.NORTHWEST: 0,
        }

        self._anti_counter_clockwise_map = {
            Location.NORTH: 315,
            Location.EAST: 45,
            Location.SOUTH: 135,
            Location.WEST: 225,
            Location.NORTHEAST: 0,
            Location.SOUTHEAST: 90,
            Location.SOUTHWEST: 180,
            Location.NORTHWEST: 270,
        }

        # DASH rotation angles by rotation direction
        self._dash_clockwise_map = {
            Location.NORTH: 270,
            Location.EAST: 0,
            Location.SOUTH: 90,
            Location.WEST: 180,
            Location.NORTHEAST: 315,
            Location.SOUTHEAST: 45,
            Location.SOUTHWEST: 135,
            Location.NORTHWEST: 225,
        }

        self._dash_counter_clockwise_map = {
            Location.NORTH: 270,
            Location.EAST: 180,
            Location.SOUTH: 90,
            Location.WEST: 0,
            Location.NORTHEAST: 225,
            Location.SOUTHEAST: 135,
            Location.SOUTHWEST: 45,
            Location.NORTHWEST: 315,
        }

        # DASH NO_ROTATION mapping (start_loc, end_loc) -> angle
        self._dash_no_rotation_map = {
            (Location.NORTH, Location.SOUTH): 90,
            (Location.EAST, Location.WEST): 180,
            (Location.SOUTH, Location.NORTH): 270,
            (Location.WEST, Location.EAST): 0,
            (Location.SOUTHEAST, Location.NORTHWEST): 225,
            (Location.SOUTHWEST, Location.NORTHEAST): 315,
            (Location.NORTHWEST, Location.SOUTHEAST): 45,
            (Location.NORTHEAST, Location.SOUTHWEST): 135,
        }

    def calculate_rotation(self, motion: MotionData, location: Location) -> float:
        """
        Calculate arrow rotation angle based on motion type and location.

        Args:
            motion: Motion data containing type and rotation direction
            location: Calculated arrow location

        Returns:
            Rotation angle in degrees (0-360)
        """
        if motion.motion_type == MotionType.STATIC:
            return self._calculate_static_rotation(location)
        elif motion.motion_type == MotionType.PRO:
            return self._calculate_pro_rotation(motion, location)
        elif motion.motion_type == MotionType.ANTI:
            return self._calculate_anti_rotation(motion, location)
        elif motion.motion_type == MotionType.DASH:
            return self._calculate_dash_rotation(motion, location)
        elif motion.motion_type == MotionType.FLOAT:
            return self._calculate_float_rotation(motion, location)
        else:
            logger.warning(f"Unknown motion type: {motion.motion_type}, returning 0.0")
            return 0.0

    def _calculate_static_rotation(self, location: Location) -> float:
        """Calculate rotation for static arrows (point inward)."""
        return self._static_rotation_map.get(location, 0.0)

    def _calculate_pro_rotation(self, motion: MotionData, location: Location) -> float:
        """Calculate rotation for PRO arrows based on rotation direction."""
        if motion.prop_rot_dir == RotationDirection.CLOCKWISE:
            return self._pro_clockwise_map.get(location, 0.0)
        else:  # COUNTER_CLOCKWISE
            return self._pro_counter_clockwise_map.get(location, 0.0)

    def _calculate_anti_rotation(self, motion: MotionData, location: Location) -> float:
        """Calculate rotation for ANTI arrows based on rotation direction."""
        if motion.prop_rot_dir == RotationDirection.CLOCKWISE:
            return self._anti_clockwise_map.get(location, 0.0)
        else:  # COUNTER_CLOCKWISE
            return self._anti_counter_clockwise_map.get(location, 0.0)

    def _calculate_dash_rotation(self, motion: MotionData, location: Location) -> float:
        """Calculate rotation for DASH arrows with special NO_ROTATION handling."""
        # Handle NO_ROTATION case first (most common for dash)
        if motion.prop_rot_dir == RotationDirection.NO_ROTATION:
            return self._dash_no_rotation_map.get(
                (motion.start_loc, motion.end_loc), 0.0
            )

        # Handle rotation-based dash arrows
        if motion.prop_rot_dir == RotationDirection.CLOCKWISE:
            return self._dash_clockwise_map.get(location, 0.0)
        else:  # COUNTER_CLOCKWISE
            return self._dash_counter_clockwise_map.get(location, 0.0)

    def _calculate_float_rotation(
        self, motion: MotionData, location: Location
    ) -> float:
        """Calculate rotation for FLOAT arrows (similar to PRO)."""
        return self._calculate_pro_rotation(motion, location)

    def get_supported_motion_types(self) -> list[MotionType]:
        """Get list of motion types supported by this calculator."""
        return [
            MotionType.STATIC,
            MotionType.PRO,
            MotionType.ANTI,
            MotionType.DASH,
            MotionType.FLOAT,
        ]

    def validate_motion_data(self, motion: MotionData) -> bool:
        """Validate that motion data is suitable for rotation calculation."""
        if not motion:
            return False

        if motion.motion_type not in self.get_supported_motion_types():
            return False

        # Validate rotation direction is provided
        if motion.prop_rot_dir is None:
            return False

        return True
