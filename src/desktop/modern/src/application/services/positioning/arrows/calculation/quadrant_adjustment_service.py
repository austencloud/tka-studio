"""
Quadrant Adjustment Service

Handles quadrant-based position adjustments and directional modifications.

This service provides:
- Quadrant-based adjustments for different motion types
- Directional tuple generation
- Position-specific modifications

Ported from legacy quadrant adjustment logic.
"""

import logging
from typing import Dict, List, Tuple

from domain.models.core_models import Location, MotionType

# Conditional PyQt6 imports for testing compatibility
try:
    from PyQt6.QtCore import QPointF

    QT_AVAILABLE = True
except ImportError:
    # Create mock QPointF for testing when Qt is not available
    class QPointF:
        def __init__(self, x=0.0, y=0.0):
            self._x = x
            self._y = y

        def x(self):
            return self._x

        def y(self):
            return self._y

    QT_AVAILABLE = False

logger = logging.getLogger(__name__)


class QuadrantAdjustmentService:
    """
    Service for applying quadrant-based position adjustments.

    Handles directional adjustments based on motion properties and locations.
    """

    def __init__(self):
        """Initialize quadrant adjustment mappings."""
        self._quadrant_adjustments = self._load_quadrant_adjustments()

    def apply_quadrant_adjustments(
        self,
        base_adjustment: QPointF,
        motion_type: MotionType,
        start_loc: Location,
        end_loc: Location,
        color: str = "blue",
    ) -> QPointF:
        """
        Apply quadrant-based adjustments to base position.

        Args:
            base_adjustment: Base adjustment from placement lookup
            motion_type: Type of motion (pro, anti, static, etc.)
            start_loc: Starting location
            end_loc: Ending location
            color: Arrow color (blue/red)

        Returns:
            Adjusted position with quadrant modifications applied
        """
        # Generate directional tuple for this motion
        directional_tuple = self.generate_directional_tuple(
            start_loc, end_loc, motion_type
        )

        # Look up quadrant adjustment for this tuple
        quadrant_adj = self._get_quadrant_adjustment(directional_tuple, color)

        # Apply adjustment
        adjusted_x = base_adjustment.x() + quadrant_adj.x()
        adjusted_y = base_adjustment.y() + quadrant_adj.y()

        logger.debug(
            f"Quadrant adjustment: base=({base_adjustment.x()}, {base_adjustment.y()}) "
            f"+ quad=({quadrant_adj.x()}, {quadrant_adj.y()}) "
            f"= ({adjusted_x}, {adjusted_y})"
        )

        return QPointF(adjusted_x, adjusted_y)

    def generate_directional_tuple(
        self, start_loc: Location, end_loc: Location, motion_type: MotionType
    ) -> str:
        """
        Generate directional tuple for quadrant lookup.

        Format: "start_loc-end_loc-motion_type" (e.g., "n-e-pro")

        Args:
            start_loc: Starting location
            end_loc: Ending location
            motion_type: Type of motion

        Returns:
            Directional tuple string
        """
        tuple_str = f"{start_loc.value}-{end_loc.value}-{motion_type.value}"
        logger.debug(f"Generated directional tuple: {tuple_str}")
        return tuple_str

    def _get_quadrant_adjustment(self, directional_tuple: str, color: str) -> QPointF:
        """
        Get quadrant adjustment for directional tuple and color.

        Args:
            directional_tuple: Generated directional tuple
            color: Arrow color

        Returns:
            Quadrant adjustment as QPointF
        """
        # Look up in quadrant adjustments mapping
        color_adjustments = self._quadrant_adjustments.get(color, {})
        adjustment = color_adjustments.get(directional_tuple, (0, 0))

        return QPointF(adjustment[0], adjustment[1])

    def _load_quadrant_adjustments(self) -> Dict[str, Dict[str, Tuple[float, float]]]:
        """
        Load quadrant adjustment mappings.

        In a real implementation, this would load from configuration files.
        For now, we provide basic adjustments based on common patterns.
        """
        return {
            "blue": {
                # Pro motion adjustments
                "n-e-pro": (2.0, -1.0),
                "e-s-pro": (1.0, 2.0),
                "s-w-pro": (-2.0, 1.0),
                "w-n-pro": (-1.0, -2.0),
                # Anti motion adjustments
                "n-e-anti": (-1.0, 1.0),
                "e-s-anti": (-1.0, -1.0),
                "s-w-anti": (1.0, -1.0),
                "w-n-anti": (1.0, 1.0),
                # Static motion adjustments
                "n-n-static": (0.0, -1.5),
                "e-e-static": (1.5, 0.0),
                "s-s-static": (0.0, 1.5),
                "w-w-static": (-1.5, 0.0),
                # Diagonal adjustments
                "ne-se-pro": (1.5, 1.5),
                "se-sw-pro": (-1.5, 1.5),
                "sw-nw-pro": (-1.5, -1.5),
                "nw-ne-pro": (1.5, -1.5),
            },
            "red": {
                # Red adjustments are often mirrored or offset from blue
                "n-e-pro": (-2.0, 1.0),
                "e-s-pro": (-1.0, -2.0),
                "s-w-pro": (2.0, -1.0),
                "w-n-pro": (1.0, 2.0),
                "n-e-anti": (1.0, -1.0),
                "e-s-anti": (1.0, 1.0),
                "s-w-anti": (-1.0, 1.0),
                "w-n-anti": (-1.0, -1.0),
                "n-n-static": (0.0, 1.5),
                "e-e-static": (-1.5, 0.0),
                "s-s-static": (0.0, -1.5),
                "w-w-static": (1.5, 0.0),
                "ne-se-pro": (-1.5, -1.5),
                "se-sw-pro": (1.5, -1.5),
                "sw-nw-pro": (1.5, 1.5),
                "nw-ne-pro": (-1.5, 1.5),
            },
        }

    def get_position_specific_adjustments(
        self, location: Location, motion_type: MotionType
    ) -> List[Tuple[float, float]]:
        """
        Get position-specific adjustments for fine-tuning.

        These are micro-adjustments based on specific location and motion combinations.

        Args:
            location: Location to adjust for
            motion_type: Motion type

        Returns:
            List of (x, y) adjustment tuples
        """
        adjustments = []

        # Location-specific adjustments
        location_adjustments = {
            Location.NORTH: [(0.0, -0.5)],
            Location.SOUTH: [(0.0, 0.5)],
            Location.EAST: [(0.5, 0.0)],
            Location.WEST: [(-0.5, 0.0)],
            Location.NORTHEAST: [(0.3, -0.3)],
            Location.SOUTHEAST: [(0.3, 0.3)],
            Location.SOUTHWEST: [(-0.3, 0.3)],
            Location.NORTHWEST: [(-0.3, -0.3)],
        }

        adjustments.extend(location_adjustments.get(location, []))

        # Motion-specific adjustments
        motion_adjustments = {
            MotionType.PRO: [(0.2, 0.0)],
            MotionType.ANTI: [(-0.2, 0.0)],
            MotionType.STATIC: [(0.0, 0.0)],
            MotionType.DASH: [(0.0, 0.1)],
            MotionType.FLOAT: [(0.1, 0.1)],
        }

        adjustments.extend(motion_adjustments.get(motion_type, []))

        logger.debug(
            f"Position-specific adjustments for {location.value}-{motion_type.value}: {adjustments}"
        )

        return adjustments

    def apply_position_specific_adjustments(
        self, base_position: QPointF, adjustments: List[Tuple[float, float]]
    ) -> QPointF:
        """
        Apply a list of position adjustments to a base position.

        Args:
            base_position: Starting position
            adjustments: List of (x, y) adjustments to apply

        Returns:
            Final adjusted position
        """
        total_x = base_position.x()
        total_y = base_position.y()

        for adj_x, adj_y in adjustments:
            total_x += adj_x
            total_y += adj_y

        return QPointF(total_x, total_y)
