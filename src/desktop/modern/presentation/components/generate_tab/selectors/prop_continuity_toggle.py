"""
Prop continuity toggle component.

Provides a toggle between continuous and random prop behavior.
"""

from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QButtonGroup, QHBoxLayout, QPushButton, QWidget

from desktop.modern.core.interfaces.generation_services import PropContinuity

from .generation_control_base import GenerationControlBase


class PropContinuityToggle(GenerationControlBase):
    """Toggle for prop continuity setting"""

    value_changed = pyqtSignal(PropContinuity)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Prop Continuity", "How props should behave throughout the sequence", parent
        )
        self._current_value = PropContinuity.CONTINUOUS
        self._setup_controls()

    def _setup_controls(self):
        """Setup prop continuity controls"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        self._button_group = QButtonGroup(self)

        # Continuous button
        self._continuous_button = QPushButton("Continuous")
        self._continuous_button.setCheckable(True)
        self._continuous_button.setChecked(True)
        self._continuous_button.setMinimumHeight(32)
        self._continuous_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button_group.addButton(self._continuous_button, 0)
        button_layout.addWidget(self._continuous_button)

        # Random button
        self._random_button = QPushButton("Random")
        self._random_button.setCheckable(True)
        self._random_button.setMinimumHeight(32)
        self._random_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button_group.addButton(self._random_button, 1)
        button_layout.addWidget(self._random_button)

        self._content_layout.addLayout(button_layout)

        # Connect signals
        self._button_group.buttonClicked.connect(self._on_button_clicked)

        # Apply styling
        self._apply_toggle_styling()

    def _apply_toggle_styling(self):
        """Apply toggle button styling"""
        button_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: 500;
                color: rgba(255, 255, 255, 0.8);
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
                border-color: rgba(255, 255, 255, 0.3);
                color: rgba(255, 255, 255, 0.9);
            }
            QPushButton:checked {
                background: rgba(76, 175, 80, 0.7);
                border-color: rgba(76, 175, 80, 0.8);
                color: white;
            }
        """
        self._continuous_button.setStyleSheet(button_style)
        self._random_button.setStyleSheet(button_style)

    def _on_button_clicked(self, button):
        """Handle button click"""
        if button == self._continuous_button:
            self._current_value = PropContinuity.CONTINUOUS
        else:
            self._current_value = PropContinuity.RANDOM

        self.value_changed.emit(self._current_value)

    def set_value(self, value: PropContinuity):
        """Set the current value"""
        self._current_value = value
        if value == PropContinuity.CONTINUOUS:
            self._continuous_button.setChecked(True)
        else:
            self._random_button.setChecked(True)
