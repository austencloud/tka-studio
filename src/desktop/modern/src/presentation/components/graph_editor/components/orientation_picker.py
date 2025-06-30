"""
Modern Orientation Picker Component for TKA Graph Editor
========================================================

Modern 2025 design with large, easily pressable orientation buttons.
Features glassmorphism styling and direct orientation selection.
"""

import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QGridLayout,
)

from domain.models.core_models import Orientation

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

        # Apply modern styling
        self._apply_panel_styling(panel)

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
        buttons_layout.setSpacing(6)

        # Create buttons in 2x2 grid for better touch accessibility
        for i, orientation in enumerate(self.orientations):
            row = i // 2
            col = i % 2

            btn = QPushButton(orientation.value.upper())
            btn.setCheckable(True)
            btn.setFixedSize(80, 50)  # Larger, more touch-friendly size
            btn.clicked.connect(
                lambda _, ori=orientation: self._select_orientation(ori)
            )

            # Apply modern button styling
            self._apply_button_styling(btn)

            buttons_layout.addWidget(btn, row, col)
            self._orientation_buttons[orientation] = btn

        # Set initial selection
        self._update_button_selection()

        return buttons_widget

    def _apply_panel_styling(self, panel: QGroupBox):
        """Apply modern glassmorphism styling to the panel"""
        if self._arrow_color == "blue":
            gradient_start = "rgba(74, 144, 226, 0.3)"
            gradient_end = "rgba(74, 144, 226, 0.1)"
            border_color = "rgba(74, 144, 226, 0.4)"
        else:
            gradient_start = "rgba(231, 76, 60, 0.3)"
            gradient_end = "rgba(231, 76, 60, 0.1)"
            border_color = "rgba(231, 76, 60, 0.4)"

        panel.setStyleSheet(
            f"""
            QGroupBox {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {gradient_start},
                    stop:1 {gradient_end});
                border: 2px solid {border_color};
                border-radius: 12px;
                margin-top: 0px;
                padding-top: 8px;
                font-weight: bold;
                font-size: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
            """
        )

    def _apply_button_styling(self, button: QPushButton):
        """Apply modern button styling matching turn adjustment controls"""
        if self._arrow_color == "blue":
            base_color = "74, 144, 226"
            hover_color = "94, 164, 246"
        else:
            base_color = "231, 76, 60"
            hover_color = "251, 96, 80"

        button.setStyleSheet(
            f"""
            QPushButton {{
                background: rgba({base_color}, 0.2);
                border: 2px solid rgba({base_color}, 0.4);
                border-radius: 8px;
                color: rgba(255, 255, 255, 0.9);
                font-size: 12px;
                font-weight: bold;
                padding: 4px;
            }}
            QPushButton:hover {{
                background: rgba({hover_color}, 0.3);
                border-color: rgba({hover_color}, 0.6);
                color: rgba(255, 255, 255, 1.0);
            }}
            QPushButton:pressed {{
                background: rgba({base_color}, 0.4);
                border-color: rgba({base_color}, 0.8);
            }}
            QPushButton:checked {{
                background: rgba({base_color}, 0.6);
                border-color: rgba({base_color}, 0.9);
                color: rgba(255, 255, 255, 1.0);
                font-weight: bold;
            }}
            """
        )

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

    def set_orientation(self, orientation: Orientation):
        """Set orientation programmatically"""
        self._set_orientation(orientation)

    def set_orientation(self, orientation: str):
        """Set orientation from external source"""
        if orientation in self.orientations:
            self._set_orientation(orientation)

    def get_orientation(self) -> str:
        """Get current orientation"""
        return self._current_orientation
