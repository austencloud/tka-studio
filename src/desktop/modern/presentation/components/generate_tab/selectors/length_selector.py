"""
Length selector component.

Provides a slider and spinbox for selecting sequence length.
"""

from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QSlider, QSpinBox, QWidget

from .generation_control_base import GenerationControlBase


class LengthSelector(GenerationControlBase):
    """Selector for sequence length"""

    value_changed = pyqtSignal(int)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Sequence Length",
            "Number of beats in the generated sequence (4-32)",
            parent,
        )
        self._current_value = 16
        self._setup_controls()

    def _setup_controls(self):
        """Setup length selector controls"""
        control_layout = QHBoxLayout()
        control_layout.setSpacing(12)

        # Slider
        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setMinimum(4)
        self._slider.setMaximum(32)
        self._slider.setValue(16)
        self._slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._slider.setTickInterval(4)
        self._slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                border: 1px solid rgba(255, 255, 255, 0.2);
                height: 4px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: rgba(70, 130, 255, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.3);
                width: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: rgba(80, 140, 255, 0.9);
            }
            QSlider::sub-page:horizontal {
                background: rgba(70, 130, 255, 0.5);
                border-radius: 2px;
            }
        """
        )
        control_layout.addWidget(self._slider, 1)

        # Value display/input
        self._spinbox = QSpinBox()
        self._spinbox.setMinimum(4)
        self._spinbox.setMaximum(32)
        self._spinbox.setValue(16)
        self._spinbox.setMinimumWidth(60)
        self._spinbox.setStyleSheet(
            """
            QSpinBox {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                padding: 4px 8px;
                color: rgba(255, 255, 255, 0.9);
            }
            QSpinBox:hover {
                background: rgba(255, 255, 255, 0.15);
                border-color: rgba(255, 255, 255, 0.3);
            }
            QSpinBox:focus {
                border-color: rgba(70, 130, 255, 0.8);
            }
        """
        )
        control_layout.addWidget(self._spinbox)

        self._content_layout.addLayout(control_layout)

        # Connect signals
        self._slider.valueChanged.connect(self._on_value_changed)
        self._spinbox.valueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, value: int):
        """Handle value change"""
        if value != self._current_value:
            self._current_value = value

            # Sync controls
            self._slider.blockSignals(True)
            self._spinbox.blockSignals(True)
            self._slider.setValue(value)
            self._spinbox.setValue(value)
            self._slider.blockSignals(False)
            self._spinbox.blockSignals(False)

            self.value_changed.emit(value)

    def set_value(self, value: int):
        """Set the current value"""
        self._on_value_changed(value)
