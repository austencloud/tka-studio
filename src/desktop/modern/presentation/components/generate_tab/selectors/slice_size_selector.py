"""
Slice size selector component.

Provides a toggle between halved and quartered slice sizes for circular mode.
"""

from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QButtonGroup, QHBoxLayout, QPushButton, QWidget

from desktop.modern.core.interfaces.generation_services import SliceSize

from .generation_control_base import GenerationControlBase


class SliceSizeSelector(GenerationControlBase):
    """Selector for slice size (circular mode)"""

    value_changed = pyqtSignal(SliceSize)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Slice Size",
            "Size of circular sequence slices (quartered or halved)",
            parent,
        )
        self._current_value = SliceSize.HALVED
        self._setup_controls()

    def _setup_controls(self):
        """Setup slice size controls"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        self._button_group = QButtonGroup(self)

        # Halved button (default)
        self._halved_button = QPushButton("Halved")
        self._halved_button.setCheckable(True)
        self._halved_button.setChecked(True)
        self._halved_button.setMinimumHeight(32)
        self._halved_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button_group.addButton(self._halved_button, 0)
        button_layout.addWidget(self._halved_button)

        # Quartered button
        self._quartered_button = QPushButton("Quartered")
        self._quartered_button.setCheckable(True)
        self._quartered_button.setMinimumHeight(32)
        self._quartered_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._button_group.addButton(self._quartered_button, 1)
        button_layout.addWidget(self._quartered_button)

        self._content_layout.addLayout(button_layout)

        # Connect signals
        self._button_group.buttonClicked.connect(self._on_button_clicked)

        # Apply styling
        self._apply_button_styling()

    def _apply_button_styling(self):
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
                background: rgba(156, 39, 176, 0.7);
                border-color: rgba(156, 39, 176, 0.8);
                color: white;
            }
        """
        self._halved_button.setStyleSheet(button_style)
        self._quartered_button.setStyleSheet(button_style)

    def _on_button_clicked(self, button):
        """Handle button click"""
        if button == self._halved_button:
            self._current_value = SliceSize.HALVED
        else:
            self._current_value = SliceSize.QUARTERED

        self.value_changed.emit(self._current_value)

    def set_value(self, value: SliceSize):
        """Set the current value"""
        self._current_value = value
        if value == SliceSize.HALVED:
            self._halved_button.setChecked(True)
        else:
            self._quartered_button.setChecked(True)
