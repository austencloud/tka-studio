"""
Option Picker Section Widget - Main UI Component
Split from option_picker_section.py - contains core section widget logic
"""

from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from presentation.components.option_picker.types.letter_types import LetterType
from presentation.components.option_picker.components.sections.section_header import (
    OptionPickerSectionHeader,
)
from presentation.components.option_picker.components.sections.section_container import (
    OptionPickerSectionPictographContainer,
)


class OptionPickerSection(QWidget):
    """
    Main option picker section widget.
    Contains UI setup and basic event handling.
    """

    def __init__(self, letter_type: str, parent=None, mw_size_provider=None):
        super().__init__(parent)
        self.letter_type = letter_type
        self.mw_size_provider = mw_size_provider
        self.is_groupable = letter_type in [
            LetterType.TYPE4,
            LetterType.TYPE5,
            LetterType.TYPE6,
        ]

        # Initialize layout manager
        from presentation.components.option_picker.components.sections.section_layout_manager import (
            SectionLayoutManager,
        )

        self.layout_manager = SectionLayoutManager(self)

        self._setup_ui()
        self._register_for_sizing_updates()

    def _setup_ui(self):
        """Setup UI using clean separation of concerns."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create header component
        self.header = OptionPickerSectionHeader(self)
        layout.addWidget(self.header)

        # Create pictograph container component
        self.section_pictograph_container = OptionPickerSectionPictographContainer(self)
        layout.addWidget(self.section_pictograph_container)

        # Set transparent background
        self.setStyleSheet("background-color: transparent; border: none;")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Compatibility aliases
        self.pictograph_layout = self.section_pictograph_container.layout
        self.pictographs = self.section_pictograph_container.pictographs
        self.header_button = self.header.type_button

    def add_pictograph_from_pool(self, pictograph_frame):
        """Add pictograph from pool using layout manager."""
        self.layout_manager.add_pictograph_from_pool(pictograph_frame)

    def clear_pictographs(self):
        """Clear pictographs using container component."""
        self.section_pictograph_container.clear_pictographs()

    def clear_pictographs_pool_style(self):
        """Clear pictographs using pool style."""
        self.section_pictograph_container.clear_pictographs_pool_style()

    def toggle_section(self):
        """Toggle section visibility."""
        is_visible = not self.section_pictograph_container.isVisible()
        self.section_pictograph_container.setVisible(is_visible)

    def _register_for_sizing_updates(self):
        """Register for sizing updates from option picker."""
        self.layout_manager.register_for_sizing_updates()

    def resizeEvent(self, event):
        """Handle resize events."""
        self.layout_manager.handle_resize_event(event)
        super().resizeEvent(event)

    # Properties for compatibility
    @property
    def pictographs(self):
        return self.section_pictograph_container.pictographs

    @pictographs.setter
    def pictographs(self, value):
        self.section_pictograph_container.pictographs = value
