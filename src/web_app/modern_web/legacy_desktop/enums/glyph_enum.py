from __future__ import annotations
from typing import Union
from typing import TYPE_CHECKING, Union

from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsTextItem

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
    from objects.glyphs.elemental_glyph.elemental_glyph import ElementalGlyph
    from objects.glyphs.reversal_glyph import ReversalGlyph
    from objects.glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import (
        StartToEndPosGlyph,
    )
    from objects.glyphs.tka_glyph.tka_glyph import TKA_Glyph
    from objects.glyphs.vtg_glyph.vtg_glyph import VTG_Glyph
    from objects.prop.prop import Prop


Glyph = Union[
    QGraphicsTextItem,
    QGraphicsSvgItem,
    "ReversalGlyph",
    "ElementalGlyph",
    "StartToEndPosGlyph",
    "TKA_Glyph",
    "VTG_Glyph",
    "Prop",
    "Arrow",
]
