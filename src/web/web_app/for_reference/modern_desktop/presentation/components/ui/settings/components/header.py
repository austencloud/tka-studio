"""
Settings dialog header component.

Contains the title and close button for the settings dialog.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton


class SettingsHeader(QFrame):
    """Header component for the settings dialog with title and close button."""

    close_requested = pyqtSignal()

    def __init__(self, title: str = "Settings", parent=None):
        super().__init__(parent)
        self.setObjectName("header_frame")
        self._setup_ui(title)

    def _setup_ui(self, title: str):
        """Setup the header UI with title and close button."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)

        # Title label
        self.title_label = QLabel(title)
        self.title_label.setObjectName("dialog_title")
        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(self.title_label)

        layout.addStretch()

        # Close button with enhanced accessibility
        self.close_button = QPushButton("×")
        self.close_button.setObjectName("close_button")
        # Increased size for better accessibility (WCAG compliant)
        self.close_button.setFixedSize(48, 48)
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.clicked.connect(self.close_requested.emit)
        layout.addWidget(self.close_button)

    def set_title(self, title: str):
        """Update the header title."""
        self.title_label.setText(title)
