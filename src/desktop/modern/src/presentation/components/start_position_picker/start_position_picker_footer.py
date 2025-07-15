"""
Start Position Picker Footer Component

Handles the footer section with variations button.
Extracted from the main StartPositionPicker for better maintainability.
"""

import logging
from enum import Enum

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget

logger = logging.getLogger(__name__)


class PickerMode(Enum):
    """Picker display modes."""

    BASIC = "basic"
    ADVANCED = "advanced"
    AUTO = "auto"


class StartPositionPickerFooter(QWidget):
    """
    Footer component for start position picker.

    Responsibilities:
    - Variations button display and interaction
    - Back button display and interaction
    - Mode-based visibility control
    - Footer layout management
    """

    show_variations_requested = pyqtSignal()
    back_to_basic_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # UI components
        self.variations_button = None
        self.back_button = None

        self._setup_ui()
        logger.debug("StartPositionPickerFooter initialized")

    def _setup_ui(self):
        """Setup the footer UI."""
        layout = QHBoxLayout(self)
        layout.addStretch()

        # Variations button (shown in basic mode)
        self.variations_button = QPushButton("✨ Show All Variations")
        self.variations_button.setObjectName("VariationsButton")
        self.variations_button.clicked.connect(self._on_variations_button_clicked)
        self.variations_button.setVisible(True)  # Visible by default (basic mode)

        # Apply styling
        self.variations_button.setStyleSheet(self._get_variations_button_styles())

        layout.addWidget(self.variations_button)

        # Back button (shown in advanced mode)
        self.back_button = QPushButton("← Back to Simple")
        self.back_button.setObjectName("BackButton")
        self.back_button.clicked.connect(self._on_back_button_clicked)
        self.back_button.setVisible(False)  # Hidden by default

        # Apply styling
        self.back_button.setStyleSheet(self._get_back_button_styles())

        layout.addWidget(self.back_button)
        layout.addStretch()

    def _get_variations_button_styles(self) -> str:
        """Get variations button styling - EXACT copy from original."""
        return """
            QPushButton#VariationsButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(99, 102, 241, 0.15),
                    stop:1 rgba(168, 85, 247, 0.1)
                );
                border: 2px solid rgba(255, 255, 255, 0.25);
                border-radius: 16px;
                color: #4c1d95;
                font-weight: 600;
                padding: 12px 24px;
                min-width: 160px;
            }
            
            QPushButton#VariationsButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(99, 102, 241, 0.25),
                    stop:1 rgba(168, 85, 247, 0.2)
                );
                border: 2px solid rgba(255, 255, 255, 0.4);
            }
        """

    def _get_back_button_styles(self) -> str:
        """Get back button styling - consistent with header back button."""
        return """
            QPushButton#BackButton {
                background: rgba(239, 68, 68, 0.9);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 14px;
                min-width: 160px;
            }

            QPushButton#BackButton:hover {
                background: rgba(239, 68, 68, 1.0);
            }
        """

    def update_for_mode(self, mode: PickerMode):
        """Update footer elements based on current mode."""
        if mode == PickerMode.ADVANCED:
            # In advanced mode: hide variations button, show back button
            self.variations_button.setVisible(False)
            self.back_button.setVisible(True)
        else:
            # In basic/auto mode: show variations button, hide back button
            self.variations_button.setVisible(True)
            self.back_button.setVisible(False)

    def _on_variations_button_clicked(self):
        """Handle variations button click."""
        logger.debug("Variations button clicked")
        self.show_variations_requested.emit()

    def _on_back_button_clicked(self):
        """Handle back button click."""
        logger.debug("Back button clicked")
        self.back_to_basic_requested.emit()
