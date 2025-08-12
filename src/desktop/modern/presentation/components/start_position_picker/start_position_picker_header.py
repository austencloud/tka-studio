"""
Start Position Picker Header Component

Handles the header section with mode controls and titles.
Extracted from the main StartPositionPicker for better maintainability.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QEasingCurve, QEvent, Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

# Import the legacy PyToggle for animated grid mode switching
from desktop.modern.domain.models.enums import PickerMode
from desktop.modern.presentation.components.ui.pytoggle import PyToggle


logger = logging.getLogger(__name__)


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
    grid_mode_changed = pyqtSignal(str)  # Emits the new grid mode ("diamond" or "box")

    def __init__(self, parent=None):
        super().__init__(parent)

        # UI components
        self.back_button = None
        self.grid_mode_toggle = None
        self.diamond_label = None
        self.box_label = None
        self.title_label = None
        self.subtitle_label = None

        self._setup_ui()
        logger.debug("StartPositionPickerHeader initialized")

    def _setup_ui(self):
        """Setup the header UI with PyToggle for grid mode switching."""
        layout = QVBoxLayout(self)
        layout.setSpacing(2)  # Minimal spacing between sections
        layout.setContentsMargins(0, 0, 0, 0)  # Remove all margins

        # Title section - match option picker margins exactly
        title_section = QWidget()
        title_layout = QVBoxLayout(title_section)
        title_layout.setSpacing(8)  # Match option picker spacing
        title_layout.setContentsMargins(
            16, 16, 16, 16
        )  # Match option picker margins exactly

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

        # Control and toggle bar - back button (left), diamond/box toggle (center), future controls (right)
        controls_toggle_section = QWidget()
        controls_toggle_layout = QHBoxLayout(controls_toggle_section)
        controls_toggle_layout.setSpacing(8)
        controls_toggle_layout.setContentsMargins(
            16, 8, 16, 8
        )  # Consistent side margins

        # Left: Back button (shown in advanced mode)
        self.back_button = QPushButton("← Back to Simple")
        self.back_button.setObjectName("BackButton")
        self.back_button.clicked.connect(self._on_back_button_clicked)
        self.back_button.setVisible(False)
        controls_toggle_layout.addWidget(self.back_button)

        # Center: Diamond/Box toggle
        toggle_container = QWidget()
        toggle_layout = QHBoxLayout(toggle_container)
        toggle_layout.setSpacing(8)
        toggle_layout.setContentsMargins(0, 0, 0, 0)

        # Create clickable labels (Diamond on left, Box on right)
        self.diamond_label = QLabel("Diamond")
        self.diamond_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        self.diamond_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.diamond_label.setObjectName("GridModeLabel")
        self.diamond_label.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.diamond_label.installEventFilter(self)

        # Create the PyToggle with proper legacy styling
        self.grid_mode_toggle = PyToggle(
            width=80,
            bg_color="#3B82F6",  # Blue for diamond (unchecked)
            active_color="#10B981",  # Green for box (checked)
            circle_color="#FFFFFF",  # White circle
            animation_curve=QEasingCurve.Type.OutCubic,
            change_bg_on_state=True,
        )
        self.grid_mode_toggle.stateChanged.connect(self._on_grid_mode_toggled)

        self.box_label = QLabel("Box")
        self.box_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        self.box_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.box_label.setObjectName("GridModeLabel")
        self.box_label.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.box_label.installEventFilter(self)

        # Add toggle elements to container
        toggle_layout.addWidget(self.diamond_label)
        toggle_layout.addWidget(self.grid_mode_toggle)
        toggle_layout.addWidget(self.box_label)

        # Set wider label width for "Diamond" visibility
        self.diamond_label.setFixedWidth(80)  # Wider for full "DIAMOND" text
        self.box_label.setFixedWidth(50)  # Sufficient for "BOX"

        # Add toggle container to center with stretch on both sides
        controls_toggle_layout.addStretch(1)  # Push toggle to center
        controls_toggle_layout.addWidget(toggle_container)
        controls_toggle_layout.addStretch(1)  # Keep toggle centered

        # Right: Future controls placeholder (empty for now)
        # Could add export button, settings, etc. here later

        layout.addWidget(controls_toggle_section)

        # Update label styles based on initial state (Diamond is default)
        self._update_label_styles()

        # Apply styling
        self.setStyleSheet(self._get_header_styles())

    def _get_header_styles(self) -> str:
        """Get header styling - Updated for cleaner design."""
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

            QLabel#GridModeLabel {
                color: rgba(0, 0, 0, 0.8);
                background: transparent;
                font-weight: 500;
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
        """

    def update_for_mode(self, mode: PickerMode, grid_mode: str):
        """Update header elements based on current mode."""
        if mode == PickerMode.ADVANCED:
            self.title_label.setText("All Start Positions")
            self.subtitle_label.setText("Choose from 16 available starting positions")
            self.back_button.setVisible(True)  # Show back button on left
        else:
            self.title_label.setText("Choose Your Start Position")
            self.subtitle_label.setText(
                "Select a starting position to begin crafting your sequence"
            )
            self.back_button.setVisible(False)  # Hide back button, leave space empty

        # Update grid mode toggle
        self.set_grid_mode(grid_mode)

    def set_grid_mode(self, grid_mode: str):
        """Set grid mode toggle state and update label styles."""
        is_box_mode = grid_mode == "box"

        # Block signals temporarily to prevent recursion
        self.grid_mode_toggle.blockSignals(True)
        self.grid_mode_toggle.setChecked(is_box_mode)
        self.grid_mode_toggle.blockSignals(False)

        # Update label styles to reflect the current state
        self._update_label_styles()

    def _on_back_button_clicked(self):
        """Handle back button click."""
        logger.debug("Back button clicked")
        self.back_to_basic_requested.emit()

    def _on_grid_mode_toggled(self, checked):
        """Handle grid mode toggle change."""
        # Get the new mode
        new_mode = "box" if checked else "diamond"

        # Update label styles to reflect current state
        self._update_label_styles()

        # Notify about the change
        self.grid_mode_changed.emit(new_mode)

    def _update_label_styles(self):
        """Update label styles based on current toggle state."""
        is_box_mode = self.grid_mode_toggle.isChecked()

        if is_box_mode:
            # Box mode active - emphasize box label
            self.diamond_label.setStyleSheet(
                """
                QLabel {
                    color: #6B7280;
                    font-weight: normal;
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    letter-spacing: 0.5px;
                    text-transform: uppercase;
                }
                QLabel:hover {
                    color: #4B5563;
                    background-color: rgba(75, 85, 99, 0.1);
                }
            """
            )
            self.box_label.setStyleSheet(
                """
                QLabel {
                    color: #10B981;
                    font-weight: bold;
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    letter-spacing: 0.8px;
                    text-transform: uppercase;
                }
                QLabel:hover {
                    color: #059669;
                    background-color: rgba(5, 150, 105, 0.1);
                }
            """
            )
        else:
            # Diamond mode active - emphasize diamond label
            self.diamond_label.setStyleSheet(
                """
                QLabel {
                    color: #3B82F6;
                    font-weight: bold;
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    letter-spacing: 0.8px;
                    text-transform: uppercase;
                }
                QLabel:hover {
                    color: #2563EB;
                    background-color: rgba(37, 99, 235, 0.1);
                }
            """
            )
            self.box_label.setStyleSheet(
                """
                QLabel {
                    color: #6B7280;
                    font-weight: normal;
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    letter-spacing: 0.5px;
                    text-transform: uppercase;
                }
                QLabel:hover {
                    color: #4B5563;
                    background-color: rgba(75, 85, 99, 0.1);
                }
            """
            )

    def eventFilter(self, obj, event):
        """Handle click events on labels to toggle the state."""
        if event.type() == QEvent.Type.MouseButtonPress:
            if obj == self.diamond_label and self.grid_mode_toggle.isChecked():
                # Click diamond label when in box mode - switch to diamond
                self.grid_mode_toggle.setChecked(False)
                return True
            if obj == self.box_label and not self.grid_mode_toggle.isChecked():
                # Click box label when in diamond mode - switch to box
                self.grid_mode_toggle.setChecked(True)
                return True

        return super().eventFilter(obj, event)
