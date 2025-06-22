"""
Arrow Coordinate System Service

Pure service for managing coordinate systems and initial position calculations.
Extracted from ArrowPositioningService to follow single responsibility principle.

This service handles:
- Scene coordinate system management (950x950 scene with center at 475,475)
- Hand point coordinates (for STATIC/DASH arrows)
- Layer2 point coordinates (for PRO/ANTI/FLOAT arrows)
- Initial position computation based on motion type

No UI dependencies, completely testable in isolation.
"""

import logging
from PyQt6.QtCore import QPointF

from desktop.modern.src.core.interfaces.positioning_services import (
    IArrowCoordinateSystemService,
)
from desktop.modern.src.domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
)

logger = logging.getLogger(__name__)


class ArrowCoordinateSystemService(IArrowCoordinateSystemService):
    """
    Pure service for coordinate system management and initial position calculation.

    Manages the TKA coordinate systems without any UI dependencies.
    Provides precise coordinate mappings for different arrow types.
    """

    def __init__(self):
        """Initialize the coordinate system with precise TKA coordinates."""
        # Scene dimensions: 950x950 scene with center at (475, 475)
        self.SCENE_SIZE = 950
        self.CENTER_X = 475.0
        self.CENTER_Y = 475.0

        # Hand point coordinates (for STATIC/DASH arrows)
        # These are the inner grid positions where props are placed
        self.HAND_POINTS = {
            Location.NORTH: QPointF(475.0, 331.9),
            Location.EAST: QPointF(618.1, 475.0),
            Location.SOUTH: QPointF(475.0, 618.1),
            Location.WEST: QPointF(331.9, 475.0),
            # Diagonal hand points (calculated from radius)
            Location.NORTHEAST: QPointF(618.1, 331.9),
            Location.SOUTHEAST: QPointF(618.1, 618.1),
            Location.SOUTHWEST: QPointF(331.9, 618.1),
            Location.NORTHWEST: QPointF(331.9, 331.9),
        }

        # Layer2 point coordinates (for PRO/ANTI/FLOAT arrows)
        # Using DIAMOND layer2 points from circle_coords.json
        self.LAYER2_POINTS = {
            # Diamond layer2 points are diagonal positions
            Location.NORTHEAST: QPointF(618.1, 331.9),
            Location.SOUTHEAST: QPointF(618.1, 618.1),
            Location.SOUTHWEST: QPointF(331.9, 618.1),
            Location.NORTHWEST: QPointF(331.9, 331.9),
            # For cardinal directions, map to nearest diagonal
            Location.NORTH: QPointF(618.1, 331.9),  # Maps to NE
            Location.EAST: QPointF(618.1, 618.1),  # Maps to SE
            Location.SOUTH: QPointF(331.9, 618.1),  # Maps to SW
            Location.WEST: QPointF(331.9, 331.9),  # Maps to NW
        }

    def get_initial_position(self, motion: MotionData, location: Location) -> QPointF:
        """
        Get initial position coordinates based on motion type and location.

        Args:
            motion: Motion data to determine coordinate system (hand points vs layer2)
            location: Arrow location

        Returns:
            QPointF representing the initial position coordinates
        """
        if motion.motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
            # Shift arrows use layer2 points
            return self._get_layer2_coords(location)
        elif motion.motion_type in [MotionType.STATIC, MotionType.DASH]:
            # Static/dash arrows use hand points
            return self._get_hand_point_coords(location)
        else:
            # Default fallback
            logger.warning(f"Unknown motion type: {motion.motion_type}, using center")
            return self.get_scene_center()

    def get_scene_center(self) -> QPointF:
        """Get the center point of the scene coordinate system."""
        return QPointF(self.CENTER_X, self.CENTER_Y)

    def _get_layer2_coords(self, location: Location) -> QPointF:
        """Get layer2 point coordinates for shift arrows."""
        coords = self.LAYER2_POINTS.get(location)
        if coords is None:
            logger.warning(
                f"No layer2 coordinates for location: {location}, using center"
            )
            return self.get_scene_center()
        return coords

    def _get_hand_point_coords(self, location: Location) -> QPointF:
        """Get hand point coordinates for static/dash arrows."""
        coords = self.HAND_POINTS.get(location)
        if coords is None:
            logger.warning(
                f"No hand point coordinates for location: {location}, using center"
            )
            return self.get_scene_center()
        return coords

    def get_scene_dimensions(self) -> tuple[int, int]:
        """
        Get the scene dimensions.

        Returns:
            Tuple of (width, height) for the scene
        """
        return (self.SCENE_SIZE, self.SCENE_SIZE)

    def get_coordinate_info(self, location: Location) -> dict:
        """
        Get detailed coordinate information for debugging.

        Args:
            location: Location to get coordinate info for

        Returns:
            Dictionary with coordinate details
        """
        hand_point = self.HAND_POINTS.get(location)
        layer2_point = self.LAYER2_POINTS.get(location)

        return {
            "location": location.value,
            "hand_point": {
                "x": hand_point.x() if hand_point else None,
                "y": hand_point.y() if hand_point else None,
            },
            "layer2_point": {
                "x": layer2_point.x() if layer2_point else None,
                "y": layer2_point.y() if layer2_point else None,
            },
            "scene_center": {"x": self.CENTER_X, "y": self.CENTER_Y},
            "scene_size": self.SCENE_SIZE,
        }

    def validate_coordinates(self, point: QPointF) -> bool:
        """
        Validate that coordinates are within scene bounds.

        Args:
            point: Point to validate

        Returns:
            True if point is within scene bounds
        """
        return 0 <= point.x() <= self.SCENE_SIZE and 0 <= point.y() <= self.SCENE_SIZE

    def get_all_hand_points(self) -> dict[Location, QPointF]:
        """Get all hand point coordinates."""
        return self.HAND_POINTS.copy()

    def get_all_layer2_points(self) -> dict[Location, QPointF]:
        """Get all layer2 point coordinates."""
        return self.LAYER2_POINTS.copy()

    def get_supported_locations(self) -> list[Location]:
        """Get list of supported location values."""
        return [
            Location.NORTH,
            Location.EAST,
            Location.SOUTH,
            Location.WEST,
            Location.NORTHEAST,
            Location.SOUTHEAST,
            Location.SOUTHWEST,
            Location.NORTHWEST,
        ]
