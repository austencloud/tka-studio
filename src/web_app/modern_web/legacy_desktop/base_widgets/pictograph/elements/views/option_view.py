from __future__ import annotations
from collections.abc import Callable
from typing import TYPE_CHECKING

from base_widgets.pictograph.elements.views.bordered_pictograph_view import (
    BorderedPictographView,
)
from PyQt6.QtCore import QSize, Qt

if TYPE_CHECKING:
    from base_widgets.pictograph.legacy_pictograph import LegacyPictograph
    from main_window.main_widget.construct_tab.option_picker.widgets.legacy_option_picker import (
        LegacyOptionPicker,
    )


class OptionView(BorderedPictographView):
    def __init__(
        self,
        op: "LegacyOptionPicker",
        pictograph: "LegacyPictograph",
        mw_size_provider: Callable[[], QSize],
    ):
        super().__init__(pictograph)
        self.option_picker = op
        self.pictograph = pictograph
        self.click_handler = op.option_click_handler
        self.mw_size_provider = mw_size_provider

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.click_handler.handle_option_click(self.pictograph)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.resize_option_view()

    def resize_option_view(self):
        spacing = self.option_picker.option_scroll.spacing
        size = max(
            self.mw_size_provider().width() // 16, self.option_picker.width() // 8
        )
        bw = max(1, int(size * 0.015))
        size -= 2 * bw + spacing
        self.pictograph.elements.view.update_border_widths()
        self.setFixedSize(size, size)
        self.view_scale = size / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
