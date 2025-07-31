"""
Grid Mode Selector for Generate Panel

A modern control for selecting between Diamond and Box grid modes.
Follows the same pattern as other generation controls.
"""

from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QButtonGroup, QHBoxLayout, QRadioButton, QWidget

from desktop.modern.domain.models.enums import GridMode

from .generation_control_base import GenerationControlBase


class ModernGridModeSelector(GenerationControlBase):
    """Modern grid mode selector for generation configuration"""

    value_changed = pyqtSignal(GridMode)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Grid Mode",
            "Choose between Diamond or Box grid layout for generated sequences",
            parent,
        )
        self._current_mode = GridMode.DIAMOND
        self._setup_controls()

    def _setup_controls(self):
        """Setup the radio button controls."""
        control_layout = QHBoxLayout()
        control_layout.setSpacing(16)
        control_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create button group for mutual exclusivity
        self._button_group = QButtonGroup(self)

        # Diamond radio button
        self._diamond_radio = QRadioButton("Diamond", self)
        self._diamond_radio.setChecked(True)  # Default to diamond
        self._diamond_radio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._diamond_radio.setStyleSheet(self._get_radio_button_style())

        # Box radio button
        self._box_radio = QRadioButton("Box", self)
        self._box_radio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._box_radio.setStyleSheet(self._get_radio_button_style())

        # Add to button group
        self._button_group.addButton(self._diamond_radio)
        self._button_group.addButton(self._box_radio)

        # Connect signals
        self._diamond_radio.toggled.connect(self._on_diamond_toggled)
        self._box_radio.toggled.connect(self._on_box_toggled)

        # Add to layout
        control_layout.addStretch(1)
        control_layout.addWidget(self._diamond_radio)
        control_layout.addWidget(self._box_radio)
        control_layout.addStretch(1)

        self._content_layout.addLayout(control_layout)

    def _get_radio_button_style(self) -> str:
        """Get consistent radio button styling."""
        return """
            QRadioButton {
                color: rgba(255, 255, 255, 0.9);
                font-size: 12px;
                font-weight: 500;
                spacing: 8px;
                padding: 4px 8px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                background: rgba(255, 255, 255, 0.1);
            }
            QRadioButton::indicator:hover {
                border-color: rgba(255, 255, 255, 0.5);
                background: rgba(255, 255, 255, 0.15);
            }
            QRadioButton::indicator:checked {
                border-color: rgba(70, 130, 255, 0.8);
                background: rgba(70, 130, 255, 0.3);
            }
            QRadioButton::indicator:checked:hover {
                border-color: rgba(70, 130, 255, 1.0);
                background: rgba(70, 130, 255, 0.4);
            }
            QRadioButton:hover {
                color: rgba(255, 255, 255, 1.0);
            }
        """

    def _on_diamond_toggled(self, checked: bool):
        """Handle diamond radio button toggle."""
        if checked:
            self._current_mode = GridMode.DIAMOND
            self.value_changed.emit(self._current_mode)

    def _on_box_toggled(self, checked: bool):
        """Handle box radio button toggle."""
        if checked:
            self._current_mode = GridMode.BOX
            self.value_changed.emit(self._current_mode)

    def get_value(self) -> GridMode:
        """Get the current grid mode value."""
        return self._current_mode

    def set_value(self, mode: GridMode):
        """Set the grid mode value."""
        if mode != self._current_mode:
            self._current_mode = mode

            # Update radio buttons without triggering signals
            self._diamond_radio.blockSignals(True)
            self._box_radio.blockSignals(True)

            if mode == GridMode.DIAMOND:
                self._diamond_radio.setChecked(True)
            else:
                self._box_radio.setChecked(True)

            self._diamond_radio.blockSignals(False)
            self._box_radio.blockSignals(False)

    def reset_to_default(self):
        """Reset to default value (Diamond)."""
        self.set_value(GridMode.DIAMOND)
