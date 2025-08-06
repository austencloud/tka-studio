"""
CAP type selector component.

Grid of buttons for selecting circular arrangement pattern types.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QButtonGroup,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.interfaces.generation_services import CAPType


class CAPTypeSelector(QWidget):
    """Grid selector for CAP type (circular mode)"""

    value_changed = pyqtSignal(CAPType)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._current_value = CAPType.STRICT_ROTATED
        self._button_group = QButtonGroup(self)
        self._setup_controls()

    def _setup_controls(self):
        """Setup CAP type grid"""
        # Main vertical layout
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Header label
        header_layout = QHBoxLayout()
        header_label = QLabel("CAP Type:")
        header_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: 500;
            }
        """)
        header_layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(header_layout)

        # Grid layout for buttons
        grid_layout = QGridLayout()
        grid_layout.setSpacing(4)

        # CAP type data: (cap_type, display_text, row, col)
        cap_types = [
            (CAPType.STRICT_ROTATED, "Rotated", 0, 0),
            (CAPType.STRICT_MIRRORED, "Mirrored", 0, 1),
            (CAPType.STRICT_SWAPPED, "Swapped", 0, 2),
            (CAPType.STRICT_COMPLEMENTARY, "Complementary", 0, 3),
            (CAPType.MIRRORED_SWAPPED, "Mirrored / Swapped", 1, 0),
            (CAPType.SWAPPED_COMPLEMENTARY, "Swapped / Complementary", 1, 1),
            (CAPType.ROTATED_COMPLEMENTARY, "Rotated / Complementary", 1, 2),
            (CAPType.MIRRORED_COMPLEMENTARY, "Mirrored / Complementary", 1, 3),
            (CAPType.ROTATED_SWAPPED, "Rotated / Swapped", 2, 0),
            (CAPType.MIRRORED_ROTATED, "Mirrored / Rotated", 2, 1),
            (CAPType.MIRRORED_COMPLEMENTARY_ROTATED, "Mir / Comp / Rot", 2, 2),
        ]

        for i, (cap_type, text, row, col) in enumerate(cap_types):
            button = QPushButton(text)
            button.setCheckable(True)
            button.setFixedSize(120, 32)
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            # Apply styling
            button.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 6px;
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 10px;
                    font-weight: 500;
                    padding: 4px 8px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.15);
                    border-color: rgba(255, 255, 255, 0.3);
                }
                QPushButton:checked {
                    background: rgba(70, 130, 255, 0.8);
                    border-color: rgba(70, 130, 255, 0.9);
                    color: white;
                    font-weight: 600;
                }
            """)

            if cap_type == CAPType.STRICT_ROTATED:  # Default selection
                button.setChecked(True)

            # Use integer index as button ID, store cap_type separately
            self._button_group.addButton(button, i)
            button.cap_type = cap_type  # Store the actual cap_type on the button
            grid_layout.addWidget(button, row, col)

        # Center the grid
        grid_container = QHBoxLayout()
        grid_container.addStretch()
        grid_container.addLayout(grid_layout)
        grid_container.addStretch()
        layout.addLayout(grid_container)

        # Connect signals
        self._button_group.buttonClicked.connect(self._on_button_clicked)

    def _on_button_clicked(self, button):
        """Handle button click"""
        cap_type = button.cap_type  # Get the stored cap_type from the button
        if cap_type != self._current_value:
            self._current_value = cap_type
            self.value_changed.emit(cap_type)

    def set_value(self, value: CAPType):
        """Set the current value"""
        self._current_value = value
        # Find the button with the matching cap_type
        for button in self._button_group.buttons():
            if hasattr(button, "cap_type") and button.cap_type == value:
                button.setChecked(True)
                break

    def get_value(self) -> CAPType:
        """Get the current value"""
        return self._current_value
