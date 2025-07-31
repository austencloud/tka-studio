"""
Generation mode toggle component.

Provides a toggle between freeform and circular generation modes.
"""

from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QButtonGroup, QHBoxLayout, QPushButton, QWidget

from desktop.modern.core.interfaces.generation_services import GenerationMode

from .generation_control_base import GenerationControlBase


class GenerationModeToggle(GenerationControlBase):
    """Toggle between freeform and circular generation modes"""

    mode_changed = pyqtSignal(GenerationMode)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Generation Mode",
            "Choose between freeform or circular sequence generation",
            parent,
        )
        self._current_mode = GenerationMode.FREEFORM
        self._setup_controls()

    def _setup_controls(self):
        """Setup the mode toggle controls"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        # Create button group for exclusive selection
        self._button_group = QButtonGroup(self)

        # Freeform button
        self._freeform_button = QPushButton("Freeform")
        self._freeform_button.setCheckable(True)
        self._freeform_button.setChecked(True)
        self._freeform_button.setMinimumHeight(32)
        self._freeform_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button_group.addButton(self._freeform_button, 0)
        button_layout.addWidget(self._freeform_button)

        # Circular button
        self._circular_button = QPushButton("Circular")
        self._circular_button.setCheckable(True)
        self._circular_button.setMinimumHeight(32)
        self._circular_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button_group.addButton(self._circular_button, 1)
        button_layout.addWidget(self._circular_button)

        self._content_layout.addLayout(button_layout)

        # Connect signals
        self._button_group.buttonClicked.connect(self._on_button_clicked)

        # Apply styling
        self._apply_button_styling()

    def _apply_button_styling(self):
        """Apply modern toggle button styling"""
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
                background: rgba(70, 130, 255, 0.7);
                border-color: rgba(70, 130, 255, 0.8);
                color: white;
            }
            QPushButton:checked:hover {
                background: rgba(80, 140, 255, 0.8);
            }
        """
        self._freeform_button.setStyleSheet(button_style)
        self._circular_button.setStyleSheet(button_style)

    def _on_button_clicked(self, button):
        """Handle button click"""
        if button == self._freeform_button:
            self._current_mode = GenerationMode.FREEFORM
        else:
            self._current_mode = GenerationMode.CIRCULAR

        self.mode_changed.emit(self._current_mode)

    def set_mode(self, mode: GenerationMode):
        """Set the current mode"""
        self._current_mode = mode
        if mode == GenerationMode.FREEFORM:
            self._freeform_button.setChecked(True)
        else:
            self._circular_button.setChecked(True)
