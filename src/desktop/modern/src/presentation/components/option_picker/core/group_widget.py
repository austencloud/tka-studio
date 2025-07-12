"""
Simplified Option Picker Group Widget - Direct Copy of Legacy Success Pattern

This widget directly copies the successful Legacy OptionPickerSectionGroupWidget pattern,
replacing complex Modern group logic with simple Qt QWidget and QHBoxLayout.

Key principles from Legacy:
- Simple QWidget with QHBoxLayout
- Fixed size policy for the group
- Minimum size policy for individual sections
- No complex business logic or orchestration
"""

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QSizePolicy, QWidget

if TYPE_CHECKING:
    from presentation.components.option_picker.core.option_picker_scroll import (
        OptionPickerScroll,
    )
    from presentation.components.option_picker.core.option_picker_section import (
        OptionPickerSection,
    )


class OptionPickerGroupWidget(QWidget):
    """
    Simplified group widget using Legacy success pattern.

    Direct copy of Legacy OptionPickerSectionGroupWidget with minimal changes.
    """

    def __init__(self, scroll_area: "OptionPickerScroll") -> None:
        super().__init__(scroll_area)
        self.scroll_area = scroll_area

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setLayout(self.layout)

    def add_section_widget(self, section: "OptionPickerSection") -> None:
        """Add a section widget to the group exactly like Legacy."""
        section.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        section.setMinimumWidth(section.sizeHint().width())
        section.setMaximumWidth(section.sizeHint().width())

        self.layout.addWidget(section, alignment=Qt.AlignmentFlag.AlignCenter)
