from __future__ import annotations
from typing import TYPE_CHECKING

from base_widgets.pictograph.elements.views.base_pictograph_view import (
    BasePictographView,
)
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from base_widgets.pictograph.legacy_pictograph import LegacyPictograph

    from .....main_window.main_widget.codex.codex import Codex


class CodexPictographView(BasePictographView):
    def __init__(self, pictograph: "LegacyPictograph", codex: "Codex") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.codex = codex
        self.setStyleSheet("border: 1px solid black;")

    def resizeEvent(self, event):
        size = self.codex.main_widget.width() // 16
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        super().resizeEvent(event)
