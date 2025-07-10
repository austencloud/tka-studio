import logging
import os
import re
from functools import lru_cache
from typing import TYPE_CHECKING, Any

from application.services.assets.asset_manager import AssetManager
from application.services.positioning.props.orchestration.prop_management_service import (
    PropManagementService,
)
from core.dependency_injection.di_container import get_container
from core.interfaces.positioning_services import IArrowCoordinateSystemService
from domain.models import Location, MotionData, MotionType, Orientation
from presentation.components.pictograph.asset_utils import get_image_path
from PyQt6.QtCore import QPointF
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from ui.adapters.qt_geometry_adapter import QtGeometryAdapter

if TYPE_CHECKING:
    from presentation.components.pictograph.pictograph_scene import PictographScene

logger = logging.getLogger(__name__)


class PropRenderer:
    def __init__(self, scene: "PictographScene"):
        self.scene = scene
        self.CENTER_X = 475
        self.CENTER_Y = 475
        self.HAND_RADIUS = 143.1

        # Initialize asset manager service
        self.asset_manager = AssetManager()

        # Initialize prop management service
        self.prop_management_service = PropManagementService()
        self.rendered_props: dict[str, QGraphicsSvgItem] = {}

        # Get coordinate system service from DI container
        try:
            container = get_container()
            self.coordinate_system = container.resolve(IArrowCoordinateSystemService)
        except Exception as e:
            logger.warning(f"Failed to resolve coordinate system service: {e}")
            self.coordinate_system = None

        # Fallback coordinates for when coordinate system service is not available
        self._fallback_location_coordinates = {
            Location.NORTH.value: (0, -self.HAND_RADIUS),
            Location.EAST.value: (self.HAND_RADIUS, 0),
            Location.SOUTH.value: (0, self.HAND_RADIUS),
            Location.WEST.value: (-self.HAND_RADIUS, 0),
            Location.NORTHEAST.value: (
                self.HAND_RADIUS * 0.707,
                -self.HAND_RADIUS * 0.707,
            ),
            Location.SOUTHEAST.value: (
                self.HAND_RADIUS * 0.707,
                self.HAND_RADIUS * 0.707,
            ),
            Location.SOUTHWEST.value: (
                -self.HAND_RADIUS * 0.707,
                self.HAND_RADIUS * 0.707,
            ),
            Location.NORTHWEST.value: (
                -self.HAND_RADIUS * 0.707,
                -self.HAND_RADIUS * 0.707,
            ),
        }

    def render_prop(self, color: str, motion_data: MotionData) -> None:
        # Use asset manager to get prop SVG path
        prop_svg_path = self.asset_manager.get_prop_asset_path("staff", color)

        if not os.path.exists(prop_svg_path):
            logger.warning(f"Prop asset not found: {prop_svg_path}")
            return

        prop_item = QGraphicsSvgItem()
        # Use asset manager to load and transform SVG
        svg_data = self.asset_manager.load_and_cache_asset(prop_svg_path)
        colored_svg_data = self.asset_manager.apply_color_transformation(
            svg_data, color
        )

        renderer = QSvgRenderer(bytearray(colored_svg_data, encoding="utf-8"))
        if not renderer.isValid():
            logger.warning(f"Invalid SVG renderer for {prop_svg_path}")
            return

        prop_item.setSharedRenderer(renderer)

        end_pos = self._get_location_position(motion_data.end_loc)
        if end_pos == (0, 0) and motion_data.end_loc != Location.NORTH:
            logger.warning(
                f"Invalid location {motion_data.end_loc}, using default position"
            )
            end_pos = self._fallback_location_coordinates[Location.NORTH.value]

        target_hand_point_x = self.CENTER_X + end_pos[0]
        target_hand_point_y = self.CENTER_Y + end_pos[1]

        prop_rotation = self._calculate_prop_rotation(motion_data)

        bounds = prop_item.boundingRect()
        prop_item.setTransformOriginPoint(bounds.center())
        prop_item.setRotation(prop_rotation)

        self._place_prop_at_hand_point(
            prop_item, target_hand_point_x, target_hand_point_y
        )

        self.rendered_props[color] = prop_item
        self.scene.addItem(prop_item)

    def _place_prop_at_hand_point(
        self, prop_item: QGraphicsSvgItem, target_x: float, target_y: float
    ) -> None:
        bounds = prop_item.boundingRect()
        center_point_in_local_coords = bounds.center()
        center_point_in_scene = prop_item.mapToScene(center_point_in_local_coords)
        target_hand_point = QPointF(target_x, target_y)
        offset = target_hand_point - center_point_in_scene
        new_position = prop_item.pos() + offset
        prop_item.setPos(new_position)

    def _get_location_position(self, location) -> tuple[float, float]:
        """Get the coordinate position for a location using the coordinate system service."""
        if self.coordinate_system:
            # Use the coordinate system service to get proper coordinates
            # Since we don't have motion data context, create a dummy static motion
            # for coordinate calculation
            from domain.models import RotationDirection

            dummy_motion = MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                turns=0.0,
                start_loc=location,
                end_loc=location,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
            )
            point = self.coordinate_system.get_initial_position(dummy_motion, location)
            return (point.x(), point.y())
        else:
            # Fallback to manual calculation if service is not available
            # Handle both enum and string location values
            if hasattr(location, "value"):
                location_key = location.value
            else:
                location_key = str(location)

            position = self._fallback_location_coordinates.get(location_key)
            if position is None:
                logger.warning(f"Unknown location {location}, using NORTH as fallback")
                return self._fallback_location_coordinates.get(
                    Location.NORTH.value, (0, -143.1)
                )
            return position
            return position

    def _calculate_prop_rotation(self, motion_data: MotionData) -> float:
        # Use the actual start orientation from motion data instead of hardcoded IN
        start_orientation = self._get_start_orientation_from_motion_data(motion_data)
        return self.prop_management_service.calculate_prop_rotation_angle(
            motion_data, start_orientation
        )

    def _get_start_orientation_from_motion_data(
        self, motion_data: MotionData
    ) -> Orientation:
        """Extract start orientation from motion data, with fallback to IN."""
        if hasattr(motion_data, "start_ori") and motion_data.start_ori:
            # Handle both string and Orientation enum cases
            if isinstance(motion_data.start_ori, Orientation):
                return motion_data.start_ori
            else:
                # Convert string orientation to Orientation enum
                ori_str = motion_data.start_ori.lower()
                if ori_str == "in":
                    return Orientation.IN
                elif ori_str == "out":
                    return Orientation.OUT
                elif ori_str == "clock":
                    return Orientation.CLOCK
                elif ori_str == "counter":
                    return Orientation.COUNTER

        # Fallback to IN if no valid orientation found
        return Orientation.IN

    def apply_beta_positioning(self, beat_data: Any) -> None:
        from domain.models import BeatData

        if not isinstance(beat_data, BeatData):
            return
        if not self.prop_management_service.should_apply_beta_positioning(beat_data):
            return

        if "blue" not in self.rendered_props or "red" not in self.rendered_props:
            return

        (
            blue_offset,
            red_offset,
        ) = self.prop_management_service.calculate_separation_offsets(beat_data)

        blue_prop = self.rendered_props["blue"]
        red_prop = self.rendered_props["red"]

        blue_current_pos = blue_prop.pos()
        red_current_pos = red_prop.pos()

        blue_current_point = QtGeometryAdapter.qpointf_to_point(blue_current_pos)
        red_current_point = QtGeometryAdapter.qpointf_to_point(red_current_pos)

        new_blue_point = blue_current_point + blue_offset
        new_red_point = red_current_point + red_offset

        new_blue_pos = QtGeometryAdapter.point_to_qpointf(new_blue_point)
        new_red_pos = QtGeometryAdapter.point_to_qpointf(new_red_point)

        blue_prop.setPos(new_blue_pos)
        red_prop.setPos(new_red_pos)

    def clear_rendered_props(self) -> None:
        self.rendered_props.clear()
