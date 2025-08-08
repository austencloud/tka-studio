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

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QSizePolicy, QWidget


if TYPE_CHECKING:
    from desktop.modern.presentation.components.option_picker.components.option_picker_scroll import (
        OptionPickerScroll,
    )
    from desktop.modern.presentation.components.option_picker.components.option_picker_section import (
        OptionPickerSection,
    )


class OptionPickerGroupWidget(QWidget):
    """
    Simplified group widget using Legacy success pattern.

    Direct copy of Legacy OptionPickerSectionGroupWidget with minimal changes.
    FIXED: Added proper width constraints to prevent pictograph alignment issues.
    """

    def __init__(self, scroll_area: OptionPickerScroll) -> None:
        super().__init__(scroll_area)
        self.scroll_area = scroll_area

        self.layout: QHBoxLayout = QHBoxLayout(self)
        # FIXED: Reduce spacing to prevent overflow (5px × 2 = 10px was causing 8px overflow)
        self.layout.setSpacing(1)  # Minimal spacing to prevent overflow
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # FIXED: Use Expanding policy to fill available width properly
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setLayout(self.layout)

    def add_section_widget(self, section: OptionPickerSection) -> None:
        """Add a section widget to the group exactly like Legacy."""
        # FIXED: Use Fixed size policy and set exact constraints to prevent stretching
        section.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # FIXED: Force the section to use its calculated width, not expand
        if (
            hasattr(section, "calculated_width")
            and section.calculated_width is not None
        ):
            section.setFixedWidth(section.calculated_width)
        else:
            # Fallback to size hint if calculated width not available
            size_hint = section.sizeHint()
            if size_hint.width() > 0:
                section.setMinimumWidth(size_hint.width())
                section.setMaximumWidth(size_hint.width())
            else:
                # Final fallback to a reasonable default width
                section.setFixedWidth(300)

        self.layout.addWidget(section, alignment=Qt.AlignmentFlag.AlignCenter)
