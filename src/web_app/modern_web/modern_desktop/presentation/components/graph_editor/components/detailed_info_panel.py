"""
Detailed Information Panel Component for TKA Graph Editor
========================================================

Displays detailed information about the selected beat/pictograph in human-readable format.


Features:
- Beat information display (letter, duration, motion details)
- Motion data visualization (blue/red motion types, directions, locations)
- Reversal and glyph information
- Glassmorphism styling consistent with TKA design system
- Responsive layout with centered content

Architecture:
- Follows TKA presentation layer patterns
- Uses immutable domain models (BeatData)
- Maintains clean separation from business logic
- Supports dependency injection for future extensibility
"""

from __future__ import annotations

import logging
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from desktop.modern.domain.models import BeatData


logger = logging.getLogger(__name__)


class DetailedInfoPanel(QWidget):
    """
    Panel that displays detailed information about the selected beat/pictograph
    in human-readable format.

    This component provides a clean, readable display of beat data including:
    - Beat identification (letter, duration)
    - Motion information (blue/red motion types, directions, locations, turns)
    - Additional properties (reversals, glyph data)

    The panel uses glassmorphism styling and centers content vertically for
    optimal visual presentation.
    """

    def __init__(self, parent=None):
        """
        Initialize the detailed information panel.

        Args:
            parent: Parent widget (typically the graph editor)
        """
        super().__init__(parent)
        self._setup_ui()
        self._setup_styling()
        logger.debug("DetailedInfoPanel initialized")

    def _setup_ui(self):
        """Set up the detailed information panel UI with centered content"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # Add stretch to center content vertically
        layout.addStretch()

        # Title
        self._title_label = QLabel("Beat Information")
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._title_label.setStyleSheet(
            """
            font-weight: bold;
            font-size: 16px;
            color: rgba(255, 255, 255, 0.9);
            padding: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            margin-bottom: 8px;
        """
        )
        layout.addWidget(self._title_label)

        # Beat details
        self._beat_info_label = QLabel("No beat selected")
        self._beat_info_label.setWordWrap(True)
        self._beat_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._beat_info_label.setStyleSheet(
            """
            color: rgba(255, 255, 255, 0.8);
            font-size: 13px;
            padding: 6px;
            line-height: 1.4;
        """
        )
        layout.addWidget(self._beat_info_label)

        # Motion details
        self._motion_info_label = QLabel("")
        self._motion_info_label.setWordWrap(True)
        self._motion_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._motion_info_label.setStyleSheet(
            """
            color: rgba(255, 255, 255, 0.7);
            font-size: 12px;
            padding: 6px;
            line-height: 1.3;
        """
        )
        layout.addWidget(self._motion_info_label)

        # Additional details
        self._arrow_info_label = QLabel("")
        self._arrow_info_label.setWordWrap(True)
        self._arrow_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._arrow_info_label.setStyleSheet(
            """
            color: rgba(255, 255, 255, 0.6);
            font-size: 11px;
            padding: 6px;
            line-height: 1.2;
        """
        )
        layout.addWidget(self._arrow_info_label)

        # Add stretch to center content vertically
        layout.addStretch()

    def _setup_styling(self):
        """Apply glassmorphism styling to the info panel"""
        self.setStyleSheet(
            """
            DetailedInfoPanel {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
            }
        """
        )

    def update_beat_info(self, beat_index: int, beat_data: Optional[BeatData]):
        """
        Update the panel with beat information.

        Args:
            beat_index: Index of the beat (-1 for start position)
            beat_data: Beat data to display (None to clear)
        """
        if not beat_data:
            self._clear_info()
            return

        self._update_title(beat_index)
        self._update_beat_details(beat_data)
        self._update_motion_details(beat_data)
        self._update_additional_details(beat_data)

        logger.debug(f"Updated info panel for beat {beat_index}: {beat_data.letter}")

    def _clear_info(self):
        """Clear all information from the panel"""
        self._title_label.setText("Beat Information")
        self._beat_info_label.setText("No beat selected")
        self._motion_info_label.setText("")
        self._arrow_info_label.setText("")

    def _update_title(self, beat_index: int):
        """Update the title based on beat index"""
        if beat_index == -1:
            self._title_label.setText("Start Position")
        else:
            self._title_label.setText(f"Beat {beat_index + 1}")

    def _update_beat_details(self, beat_data: BeatData):
        """Update basic beat information"""
        beat_info = f"Letter: {beat_data.letter}\n"
        beat_info += f"Duration: {beat_data.duration} beats"
        self._beat_info_label.setText(beat_info)

    def _update_motion_details(self, beat_data: BeatData):
        """Update motion information for blue and red motions"""
        motion_info = ""

        # Blue motion details
        if beat_data.pictograph_data.motions["blue"]:
            motion_info += f"Blue Motion: {beat_data.pictograph_data.motions['blue'].motion_type.value}\n"
            motion_info += f"Blue Direction: {beat_data.pictograph_data.motions['blue'].prop_rot_dir.value}\n"
            motion_info += f"Blue Start: {beat_data.pictograph_data.motions['blue'].start_loc.value}\n"
            motion_info += (
                f"Blue End: {beat_data.pictograph_data.motions['blue'].end_loc.value}\n"
            )
            if beat_data.pictograph_data.motions["blue"].turns:
                motion_info += (
                    f"Blue Turns: {beat_data.pictograph_data.motions['blue'].turns}\n"
                )

        # Red motion details
        if beat_data.pictograph_data.motions["red"]:
            motion_info += f"Red Motion: {beat_data.pictograph_data.motions['red'].motion_type.value}\n"
            motion_info += f"Red Direction: {beat_data.pictograph_data.motions['red'].prop_rot_dir.value}\n"
            motion_info += f"Red Start: {beat_data.pictograph_data.motions['red'].start_loc.value}\n"
            motion_info += (
                f"Red End: {beat_data.pictograph_data.motions['red'].end_loc.value}\n"
            )
            if beat_data.pictograph_data.motions["red"].turns:
                motion_info += (
                    f"Red Turns: {beat_data.pictograph_data.motions['red'].turns}\n"
                )

        self._motion_info_label.setText(motion_info)

    def _update_additional_details(self, beat_data: BeatData):
        """Update additional information like reversals and glyph data"""
        additional_info = ""

        if beat_data.blue_reversal:
            additional_info += "Blue Reversal: Yes\n"
        if beat_data.red_reversal:
            additional_info += "Red Reversal: Yes\n"
        if beat_data.pictograph_data.letter_type:
            glyph_type = beat_data.pictograph_data.letter_type.value
            additional_info += f"Glyph: {glyph_type}\n"

        self._arrow_info_label.setText(additional_info)
