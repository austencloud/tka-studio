"""
Quadrant Index Service

Replicates the legacy QuadrantIndexHandler logic for determining
which directional tuple to use based on arrow location and motion type.

This service provides the quadrant index calculation that was
missing from the modern arrow positioning system.
"""

import logging
from typing import Literal

from desktop.modern.core.interfaces.positioning_services import IQuadrantIndexCalculator
from desktop.modern.domain.models import Location, MotionData, MotionType

logger = logging.getLogger(__name__)


class QuadrantIndexCalculator(IQuadrantIndexCalculator):
    """
    Service for determining quadrant index for directional tuple selection.

    This replicates the exact behavior of the legacy QuadrantIndexHandler
    to ensure the correct directional adjustment is selected from the tuple array.
    """

    def __init__(self):
        """Initialize the quadrant index service."""

    def calculate_quadrant_index(self, location: Location) -> int:
        """
        Calculate quadrant index for the given location.

        Args:
            location: Arrow location

        Returns:
            Quadrant index (0-3)
        """
        # Use the legacy method with minimal motion data
        from desktop.modern.domain.models import MotionData, MotionType

        # Create a minimal motion data to maintain compatibility
        motion = MotionData(
            motion_type=MotionType.STATIC,
            start_location=location,
            end_location=location,
            turns=0.0,
            rotation_direction=None,
        )

        return self.get_quadrant_index(motion, location)

    def get_quadrant_index(
        self, motion: MotionData, arrow_location: Location
    ) -> Literal[0, 1, 2, 3]:
        """
        Get the quadrant index for the given motion and arrow location.

        Args:
            motion: Motion data containing type and location info
            arrow_location: The calculated arrow location

        Returns:
            Quadrant index (0, 1, 2, or 3) for directional tuple selection
        """
        grid_mode = self._determine_grid_mode(motion)
        motion_type = motion.motion_type

        if grid_mode == "diamond":
            if motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
                index = self._diamond_shift_quadrant_index(arrow_location)
            elif motion_type in [MotionType.STATIC, MotionType.DASH]:
                index = self._diamond_static_dash_quadrant_index(arrow_location)
            else:
                index = 0
        elif grid_mode == "box":
            if motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
                index = self._box_shift_quadrant_index(arrow_location)
            elif motion_type in [MotionType.STATIC, MotionType.DASH]:
                index = self._box_static_dash_quadrant_index(arrow_location)
            else:
                index = 0
        else:
            index = 0

        logger.debug(f"Quadrant index result: {index}")
        return index

    def _determine_grid_mode(self, motion: MotionData) -> str:
        """
        Determine grid mode (diamond/box) based on motion location.

        Args:
            motion: Motion data with location information

        Returns:
            Grid mode string ("diamond" or "box")
        """
        # Use start location to determine grid mode (same as DirectionalTupleService)
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

    def _diamond_shift_quadrant_index(self, location: Location) -> Literal[0, 1, 2, 3]:
        """
        Get quadrant index for shift motions (PRO/ANTI/FLOAT) in diamond grid.

        Args:
            location: Arrow location

        Returns:
            Quadrant index for diamond grid shift motions
        """
        location_to_index = {
            Location.NORTHEAST: 0,
            Location.SOUTHEAST: 1,
            Location.SOUTHWEST: 2,
            Location.NORTHWEST: 3,
        }
        return location_to_index.get(location, 0)

    def _diamond_static_dash_quadrant_index(
        self, location: Location
    ) -> Literal[0, 1, 2, 3]:
        """
        Get quadrant index for static/dash motions in diamond grid.

        Args:
            location: Arrow location

        Returns:
            Quadrant index for diamond grid static/dash motions
        """
        location_to_index = {
            Location.NORTH: 0,
            Location.EAST: 1,
            Location.SOUTH: 2,
            Location.WEST: 3,
        }
        return location_to_index.get(location, 0)

    def _box_shift_quadrant_index(self, location: Location) -> Literal[0, 1, 2, 3]:
        """
        Get quadrant index for shift motions (PRO/ANTI/FLOAT) in box grid.

        Args:
            location: Arrow location

        Returns:
            Quadrant index for box grid shift motions
        """
        location_to_index = {
            Location.NORTH: 0,
            Location.EAST: 1,
            Location.SOUTH: 2,
            Location.WEST: 3,
        }
        return location_to_index.get(location, 0)

    def _box_static_dash_quadrant_index(
        self, location: Location
    ) -> Literal[0, 1, 2, 3]:
        """
        Get quadrant index for static/dash motions in box grid.

        Args:
            location: Arrow location

        Returns:
            Quadrant index for box grid static/dash motions
        """
        location_to_index = {
            Location.NORTHEAST: 0,
            Location.SOUTHEAST: 1,
            Location.SOUTHWEST: 2,
            Location.NORTHWEST: 3,
        }
        return location_to_index.get(location, 0)
