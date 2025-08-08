from __future__ import annotations
from typing import TYPE_CHECKING, Optional,Optional

from PyQt6.QtWidgets import QGraphicsPixmapItem

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class PropState:
    def __init__(
        self,
        color: str,
        loc: str,
        ori: str,
        previous_location: str,
        arrow: "Arrow",
        pixmap_item: "QGraphicsPixmapItem" | None,
    ):
        self.color = color
        self.loc = loc
        self.ori = ori
        self.previous_location = previous_location
        self.arrow = arrow
        self.pixmap_item = pixmap_item
