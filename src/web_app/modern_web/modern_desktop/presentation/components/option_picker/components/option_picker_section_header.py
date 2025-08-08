"""
Simplified Option Picker Section Header - Direct Copy of Legacy Success Pattern

This header directly copies the successful Legacy OptionPickerSectionHeader pattern,
replacing complex Modern header logic with simple Qt QWidget and QHBoxLayout.

Key principles from Legacy:
- Simple QWidget with QHBoxLayout
- Centered button with stretches
- Direct button connection to section toggle
- No complex height calculations or business logic
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QHBoxLayout, QWidget


if TYPE_CHECKING:
    from desktop.modern.presentation.components.option_picker.components.option_picker_section import (
        OptionPickerSection,
    )


class OptionPickerSectionHeader(QWidget):
    """
    Simplified section header using Legacy success pattern.

    Direct copy of Legacy OptionPickerSectionHeader with minimal changes.
    """

    def __init__(self, section: OptionPickerSection) -> None:
        super().__init__()
        self.section = section
        self._setup_layout()

    def _setup_layout(self) -> None:
        """Setup layout exactly like Legacy."""
        from desktop.modern.presentation.components.option_picker.components.option_picker_section_button import (
            OptionPickerSectionButton,
        )

        self.type_button = OptionPickerSectionButton(self.section)

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.type_button)
        self.layout.addStretch(1)
        self.setLayout(self.layout)
