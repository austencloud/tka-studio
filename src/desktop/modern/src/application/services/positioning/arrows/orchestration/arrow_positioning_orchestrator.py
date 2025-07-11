"""
Arrow Positioning Orchestrator

Coordinates microservices to provide the same interface as the monolith.
Uses dependency injection to compose positioning pipeline.
"""

import logging
from typing import Tuple

from core.interfaces.positioning_services import (
    IArrowAdjustmentCalculator,
    IArrowCoordinateSystemService,
    IArrowLocationCalculator,
    IArrowPositioningOrchestrator,
    IArrowRotationCalculator,
)
from domain.models.arrow_data import ArrowData
from domain.models.motion_models import MotionData
from domain.models.pictograph_data import PictographData
from presentation.components.pictograph.graphics_items.arrow_item import ArrowItem

logger = logging.getLogger(__name__)


class ArrowPositioningOrchestrator(IArrowPositioningOrchestrator):
    """Orchestrates microservices to handle arrow positioning."""

    def __init__(
        self,
        location_calculator: IArrowLocationCalculator,
        rotation_calculator: IArrowRotationCalculator,
        adjustment_calculator: IArrowAdjustmentCalculator,
        coordinate_system: IArrowCoordinateSystemService,
    ):
        self.location_calculator = location_calculator
        self.rotation_calculator = rotation_calculator
        self.adjustment_calculator = adjustment_calculator
        self.coordinate_system = coordinate_system

        self.mirror_conditions = {
            "anti": {"cw": True, "ccw": False},
            "other": {"cw": False, "ccw": True},
        }

    def calculate_arrow_position(
        self,
        arrow_data: ArrowData,
        pictograph_data: PictographData,
        motion_data: MotionData,
    ) -> Tuple[float, float, float]:
        """Calculate arrow position using microservices pipeline."""
        motion = motion_data or self._get_motion_from_pictograph(
            arrow_data, pictograph_data
        )

        if not motion:
            logger.warning(
                f"No motion data for {arrow_data.color}, returning center position"
            )
            center = self.coordinate_system.get_scene_center()
            return center.x(), center.y(), 0.0

        location = self.location_calculator.calculate_location(motion, pictograph_data)
        initial_position = self.coordinate_system.get_initial_position(motion, location)

        initial_position = self._ensure_valid_position(initial_position)

        rotation = self.rotation_calculator.calculate_rotation(motion, location)
        adjustment = self.adjustment_calculator.calculate_adjustment(
            arrow_data, pictograph_data
        )

        adjustment_x, adjustment_y = self._extract_adjustment_values(adjustment)

        final_x = initial_position.x + adjustment_x
        final_y = initial_position.y + adjustment_y

        return final_x, final_y, rotation

    def calculate_all_arrow_positions(
        self, pictograph_data: PictographData
    ) -> PictographData:
        """Calculate positions for all arrows in the pictograph."""
        updated_pictograph = pictograph_data

        for color, arrow_data in pictograph_data.arrows.items():
            motion_data = pictograph_data.motions.get(color)

            if arrow_data.is_visible and motion_data:
                x, y, rotation = self.calculate_arrow_position(
                    arrow_data, pictograph_data, motion_data
                )

                updated_pictograph = updated_pictograph.update_arrow(
                    color, position_x=x, position_y=y, rotation_angle=rotation
                )

        return updated_pictograph

    def should_mirror_arrow(
        self, arrow_data: ArrowData, pictograph_data: "PictographData" = None
    ) -> bool:
        """Determine if arrow should be mirrored."""
        motion = None
        if pictograph_data and pictograph_data.motions:
            motion = pictograph_data.motions.get(arrow_data.color)

        if not motion:
            return False

        motion_type = motion.motion_type.value.lower()
        prop_rot_dir = motion.prop_rot_dir.value.lower()

        if motion_type == "anti":
            return self.mirror_conditions["anti"].get(prop_rot_dir, False)
        else:
            return self.mirror_conditions["other"].get(prop_rot_dir, False)

    def apply_mirror_transform(
        self, arrow_item: ArrowItem, should_mirror: bool
    ) -> None:
        """Apply mirror transformation."""
        try:
            from PyQt6.QtGui import QTransform

            center_x = arrow_item.boundingRect().center().x()
            center_y = arrow_item.boundingRect().center().y()

            transform = QTransform()
            transform.translate(center_x, center_y)
            transform.scale(-1 if should_mirror else 1, 1)
            transform.translate(-center_x, -center_y)

            arrow_item.setTransform(transform)
        except (ImportError, AttributeError):
            pass

    def _get_motion_from_pictograph(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> MotionData:
        """Extract motion data from pictograph data."""
        if (
            not pictograph_data
            or not hasattr(pictograph_data, "motions")
            or not pictograph_data.motions
        ):
            return None
        return pictograph_data.motions.get(arrow_data.color)

    def _ensure_valid_position(self, initial_position):
        """Ensure position object has valid x and y attributes."""
        if hasattr(initial_position, "x") and hasattr(initial_position, "y"):
            return initial_position

        from core.types.geometry import Point

        return Point(475.0, 475.0)

    def _extract_adjustment_values(self, adjustment) -> Tuple[float, float]:
        """Extract x and y values from adjustment object."""
        if isinstance(adjustment, (int, float)):
            return adjustment, adjustment

        if hasattr(adjustment, "x") and hasattr(adjustment, "y"):
            x_attr = adjustment.x
            y_attr = adjustment.y
            adjustment_x = x_attr() if callable(x_attr) else x_attr
            adjustment_y = y_attr() if callable(y_attr) else y_attr
            return adjustment_x, adjustment_y

        return 0.0, 0.0
