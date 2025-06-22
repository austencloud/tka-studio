from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

try:
    from data.constants import CLOCK, COUNTER, IN, OUT
except ImportError:
    # Fallback constants if data module not available
    IN = "in"
    COUNTER = "counter"
    OUT = "out"
    CLOCK = "clock"


class OrientationPickerWidget(QWidget):
    """Orientation picker for start position - only 4 orientations"""

    orientation_changed = pyqtSignal(str, str)  # arrow_color, orientation

    def __init__(self, arrow_color: str):
        super().__init__()
        self._arrow_color = arrow_color
        self._current_orientation = IN

        # VERIFIED: Use actual orientations from Legacy
        self.orientations = [IN, COUNTER, OUT, CLOCK]
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Orientation text label
        self._text_label = QLabel("Orientation")
        self._text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._text_label)

        # Clickable orientation display (like Legacy)
        self._orientation_display = QPushButton(self._current_orientation)
        self._orientation_display.clicked.connect(self._show_orientation_dialog)
        layout.addWidget(self._orientation_display)

        # Rotate buttons (like Legacy)
        self._rotate_buttons = QWidget()
        rotate_layout = QHBoxLayout(self._rotate_buttons)

        self._rotate_left = QPushButton("◀")
        self._rotate_right = QPushButton("▶")
        self._rotate_left.clicked.connect(self._rotate_orientation_left)
        self._rotate_right.clicked.connect(self._rotate_orientation_right)

        rotate_layout.addWidget(self._rotate_left)
        rotate_layout.addWidget(self._rotate_right)
        layout.addWidget(self._rotate_buttons)

    def _show_orientation_dialog(self):
        """Show orientation selection dialog with 4 buttons"""
        dialog = QDialog(self)
        dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        layout = QHBoxLayout(dialog)

        for orientation in self.orientations:
            button = QPushButton(orientation)
            button.clicked.connect(
                lambda _, ori=orientation: self._select_orientation(dialog, ori)
            )
            layout.addWidget(button)

        dialog.exec()

    def _select_orientation(self, dialog, orientation: str):
        self._set_orientation(orientation)
        dialog.accept()

    def _rotate_orientation_left(self):
        """Cycle through orientations backwards"""
        current_index = self.orientations.index(self._current_orientation)
        new_index = (current_index - 1) % len(self.orientations)
        self._set_orientation(self.orientations[new_index])

    def _rotate_orientation_right(self):
        """Cycle through orientations forwards"""
        current_index = self.orientations.index(self._current_orientation)
        new_index = (current_index + 1) % len(self.orientations)
        self._set_orientation(self.orientations[new_index])

    def _set_orientation(self, orientation: str):
        self._current_orientation = orientation
        self._orientation_display.setText(orientation)
        self.orientation_changed.emit(self._arrow_color, orientation)

    def set_orientation(self, orientation: str):
        """Set orientation from external source"""
        if orientation in self.orientations:
            self._set_orientation(orientation)

    def get_orientation(self) -> str:
        """Get current orientation"""
        return self._current_orientation
