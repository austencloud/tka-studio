"""
Length selector component.

Simple increment/decrement control for sequence length.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from .increment_adjuster_button import IncrementAdjusterButton


class LengthSelector(QWidget):
    """Simple length adjuster with +/- buttons"""

    value_changed = pyqtSignal(int)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._current_value = 16
        self._min_value = 4
        self._max_value = 64
        self._adjustment_amount = 2
        self._setup_controls()

    def _setup_controls(self):
        """Setup simple length controls"""
        # Main horizontal layout
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        # Label
        self._label = QLabel("Length:")
        self._label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: 500;
            }
        """)

        # Minus button
        self._minus_button = IncrementAdjusterButton("-")
        self._minus_button.clicked.connect(self._decrease_length)

        # Value display
        self._value_label = QLabel(str(self._current_value))
        self._value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._value_label.setFont(QFont("Georgia", 14, QFont.Weight.Bold))
        self._value_label.setStyleSheet("""
            QLabel {
                color: white;
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 6px 12px;
                min-width: 30px;
            }
        """)

        # Plus button
        self._plus_button = IncrementAdjusterButton("+")
        self._plus_button.clicked.connect(self._increase_length)

        # Add to layout
        layout.addWidget(self._label)
        layout.addWidget(self._minus_button)
        layout.addWidget(self._value_label)
        layout.addWidget(self._plus_button)

    def _increase_length(self):
        """Increase length"""
        if self._current_value < self._max_value:
            self._current_value += self._adjustment_amount
            self._value_label.setText(str(self._current_value))
            self.value_changed.emit(self._current_value)

    def _decrease_length(self):
        """Decrease length"""
        if self._current_value > self._min_value:
            self._current_value -= self._adjustment_amount
            self._value_label.setText(str(self._current_value))
            self.value_changed.emit(self._current_value)

    def set_value(self, value: int):
        """Set the current value"""
        if self._min_value <= value <= self._max_value:
            self._current_value = value
            self._value_label.setText(str(value))

    def get_value(self) -> int:
        """Get the current value"""
        return self._current_value

    def set_adjustment_amount(self, amount: int):
        """Set the increment/decrement amount"""
        self._adjustment_amount = amount
