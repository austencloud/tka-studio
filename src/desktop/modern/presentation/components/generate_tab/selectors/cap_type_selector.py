"""
CAP type selector component.

Provides a dropdown for selecting circular arrangement pattern types.
"""

from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox, QWidget

from desktop.modern.core.interfaces.generation_services import CAPType

from .generation_control_base import GenerationControlBase


class CAPTypeSelector(GenerationControlBase):
    """Selector for CAP type (circular mode)"""

    value_changed = pyqtSignal(CAPType)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("CAP Type", "Circular arrangement pattern type", parent)
        self._current_value = CAPType.STRICT_ROTATED
        self._setup_controls()

    def _setup_controls(self):
        """Setup CAP type controls"""
        combo = QComboBox()
        combo.setMinimumHeight(32)
        combo.setStyleSheet(
            """
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 4px 8px;
                color: rgba(255, 255, 255, 0.9);
            }
            QComboBox:hover {
                background: rgba(255, 255, 255, 0.15);
                border-color: rgba(255, 255, 255, 0.3);
            }
            QComboBox:focus {
                border-color: rgba(70, 130, 255, 0.8);
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid rgba(255, 255, 255, 0.6);
                margin-right: 6px;
            }
            QComboBox QAbstractItemView {
                background: rgba(40, 40, 60, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                color: rgba(255, 255, 255, 0.9);
                selection-background-color: rgba(70, 130, 255, 0.7);
            }
        """
        )

        # Add all Legacy CAP types
        cap_types = [
            ("Strict Rotated", CAPType.STRICT_ROTATED),
            ("Strict Mirrored", CAPType.STRICT_MIRRORED),
            ("Strict Swapped", CAPType.STRICT_SWAPPED),
            ("Strict Complementary", CAPType.STRICT_COMPLEMENTARY),
            ("Swapped Complementary", CAPType.SWAPPED_COMPLEMENTARY),
            ("Rotated Complementary", CAPType.ROTATED_COMPLEMENTARY),
            ("Mirrored Swapped", CAPType.MIRRORED_SWAPPED),
            ("Mirrored Complementary", CAPType.MIRRORED_COMPLEMENTARY),
            ("Rotated Swapped", CAPType.ROTATED_SWAPPED),
            ("Mirrored Rotated", CAPType.MIRRORED_ROTATED),
            ("Mirrored Complementary Rotated", CAPType.MIRRORED_COMPLEMENTARY_ROTATED),
        ]

        for name, cap_type in cap_types:
            combo.addItem(name, cap_type)

        combo.currentIndexChanged.connect(self._on_combo_changed)
        self._combo = combo

        self._content_layout.addWidget(combo)

    def _on_combo_changed(self, index: int):
        """Handle combo box change"""
        value = self._combo.itemData(index)
        if value != self._current_value:
            self._current_value = value
            self.value_changed.emit(value)

    def set_value(self, value: CAPType):
        """Set the current value"""
        self._current_value = value
        for i in range(self._combo.count()):
            if self._combo.itemData(i) == value:
                self._combo.setCurrentIndex(i)
                break
