"""
Start Position Picker Header Component

Handles the header section with mode controls and titles.
Extracted from the main StartPositionPicker for better maintainability.
"""

import logging
from enum import Enum

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

logger = logging.getLogger(__name__)


class PickerMode(Enum):
    """Picker display modes."""

    BASIC = "basic"
    ADVANCED = "advanced"
    AUTO = "auto"


class StartPositionPickerHeader(QWidget):
    """
    Header component for start position picker.

    Responsibilities:
    - Mode control buttons (back button, grid mode toggle)
    - Title and subtitle display
    - Mode-based header updates
    - Header layout management
    """

    back_to_basic_requested = pyqtSignal()
    grid_mode_toggle_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # UI components
        self.back_button = None
        self.mode_toggle_button = None
        self.title_label = None
        self.subtitle_label = None

        self._setup_ui()
        logger.debug("StartPositionPickerHeader initialized")

    def _setup_ui(self):
        """Setup the header UI - EXACT copy from original."""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Control bar
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)

        # Back button (shown in advanced mode)
        self.back_button = QPushButton("← Back to Simple")
        self.back_button.setObjectName("BackButton")
        self.back_button.clicked.connect(self._on_back_button_clicked)
        self.back_button.setVisible(False)
        controls_layout.addWidget(self.back_button)

        controls_layout.addStretch()

        # Mode toggle (grid mode switcher)
        self.mode_toggle_button = QPushButton("⚡ Diamond Grid")
        self.mode_toggle_button.setObjectName("ModeToggleButton")
        self.mode_toggle_button.clicked.connect(self._on_mode_toggle_clicked)
        controls_layout.addWidget(self.mode_toggle_button)

        layout.addWidget(controls)

        # Title section
        title_section = QWidget()
        title_layout = QVBoxLayout(title_section)
        title_layout.setSpacing(8)
        title_layout.setContentsMargins(16, 16, 16, 16)

        # Title
        self.title_label = QLabel("Choose Your Start Position")
        self.title_label.setFont(QFont("Monotype Corsiva", 24, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("UnifiedTitle")
        title_layout.addWidget(self.title_label)

        # Subtitle
        self.subtitle_label = QLabel(
            "Select a starting position to begin crafting your sequence"
        )
        self.subtitle_label.setFont(QFont("Monotype Corsiva", 14))
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setObjectName("UnifiedSubtitle")
        title_layout.addWidget(self.subtitle_label)

        title_section.setObjectName("TitleSection")
        layout.addWidget(title_section)

        # Apply styling - EXACT copy from original
        self.setStyleSheet(self._get_header_styles())

    def _get_header_styles(self) -> str:
        """Get header styling - EXACT copy from original."""
        return """
            QWidget#TitleSection {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 16px;
            }
            
            QLabel#UnifiedTitle {
                color: black;
                background: transparent;
                font-weight: 700;
            }
            
            QLabel#UnifiedSubtitle {
                color: black;
                background: transparent;
                font-weight: 400;
            }
            
            QPushButton#BackButton {
                background: rgba(239, 68, 68, 0.9);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 14px;
            }
            
            QPushButton#BackButton:hover {
                background: rgba(239, 68, 68, 1.0);
            }
            
            QPushButton#ModeToggleButton {
                background: rgba(59, 130, 246, 0.9);
                color: white;
                border: none;
                border-radius: 14px;
                padding: 6px 14px;
                font-weight: 600;
                font-size: 12px;
            }
            
            QPushButton#ModeToggleButton:hover {
                background: rgba(59, 130, 246, 1.0);
            }
        """

    def update_for_mode(self, mode: PickerMode, grid_mode: str):
        """Update header elements based on current mode - EXACT logic from original."""
        if mode == PickerMode.ADVANCED:
            self.title_label.setText("All Start Positions")
            self.subtitle_label.setText("Choose from 16 available starting positions")
            self.back_button.setVisible(True)
            self.mode_toggle_button.setVisible(True)
        else:
            self.title_label.setText("Choose Your Start Position")
            self.subtitle_label.setText(
                "Select a starting position to begin crafting your sequence"
            )
            self.back_button.setVisible(False)
            self.mode_toggle_button.setVisible(True)

        # Update grid mode button text
        self.set_grid_mode_button_text(grid_mode)

    def set_grid_mode_button_text(self, grid_mode: str):
        """Update grid mode button text - EXACT logic from original."""
        self.mode_toggle_button.setText(f"⚡ {grid_mode.title()} Grid")

    def _on_back_button_clicked(self):
        """Handle back button click."""
        logger.debug("Back button clicked")
        self.back_to_basic_requested.emit()

    def _on_mode_toggle_clicked(self):
        """Handle mode toggle button click."""
        logger.debug("Mode toggle button clicked")
        self.grid_mode_toggle_requested.emit()
