"""
Turn intensity selector component.

Simple increment/decrement control for turn intensity values.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from .increment_adjuster_button import IncrementAdjusterButton


class TurnIntensitySelector(QWidget):
    """Simple turn intensity adjuster with +/- buttons"""

    value_changed = pyqtSignal(float)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._current_value = 1.0
        self._values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        self._setup_controls()

    def _setup_controls(self):
        """Setup simple turn intensity controls"""
        # Main horizontal layout
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        # Label
        self._label = QLabel("Turn Intensity:")
        self._label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: 500;
            }
        """)

        # Minus button
        self._minus_button = IncrementAdjusterButton("-")
        self._minus_button.clicked.connect(self._decrease_intensity)

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
        self._plus_button.clicked.connect(self._increase_intensity)

        # Add to layout
        layout.addWidget(self._label)
        layout.addWidget(self._minus_button)
        layout.addWidget(self._value_label)
        layout.addWidget(self._plus_button)

    def _adjust_intensity(self, change: int):
        """Adjust intensity by change amount"""
        try:
            current_index = self._values.index(self._current_value)
        except ValueError:
            # Find closest value
            current_index = min(
                range(len(self._values)),
                key=lambda i: abs(self._values[i] - self._current_value),
            )

        new_index = current_index + change
        if 0 <= new_index < len(self._values):
            self._current_value = self._values[new_index]
            self._value_label.setText(str(self._current_value))
            self.value_changed.emit(self._current_value)

    def _increase_intensity(self):
        """Increase turn intensity"""
        self._adjust_intensity(1)

    def _decrease_intensity(self):
        """Decrease turn intensity"""
        self._adjust_intensity(-1)

    def set_value(self, value: float):
        """Set the current value"""
        if value in self._values:
            self._current_value = value
            self._value_label.setText(str(value))
        else:
            # Find closest value
            closest = min(self._values, key=lambda x: abs(x - value))
            self._current_value = closest
            self._value_label.setText(str(closest))

    def get_value(self) -> float:
        """Get the current value"""
        return self._current_value
