"""
Letter type selector component.

Simple horizontal row of numbered buttons for letter types in freeform mode.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.interfaces.generation_services import LetterType


class LetterTypeSelector(QWidget):
    """Simple horizontal selector for letter types (freeform mode)"""

    value_changed = pyqtSignal(set)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._current_value = {
            LetterType.TYPE1,
            LetterType.TYPE2,
            LetterType.TYPE3,
            LetterType.TYPE4,
            LetterType.TYPE5,
            LetterType.TYPE6,
        }
        self._buttons = {}
        self._setup_controls()

    def _setup_controls(self):
        """Setup simple letter type controls"""
        # Main vertical layout
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Header label
        header_layout = QHBoxLayout()
        header_label = QLabel("Filter by type:")
        header_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: 500;
            }
        """)
        header_layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(header_layout)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Letter type data: (letter_type, number)
        letter_types = [
            (LetterType.TYPE1, "1"),
            (LetterType.TYPE2, "2"),
            (LetterType.TYPE3, "3"),
            (LetterType.TYPE4, "4"),
            (LetterType.TYPE5, "5"),
            (LetterType.TYPE6, "6"),
        ]

        for letter_type, number in letter_types:
            button = QPushButton(number)
            button.setCheckable(True)
            button.setChecked(True)  # All selected by default
            button.setFixedSize(60, 45)  # Even larger for better usability
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            # Apply exact legacy double border colors for each type
            # Each type has primary and secondary colors from legacy
            legacy_color_pairs = [
                ("#36c3ff", "#6F2DA8"),  # Type 1: Light blue + Purple
                ("#6F2DA8", "#6F2DA8"),  # Type 2: Purple + Purple
                ("#26e600", "#6F2DA8"),  # Type 3: Green + Purple
                ("#26e600", "#26e600"),  # Type 4: Green + Green
                ("#00b3ff", "#26e600"),  # Type 5: Blue + Green
                ("#eb7d00", "#eb7d00"),  # Type 6: Orange + Orange
            ]
            primary_color, secondary_color = legacy_color_pairs[int(number) - 1]

            button.setStyleSheet(f"""
                QPushButton {{
                    background: white;
                    border: 2px solid rgba(150, 150, 150, 0.4);
                    border-radius: 6px;
                    color: black;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover:!checked {{
                    background: rgba(240, 240, 240, 1.0);
                    border-color: rgba(180, 180, 180, 0.5);
                    color: black;
                }}
                QPushButton:checked {{
                    background: white;
                    border: 3px solid {secondary_color};
                    color: black;
                    font-weight: bold;
                    outline: 2px solid {primary_color};
                    outline-offset: -1px;
                }}
                QPushButton:checked:hover {{
                    background: rgba(250, 250, 250, 1.0);
                }}
            """)

            button.clicked.connect(
                lambda checked, lt=letter_type: self._on_button_clicked(lt, checked)
            )
            self._buttons[letter_type] = button
            button_layout.addWidget(button)

        layout.addLayout(button_layout)

    def _on_button_clicked(self, letter_type: LetterType, checked: bool):
        """Handle button click"""
        if checked:
            self._current_value.add(letter_type)
        else:
            self._current_value.discard(letter_type)

        # Ensure at least one type is selected
        if not self._current_value:
            self._current_value.add(letter_type)
            self._buttons[letter_type].setChecked(True)

        self.value_changed.emit(self._current_value.copy())

    def set_value(self, value: set[LetterType]):
        """Set the current value"""
        self._current_value = value.copy()
        for letter_type, button in self._buttons.items():
            button.setChecked(letter_type in value)

    def get_value(self) -> set[LetterType]:
        """Get the current value"""
        return self._current_value.copy()
