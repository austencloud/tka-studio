"""
Arrow Adjustment Calculator Service

Pure algorithmic service for calculating arrow position adjustments.
Extracted from ArrowPositioningService to follow single responsibility principle.

This service handles:
- Default adjustments based on motion type and placement key
- Special adjustments for specific letters and configurations
- Quadrant-based directional adjustments
- Integration with placement services

No UI dependencies, completely testable in isolation.
"""

import logging
from typing import Optional, Union

from desktop.modern.src.core.interfaces.positioning_services import (
    IArrowAdjustmentCalculator,
)
from desktop.modern.src.domain.models.core_models import (
    Location,
    MotionData,
    MotionType,
    RotationDirection,
)
from desktop.modern.src.domain.models.pictograph_models import ArrowData, PictographData
from PyQt6.QtCore import QPointF

from .default_placement_service import DefaultPlacementService
from .placement_key_service import PlacementKeyService

logger = logging.getLogger(__name__)


class ArrowAdjustmentCalculatorService(IArrowAdjustmentCalculator):
    """
    Pure algorithmic service for calculating arrow position adjustments.

    Implements the complete adjustment pipeline:
    1. Default adjustments based on motion type and placement key
    2. Special adjustments for specific letters and configurations
    3. Quadrant-based directional adjustments

    No UI dependencies, completely testable in isolation.
    """

    def __init__(
        self,
        default_placement_service: Optional[DefaultPlacementService] = None,
        placement_key_service: Optional[PlacementKeyService] = None,
    ):
        """
        Initialize the adjustment calculator.

        Args:
            default_placement_service: Service for default placement calculations
            placement_key_service: Service for generating placement keys
        """
        self.default_placement_service = (
            default_placement_service or DefaultPlacementService()
        )
        self.placement_key_service = placement_key_service or PlacementKeyService()

    def calculate_adjustment(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> QPointF:
        """
        Calculate position adjustment for arrow based on placement rules.

        Implements the complete adjustment pipeline:
        1. Default adjustments based on motion type and placement key
        2. Special adjustments for specific letters and configurations
        3. Quadrant-based directional adjustments

        Args:
            arrow_data: Arrow data including motion and color
            pictograph_data: Pictograph context for special placement rules

        Returns:
            QPointF representing the adjustment offset
        """
        motion = arrow_data.motion_data
        if not motion:
            return QPointF(0, 0)

        # Step 1: Get default adjustment
        default_adjustment = self._get_default_adjustment(arrow_data)

        # Step 2: Check for special adjustments (letter-specific overrides)
        special_adjustment = self._get_special_adjustment(arrow_data, pictograph_data)
        if special_adjustment is not None:
            # Special adjustment overrides default
            adjustment = special_adjustment
        else:
            # Use default adjustment
            adjustment = default_adjustment

        # Step 3: Apply quadrant-based directional adjustments
        final_adjustment = self._apply_quadrant_adjustments(arrow_data, adjustment)

        logger.debug(
            f"Adjustment calculation for {arrow_data.color} arrow: "
            f"default={default_adjustment}, special={special_adjustment}, "
            f"final={final_adjustment}"
        )

        return final_adjustment

    def _get_default_adjustment(self, arrow_data: ArrowData) -> QPointF:
        """
        Get default adjustment using data-driven placement system.

        Args:
            arrow_data: Arrow data with motion information

        Returns:
            QPointF representing the default adjustment
        """
        motion = arrow_data.motion_data
        if not motion:
            return QPointF(0, 0)

        # Generate placement key using the key service
        placement_key = self.placement_key_service.generate_placement_key(motion)

        # Get adjustment from default placement service
        adjustment = self.default_placement_service.get_default_adjustment(
            motion, grid_mode="diamond", placement_key=placement_key
        )

        return adjustment

    def _get_special_adjustment(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Optional[QPointF]:
        """
        Get special adjustment for specific letters and configurations.

        Special adjustments override default adjustments for specific cases
        like certain letters or motion combinations that need custom positioning.

        Args:
            arrow_data: Arrow data with motion and color
            pictograph_data: Pictograph context for letter-specific rules

        Returns:
            QPointF if special adjustment applies, None otherwise
        """
        # TODO: Implement special placement logic
        # This would load from special placement JSON files or rules
        # For now, return None (no special adjustments)

        letter = pictograph_data.letter
        motion = arrow_data.motion_data

        if not letter or not motion:
            return None

        # Placeholder for future special adjustment logic
        # Example: if letter == "A" and motion.motion_type == MotionType.PRO:
        #     return QPointF(10, 5)  # Custom adjustment for letter A PRO arrows

        return None

    def _apply_quadrant_adjustments(
        self, arrow_data: ArrowData, base_adjustment: QPointF
    ) -> QPointF:
        """
        Apply quadrant-based directional adjustments using positioning logic.

        This implements the exact quadrant adjustment algorithm from the original service.

        Args:
            arrow_data: Arrow data with motion information
            base_adjustment: Base adjustment to modify

        Returns:
            QPointF with quadrant adjustments applied
        """
        motion = arrow_data.motion_data
        if not motion:
            return base_adjustment

        # Step 1: Generate directional tuples for all 4 quadrants
        directional_tuples = self._generate_directional_tuples(
            motion, int(base_adjustment.x()), int(base_adjustment.y())
        )

        # Step 2: Get quadrant index for this arrow
        quadrant_index = self._get_quadrant_index(motion)

        # Step 3: Apply the quadrant-specific adjustment
        if directional_tuples and 0 <= quadrant_index < len(directional_tuples):
            adjusted_x, adjusted_y = directional_tuples[quadrant_index]
            return QPointF(adjusted_x, adjusted_y)

        return base_adjustment

    def get_adjustment_info(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> dict:
        """
        Get detailed information about adjustment calculation for debugging.

        Args:
            arrow_data: Arrow data
            pictograph_data: Pictograph context

        Returns:
            Dictionary with adjustment calculation details
        """
        motion = arrow_data.motion_data
        if not motion:
            return {"error": "No motion data"}

        default_adjustment = self._get_default_adjustment(arrow_data)
        special_adjustment = self._get_special_adjustment(arrow_data, pictograph_data)
        final_adjustment = self.calculate_adjustment(arrow_data, pictograph_data)

        placement_key = self.placement_key_service.generate_placement_key(motion)

        return {
            "placement_key": placement_key,
            "default_adjustment": {
                "x": default_adjustment.x(),
                "y": default_adjustment.y(),
            },
            "special_adjustment": (
                {"x": special_adjustment.x(), "y": special_adjustment.y()}
                if special_adjustment
                else None
            ),
            "final_adjustment": {"x": final_adjustment.x(), "y": final_adjustment.y()},
            "motion_type": motion.motion_type.value,
            "color": arrow_data.color,
            "letter": pictograph_data.letter,
        }

    def validate_arrow_data(self, arrow_data: ArrowData) -> bool:
        """
        Validate that arrow data is suitable for adjustment calculation.

        Args:
            arrow_data: Arrow data to validate

        Returns:
            True if arrow data is valid for adjustment calculation
        """
        if not arrow_data:
            return False

        if not arrow_data.motion_data:
            return False

        # Validate motion data has required fields
        motion = arrow_data.motion_data
        return motion.motion_type is not None and motion.start_loc is not None

    def _generate_directional_tuples(
        self, motion: MotionData, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Generate directional tuples for all 4 quadrants using positioning logic."""
        motion_type = motion.motion_type
        prop_rot_dir = motion.prop_rot_dir

        # Determine grid mode (simplified for now - always diamond)
        grid_mode = "diamond"

        if motion_type == MotionType.PRO:
            return self._get_pro_directional_tuples(grid_mode, prop_rot_dir, x, y)
        elif motion_type == MotionType.ANTI:
            return self._get_anti_directional_tuples(grid_mode, prop_rot_dir, x, y)
        elif motion_type == MotionType.STATIC:
            return self._get_static_directional_tuples(grid_mode, prop_rot_dir, x, y)
        elif motion_type == MotionType.DASH:
            return self._get_dash_directional_tuples(grid_mode, prop_rot_dir, x, y)
        elif motion_type == MotionType.FLOAT:
            return self._get_float_directional_tuples(motion, x, y)
        else:
            return [(x, y)] * 4

    def _get_pro_directional_tuples(
        self, grid_mode: str, prop_rot_dir: RotationDirection, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Get PRO directional tuples using positioning mapping."""
        if grid_mode == "diamond":
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(x, y), (-y, x), (-x, -y), (y, -x)]
            else:  # COUNTER_CLOCKWISE
                return [(-y, -x), (x, -y), (y, x), (-x, y)]
        else:  # box mode
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(-x, y), (-y, -x), (x, -y), (y, x)]
            else:  # COUNTER_CLOCKWISE
                return [(x, y), (-y, x), (-x, -y), (y, -x)]

    def _get_anti_directional_tuples(
        self, grid_mode: str, prop_rot_dir: RotationDirection, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Get ANTI directional tuples using positioning mapping."""
        if grid_mode == "diamond":
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(-y, -x), (x, -y), (y, x), (-x, y)]
            else:  # COUNTER_CLOCKWISE
                return [(x, y), (-y, x), (-x, -y), (y, -x)]
        else:  # box mode
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(-x, y), (-y, -x), (x, -y), (y, x)]
            else:  # COUNTER_CLOCKWISE
                return [(x, y), (-y, x), (-x, -y), (y, -x)]

    def _get_static_directional_tuples(
        self, grid_mode: str, prop_rot_dir: RotationDirection, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Get STATIC directional tuples using positioning mapping."""
        if prop_rot_dir == RotationDirection.NO_ROTATION:
            return [(x, y), (-x, -y), (-y, x), (y, -x)]

        if grid_mode == "diamond":
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]
            else:  # COUNTER_CLOCKWISE
                return [(-x, -y), (y, -x), (x, y), (-y, x)]
        else:  # box mode
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(x, y), (-y, x), (-x, -y), (y, -x)]
            else:  # COUNTER_CLOCKWISE
                return [(-y, -x), (x, -y), (y, x), (-x, y)]

    def _get_dash_directional_tuples(
        self, grid_mode: str, prop_rot_dir: RotationDirection, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Get DASH directional tuples using positioning mapping."""
        if grid_mode == "diamond":
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]
            elif prop_rot_dir == RotationDirection.COUNTER_CLOCKWISE:
                return [(-x, -y), (y, -x), (x, y), (-y, x)]
            else:  # NO_ROTATION
                return [(x, y), (-y, -x), (x, -y), (y, -x)]
        else:  # box mode
            if prop_rot_dir == RotationDirection.CLOCKWISE:
                return [(-y, x), (-x, -y), (y, -x), (x, y)]
            elif prop_rot_dir == RotationDirection.COUNTER_CLOCKWISE:
                return [(-x, y), (-y, -x), (x, -y), (y, x)]
            else:  # NO_ROTATION
                return [(x, y), (-y, x), (-x, -y), (y, -x)]

    def _get_float_directional_tuples(
        self, motion: MotionData, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Get FLOAT directional tuples using positioning mapping."""
        # Use simplified float logic (CW handpath)
        return [(x, y), (-y, x), (-x, -y), (y, -x)]

    def _get_quadrant_index(self, motion: MotionData) -> int:
        """Get quadrant index for arrow using positioning logic."""
        # For diamond grid (simplified - always diamond for now)
        arrow_location = self._calculate_arrow_location(motion)

        if motion.motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
            # Shift arrows use layer2 quadrant mapping
            location_to_index = {
                Location.NORTHEAST: 0,
                Location.SOUTHEAST: 1,
                Location.SOUTHWEST: 2,
                Location.NORTHWEST: 3,
            }
        else:  # STATIC, DASH
            # Static/dash arrows use hand point quadrant mapping
            location_to_index = {
                Location.NORTH: 0,
                Location.EAST: 1,
                Location.SOUTH: 2,
                Location.WEST: 3,
            }

        return location_to_index.get(arrow_location, 0)

    def _calculate_arrow_location(self, motion: MotionData) -> Location:
        """Calculate arrow location - simplified version for adjustment calculation."""
        if motion.motion_type == MotionType.STATIC:
            return motion.start_loc
        elif motion.motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
            # Simplified shift location calculation
            direction_pairs = {
                frozenset({Location.NORTH, Location.EAST}): Location.NORTHEAST,
                frozenset({Location.EAST, Location.SOUTH}): Location.SOUTHEAST,
                frozenset({Location.SOUTH, Location.WEST}): Location.SOUTHWEST,
                frozenset({Location.WEST, Location.NORTH}): Location.NORTHWEST,
                frozenset({Location.NORTHEAST, Location.NORTHWEST}): Location.NORTH,
                frozenset({Location.NORTHEAST, Location.SOUTHEAST}): Location.EAST,
                frozenset({Location.SOUTHWEST, Location.SOUTHEAST}): Location.SOUTH,
                frozenset({Location.NORTHWEST, Location.SOUTHWEST}): Location.WEST,
            }
            return direction_pairs.get(
                frozenset({motion.start_loc, motion.end_loc}), motion.start_loc
            )
        else:
            return motion.start_loc
