"""
Settings dialog action buttons component.

Contains the Reset, Apply, and OK buttons for the settings dialog.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton


class SettingsActionButtons(QFrame):
    """Action buttons component for the settings dialog."""

    reset_requested = pyqtSignal()
    apply_requested = pyqtSignal()
    ok_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("button_frame")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the action buttons UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.addStretch()

        # Reset button
        self.reset_button = QPushButton("Reset to Defaults")
        self.reset_button.setObjectName("secondary_button")
        self.reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_button.clicked.connect(self.reset_requested.emit)

        # Apply button
        self.apply_button = QPushButton("Apply")
        self.apply_button.setObjectName("secondary_button")
        self.apply_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_button.clicked.connect(self.apply_requested.emit)

        # OK button (primary)
        self.ok_button = QPushButton("OK")
        self.ok_button.setObjectName("primary_button")
        self.ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ok_button.clicked.connect(self.ok_requested.emit)

        layout.addWidget(self.reset_button)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.ok_button)

    def set_apply_enabled(self, enabled: bool):
        """Enable or disable the apply button."""
        self.apply_button.setEnabled(enabled)

    def set_reset_enabled(self, enabled: bool):
        """Enable or disable the reset button."""
        self.reset_button.setEnabled(enabled)
