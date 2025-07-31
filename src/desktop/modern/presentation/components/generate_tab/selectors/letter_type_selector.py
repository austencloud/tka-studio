"""
Letter type selector component.

Provides multi-select checkboxes for letter types in freeform mode.
"""

from typing import Optional, Set

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QCheckBox, QVBoxLayout, QWidget

from desktop.modern.core.interfaces.generation_services import LetterType

from .generation_control_base import GenerationControlBase


class LetterTypeSelector(GenerationControlBase):
    """Multi-select for letter types (freeform mode)"""

    value_changed = pyqtSignal(set)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            "Letter Types", "Select which letter types to include in generation", parent
        )
        self._current_value = {
            LetterType.TYPE1,
            LetterType.TYPE2,
            LetterType.TYPE3,
            LetterType.TYPE4,
            LetterType.TYPE5,
            LetterType.TYPE6,
        }
        self._setup_controls()

    def _setup_controls(self):
        """Setup letter type controls"""
        checkbox_layout = QVBoxLayout()
        checkbox_layout.setSpacing(4)

        self._checkboxes = {}

        # Legacy's letter type descriptions
        letter_type_info = [
            (LetterType.TYPE1, "Type 1 (Dual-Shift: A-V)"),
            (LetterType.TYPE2, "Type 2 (Shift: W,X,Y,Z,Σ,Δ,θ,Ω)"),
            (LetterType.TYPE3, "Type 3 (Cross-Shift: W-,X-,Y-,Z-,Σ-,Δ-,θ-,Ω-)"),
            (LetterType.TYPE4, "Type 4 (Dash: Φ,Ψ,Λ)"),
            (LetterType.TYPE5, "Type 5 (Dual-Dash: Φ-,Ψ-,Λ-)"),
            (LetterType.TYPE6, "Type 6 (Static: α,β,Γ)"),
        ]

        for letter_type, description in letter_type_info:
            checkbox = QCheckBox(description)
            checkbox.setChecked(True)
            checkbox.setStyleSheet(
                """
                QCheckBox {
                    color: rgba(255, 255, 255, 0.8);
                    spacing: 8px;
                    font-size: 9px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border-radius: 3px;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    background: rgba(255, 255, 255, 0.1);
                }
                QCheckBox::indicator:hover {
                    border-color: rgba(255, 255, 255, 0.4);
                    background: rgba(255, 255, 255, 0.15);
                }
                QCheckBox::indicator:checked {
                    background: rgba(76, 175, 80, 0.7);
                    border-color: rgba(76, 175, 80, 0.8);
                }
                QCheckBox::indicator:checked:hover {
                    background: rgba(76, 175, 80, 0.8);
                }
            """
            )
            checkbox.stateChanged.connect(self._on_checkbox_changed)
            self._checkboxes[letter_type] = checkbox
            checkbox_layout.addWidget(checkbox)

        self._content_layout.addLayout(checkbox_layout)

    def _on_checkbox_changed(self):
        """Handle checkbox state change"""
        new_value = set()
        for letter_type, checkbox in self._checkboxes.items():
            if checkbox.isChecked():
                new_value.add(letter_type)

        if new_value != self._current_value:
            self._current_value = new_value
            self.value_changed.emit(new_value)

    def set_value(self, value: Set[LetterType]):
        """Set the current value"""
        self._current_value = value
        for letter_type, checkbox in self._checkboxes.items():
            checkbox.blockSignals(True)
            checkbox.setChecked(letter_type in value)
            checkbox.blockSignals(False)
