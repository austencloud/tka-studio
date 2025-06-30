"""
Turn Adjustment Controls Component for TKA Graph Editor
======================================================

Dual blue/red turn adjustment panels with 1.0/0.5 increment controls,
rotation direction selection, and real-time value display.
"""

import logging
from typing import Optional

from domain.models.core_models import BeatData, MotionData
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QPushButton,
)

logger = logging.getLogger(__name__)


class TurnAdjustmentControls(QWidget):
    """
    Dual blue/red turn adjustment controls with 1.0/0.5 increments.
    Provides rotation direction selection and real-time value display.
    """

    # Signals for communication with parent components
    turn_amount_changed = pyqtSignal(str, float)  # color, new_amount
    rotation_direction_changed = pyqtSignal(str, str)  # color, direction
    beat_data_updated = pyqtSignal(BeatData)  # updated beat data

    def __init__(self, parent=None):
        """Initialize the turn adjustment controls."""
        super().__init__(parent)
        self._current_beat_data: Optional[BeatData] = None

        # State tracking for turn amounts
        self._blue_turn_amount = 0.0
        self._red_turn_amount = 0.0

        # UI component references
        self._blue_cw_btn: Optional[QPushButton] = None
        self._blue_ccw_btn: Optional[QPushButton] = None
        self._blue_amount_label: Optional[QLabel] = None
        self._red_cw_btn: Optional[QPushButton] = None
        self._red_ccw_btn: Optional[QPushButton] = None
        self._red_amount_label: Optional[QLabel] = None

        self._setup_ui()
        logger.debug("TurnAdjustmentControls initialized")

    def _setup_ui(self):
        """Set up the dual turn adjustment panels UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        blue_panel = self._create_turn_panel("blue")
        layout.addWidget(blue_panel, 1)

        red_panel = self._create_turn_panel("red")
        layout.addWidget(red_panel, 1)

    def _create_turn_panel(self, color: str) -> QWidget:
        """Create a single turn adjustment panel for blue or red."""
        panel = QGroupBox(f"{color.title()} Turns")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)

        direction_widget = self._create_direction_controls(color)
        layout.addWidget(direction_widget)

        amount_widget = self._create_amount_controls(color)
        layout.addWidget(amount_widget)

        self._apply_panel_styling(panel, color)

        return panel

    def _create_direction_controls(self, color: str) -> QWidget:
        """Create rotation direction control buttons."""
        direction_widget = QWidget()
        direction_layout = QHBoxLayout(direction_widget)
        direction_layout.setContentsMargins(0, 0, 0, 0)
        direction_layout.setSpacing(5)

        cw_btn = QPushButton("⟲ CW")
        cw_btn.setCheckable(True)
        cw_btn.setFixedSize(60, 30)
        cw_btn.clicked.connect(lambda: self._set_rotation_direction(color, "CLOCKWISE"))

        ccw_btn = QPushButton("⟳ CCW")
        ccw_btn.setCheckable(True)
        ccw_btn.setFixedSize(60, 30)
        ccw_btn.clicked.connect(
            lambda: self._set_rotation_direction(color, "COUNTER_CLOCKWISE")
        )

        direction_layout.addWidget(cw_btn)
        direction_layout.addWidget(ccw_btn)

        if color == "blue":
            self._blue_cw_btn = cw_btn
            self._blue_ccw_btn = ccw_btn
        else:
            self._red_cw_btn = cw_btn
            self._red_ccw_btn = ccw_btn

        return direction_widget

    def _create_amount_controls(self, color: str) -> QWidget:
        """Create turn amount adjustment controls with 1.0 and 0.5 increments."""
        amount_widget = QWidget()
        amount_layout = QVBoxLayout(amount_widget)
        amount_layout.setContentsMargins(0, 0, 0, 0)
        amount_layout.setSpacing(5)

        full_turn_widget = QWidget()
        full_turn_layout = QHBoxLayout(full_turn_widget)
        full_turn_layout.setContentsMargins(0, 0, 0, 0)
        full_turn_layout.setSpacing(3)

        dec_full_btn = QPushButton("-1")
        dec_full_btn.setFixedSize(35, 25)
        dec_full_btn.clicked.connect(lambda: self._adjust_turn_amount(color, -1.0))
        amount_label = QLabel("0")
        amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amount_label.setStyleSheet(
            "QLabel { background: rgba(255, 255, 255, 0.2); border: 1px solid rgba(255, 255, 255, 0.4); "
            "border-radius: 4px; padding: 6px 12px; font-weight: bold; min-width: 50px; "
            "color: rgba(255, 255, 255, 0.95); }"
        )

        inc_full_btn = QPushButton("+1")
        inc_full_btn.setFixedSize(35, 25)
        inc_full_btn.clicked.connect(lambda: self._adjust_turn_amount(color, 1.0))

        full_turn_layout.addWidget(dec_full_btn)
        full_turn_layout.addWidget(amount_label)
        full_turn_layout.addWidget(inc_full_btn)
        half_turn_widget = QWidget()
        half_turn_layout = QHBoxLayout(half_turn_widget)
        half_turn_layout.setContentsMargins(0, 0, 0, 0)
        half_turn_layout.setSpacing(3)

        dec_half_btn = QPushButton("-0.5")
        dec_half_btn.setFixedSize(35, 25)
        dec_half_btn.clicked.connect(lambda: self._adjust_turn_amount(color, -0.5))

        half_turn_layout.addStretch()

        inc_half_btn = QPushButton("+0.5")
        inc_half_btn.setFixedSize(35, 25)
        inc_half_btn.clicked.connect(lambda: self._adjust_turn_amount(color, 0.5))

        half_turn_layout.addWidget(dec_half_btn)
        half_turn_layout.addStretch()
        half_turn_layout.addWidget(inc_half_btn)

        amount_layout.addWidget(full_turn_widget)
        amount_layout.addWidget(half_turn_widget)

        if color == "blue":
            self._blue_amount_label = amount_label
        else:
            self._red_amount_label = amount_label

        return amount_widget

    def _apply_panel_styling(self, panel: QGroupBox, color: str):
        """Apply color-specific styling to the turn panel."""
        if color == "blue":
            border_color = "#0066cc"
            bg_color = "rgba(0, 102, 204, 0.1)"
        else:
            border_color = "#cc0000"
            bg_color = "rgba(204, 0, 0, 0.1)"

        panel.setStyleSheet(
            f"QGroupBox {{ background-color: {bg_color}; border: 2px solid {border_color}; "
            f"border-radius: 8px; font-weight: bold; color: {border_color}; }} "
            f"QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 8px 0 8px; "
            f"background-color: rgba(255, 255, 255, 0.9); }}"
        )

    def _set_rotation_direction(self, color: str, direction: str):
        """Set rotation direction for the specified color."""
        if color == "blue" and self._blue_cw_btn and self._blue_ccw_btn:
            if direction == "CLOCKWISE":
                self._blue_cw_btn.setChecked(True)
                self._blue_ccw_btn.setChecked(False)
            else:
                self._blue_cw_btn.setChecked(False)
                self._blue_ccw_btn.setChecked(True)
        elif color == "red" and self._red_cw_btn and self._red_ccw_btn:
            if direction == "CLOCKWISE":
                self._red_cw_btn.setChecked(True)
                self._red_ccw_btn.setChecked(False)
            else:
                self._red_cw_btn.setChecked(False)
                self._red_ccw_btn.setChecked(True)

        self.rotation_direction_changed.emit(color, direction)
        logger.debug(f"{color.title()} rotation direction set to: {direction}")

    def _adjust_turn_amount(self, color: str, delta: float):
        """Adjust turn amount by the specified delta."""
        if color == "blue":
            self._blue_turn_amount = max(0, self._blue_turn_amount + delta)
            new_amount = self._blue_turn_amount
            label = self._blue_amount_label
        else:
            self._red_turn_amount = max(0, self._red_turn_amount + delta)
            new_amount = self._red_turn_amount
            label = self._red_amount_label

        # Update display
        if label:
            if new_amount == int(new_amount):
                label.setText(str(int(new_amount)))
            else:
                label.setText(f"{new_amount:.1f}")

        # Update beat data if available
        if self._current_beat_data:
            self._update_beat_with_turn_changes()

        self.turn_amount_changed.emit(color, new_amount)
        logger.debug(
            f"{color.title()} turn amount adjusted by {delta} to: {new_amount}"
        )

    def _update_beat_with_turn_changes(self):
        """Update the current beat data with new turn values"""
        if not self._current_beat_data:
            return

        try:
            updated_beat = self._current_beat_data

            # Update blue motion if it exists
            if updated_beat.blue_motion and self._blue_turn_amount > 0:
                blue_motion = MotionData(
                    motion_type=updated_beat.blue_motion.motion_type,
                    prop_rot_dir=updated_beat.blue_motion.prop_rot_dir,
                    start_loc=updated_beat.blue_motion.start_loc,
                    end_loc=updated_beat.blue_motion.end_loc,
                    turns=self._blue_turn_amount,
                    start_ori=updated_beat.blue_motion.start_ori,
                    end_ori=updated_beat.blue_motion.end_ori,
                )
                updated_beat = updated_beat.update(blue_motion=blue_motion)

            # Update red motion if it exists
            if updated_beat.red_motion and self._red_turn_amount > 0:
                red_motion = MotionData(
                    motion_type=updated_beat.red_motion.motion_type,
                    prop_rot_dir=updated_beat.red_motion.prop_rot_dir,
                    start_loc=updated_beat.red_motion.start_loc,
                    end_loc=updated_beat.red_motion.end_loc,
                    turns=self._red_turn_amount,
                    start_ori=updated_beat.red_motion.start_ori,
                    end_ori=updated_beat.red_motion.end_ori,
                )
                updated_beat = updated_beat.update(red_motion=red_motion)

            self._current_beat_data = updated_beat
            self.beat_data_updated.emit(updated_beat)
            logger.debug("Beat data updated with turn changes")

        except Exception as e:
            logger.error(f"Error updating beat with turn changes: {e}")

    def set_beat_data(self, beat_data: Optional[BeatData]):
        """Set the current beat data and update the UI."""
        self._current_beat_data = beat_data

        if beat_data:
            # Extract current turn amounts from beat data
            if beat_data.blue_motion:
                self._blue_turn_amount = getattr(beat_data.blue_motion, "turns", 0.0)
            else:
                self._blue_turn_amount = 0.0

            if beat_data.red_motion:
                self._red_turn_amount = getattr(beat_data.red_motion, "turns", 0.0)
            else:
                self._red_turn_amount = 0.0
        else:
            # Reset to defaults
            self._blue_turn_amount = 0.0
            self._red_turn_amount = 0.0

        # Update UI displays
        self._update_turn_displays()
        self._reset_direction_buttons()

    def _update_turn_displays(self):
        """Update the turn amount displays"""
        for amount, label in [
            (self._blue_turn_amount, self._blue_amount_label),
            (self._red_turn_amount, self._red_amount_label),
        ]:
            if label:
                if amount == int(amount):
                    label.setText(str(int(amount)))
                else:
                    label.setText(f"{amount:.1f}")

    def _reset_direction_buttons(self):
        """Reset all direction buttons to unchecked state"""
        for btn in [
            self._blue_cw_btn,
            self._blue_ccw_btn,
            self._red_cw_btn,
            self._red_ccw_btn,
        ]:
            if btn:
                btn.setChecked(False)
