"""
Dual Orientation Picker Component for TKA Graph Editor
======================================================

Provides dual blue/red orientation selection panels for start position configuration.
This component maintains the exact functionality of the legacy orientation picker
while following TKA clean architecture patterns.

Features:
- Dual blue/red orientation picker panels (50/50 layout)
- Four orientation options: IN, OUT, CLOCK, COUNTER
- Current orientation display with color-coded styling
- Real-time orientation updates and validation
- Signal-based communication for orientation changes

Architecture:
- Follows TKA presentation layer patterns
- Uses immutable domain models for data handling
- Maintains clean separation between UI and business logic
- Supports dependency injection for service integration
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.domain.models import BeatData, Orientation
from desktop.modern.presentation.components.graph_editor.components.turn_adjustment_controls.styling_helpers import (
    UNIFIED_BUTTON_HEIGHT,
    UNIFIED_BUTTON_WIDTH,
    apply_modern_panel_styling,
    apply_turn_button_styling,
)


logger = logging.getLogger(__name__)


class DualOrientationPicker(QWidget):
    """
    Dual blue/red orientation picker controls component.

    This component provides orientation selection controls for start positions,
    allowing users to set the initial orientation for both blue and red motions.


    Features:
    - Dual panels for blue and red orientation selection
    - Four orientation options per panel: IN, OUT, CLOCK, COUNTER
    - Current orientation display with visual feedback
    - Color-coded styling for visual distinction
    """

    # Signals for communication with parent components
    orientation_changed = pyqtSignal(
        str, object
    )  # color, orientation (Orientation enum)
    beat_data_updated = pyqtSignal(BeatData)  # updated beat data

    def __init__(self, parent=None):
        """
        Initialize the orientation picker controls.

        Args:
            parent: Parent widget (typically the graph editor)
        """
        super().__init__(parent)
        self._current_beat_data: BeatData | None = None

        # State tracking for orientations
        self._blue_orientation = Orientation.IN
        self._red_orientation = Orientation.IN

        # UI component references
        self._blue_orientation_label: QLabel | None = None
        self._red_orientation_label: QLabel | None = None

        self._setup_ui()
        logger.debug("DualOrientationPicker initialized")

    def _setup_ui(self):
        """Set up the dual orientation picker panels UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Blue orientation picker (left side)
        blue_panel = self._create_orientation_panel("blue")
        layout.addWidget(blue_panel, 1)

        # Red orientation picker (right side)
        red_panel = self._create_orientation_panel("red")
        layout.addWidget(red_panel, 1)

    def _create_orientation_panel(self, color: str) -> QWidget:
        """
        Create a single orientation picker panel for blue or red.

        Args:
            color: "blue" or "red" to determine styling and behavior

        Returns:
            QWidget: Configured orientation panel
        """
        panel = QGroupBox(f"{color.title()} Orientation")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)

        # Current orientation display
        orientation_label = self._create_orientation_display(color)
        layout.addWidget(orientation_label)

        # Orientation selection buttons
        buttons_widget = self._create_orientation_buttons(color)
        layout.addWidget(buttons_widget)

        # Apply color-specific styling
        self._apply_panel_styling(panel, color)

        # Store reference for updates
        if color == "blue":
            self._blue_orientation_label = orientation_label
        else:
            self._red_orientation_label = orientation_label

        return panel

    def _create_orientation_display(self, color: str) -> QLabel:
        """Create the current orientation display label."""
        orientation_label = QLabel(Orientation.IN.value.upper())
        orientation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        border_color = "#0066cc" if color == "blue" else "#cc0000"
        text_color = "#0066cc" if color == "blue" else "#cc0000"

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

    def _create_orientation_buttons(self, color: str) -> QWidget:
        """Create the orientation selection buttons."""
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(5)

        orientations = [
            Orientation.IN,
            Orientation.OUT,
            Orientation.CLOCK,
            Orientation.COUNTER,
        ]
        for orientation in orientations:
            btn = QPushButton(orientation.value.upper())
            btn.setFixedSize(
                UNIFIED_BUTTON_WIDTH, UNIFIED_BUTTON_HEIGHT
            )  # Use unified sizing
            btn.setCheckable(True)  # Enable checkable state for selection feedback
            btn.clicked.connect(
                lambda _, ori=orientation, c=color: self._set_orientation(c, ori)
            )

            # Apply modern button styling matching turn adjustment controls
            apply_turn_button_styling(btn, color, orientation.value)

            buttons_layout.addWidget(btn)

        return buttons_widget

    def _apply_panel_styling(self, panel: QGroupBox, color: str):
        """
        Apply modern glassmorphism styling to the orientation panel.

        Args:
            panel: The QGroupBox to style
            color: "blue" or "red" to determine color scheme
        """
        # Use the same modern styling as turn adjustment controls
        apply_modern_panel_styling(panel, color)

    def _set_orientation(self, color: str, orientation: Orientation):
        """
        Set orientation for the specified color.

        Args:
            color: "blue" or "red"
            orientation: Orientation enum value
        """
        if color == "blue":
            self._blue_orientation = orientation
            if self._blue_orientation_label:
                self._blue_orientation_label.setText(orientation.value.upper())
        else:
            self._red_orientation = orientation
            if self._red_orientation_label:
                self._red_orientation_label.setText(orientation.value.upper())

        self.orientation_changed.emit(color, orientation)
        logger.debug(f"{color.title()} orientation set to: {orientation.value}")

    def set_beat_data(self, beat_data: BeatData | None):
        """
        Set the current beat data and update the UI.

        Args:
            beat_data: Beat data to display (None to clear)
        """
        self._current_beat_data = beat_data

        if beat_data:
            # Extract current orientations from beat data
            if beat_data.pictograph_data.motions["blue"]:
                blue_ori = getattr(
                    beat_data.pictograph_data.motions["blue"], "start_ori", None
                )
                if blue_ori:
                    # Handle both enum and string values
                    if isinstance(blue_ori, Orientation):
                        self._blue_orientation = blue_ori
                    else:
                        # Convert string to enum
                        try:
                            self._blue_orientation = Orientation(str(blue_ori).lower())
                        except ValueError:
                            self._blue_orientation = Orientation.IN
                else:
                    self._blue_orientation = Orientation.IN
            else:
                self._blue_orientation = Orientation.IN

            if beat_data.pictograph_data.motions["red"]:
                red_ori = getattr(
                    beat_data.pictograph_data.motions["red"], "start_ori", None
                )
                if red_ori:
                    # Handle both enum and string values
                    if isinstance(red_ori, Orientation):
                        self._red_orientation = red_ori
                    else:
                        # Convert string to enum
                        try:
                            self._red_orientation = Orientation(str(red_ori).lower())
                        except ValueError:
                            self._red_orientation = Orientation.IN
                else:
                    self._red_orientation = Orientation.IN
            else:
                self._red_orientation = Orientation.IN
        else:
            # Reset to defaults
            self._blue_orientation = Orientation.IN
            self._red_orientation = Orientation.IN

        # Update UI displays
        self._update_orientation_displays()

    def _update_orientation_displays(self):
        """Update the orientation display labels"""
        if self._blue_orientation_label:
            self._blue_orientation_label.setText(self._blue_orientation.value.upper())
        if self._red_orientation_label:
            self._red_orientation_label.setText(self._red_orientation.value.upper())

    def get_blue_orientation(self) -> Orientation:
        """Get the current blue orientation."""
        return self._blue_orientation

    def get_red_orientation(self) -> Orientation:
        """Get the current red orientation."""
        return self._red_orientation

    def set_blue_orientation(self, orientation: Orientation):
        """Set the blue orientation programmatically."""
        self._set_orientation("blue", orientation)

    def set_red_orientation(self, orientation: Orientation):
        """Set the red orientation programmatically."""
        self._set_orientation("red", orientation)

    def reset_orientations(self):
        """Reset both orientations to default (IN)"""
        self._set_orientation("blue", Orientation.IN)
        self._set_orientation("red", Orientation.IN)

    def get_current_beat_data(self) -> BeatData | None:
        """Get the currently set beat data."""
        return self._current_beat_data
