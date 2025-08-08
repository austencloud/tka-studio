from __future__ import annotations
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QGraphicsOpacityEffect, QGridLayout

if TYPE_CHECKING:
    from .section_widget import OptionPickerSectionWidget


class OptionPickerSectionPictographFrame(QFrame):
    opacity_effect: QGraphicsOpacityEffect

    def __init__(self, section: "OptionPickerSectionWidget") -> None:
        super().__init__()
        self.section = section
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(self.section.option_scroll.spacing)

        # Ensure frame expands to fill section width (like original QFrame behavior)
        from PyQt6.QtWidgets import QSizePolicy

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
