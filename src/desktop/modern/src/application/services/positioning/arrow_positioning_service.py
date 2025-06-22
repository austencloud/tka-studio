"""
Arrow Positioning Service for Kinetic Constructor

This service implements the complete arrow positioning pipeline with pixel-perfect accuracy.
It handles complex geometric calculations for arrow placement using proven positioning algorithms.

IMPLEMENTS COMPLETE POSITIONING PIPELINE:
- Initial placement strategy (layer2_point vs hand_point coordinates)
- Location calculation algorithms (shift, static, dash)
- Adjustment calculators (default placement, special placement rules)
- Quadrant-based directional adjustments
- Complex geometric calculations

PROVIDES:
- Pixel-perfect arrow positioning accuracy
- Complete positioning system integration
- Clean service interface for modern architecture
"""

import logging
from typing import TYPE_CHECKING

from desktop.modern.src.domain.models.core_models import MotionType, RotationDirection
from PyQt6.QtGui import QTransform
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

if TYPE_CHECKING:
    from domain.models.pictograph_models import ArrowData

from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple, Union

from PyQt6.QtCore import QPointF

try:
    from src.core.decorators import handle_service_errors
    from src.core.exceptions import ServiceOperationError, ValidationError
    from src.core.monitoring import monitor_performance
except ImportError:
    # For tests, create dummy decorators if imports fail
    def handle_service_errors(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    def monitor_performance(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    class ServiceOperationError(Exception):
        pass

    class ValidationError(Exception):
        pass


logger = logging.getLogger(__name__)

from desktop.modern.src.domain.models.core_models import (
    Location,
    MotionData,
    MotionType,
    RotationDirection,
)
from desktop.modern.src.domain.models.pictograph_models import (
    ArrowData,
    GridMode,
    PictographData,
)

from .dash_location_service import DashLocationService
from .default_placement_service import DefaultPlacementService
from .placement_key_service import PlacementKeyService


class IArrowPositioningService(ABC):
    """Interface for arrow positioning calculations."""

    @abstractmethod
    def calculate_arrow_position(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Tuple[float, float, float]:
        """
        Calculate arrow position and rotation.

        Returns:
            Tuple of (x, y, rotation_angle)
        """
        pass

    @abstractmethod
    def calculate_all_arrow_positions(
        self, pictograph_data: PictographData
    ) -> PictographData:
        """Calculate positions for all arrows in the pictograph."""
        pass

    @abstractmethod
    def apply_mirror_transform(
        self, arrow_item: QGraphicsSvgItem, should_mirror: bool
    ) -> None:
        """Apply mirror transform to arrow item if needed."""
        pass

    @abstractmethod
    def should_mirror_arrow(self, arrow_data: ArrowData) -> bool:
        """Determine if arrow should be mirrored based on motion type."""
        pass


class ArrowPositioningService(IArrowPositioningService):
    """
    Service that implements complete arrow positioning algorithms.

    This provides pixel-perfect positioning calculations using proven
    geometric algorithms and coordinate systems.
    """

    def __init__(
        self,
        location_calculator=None,
        rotation_calculator=None,
        adjustment_calculator=None,
        coordinate_system=None,
    ):
        """Initialize the positioning service with refactored services."""
        # Import here to avoid circular dependencies
        from .arrow_adjustment_calculator_service import (
            ArrowAdjustmentCalculatorService,
        )
        from .arrow_coordinate_system_service import ArrowCoordinateSystemService
        from .arrow_location_calculator_service import ArrowLocationCalculatorService
        from .arrow_rotation_calculator_service import ArrowRotationCalculatorService

        # Initialize refactored services with dependency injection
        self.location_calculator = (
            location_calculator or ArrowLocationCalculatorService()
        )
        self.rotation_calculator = (
            rotation_calculator or ArrowRotationCalculatorService()
        )
        self.adjustment_calculator = (
            adjustment_calculator or ArrowAdjustmentCalculatorService()
        )
        self.coordinate_system = coordinate_system or ArrowCoordinateSystemService()

        # Legacy compatibility - expose coordinate system properties
        self.SCENE_SIZE = self.coordinate_system.SCENE_SIZE
        self.CENTER_X = self.coordinate_system.CENTER_X
        self.CENTER_Y = self.coordinate_system.CENTER_Y
        self.HAND_POINTS = self.coordinate_system.HAND_POINTS
        self.LAYER2_POINTS = self.coordinate_system.LAYER2_POINTS

        # Mirror conditions for legacy compatibility
        self.mirror_conditions = {
            "anti": {
                "cw": True,
                "ccw": False,
            },
            "other": {
                "cw": False,
                "ccw": True,
            },
        }

    def should_mirror_arrow(self, arrow_data: "ArrowData") -> bool:
        if not arrow_data.motion_data:
            return False

        motion_type = arrow_data.motion_data.motion_type.value.lower()
        prop_rot_dir = arrow_data.motion_data.prop_rot_dir.value.lower()

        if motion_type == "anti":
            return self.mirror_conditions["anti"].get(prop_rot_dir, False)
        else:
            return self.mirror_conditions["other"].get(prop_rot_dir, False)

    def apply_mirror_transform(
        self, arrow_item: QGraphicsSvgItem, should_mirror: bool
    ) -> None:
        center_x = arrow_item.boundingRect().center().x()
        center_y = arrow_item.boundingRect().center().y()

        transform = QTransform()
        transform.translate(center_x, center_y)
        transform.scale(-1 if should_mirror else 1, 1)
        transform.translate(-center_x, -center_y)

        arrow_item.setTransform(transform)

    @handle_service_errors("calculate_arrow_position")
    @monitor_performance("arrow_positioning")
    def calculate_arrow_position(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Tuple[float, float, float]:
        """
        Calculate arrow position and rotation using refactored positioning pipeline.
        """
        if not arrow_data.motion_data:
            return self.CENTER_X, self.CENTER_Y, 0.0

        motion = arrow_data.motion_data

        # Step 1: Calculate arrow location using location calculator
        arrow_location = self.location_calculator.calculate_location(
            motion, pictograph_data
        )

        # Step 2: Get initial position using coordinate system
        initial_position = self.coordinate_system.get_initial_position(
            motion, arrow_location
        )

        # Step 3: Calculate rotation using rotation calculator
        rotation = self.rotation_calculator.calculate_rotation(motion, arrow_location)

        # Step 4: Get adjustment using adjustment calculator
        adjustment = self.adjustment_calculator.calculate_adjustment(
            arrow_data, pictograph_data
        )

        # Step 5: Apply final positioning formula
        # Formula: final_pos = initial_pos + adjustment - bounding_rect_center
        # Note: bounding_rect_center will be applied in the component during setPos()
        final_x = initial_position.x() + adjustment.x()
        final_y = initial_position.y() + adjustment.y()

        return final_x, final_y, rotation

    @handle_service_errors("calculate_all_arrow_positions")
    @monitor_performance("batch_arrow_positioning")
    def calculate_all_arrow_positions(
        self, pictograph_data: PictographData
    ) -> PictographData:
        """Calculate positions for all arrows in the pictograph."""
        updated_pictograph = pictograph_data

        for color, arrow_data in pictograph_data.arrows.items():
            if arrow_data.is_visible and arrow_data.motion_data:
                x, y, rotation = self.calculate_arrow_position(
                    arrow_data, pictograph_data
                )

                updated_pictograph = updated_pictograph.update_arrow(
                    color, position_x=x, position_y=y, rotation_angle=rotation
                )

        return updated_pictograph
