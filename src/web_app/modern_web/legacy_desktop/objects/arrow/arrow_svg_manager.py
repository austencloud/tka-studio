from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtSvg import QSvgRenderer

from data.constants import CLOCK, COUNTER, FLOAT, IN, OUT
from objects.arrow.arrow import Arrow
from utils.path_helpers import get_image_path

if TYPE_CHECKING:
    from svg_manager.svg_manager import SvgManager


class ArrowSvgManager:
    def __init__(self, manager: "SvgManager"):
        self.manager = manager

    def update_arrow_svg(self, arrow: "Arrow") -> None:
        svg_file = self._get_arrow_svg_file(arrow)
        svg_data = self.manager.load_svg_file(svg_file)
        colored_svg_data = self.manager.color_manager.apply_color_transformations(
            svg_data, arrow.state.color
        )
        self._setup_arrow_svg_renderer(arrow, colored_svg_data)

    def _get_arrow_svg_file(self, arrow: "Arrow") -> str:
        # Debug: Print arrow state information
        motion_type = arrow.motion.state.motion_type
        turns = arrow.motion.state.turns
        start_ori = arrow.motion.state.start_ori

        if motion_type == FLOAT:
            return self._get_float_svg_file()

        turns = self._get_turns(turns)

        if start_ori in [IN, OUT]:
            return self._get_radial_svg_file(motion_type, turns)
        elif start_ori in [CLOCK, COUNTER]:
            return self._get_nonradial_svg_file(motion_type, turns)
        else:
            # Return a default SVG path instead of None
            return self._get_float_svg_file()  # Use float as fallback

    def _get_float_svg_file(self) -> str:
        return get_image_path("arrows/float.svg")

    def _get_turns(self, arrow_turns: str | int | float) -> float:
        if isinstance(arrow_turns, (int, float)):
            return float(arrow_turns)
        return arrow_turns

    def _get_radial_svg_file(self, motion_type: str, turns: float) -> str:
        return get_image_path(
            f"arrows/{motion_type}/from_radial/{motion_type}_{turns}.svg"
        )

    def _get_nonradial_svg_file(self, motion_type: str, turns: float) -> str:
        return get_image_path(
            f"arrows/{motion_type}/from_nonradial/{motion_type}_{turns}.svg"
        )

    def _setup_arrow_svg_renderer(self, arrow: "Arrow", svg_data: str) -> None:
        renderer = QSvgRenderer()
        renderer.load(svg_data.encode("utf-8"))
        arrow.setSharedRenderer(renderer)
