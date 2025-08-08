from __future__ import annotations
from typing import Union
from typing import TYPE_CHECKING

from objects.arrow.arrow import Arrow
from PyQt6.QtSvg import QSvgRenderer
from utils.path_helpers import get_image_path

from data.constants import CLOCK, COUNTER, FLOAT, IN, OUT  # Add FLOAT here

if TYPE_CHECKING:
    from svg_manager.graphical_object_svg_manager import (
        SvgManager,
    )


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
        start_ori = arrow.motion.state.start_ori
        if arrow.motion.state.motion_type == FLOAT:
            return get_image_path("arrows/float.svg")
        arrow_turns: str | int | float = arrow.motion.state.turns
        if isinstance(arrow_turns, (int, float)):
            turns = float(arrow_turns)
        else:
            turns = arrow_turns
        if turns != "fl":
            if start_ori in [IN, OUT]:
                return get_image_path(
                    f"arrows/{arrow.motion.state.motion_type}/from_radial/"
                    f"{arrow.motion.state.motion_type}_{turns}.svg"
                )
            elif start_ori in [CLOCK, COUNTER]:
                return get_image_path(
                    f"arrows/{arrow.motion.state.motion_type}/from_nonradial/"
                    f"{arrow.motion.state.motion_type}_{turns}.svg"
                )

    def _setup_arrow_svg_renderer(self, arrow: "Arrow", svg_data: str) -> None:
        renderer = QSvgRenderer()
        renderer.load(svg_data.encode("utf-8"))
        arrow.setSharedRenderer(renderer)
        # arrow.update()
