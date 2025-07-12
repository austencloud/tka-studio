"""
Simplified Option Picker Section Button - Direct Copy of Legacy Success Pattern

This button directly copies the successful Legacy OptionPickerSectionTypeButton pattern,
replacing complex Modern button logic with simple Qt QPushButton management.

Key principles from Legacy:
- Simple QPushButton with embedded QLabel for HTML text
- Natural Qt sizing with resizeEvent
- Direct hover/press/release handling
- No complex business logic or orchestration
"""

from typing import TYPE_CHECKING

from presentation.components.option_picker.types.letter_types import LetterType
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QMouseEvent
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton

if TYPE_CHECKING:
    from presentation.components.option_picker.core.option_picker_section import (
        OptionPickerSection,
    )


class OptionPickerSectionButton(QPushButton):
    """
    Simplified section button using Legacy success pattern.

    Direct copy of Legacy OptionPickerSectionTypeButton with minimal changes.
    """

    clicked = pyqtSignal()

    def __init__(self, section_widget: "OptionPickerSection"):
        super().__init__(section_widget)
        self.section_widget = section_widget
        self._base_background_color = "rgba(255, 255, 255, 200)"
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Create a label that will render HTML
        self.label = QLabel(self)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        # Put the label inside the button via a layout
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._layout)

        # Generate HTML from the letter type
        self._paint_text(section_widget.letter_type)

        # Initial style
        self._set_initial_styles()

    def _paint_text(self, letter_type: str) -> None:
        """Generate and set HTML text for the button."""
        html_text = self._generate_html_text(letter_type)
        self.label.setText(html_text)

    def _generate_html_text(self, letter_type: str) -> str:
        """Generate HTML text for letter type - simplified version."""
        # Get description from LetterType class
        description, type_name = LetterType.get_type_description(letter_type)
        return f"{type_name}: {description}"

    def _set_initial_styles(self) -> None:
        """Set initial styles exactly like Legacy."""
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)
        self._update_style()

    def _update_style(self, background_color: str = None) -> None:
        """Update button style exactly like Legacy."""
        background_color = background_color or self._base_background_color
        style = (
            f"QPushButton {{"
            f"  background-color: {background_color};"
            f"  font-weight: bold;"
            f"  border: none;"
            f"  border-radius: {self.height() // 2}px;"
            f"  padding: 5px;"
            f"}}"
            f"QPushButton:hover {{"
            f"  border: 2px solid black;"
            f"}}"
        )
        self.setStyleSheet(style)

    def enterEvent(self, event) -> None:
        """Handle hover enter exactly like Legacy."""
        gradient = (
            "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
            "stop:0 rgba(200, 200, 200, 1), stop:1 rgba(150, 150, 150, 1))"
        )
        self._update_style(background_color=gradient)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """Handle hover leave exactly like Legacy."""
        self._update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse press exactly like Legacy."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._update_style(background_color="#aaaaaa")
            self.clicked.emit()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """Handle mouse release exactly like Legacy."""
        self._update_style()
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event) -> None:
        """Handle resize exactly like Legacy."""
        super().resizeEvent(event)

        parent_height = self.section_widget.mw_size_provider().height()
        font_size = max(parent_height // 70, 10)
        label_height = max(int(font_size * 3), 20)
        label_width = max(int(label_height * 6), 100)

        # Adjust label's font
        font = self.label.font()
        font.setPointSize(font_size)
        self.label.setFont(font)

        # Resize the push-button
        self.setFixedSize(QSize(label_width, label_height))

        # Reapply style so corner radius is correct
        self._update_style()
