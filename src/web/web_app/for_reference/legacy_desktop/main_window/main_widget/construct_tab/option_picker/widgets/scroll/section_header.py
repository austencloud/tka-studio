from __future__ import annotations
from typing import TYPE_CHECKING

from main_window.main_widget.construct_tab.option_picker.widgets.scroll.section_type_button import (
    OptionPickerSectionTypeButton,
)
from PyQt6.QtWidgets import QHBoxLayout, QWidget

if TYPE_CHECKING:
    from .section_widget import OptionPickerSectionWidget


class OptionPickerSectionHeader(QWidget):
    def __init__(self, section: "OptionPickerSectionWidget") -> None:
        super().__init__()
        self.section = section
        self.type_button = OptionPickerSectionTypeButton(section)
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.type_button)
        self.layout.addStretch(1)
        self.setLayout(self.layout)
