"""
Level selector component.

Simple 3-level difficulty selector with circular buttons.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LevelSelector(QWidget):
    """Simple level selector with circular numbered buttons"""

    value_changed = pyqtSignal(int)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._current_value = 2  # Default to "Whole Turns"
        self._setup_controls()

    def _setup_controls(self):
        """Setup simple level selector"""
        # Main horizontal layout
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        self._button_group = QButtonGroup(self)

        # Level data with exact legacy gradient colors
        level_data = [
            (1, "1", "No Turns"),
            (2, "2", "Whole Turns"),
            (3, "3", "Half Turns"),
        ]

        for level, number, label in level_data:
            # Create vertical layout for button + label
            vbox = QVBoxLayout()
            vbox.setSpacing(8)
            vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Create circular button
            button = QPushButton(number)
            button.setCheckable(True)
            button.setFixedSize(60, 60)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFont(QFont("Georgia", 18, QFont.Weight.Bold))

            # Apply exact legacy gradient styling
            if level == 1:
                # Level 1: Light gray (exact legacy color)
                gradient_style = """
                    background: rgb(245, 245, 245);
                    color: black;
                """
            elif level == 2:
                # Level 2: Complex gray gradient (exact legacy colors)
                gradient_style = """
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgb(170, 170, 170),
                        stop:0.3 rgb(120, 120, 120),
                        stop:0.6 rgb(180, 180, 180),
                        stop:1 rgb(110, 110, 110));
                    color: black;
                """
            else:  # level == 3
                # Level 3: Gold to dark olive gradient (exact legacy colors)
                gradient_style = """
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgb(255, 215, 0),
                        stop:0.2 rgb(238, 201, 0),
                        stop:0.4 rgb(218, 165, 32),
                        stop:0.6 rgb(184, 134, 11),
                        stop:0.8 rgb(139, 69, 19),
                        stop:1 rgb(85, 107, 47));
                    color: black;
                """

            button.setStyleSheet(f"""
                QPushButton {{
                    {gradient_style}
                    border: 2px solid rgba(255, 255, 255, 0.4);
                    border-radius: 30px;
                    font-weight: bold;
                }}
                QPushButton:hover:!checked {{
                    border: 3px solid rgba(255, 255, 255, 0.6);
                }}
                QPushButton:checked {{
                    border: 4px solid rgba(255, 255, 255, 0.95);
                }}
            """)

            if level == 2:  # Default selection
                button.setChecked(True)

            # Create label
            label_widget = QLabel(label)
            label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_widget.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                }
            """)

            # Add to layout
            vbox.addWidget(button)
            vbox.addWidget(label_widget)
            layout.addLayout(vbox)

            # Add to button group
            self._button_group.addButton(button, level)

        # Connect signals
        self._button_group.buttonClicked.connect(self._on_button_clicked)

    def _on_button_clicked(self, button):
        """Handle button click"""
        level = self._button_group.id(button)
        if level != self._current_value:
            self._current_value = level
            self.value_changed.emit(level)

    def set_value(self, value: int):
        """Set the current value"""
        if 1 <= value <= 3:
            self._current_value = value
            button = self._button_group.button(value)
            if button:
                button.setChecked(True)

    def get_value(self) -> int:
        """Get the current value"""
        return self._current_value
