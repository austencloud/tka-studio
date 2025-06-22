"""
Arrow Adjustment Service

Pure service for calculating arrow position adjustments.
Extracted from ArrowManagementService to follow single responsibility principle.

PROVIDES:
- Default adjustment calculation using placement services
- Special adjustment calculation for letter-specific overrides
- Quadrant-based directional adjustments
- Pure algorithms with no Qt dependencies
"""

from typing import Optional, Any
from abc import ABC, abstractmethod

from PyQt6.QtCore import QPointF

from desktop.modern.src.domain.models.core_models import (
    MotionData,
    MotionType,
    RotationDirection,
)
from desktop.modern.src.domain.models.pictograph_models import ArrowData
from desktop.modern.src.domain.models.pictograph_models import PictographData
from .default_placement_service import DefaultPlacementService
from .placement_key_service import PlacementKeyService
from .special_placement_service import SpecialPlacementService


class IArrowAdjustmentService(ABC):
    """Interface for arrow adjustment calculation."""

    @abstractmethod
    def calculate_adjustment(
        self, arrow_data: ArrowData, pictograph_data: Optional[PictographData] = None
    ) -> QPointF:
        """Calculate adjustment for arrow positioning."""
        pass


class ArrowAdjustmentService(IArrowAdjustmentService):
    """
    Pure service for arrow adjustment calculation.

    Handles all adjustment algorithms without Qt dependencies.
    Uses immutable data patterns following TKA architecture.
    """

    def __init__(
        self,
        default_placement_service: Optional[DefaultPlacementService] = None,
        placement_key_service: Optional[PlacementKeyService] = None,
        special_placement_service: Optional[SpecialPlacementService] = None,
    ):
        """Initialize with dependency injection."""
        self.default_placement_service = (
            default_placement_service or DefaultPlacementService()
        )
        self.placement_key_service = placement_key_service or PlacementKeyService()
        self.special_placement_service = (
            special_placement_service or SpecialPlacementService()
        )

    def calculate_adjustment(
        self, arrow_data: ArrowData, pictograph_data: Optional[PictographData] = None
    ) -> QPointF:
        """
        Calculate adjustment using complete adjustment pipeline.

        Implements the complete adjustment pipeline:
        1. Default adjustments based on motion type and placement key
        2. Special adjustments for specific letters and configurations
        3. Quadrant-based directional adjustments
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
        final_adjustment = self._apply_quadrant_adjustments(
            arrow_data, adjustment, pictograph_data
        )

        return final_adjustment

    def _get_default_adjustment(self, arrow_data: ArrowData) -> QPointF:
        """Get default adjustment using data-driven placement system."""
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
        self, arrow_data: ArrowData, pictograph_data: Optional[PictographData] = None
    ) -> Optional[QPointF]:
        """Get special adjustment for letter-specific overrides."""
        if not pictograph_data or not pictograph_data.letter:
            return None

        motion = arrow_data.motion_data
        if not motion:
            return None

        # Use special placement service for letter-specific adjustments
        return self.special_placement_service.get_special_adjustment(
            motion, pictograph_data.letter
        )

    def _apply_quadrant_adjustments(
        self,
        arrow_data: ArrowData,
        base_adjustment: QPointF,
        pictograph_data: Optional[PictographData] = None,
    ) -> QPointF:
        """Apply quadrant-based directional adjustments using positioning logic."""
        motion = arrow_data.motion_data
        if not motion:
            return base_adjustment

        # Step 1: Generate directional tuples for all 4 quadrants
        directional_tuples = self._generate_directional_tuples(
            motion, int(base_adjustment.x()), int(base_adjustment.y())
        )

        # Step 2: Get quadrant index for this arrow
        quadrant_index = self._get_quadrant_index(motion, pictograph_data)

        # Step 3: Apply the quadrant-specific adjustment
        if directional_tuples and 0 <= quadrant_index < len(directional_tuples):
            adjusted_x, adjusted_y = directional_tuples[quadrant_index]
            return QPointF(adjusted_x, adjusted_y)

        return base_adjustment

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

    def _get_quadrant_index(
        self, motion: MotionData, pictograph_data: Optional[PictographData] = None
    ) -> int:
        """Get quadrant index for this arrow (0-3)."""
        # Simplified quadrant calculation - can be enhanced based on specific requirements
        if motion.motion_type in [MotionType.PRO, MotionType.ANTI]:
            # Use start location to determine quadrant
            location_to_quadrant = {
                "north": 0,
                "northeast": 0,
                "east": 1,
                "southeast": 1,
                "south": 2,
                "southwest": 2,
                "west": 3,
                "northwest": 3,
            }
            return location_to_quadrant.get(motion.start_loc.value.lower(), 0)
        else:
            return 0

    def _get_pro_directional_tuples(
        self, grid_mode: str, prop_rot_dir: RotationDirection, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Generate directional tuples for PRO motion."""
        if prop_rot_dir == RotationDirection.CLOCKWISE:
            return [(x, y), (x + 5, y), (x, y + 5), (x - 5, y)]
        else:
            return [(x, y), (x - 5, y), (x, y - 5), (x + 5, y)]

    def _get_anti_directional_tuples(
        self, grid_mode: str, prop_rot_dir: RotationDirection, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Generate directional tuples for ANTI motion."""
        if prop_rot_dir == RotationDirection.CLOCKWISE:
            return [(x, y), (x - 5, y), (x, y - 5), (x + 5, y)]
        else:
            return [(x, y), (x + 5, y), (x, y + 5), (x - 5, y)]

    def _get_static_directional_tuples(
        self, grid_mode: str, prop_rot_dir: RotationDirection, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Generate directional tuples for STATIC motion."""
        return [(x, y)] * 4  # Static arrows don't vary by quadrant

    def _get_dash_directional_tuples(
        self, grid_mode: str, prop_rot_dir: RotationDirection, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Generate directional tuples for DASH motion."""
        if prop_rot_dir == RotationDirection.NO_ROTATION:
            return [(x, y)] * 4  # No rotation dash arrows don't vary
        else:
            return [(x, y), (x + 3, y), (x, y + 3), (x - 3, y)]

    def _get_float_directional_tuples(
        self, motion: MotionData, x: int, y: int
    ) -> list[tuple[int, int]]:
        """Generate directional tuples for FLOAT motion."""
        # Float motion similar to PRO
        return self._get_pro_directional_tuples("diamond", motion.prop_rot_dir, x, y)
