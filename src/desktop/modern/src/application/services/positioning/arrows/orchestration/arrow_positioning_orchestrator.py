"""
Arrow Positioning Orchestrator

Coordinates microservices to provide the same interface as the monolith.
Uses dependency injection to compose positioning pipeline.

Replaces the 700-line ArrowManagementService with clean composition
of focused services.
"""

from typing import Tuple

from domain.models.pictograph_models import ArrowData, PictographData
from core.interfaces.positioning_services import (
    IArrowLocationCalculator,
    IArrowRotationCalculator,
    IArrowAdjustmentCalculator,
    IArrowCoordinateSystemService,
    IArrowPositioningOrchestrator,
)


class ArrowPositioningOrchestrator(IArrowPositioningOrchestrator):
    """
    Orchestrates microservices to handle arrow positioning.

    Replaces the 700-line ArrowManagementService monolith with clean
    composition of focused services.
    """

    def __init__(
        self,
        location_calculator: IArrowLocationCalculator,
        rotation_calculator: IArrowRotationCalculator,
        adjustment_calculator: IArrowAdjustmentCalculator,
        coordinate_system: IArrowCoordinateSystemService,
    ):
        """Initialize with dependency injection."""
        self.location_calculator = location_calculator
        self.rotation_calculator = rotation_calculator
        self.adjustment_calculator = adjustment_calculator
        self.coordinate_system = coordinate_system

        # Mirror conditions (extracted from monolith)
        self.mirror_conditions = {
            "anti": {"cw": True, "ccw": False},
            "other": {"cw": False, "ccw": True},
        }

    def calculate_arrow_position(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Tuple[float, float, float]:
        """
        Calculate arrow position using microservices pipeline.

        PIPELINE:
        1. Calculate location (microservice)
        2. Get initial position (microservice)
        3. Calculate rotation (microservice)
        4. Calculate adjustment (microservice)
        5. Compose final position
        """
        if not arrow_data.motion_data:
            center = self.coordinate_system.get_scene_center()
            return center.x, center.y, 0.0

        motion = arrow_data.motion_data

        # Step 1: Calculate arrow location
        location = self.location_calculator.calculate_location(motion, pictograph_data)

        # Step 2: Get initial position
        initial_position = self.coordinate_system.get_initial_position(motion, location)

        # Step 3: Calculate rotation
        rotation = self.rotation_calculator.calculate_rotation(motion, location)

        # Step 4: Calculate adjustment
        adjustment = self.adjustment_calculator.calculate_adjustment(
            arrow_data, pictograph_data
        )

        # Step 5: Compose final position
        # Handle adjustment as float, QPointF, or Point object
        if isinstance(adjustment, (int, float)):
            adjustment_x = adjustment
            adjustment_y = adjustment
        elif hasattr(adjustment, "x") and hasattr(adjustment, "y"):
            x_attr = adjustment.x
            y_attr = adjustment.y
            adjustment_x = x_attr() if callable(x_attr) else x_attr
            adjustment_y = y_attr() if callable(y_attr) else y_attr
        else:
            adjustment_x = 0.0
            adjustment_y = 0.0

        final_x = initial_position.x + adjustment_x
        final_y = initial_position.y + adjustment_y

        return final_x, final_y, rotation

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

    def should_mirror_arrow(self, arrow_data: ArrowData) -> bool:
        """Determine if arrow should be mirrored (extracted from monolith)."""
        if not arrow_data.motion_data:
            return False

        motion_type = arrow_data.motion_data.motion_type.value.lower()
        prop_rot_dir = arrow_data.motion_data.prop_rot_dir.value.lower()

        if motion_type == "anti":
            return self.mirror_conditions["anti"].get(prop_rot_dir, False)
        else:
            return self.mirror_conditions["other"].get(prop_rot_dir, False)

    def apply_mirror_transform(self, arrow_item, should_mirror: bool) -> None:
        """Apply mirror transformation (extracted from monolith)."""
        try:
            from PyQt6.QtGui import QTransform

            center_x = arrow_item.boundingRect().center().x()
            center_y = arrow_item.boundingRect().center().y()

            transform = QTransform()
            transform.translate(center_x, center_y)
            transform.scale(-1 if should_mirror else 1, 1)
            transform.translate(-center_x, -center_y)

            arrow_item.setTransform(transform)
        except ImportError:
            # Handle case where PyQt6 is not available (testing scenarios)
            pass
        except AttributeError:
            # Handle case where arrow_item doesn't have expected methods
            pass
