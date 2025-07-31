"""
Level selector component.

Provides a 3-level difficulty selector with gradient styling matching legacy design.
"""

from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .generation_control_base import GenerationControlBase


class LevelSelector(GenerationControlBase):
    """Selector for difficulty level - matches legacy 3-level design"""

    value_changed = pyqtSignal(int)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Difficulty Level",
            "Complexity of the generated sequence",
            center_title=True,
            parent=parent,
        )
        self._current_value = 1
        self._setup_controls()

    def _setup_controls(self):
        """Setup level selector controls matching legacy design"""
        # Main layout for the buttons
        main_layout = QHBoxLayout()
        main_layout.setSpacing(40)  # More space between buttons
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._button_group = QButtonGroup(self)
        self._buttons = []

        # Level data matching legacy implementation
        level_data = [
            (1, "No Turns", "Base motions only\nNo turns added"),
            (2, "Whole Turns", "Whole turns allowed\nRadial orientations only"),
            (3, "Half Turns", "Half turns allowed\nRadial/nonradial orientations"),
        ]

        for level, title, description in level_data:
            # Create vertical layout for each level
            level_layout = QVBoxLayout()
            level_layout.setSpacing(8)
            level_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Create the level button with gradient
            button = QPushButton()
            button.setCheckable(True)
            button.setMinimumSize(100, 100)  # Larger size for better visibility
            button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setToolTip(description)

            if level == 1:
                button.setChecked(True)

            # Apply level-specific styling with gradients
            self._apply_level_specific_styling(button, level)

            self._button_group.addButton(button, level)
            self._buttons.append(button)
            level_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

            # Add title label
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet(
                """
                QLabel {
                    color: rgba(255, 255, 255, 0.95);
                    font-size: 13px;
                    font-weight: bold;
                    background: transparent;
                    border: none;
                    padding: 4px 2px 2px 2px;
                }
            """
            )
            level_layout.addWidget(title_label)

            # Add description label
            desc_label = QLabel(description)
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet(
                """
                QLabel {
                    color: rgba(255, 255, 255, 0.75);
                    font-size: 10px;
                    background: transparent;
                    border: none;
                    padding: 0px;
                    line-height: 1.3;
                }
            """
            )
            level_layout.addWidget(desc_label)

            main_layout.addLayout(level_layout)

        self._content_layout.addLayout(main_layout)

        # Connect signals
        self._button_group.buttonClicked.connect(self._on_button_clicked)

    def _apply_level_specific_styling(self, button: QPushButton, level: int):
        """Apply level-specific gradient styling matching legacy implementation"""
        # Base button style with proper text visibility
        base_style = """
            QPushButton {
                border: 2px solid rgba(255, 255, 255, 0.4);
                border-radius: 50px;
                font-size: 22px;
                font-weight: bold;
                color: black;
                text-align: center;
                padding: 0px;
                margin: 0px;
            }
            QPushButton:hover:!checked {
                border: 3px solid rgba(255, 255, 255, 0.6);
            }
            QPushButton:checked {
                border: 4px solid rgba(255, 255, 255, 0.95);
            }
        """

        # Level-specific gradients matching legacy exactly
        if level == 1:
            # Light gray/white gradient for level 1
            gradient_style = """
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgb(250, 250, 250),
                    stop:1 rgb(220, 220, 220));
                color: rgb(40, 40, 40);
            """
        elif level == 2:
            # Gray gradient for level 2 - matching legacy complex gradient
            gradient_style = """
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgb(170, 170, 170),
                    stop:0.15 rgb(210, 210, 210),
                    stop:0.3 rgb(120, 120, 120),
                    stop:0.4 rgb(180, 180, 180),
                    stop:0.55 rgb(190, 190, 190),
                    stop:0.75 rgb(130, 130, 130),
                    stop:1 rgb(110, 110, 110));
                color: rgb(30, 30, 30);
            """
        else:  # level == 3
            # Gold to dark olive green gradient for level 3
            gradient_style = """
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgb(255, 215, 0),
                    stop:0.2 rgb(238, 201, 0),
                    stop:0.4 rgb(218, 165, 32),
                    stop:0.6 rgb(184, 134, 11),
                    stop:0.8 rgb(139, 69, 19),
                    stop:1 rgb(85, 107, 47));
                color: rgb(20, 20, 20);
            """

        button.setStyleSheet(base_style + gradient_style)
        button.setText(str(level))

    def _on_button_clicked(self, button):
        """Handle button click"""
        level = self._button_group.id(button)
        if level != self._current_value:
            self._current_value = level
            self.value_changed.emit(level)

    def set_value(self, value: int):
        """Set the current value"""
        if 1 <= value <= 3:  # Updated to support only 3 levels
            self._current_value = value
            button = self._button_group.button(value)
            if button:
                button.setChecked(True)
