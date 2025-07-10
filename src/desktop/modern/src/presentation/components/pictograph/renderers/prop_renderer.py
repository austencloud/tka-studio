import os
import re
from functools import lru_cache
from typing import TYPE_CHECKING, Any
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from domain.models import MotionData, Location

from presentation.components.pictograph.asset_utils import (
    get_image_path,
)

from domain.models import Orientation
from application.services.positioning.props.orchestration.prop_management_service import (
    PropManagementService,
)
from ui.adapters.qt_geometry_adapter import QtGeometryAdapter

if TYPE_CHECKING:
    from presentation.components.pictograph.pictograph_scene import PictographScene


class PropRenderer:
    def __init__(self, scene: "PictographScene"):
        self.scene = scene
        self.CENTER_X = 475
        self.CENTER_Y = 475
        self.HAND_RADIUS = 143.1

        self.prop_management_service = PropManagementService()
        self.rendered_props: dict[str, QGraphicsSvgItem] = {}

        self.location_coordinates = {
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
        prop_svg_path = get_image_path("props/staff.svg")

        if not os.path.exists(prop_svg_path):
            print(f"Warning: Prop asset not found: {prop_svg_path}")
            return

        prop_item = QGraphicsSvgItem()
        svg_data = self._load_svg_file(prop_svg_path)
        colored_svg_data = self._apply_color_transformation(svg_data, color)

        renderer = QSvgRenderer(bytearray(colored_svg_data, encoding="utf-8"))
        if not renderer.isValid():
            print(f"Warning: Invalid SVG renderer for {prop_svg_path}")
            return

        prop_item.setSharedRenderer(renderer)

        end_pos = self._get_location_position(motion_data.end_loc)
        if end_pos == (0, 0) and motion_data.end_loc != Location.NORTH:
            print(
                f"Warning: Invalid location {motion_data.end_loc}, using default position"
            )
            end_pos = self.location_coordinates[Location.NORTH.value]

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
        # Handle both enum and string location values
        if hasattr(location, "value"):
            # It's an enum, use .value
            location_key = location.value
        else:
            # It's already a string
            location_key = str(location)

        position = self.location_coordinates.get(location_key)
        if position is None:
            print(f"Warning: Unknown location {location}, using NORTH as fallback")
            # Use fallback for NORTH location
            fallback_key = "n"  # NORTH in string format
            return self.location_coordinates.get(fallback_key, (0, -143.1))
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

    def _load_svg_file(self, file_path: str) -> str:
        return self._load_svg_file_cached(file_path)

    @lru_cache(maxsize=64)
    def _load_svg_file_cached(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                return content
        except Exception:
            return ""

    def _apply_color_transformation(self, svg_data: str, color: str) -> str:
        if not svg_data:
            return svg_data

        COLOR_MAP = {
            "blue": "#2E3192",
            "red": "#ED1C24",
        }

        target_color = COLOR_MAP.get(color.lower(), "#2E3192")

        patterns = [
            re.compile(r'(fill=")([^"]*)(")'),
            re.compile(r"(fill:\s*)([^;]*)(;)"),
            re.compile(r"(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)([^;}]*)([^}]*?\})"),
        ]

        for pattern in patterns:
            svg_data = pattern.sub(
                lambda m: m.group(1) + target_color + m.group(len(m.groups())), svg_data
            )

        return svg_data

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
