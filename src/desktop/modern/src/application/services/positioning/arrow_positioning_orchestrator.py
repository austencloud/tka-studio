"""
Arrow Positioning Orchestrator

Orchestrates the complete arrow positioning pipeline using focused services.
Replaces the monolithic ArrowManagementService with clean architecture.

PROVIDES:
- Complete arrow positioning pipeline coordination
- Immutable positioning result data
- Clean separation of concerns
- No Qt dependencies in business logic
"""

from typing import Optional, Dict
from abc import ABC, abstractmethod

from PyQt6.QtCore import QPointF

from desktop.modern.src.domain.models.core_models import Location, MotionType
from desktop.modern.src.domain.models.pictograph_models import ArrowData
from desktop.modern.src.domain.models.pictograph_models import PictographData
from desktop.modern.src.domain.models.positioning_models import ArrowPositionResult
from .arrow_location_calculator import IArrowLocationCalculator, ArrowLocationCalculator
from .arrow_rotation_calculator import IArrowRotationCalculator, ArrowRotationCalculator
from .arrow_adjustment_service import IArrowAdjustmentService, ArrowAdjustmentService


class IArrowPositioningService(ABC):
    """Interface for complete arrow positioning."""

    @abstractmethod
    def calculate_position(
        self, arrow_data: ArrowData, pictograph_data: Optional[PictographData] = None
    ) -> ArrowPositionResult:
        """Calculate complete arrow position and rotation."""
        pass

    @abstractmethod
    def calculate_all_positions(
        self, pictograph_data: PictographData
    ) -> Dict[str, ArrowPositionResult]:
        """Calculate positions for all arrows in pictograph."""
        pass


class ArrowPositioningOrchestrator(IArrowPositioningService):
    """
    Orchestrates the complete arrow positioning pipeline.

    Coordinates focused services to calculate arrow positions.
    Returns immutable positioning data following TKA architecture.
    """

    # Center coordinates for fallback positioning
    CENTER_X = 475.0
    CENTER_Y = 475.0

    # Coordinate mappings extracted from original service
    HAND_POINTS = {
        Location.NORTH: QPointF(475.0, 331.9),
        Location.EAST: QPointF(618.1, 475.0),
        Location.SOUTH: QPointF(475.0, 618.1),
        Location.WEST: QPointF(331.9, 475.0),
        Location.NORTHEAST: QPointF(618.1, 331.9),
        Location.SOUTHEAST: QPointF(618.1, 618.1),
        Location.SOUTHWEST: QPointF(331.9, 618.1),
        Location.NORTHWEST: QPointF(331.9, 331.9),
    }

    LAYER2_POINTS = {
        Location.NORTHEAST: QPointF(618.1, 331.9),
        Location.SOUTHEAST: QPointF(618.1, 618.1),
        Location.SOUTHWEST: QPointF(331.9, 618.1),
        Location.NORTHWEST: QPointF(331.9, 331.9),
        Location.NORTH: QPointF(618.1, 331.9),  # Maps to NE
        Location.EAST: QPointF(618.1, 618.1),  # Maps to SE
        Location.SOUTH: QPointF(331.9, 618.1),  # Maps to SW
        Location.WEST: QPointF(331.9, 331.9),  # Maps to NW
    }

    def __init__(
        self,
        location_calculator: Optional[IArrowLocationCalculator] = None,
        rotation_calculator: Optional[IArrowRotationCalculator] = None,
        adjustment_service: Optional[IArrowAdjustmentService] = None,
    ):
        """Initialize with dependency injection."""
        self.location_calculator = location_calculator or ArrowLocationCalculator()
        self.rotation_calculator = rotation_calculator or ArrowRotationCalculator()
        self.adjustment_service = adjustment_service or ArrowAdjustmentService()

    def calculate_position(
        self, arrow_data: ArrowData, pictograph_data: Optional[PictographData] = None
    ) -> ArrowPositionResult:
        """
        Calculate complete arrow position using focused service pipeline.

        Pipeline:
        1. Calculate arrow location from motion
        2. Compute initial position (layer2 vs hand points)
        3. Calculate rotation angle
        4. Apply adjustments (default placement + special rules)
        5. Return immutable positioning result
        """
        if not arrow_data.motion_data:
            return ArrowPositionResult(x=self.CENTER_X, y=self.CENTER_Y, rotation=0.0)

        motion = arrow_data.motion_data

        # Step 1: Calculate arrow location
        arrow_location = self.location_calculator.calculate_location(
            motion, pictograph_data
        )

        # Step 2: Compute initial position
        initial_position = self._compute_initial_position(motion, arrow_location)

        # Step 3: Calculate rotation
        rotation = self.rotation_calculator.calculate_rotation(motion, arrow_location)

        # Step 4: Get adjustment
        adjustment = self.adjustment_service.calculate_adjustment(
            arrow_data, pictograph_data
        )

        # Step 5: Apply final positioning formula
        final_x = initial_position.x() + adjustment.x()
        final_y = initial_position.y() + adjustment.y()

        return ArrowPositionResult(
            x=final_x,
            y=final_y,
            rotation=rotation,
            location=arrow_location.value if arrow_location else None,
        )

    def calculate_all_positions(
        self, pictograph_data: PictographData
    ) -> Dict[str, ArrowPositionResult]:
        """Calculate positions for all arrows in pictograph."""
        results = {}

        if not pictograph_data.arrows:
            return results

        for arrow_key, arrow_data in pictograph_data.arrows.items():
            if arrow_data.is_visible:
                position_result = self.calculate_position(arrow_data, pictograph_data)
                results[arrow_key] = position_result

        return results

    def _compute_initial_position(self, motion, arrow_location: Location) -> QPointF:
        """Compute initial position using placement strategy."""
        if motion.motion_type in [MotionType.PRO, MotionType.ANTI, MotionType.FLOAT]:
            return self._get_layer2_coords(arrow_location)
        elif motion.motion_type in [MotionType.STATIC, MotionType.DASH]:
            return self._get_hand_point_coords(arrow_location)
        else:
            return QPointF(self.CENTER_X, self.CENTER_Y)

    def _get_layer2_coords(self, location: Location) -> QPointF:
        """Get layer2 point coordinates for shift arrows."""
        return self.LAYER2_POINTS.get(location, QPointF(self.CENTER_X, self.CENTER_Y))

    def _get_hand_point_coords(self, location: Location) -> QPointF:
        """Get hand point coordinates for static/dash arrows."""
        return self.HAND_POINTS.get(location, QPointF(self.CENTER_X, self.CENTER_Y))
