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

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QMouseEvent
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton

from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)
from desktop.modern.presentation.utils.letter_type_text_painter import (
    LetterTypeTextPainter,
)


if TYPE_CHECKING:
    from desktop.modern.presentation.components.option_picker.components.option_picker_section import (
        OptionPickerSection,
    )


class OptionPickerSectionButton(QPushButton):
    """
    Simplified section button using Legacy success pattern.

    Direct copy of Legacy OptionPickerSectionTypeButton with minimal changes.
    """

    clicked = pyqtSignal()

    def __init__(self, section_widget: OptionPickerSection):
        super().__init__(section_widget)
        self.section_widget = section_widget
        # Updated to match glassmorphism styling of main header
        self._base_background_color = "rgba(255, 255, 255, 0.3)"
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
        """Generate HTML text for letter type with colored styling."""
        # Get description from LetterType class
        description, type_name = LetterType.get_type_description(letter_type)

        # Use LetterTypeTextPainter to generate colored HTML (matching legacy)
        styled_description = LetterTypeTextPainter.get_colored_text(description)

        return f"{type_name}: {styled_description}"

    def _set_initial_styles(self) -> None:
        """Set initial styles with glassmorphism effect and black text."""
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        # Ensure label text is black (unless modified by font color updater)
        self.label.setStyleSheet("color: black; background: transparent;")

        self._update_style()

    def _update_style(self, background_color: str = None) -> None:
        """Update button style with glassmorphism effect matching main header."""
        background_color = background_color or self._base_background_color
        style = (
            f"QPushButton {{"
            f"  background: {background_color};"
            f"  border: 1px solid rgba(255, 255, 255, 0.3);"
            f"  border-radius: {self.height() // 2}px;"
            f"  padding: 5px;"
            f"  color: black;"
            f"}}"
        )
        self.setStyleSheet(style)

    def enterEvent(self, event) -> None:
        """Handle hover enter - simplified without glassmorphism."""
        # Keep original functionality without glassmorphism styling
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """Handle hover leave - simplified without glassmorphism."""
        # Keep original functionality without glassmorphism styling
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse press with glassmorphism effect."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Use a more opaque glassmorphism effect when pressed
            press_background = "rgba(255, 255, 255, 0.4)"
            self._update_style(background_color=press_background)
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
