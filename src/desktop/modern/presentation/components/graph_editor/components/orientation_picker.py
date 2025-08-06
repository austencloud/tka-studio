"""
Modern Orientation Picker Component for TKA Graph Editor
========================================================

Modern 2025 design with large, easily pressable orientation buttons.
Features glassmorphism styling and direct orientation selection.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.domain.models import Orientation
from desktop.modern.presentation.components.graph_editor.components.turn_adjustment_controls.styling_helpers import (
    UNIFIED_BUTTON_HEIGHT,
    UNIFIED_BUTTON_SPACING,
    UNIFIED_BUTTON_WIDTH,
    apply_modern_panel_styling,
    apply_unified_button_styling,
)


logger = logging.getLogger(__name__)


class OrientationPickerWidget(QWidget):
    """
    Modern orientation picker with large, touch-friendly buttons.

    Features:
    - Large, easily pressable buttons for each orientation (IN, OUT, CLOCK, COUNTER)
    - Modern glassmorphism styling with color-themed gradients
    - Clear visual feedback for selected values
    - Compact design without excessive text labels
    """

    orientation_changed = pyqtSignal(
        str, object
    )  # arrow_color, orientation (Orientation enum)

    def __init__(self, arrow_color: str):
        super().__init__()
        self._arrow_color = arrow_color
        self._current_orientation = Orientation.IN

        # Use proper Orientation enum values
        self.orientations = [
            Orientation.IN,
            Orientation.OUT,
            Orientation.CLOCK,
            Orientation.COUNTER,
        ]

        # Button references for state management
        self._orientation_buttons = {}

        self._setup_ui()
        logger.debug(f"OrientationPickerWidget initialized for {arrow_color}")

    def _setup_ui(self):
        """Setup the modern orientation picker UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        # Create orientation panel with modern styling
        orientation_panel = self._create_orientation_panel()
        layout.addWidget(orientation_panel)

    def _create_orientation_panel(self) -> QGroupBox:
        """Create the orientation selection panel"""
        panel = QGroupBox(f"{self._arrow_color.title()} Orientation")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)

        # Current orientation display
        self._orientation_display = self._create_orientation_display()
        layout.addWidget(self._orientation_display)

        # Orientation selection buttons
        buttons_widget = self._create_orientation_buttons()
        layout.addWidget(buttons_widget)

        # Apply unified modern styling
        apply_modern_panel_styling(panel, self._arrow_color)

        return panel

    def _create_orientation_display(self) -> QLabel:
        """Create the current orientation display label"""
        orientation_label = QLabel(self._current_orientation.value.upper())
        orientation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Use same styling as dual orientation picker
        border_color = "#0066cc" if self._arrow_color == "blue" else "#cc0000"
        text_color = "#0066cc" if self._arrow_color == "blue" else "#cc0000"

        orientation_label.setStyleSheet(
            f"""
            QLabel {{
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid {border_color};
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
                font-size: 16px;
                color: {text_color};
                min-height: 30px;
            }}
        """
        )

        return orientation_label

    def _create_orientation_buttons(self) -> QWidget:
        """Create the orientation selection buttons with modern styling"""
        buttons_widget = QWidget()
        buttons_layout = QGridLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(UNIFIED_BUTTON_SPACING)

        # Create buttons in 2x2 grid for better touch accessibility
        for i, orientation in enumerate(self.orientations):
            row = i // 2
            col = i % 2

            btn = QPushButton(orientation.value.upper())
            btn.setCheckable(True)
            btn.setFixedSize(
                UNIFIED_BUTTON_WIDTH, UNIFIED_BUTTON_HEIGHT
            )  # Use unified sizing
            btn.clicked.connect(
                lambda _, ori=orientation: self._select_orientation(ori)
            )

            # Apply unified button styling
            apply_unified_button_styling(btn, self._arrow_color, "orientation")

            buttons_layout.addWidget(btn, row, col)
            self._orientation_buttons[orientation] = btn

        # Set initial selection
        self._update_button_selection()

        return buttons_widget

    def _select_orientation(self, orientation: Orientation):
        """Handle orientation selection"""
        self._set_orientation(orientation)

    def _set_orientation(self, orientation: Orientation):
        """Set the current orientation and update UI"""
        self._current_orientation = orientation
        self._orientation_display.setText(orientation.value.upper())
        self._update_button_selection()
        self.orientation_changed.emit(self._arrow_color, orientation)
        logger.debug(f"{self._arrow_color} orientation set to: {orientation.value}")

    def _update_button_selection(self):
        """Update button selection states"""
        for ori, btn in self._orientation_buttons.items():
            btn.setChecked(ori == self._current_orientation)

    def get_current_orientation(self) -> Orientation:
        """Get the current orientation"""
        return self._current_orientation

    def set_orientation(self, orientation: Orientation | str):
        """Set orientation programmatically (accepts Orientation enum or string)"""
        if isinstance(orientation, str):
            # Convert string to Orientation enum
            for ori in self.orientations:
                if ori.value.upper() == orientation.upper():
                    self._set_orientation(ori)
                    return
        elif isinstance(orientation, Orientation):
            self._set_orientation(orientation)

    def get_orientation(self) -> str:
        """Get current orientation as string"""
        return self._current_orientation.value
