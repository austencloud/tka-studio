"""
Modern Turn Adjustment Controls Component for TKA Graph Editor
=============================================================

Modern 2025 design with large, easily pressable turn value buttons.
Features glassmorphism styling and direct turn value selection.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QWidget

from desktop.modern.domain.models import BeatData, MotionData
from desktop.modern.presentation.components.graph_editor.components.turn_adjustment_controls.current_turn_display import (
    CurrentTurnDisplay,
)
from desktop.modern.presentation.components.graph_editor.components.turn_adjustment_controls.styling_helpers import (
    apply_modern_panel_styling,
)
from desktop.modern.presentation.components.graph_editor.components.turn_adjustment_controls.turn_value_button_grid import (
    TurnValueButtonGrid,
)


logger = logging.getLogger(__name__)


class TurnAdjustmentControls(QWidget):
    """
    Modern turn adjustment controls with direct turn value selection.

    Features:
    - Large, easily pressable buttons for each turn value (fl, 0, 0.5, 1, 1.5, 2, 2.5, 3)
    - Modern glassmorphism styling with color-themed gradients
    - Clear visual feedback for selected values
    - Optimized space utilization with two-row layout
    """

    # Signals for communication with parent components
    turn_amount_changed = pyqtSignal(str, float)  # color, new_amount
    rotation_direction_changed = pyqtSignal(
        str, str
    )  # color, direction (for backward compatibility)
    beat_data_updated = pyqtSignal(BeatData)  # updated beat data

    def __init__(self, parent=None):
        """Initialize the modern turn adjustment controls."""
        super().__init__(parent)
        self._current_beat_data: BeatData | None = None

        # Available turn values (fl = float = 0.25)
        self._turn_values = ["fl", "0", "0.5", "1", "1.5", "2", "2.5", "3"]
        self._turn_value_map = {
            "fl": 0.25,  # float = quarter turn
            "0": 0.0,
            "0.5": 0.5,
            "1": 1.0,
            "1.5": 1.5,
            "2": 2.0,
            "2.5": 2.5,
            "3": 3.0,
        }

        # State tracking for selected turn amounts
        self._blue_turn_amount = 0.0
        self._red_turn_amount = 0.0

        # UI component references
        self._blue_current_display: CurrentTurnDisplay | None = None
        self._red_current_display: CurrentTurnDisplay | None = None
        self._blue_turn_grid: TurnValueButtonGrid | None = None
        self._red_turn_grid: TurnValueButtonGrid | None = None

        self._setup_ui()
        logger.debug("Modern TurnAdjustmentControls initialized")

    def _setup_ui(self):
        """Set up the modern dual turn adjustment panels UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        blue_panel = self._create_modern_turn_panel("blue")
        red_panel = self._create_modern_turn_panel("red")

        layout.addWidget(blue_panel, 1)
        layout.addWidget(red_panel, 1)

        # Apply overall styling
        self.setStyleSheet("TurnAdjustmentControls { background: transparent; }")

    def _create_modern_turn_panel(self, color: str) -> QWidget:
        """Create a modern turn adjustment panel with direct value selection."""
        panel = QGroupBox()
        panel.setTitle("")  # No title, we'll add our own
        vbox = QVBoxLayout(panel)
        vbox.setContentsMargins(12, 12, 12, 12)
        vbox.setSpacing(10)

        # Current turn display at the top
        current_value = self._find_turn_value_string(
            self._blue_turn_amount if color == "blue" else self._red_turn_amount
        )
        current_display = CurrentTurnDisplay(color, current_value)
        vbox.addWidget(current_display)

        # Turn value buttons in a grid
        button_grid = TurnValueButtonGrid(
            color,
            self._turn_values,
            self._turn_value_map,
            lambda val, c=color: self._on_turn_value_selected(c, val),
        )
        vbox.addWidget(button_grid)

        # Apply modern styling
        apply_modern_panel_styling(panel, color)

        # Store references
        if color == "blue":
            self._blue_current_display = current_display
            self._blue_turn_grid = button_grid
        else:
            self._red_current_display = current_display
            self._red_turn_grid = button_grid

        return panel

    def _on_turn_value_selected(self, color: str, turn_value: str):
        """Handle turn value button selection."""
        # Get the numeric value
        turn_amount = self._turn_value_map[turn_value]

        # Update internal state
        if color == "blue":
            self._blue_turn_amount = turn_amount
            self._blue_current_display.set_value(turn_value)
            self._blue_turn_grid.set_selected(turn_value)
        else:
            self._red_turn_amount = turn_amount
            self._red_current_display.set_value(turn_value)
            self._red_turn_grid.set_selected(turn_value)

        # Update beat data if available
        if self._current_beat_data:
            self._update_beat_with_turn_changes()

        # Emit signal
        self.turn_amount_changed.emit(color, turn_amount)
        logger.debug(
            f"{color.title()} turn value selected: {turn_value} ({turn_amount})"
        )

    def _update_beat_with_turn_changes(self):
        """Update the current beat data with new turn values"""
        if not self._current_beat_data:
            return

        try:
            updated_beat = self._current_beat_data

            # Update blue motion if it exists
            if (
                updated_beat.pictograph_data.motions["blue"]
                and self._blue_turn_amount != 0
            ):
                blue_motion = MotionData(
                    motion_type=updated_beat.pictograph_data.motions[
                        "blue"
                    ].motion_type,
                    prop_rot_dir=updated_beat.pictograph_data.motions[
                        "blue"
                    ].prop_rot_dir,
                    start_loc=updated_beat.pictograph_data.motions["blue"].start_loc,
                    end_loc=updated_beat.pictograph_data.motions["blue"].end_loc,
                    turns=self._blue_turn_amount,
                    start_ori=updated_beat.pictograph_data.motions["blue"].start_ori,
                    end_ori=updated_beat.pictograph_data.motions["blue"].end_ori,
                )
                updated_beat.pictograph_data.motions["blue"] = blue_motion

            # Update red motion if it exists
            if (
                updated_beat.pictograph_data.motions["red"]
                and self._red_turn_amount != 0
            ):
                red_motion = MotionData(
                    motion_type=updated_beat.pictograph_data.motions["red"].motion_type,
                    prop_rot_dir=updated_beat.pictograph_data.motions[
                        "red"
                    ].prop_rot_dir,
                    start_loc=updated_beat.pictograph_data.motions["red"].start_loc,
                    end_loc=updated_beat.pictograph_data.motions["red"].end_loc,
                    turns=self._red_turn_amount,
                    start_ori=updated_beat.pictograph_data.motions["red"].start_ori,
                    end_ori=updated_beat.pictograph_data.motions["red"].end_ori,
                )
                updated_beat.pictograph_data.motions["red"] = red_motion

            self._current_beat_data = updated_beat
            self.beat_data_updated.emit(updated_beat)
            logger.debug("Beat data updated with turn changes")

        except Exception as e:
            logger.exception(f"Error updating beat with turn changes: {e}")

    def set_beat_data(self, beat_data: BeatData | None):
        """Set the current beat data and update the UI."""
        self._current_beat_data = beat_data

        if beat_data:
            # Extract current turn amounts from beat data
            if beat_data.pictograph_data.motions["blue"]:
                self._blue_turn_amount = getattr(
                    beat_data.pictograph_data.motions["blue"], "turns", 0.0
                )
            else:
                self._blue_turn_amount = 0.0

            if beat_data.pictograph_data.motions["red"]:
                self._red_turn_amount = getattr(
                    beat_data.pictograph_data.motions["red"], "turns", 0.0
                )
            else:
                self._red_turn_amount = 0.0
        else:
            # Reset to defaults
            self._blue_turn_amount = 0.0
            self._red_turn_amount = 0.0

        # Update UI displays
        self._update_turn_displays()

    def _update_turn_displays(self):
        """Update the turn amount displays and button states"""
        blue_value = self._find_turn_value_string(self._blue_turn_amount)
        self._blue_current_display.set_value(blue_value)
        self._blue_turn_grid.set_selected(blue_value)

        red_value = self._find_turn_value_string(self._red_turn_amount)
        self._red_current_display.set_value(red_value)
        self._red_turn_grid.set_selected(red_value)

    def _find_turn_value_string(self, turn_amount: float) -> str:
        """Find the string representation for a turn amount."""
        for value_str, amount in self._turn_value_map.items():
            if abs(amount - turn_amount) < 0.01:  # Small tolerance for float comparison
                return value_str
        return "0"  # Default fallback
