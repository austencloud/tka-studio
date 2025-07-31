"""
Turn intensity selector component.

Provides preset buttons for selecting turn intensity values.
"""

from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QButtonGroup, QHBoxLayout, QPushButton, QWidget

from .generation_control_base import GenerationControlBase


class TurnIntensitySelector(GenerationControlBase):
    """Selector for turn intensity"""

    value_changed = pyqtSignal(float)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Turn Intensity", "How complex the turns should be (0.5-3.0)", parent
        )
        self._current_value = 1.0
        self._setup_controls()

    def _setup_controls(self):
        """Setup turn intensity controls"""
        # Preset buttons for common values
        preset_layout = QHBoxLayout()
        preset_layout.setSpacing(6)

        self._preset_group = QButtonGroup(self)
        presets = [
            ("0.5", 0.5),
            ("1", 1.0),
            ("1.5", 1.5),
            ("2", 2.0),
            ("2.5", 2.5),
            ("3", 3.0),
        ]

        for i, (label, value) in enumerate(presets):
            button = QPushButton(label)
            button.setCheckable(True)
            button.setMinimumSize(32, 28)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            if value == 1.0:
                button.setChecked(True)

            self._preset_group.addButton(button, i)
            preset_layout.addWidget(button)

        preset_layout.addStretch()
        self._content_layout.addLayout(preset_layout)

        # Connect signals
        self._preset_group.buttonClicked.connect(self._on_preset_clicked)

        # Store preset values
        self._preset_values = [value for _, value in presets]

        # Apply styling
        self._apply_preset_styling()

    def _apply_preset_styling(self):
        """Apply styling to preset buttons"""
        button_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                font-weight: 500;
                color: rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
                border-color: rgba(255, 255, 255, 0.3);
                color: rgba(255, 255, 255, 0.9);
            }
            QPushButton:checked {
                background: rgba(255, 152, 0, 0.7);
                border-color: rgba(255, 152, 0, 0.8);
                color: white;
            }
        """
        for button in self._preset_group.buttons():
            button.setStyleSheet(button_style)

    def _on_preset_clicked(self, button):
        """Handle preset button click"""
        preset_index = self._preset_group.id(button)
        value = self._preset_values[preset_index]
        if value != self._current_value:
            self._current_value = value
            self.value_changed.emit(value)

    def set_value(self, value: float):
        """Set the current value"""
        self._current_value = value
        # Find closest preset
        for i, preset_value in enumerate(self._preset_values):
            if abs(preset_value - value) < 0.01:
                button = self._preset_group.button(i)
                if button:
                    button.setChecked(True)
                break
