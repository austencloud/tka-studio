from __future__ import annotations
from typing import Union,Optional
from typing import TYPE_CHECKING, Union,Optional

from base_widgets.pictograph.elements.grid.grid import Grid
from base_widgets.pictograph.elements.views.bordered_pictograph_view import (
    BorderedPictographView,
)
from base_widgets.pictograph.elements.views.codex_pictograph_view import (
    CodexPictographView,
)
from base_widgets.pictograph.elements.views.lesson_pictograph_view import (
    LessonPictographView,
)
from base_widgets.pictograph.elements.views.option_view import OptionView
from base_widgets.pictograph.elements.views.start_pos_picker_pictograph_view import (
    StartPosPickerPictographView,
)
from objects.arrow.arrow import Arrow
from objects.glyphs.elemental_glyph.elemental_glyph import ElementalGlyph
from objects.glyphs.reversal_glyph import ReversalGlyph
from objects.glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import (
    StartToEndPosGlyph,
)
from objects.glyphs.tka_glyph.tka_glyph import TKA_Glyph
from objects.glyphs.vtg_glyph.vtg_glyph import VTG_Glyph
from objects.motion.motion import Motion
from objects.prop.prop import Prop
from PyQt6.QtWidgets import QGraphicsTextItem

from .views.base_pictograph_view import BasePictographView

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )
    from base_widgets.pictograph.elements.views.visibility_pictograph_view import (
        VisibilityPictographView,
    )


from dataclasses import dataclass


@dataclass
class PictographElements:
    """Stores all elements within the pictograph."""

    view: Union[
        BasePictographView,
        BorderedPictographView,
        LessonPictographView,
        StartPosPickerPictographView,
        CodexPictographView,
        "GE_PictographView",
        "OptionView",
        "VisibilityPictographView",
    ] = None

    arrows: dict[str, Arrow] = None
    motion_set: dict[str, Motion] = None
    props: dict[str, Prop] = None
    pictograph_dict: dict[str, str | dict[str, str]] = None
    locations: dict[str, tuple[int, int, int, int]] = None
    grid: Grid | None = None

    # Symbols
    blue_reversal_symbol: QGraphicsTextItem | None = None
    red_reversal_symbol: QGraphicsTextItem | None = None

    # Items
    selected_arrow: Arrow | None = None
    blue_arrow: Arrow | None = None
    red_arrow: Arrow | None = None
    blue_motion: Motion | None = None
    red_motion: Motion | None = None
    blue_prop: Prop | None = None
    red_prop: Prop | None = None

    tka_glyph: TKA_Glyph | None = None
    vtg_glyph: VTG_Glyph | None = None
    elemental_glyph: ElementalGlyph | None = None
    start_to_end_pos_glyph: StartToEndPosGlyph | None = None
    reversal_glyph: ReversalGlyph | None = None
