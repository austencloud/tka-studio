"""
Directional Tuple Calculator Service

Framework-agnostic service for generating quadrant-based directional adjustments
using rotation matrices. Replicates the legacy DirectionalTupleGenerator logic.

This service provides the core directional tuple generation that was
missing from the modern arrow positioning system.
"""

import logging

from desktop.modern.application.services.core.interfaces.positioning_services import (
    IDirectionalTupleCalculator,
)
from desktop.modern.domain.models import (
    Location,
    MotionData,
    MotionType,
    RotationDirection,
)

logger = logging.getLogger(__name__)


class DirectionalTupleCalculator(IDirectionalTupleCalculator):
    """
    Framework-agnostic service for generating directional tuples using legacy rotation matrix logic.

    This replicates the exact behavior of the legacy DirectionalTupleGenerator
    to ensure arrows are positioned correctly with quadrant-based adjustments.
    """

    def __init__(self):
        """Initialize the directional tuple mappings."""
        self._setup_rotation_mappings()

    def _setup_rotation_mappings(self):
        """Setup the rotation matrix mappings for different motion types and grid modes."""

        # Diamond grid mappings for PRO/ANTI motions
        self._shift_mapping_diamond = {
            MotionType.PRO: {
                RotationDirection.CLOCKWISE: lambda x, y: [
                    (x, y),
                    (-y, x),
                    (-x, -y),
                    (y, -x),
                ],
                RotationDirection.COUNTER_CLOCKWISE: lambda x, y: [
                    (-y, -x),
                    (x, -y),
                    (y, x),
                    (-x, y),
                ],
            },
            MotionType.ANTI: {
                RotationDirection.CLOCKWISE: lambda x, y: [
                    (-y, -x),
                    (x, -y),
                    (y, x),
                    (-x, y),
                ],
                RotationDirection.COUNTER_CLOCKWISE: lambda x, y: [
                    (x, y),
                    (-y, x),
                    (-x, -y),
                    (y, -x),
                ],
            },
        }

        # Box grid mappings for PRO/ANTI motions
        self._shift_mapping_box = {
            MotionType.PRO: {
                RotationDirection.CLOCKWISE: lambda x, y: [
                    (x, y),
                    (-y, x),
                    (-x, -y),
                    (y, -x),
                ],
                RotationDirection.COUNTER_CLOCKWISE: lambda x, y: [
                    (-y, -x),
                    (x, -y),
                    (y, x),
                    (-x, y),
                ],
            },
            MotionType.ANTI: {
                RotationDirection.CLOCKWISE: lambda x, y: [
                    (-y, -x),
                    (x, -y),
                    (y, x),
                    (-x, y),
                ],
                RotationDirection.COUNTER_CLOCKWISE: lambda x, y: [
                    (x, y),
                    (-y, x),
                    (-x, -y),
                    (y, -x),
                ],
            },
        }

        # DASH motion mappings
        self._dash_mapping = {
            "diamond": {
                RotationDirection.CLOCKWISE: lambda x, y: [
                    (x, -y),
                    (y, x),
                    (-x, y),
                    (-y, -x),
                ],
                RotationDirection.COUNTER_CLOCKWISE: lambda x, y: [
                    (-x, -y),
                    (y, -x),
                    (x, y),
                    (-y, x),
                ],
                RotationDirection.NO_ROTATION: lambda x, y: [
                    (x, y),
                    (-y, -x),
                    (x, -y),
                    (y, x),
                ],
            },
            "box": {
                RotationDirection.CLOCKWISE: lambda x, y: [
                    (-y, x),
                    (-x, -y),
                    (y, -x),
                    (x, y),
                ],
                RotationDirection.COUNTER_CLOCKWISE: lambda x, y: [
                    (-x, y),
                    (-y, -x),
                    (x, -y),
                    (y, x),
                ],
                RotationDirection.NO_ROTATION: lambda x, y: [
                    (x, y),
                    (-y, x),
                    (-x, -y),
                    (y, -x),
                ],
            },
        }

        # STATIC motion mappings
        self._static_mapping = {
            "diamond": {
                RotationDirection.CLOCKWISE: lambda x, y: [
                    (x, -y),
                    (y, x),
                    (-x, y),
                    (-y, -x),
                ],
                RotationDirection.COUNTER_CLOCKWISE: lambda x, y: [
                    (-x, -y),
                    (y, -x),
                    (x, y),
                    (-y, x),
                ],
            },
            "box": {
                RotationDirection.CLOCKWISE: lambda x, y: [
                    (x, y),
                    (-y, x),
                    (-x, -y),
                    (y, -x),
                ],
                RotationDirection.COUNTER_CLOCKWISE: lambda x, y: [
                    (-y, -x),
                    (x, -y),
                    (y, x),
                    (-x, y),
                ],
            },
        }

    def calculate_directional_tuple(
        self, motion: MotionData, location: Location
    ) -> tuple[float, float]:
        """
        Calculate directional tuple for arrow positioning.

        Args:
            motion: Motion data containing type and rotation direction
            location: Arrow location

        Returns:
            Tuple of (x_offset, y_offset) directional adjustments
        """
        # Use default base values for calculation
        base_x, base_y = 1.0, 1.0

        # Generate all directional tuples
        tuples = self.generate_directional_tuples(motion, base_x, base_y)

        # For now, return the first tuple as a simple implementation
        # In a full implementation, you would map the location to a specific tuple
        if tuples:
            return tuples[0]
        else:
            return (base_x, base_y)

    def generate_directional_tuples(
        self, motion: MotionData, base_x: float, base_y: float
    ) -> list[tuple[float, float]]:
        """
        Generate directional tuples for the given motion and base adjustment.

        Args:
            motion: Motion data containing type, rotation, and location info
            base_x: Base X adjustment value
            base_y: Base Y adjustment value

        Returns:
            List of 4 directional tuples representing rotated adjustments
        """
        motion_type = motion.motion_type
        prop_rot_dir = motion.prop_rot_dir

        # Determine grid mode based on motion location
        grid_mode = self._determine_grid_mode(motion)

        logger.debug(
            f"Generating directional tuples: motion={motion_type.value}, "
            f"rotation={prop_rot_dir.value}, grid={grid_mode}, base=({base_x}, {base_y})"
        )

        # Handle different motion types
        if motion_type in [MotionType.PRO, MotionType.ANTI]:
            return self._handle_shift_tuples(
                motion_type, prop_rot_dir, grid_mode, base_x, base_y
            )
        elif motion_type == MotionType.DASH:
            return self._handle_dash_tuples(prop_rot_dir, grid_mode, base_x, base_y)
        elif motion_type == MotionType.STATIC:
            return self._handle_static_tuples(prop_rot_dir, grid_mode, base_x, base_y)
        elif motion_type == MotionType.FLOAT:
            return self._handle_float_tuples(motion, base_x, base_y)
        else:
            logger.warning(f"Unknown motion type: {motion_type}, using default")
            return [(base_x, base_y)] * 4

    def _determine_grid_mode(self, motion: MotionData) -> str:
        """
        Determine grid mode (diamond/box) based on motion location.

        Args:
            motion: Motion data with location information

        Returns:
            Grid mode string ("diamond" or "box")
        """
        # For shift motions, use start location to determine grid mode
        location = motion.start_loc

        if location in [
            Location.NORTHEAST,
            Location.SOUTHEAST,
            Location.SOUTHWEST,
            Location.NORTHWEST,
        ]:
            return "box"
        else:
            return "diamond"

    def _handle_shift_tuples(
        self,
        motion_type: MotionType,
        prop_rot_dir: RotationDirection,
        grid_mode: str,
        x: float,
        y: float,
    ) -> list[tuple[float, float]]:
        """Handle PRO and ANTI motion directional tuples."""
        if grid_mode == "diamond":
            mapping = self._shift_mapping_diamond.get(motion_type, {})
        else:  # box
            mapping = self._shift_mapping_box.get(motion_type, {})

        transform_func = mapping.get(prop_rot_dir, lambda x, y: [(x, y)] * 4)
        result = transform_func(x, y)

        logger.debug(
            f"Shift tuples for {motion_type.value}/{prop_rot_dir.value}/{grid_mode}: {result}"
        )
        return result

    def _handle_dash_tuples(
        self, prop_rot_dir: RotationDirection, grid_mode: str, x: float, y: float
    ) -> list[tuple[float, float]]:
        """Handle DASH motion directional tuples."""
        mapping = self._dash_mapping.get(grid_mode, {})
        transform_func = mapping.get(prop_rot_dir, lambda x, y: [(x, y)] * 4)
        result = transform_func(x, y)

        logger.debug(f"Dash tuples for {prop_rot_dir.value}/{grid_mode}: {result}")
        return result

    def _handle_static_tuples(
        self, prop_rot_dir: RotationDirection, grid_mode: str, x: float, y: float
    ) -> list[tuple[float, float]]:
        """Handle STATIC motion directional tuples."""
        if prop_rot_dir == RotationDirection.NO_ROTATION:
            result = [(x, y), (-x, -y), (-y, x), (y, -x)]
        else:
            mapping = self._static_mapping.get(grid_mode, {})
            transform_func = mapping.get(prop_rot_dir, lambda x, y: [(x, y)] * 4)
            result = transform_func(x, y)

        logger.debug(f"Static tuples for {prop_rot_dir.value}/{grid_mode}: {result}")
        return result

    def _handle_float_tuples(
        self, motion: MotionData, x: float, y: float
    ) -> list[tuple[float, float]]:
        """Handle FLOAT motion directional tuples."""
        # For FLOAT motions, we need to determine handpath direction
        # This is a simplified version - in full implementation would use HandpathCalculator
        handpath_direction = self._calculate_handpath_direction(
            motion.start_loc, motion.end_loc
        )

        if handpath_direction == "cw":
            result = [(x, y), (-y, x), (-x, -y), (y, -x)]
        else:  # COUNTER_CLOCKWISE
            result = [(-y, -x), (x, -y), (y, x), (-x, y)]

        logger.debug(f"Float tuples for {handpath_direction}: {result}")
        return result

    def _calculate_handpath_direction(
        self, start_loc: Location, end_loc: Location
    ) -> str:
        """
        Calculate handpath direction for FLOAT motions.

        Args:
            start_loc: Starting location
            end_loc: Ending location

        Returns:
            Direction string ("cw" or "COUNTER_CLOCKWISE")
        """
        # Standard location order for handpath calculation
        location_order = [
            Location.NORTH,
            Location.NORTHEAST,
            Location.EAST,
            Location.SOUTHEAST,
            Location.SOUTH,
            Location.SOUTHWEST,
            Location.WEST,
            Location.NORTHWEST,
        ]

        try:
            start_idx = location_order.index(start_loc)
            end_idx = location_order.index(end_loc)

            # Calculate shortest path direction
            diff = (end_idx - start_idx) % len(location_order)
            return "cw" if diff <= 4 else "COUNTER_CLOCKWISE"
        except ValueError:
            # Fallback if locations not in standard order
            return "cw"
