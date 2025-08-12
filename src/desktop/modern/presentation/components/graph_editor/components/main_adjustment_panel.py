"""
Main Adjustment Panel Component for TKA Graph Editor
===================================================

Orchestrates the stacked widget switching between orientation and turn controls.
This component manages the context-sensitive panel display based on beat type
and maintains the exact functionality of the legacy adjustment section.

Features:
- Stacked widget management for context-sensitive panels
- Automatic panel switching based on beat type (start position vs regular beat)
- Coordination between orientation picker and turn adjustment controls
- Signal routing and state management
- Clean component separation following TKA architecture

Architecture:
- Follows TKA presentation layer patterns
- Uses composition to manage child components
- Maintains clean separation between orchestration and implementation
- Supports dependency injection for service integration
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

from desktop.modern.domain.models import BeatData
from desktop.modern.presentation.components.graph_editor.components.turn_adjustment_controls.turn_adjustment_controls import (
    TurnAdjustmentControls,
)

from .dual_orientation_picker import DualOrientationPicker


logger = logging.getLogger(__name__)


class MainAdjustmentPanel(QWidget):
    """
    Main adjustment panel that orchestrates context-sensitive control switching.

    This component manages the stacked widget that switches between orientation
    picker (for start positions) and turn adjustment controls (for regular beats).
    It maintains the exact behavior of the legacy implementation while providing
    clean component separation.

    Panel Modes:
    - Index 0: Orientation picker (for start positions)
    - Index 1: Turn adjustment controls (for regular beats)

    The panel automatically switches based on beat type detection, following
    the same logic as the legacy implementation.
    """

    # Signals for communication with parent components
    orientation_changed = pyqtSignal(
        str, object
    )  # color, orientation (Orientation enum)
    turn_amount_changed = pyqtSignal(str, float)  # color, amount
    rotation_direction_changed = pyqtSignal(str, str)  # color, direction
    beat_data_updated = pyqtSignal(BeatData)  # updated beat data

    def __init__(self, parent=None):
        """
        Initialize the main adjustment panel.

        Args:
            parent: Parent widget (typically the graph editor)
        """
        super().__init__(parent)
        self._current_beat_data: BeatData | None = None
        self._current_beat_index: int | None = None

        # Component references
        self._stacked_widget: QStackedWidget | None = None
        self._orientation_picker: DualOrientationPicker | None = None
        self._turn_controls: TurnAdjustmentControls | None = None

        self._setup_ui()
        self._connect_signals()
        logger.debug("MainAdjustmentPanel initialized")

    def _setup_ui(self):
        """Set up the main adjustment panel UI with stacked widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create stacked widget for context-sensitive panels
        self._stacked_widget = QStackedWidget()

        # Index 0: Orientation Picker (for start positions)
        self._orientation_picker = DualOrientationPicker(parent=self)
        self._stacked_widget.addWidget(self._orientation_picker)

        # Index 1: Turn Adjustment Controls (for regular beats)
        self._turn_controls = TurnAdjustmentControls(parent=self)
        self._stacked_widget.addWidget(self._turn_controls)

        # Default to orientation picker
        self._stacked_widget.setCurrentIndex(0)

        layout.addWidget(self._stacked_widget)

    def _connect_signals(self):
        """Connect signals from child components to parent routing"""
        if self._orientation_picker:
            self._orientation_picker.orientation_changed.connect(
                self.orientation_changed
            )
            self._orientation_picker.beat_data_updated.connect(self.beat_data_updated)

        if self._turn_controls:
            self._turn_controls.turn_amount_changed.connect(self.turn_amount_changed)
            self._turn_controls.rotation_direction_changed.connect(
                self.rotation_direction_changed
            )
            self._turn_controls.beat_data_updated.connect(self.beat_data_updated)

    def set_beat_data(self, beat_index: int, beat_data: BeatData | None):
        """
        Set the current beat data and switch panels based on beat type.

        Args:
            beat_index: Index of the beat (-1 for start position)
            beat_data: Beat data to display (None to clear)
        """
        self._current_beat_index = beat_index
        self._current_beat_data = beat_data

        # Determine which panel to show based on beat type
        panel_mode = self._determine_panel_mode(beat_index, beat_data)

        if panel_mode == "orientation":
            self._show_orientation_picker(beat_data)
        else:
            self._show_turn_controls(beat_data)

        logger.debug(f"Panel switched to {panel_mode} mode for beat {beat_index}")

    def _determine_panel_mode(
        self, beat_index: int, beat_data: BeatData | None
    ) -> str:
        """
        Determine whether to show orientation picker or turn controls.

        Args:
            beat_index: Index of the beat (-1 for start position)
            beat_data: Beat data to analyze

        Returns:
            str: "orientation" or "turns" based on beat type
        """
        if not beat_data:
            return "orientation"

        # Check for start position indicators - FIXED: Only use explicit start position markers
        is_start_position = (
            # Explicit start position index (primary indicator)
            beat_index == -1
            # Check metadata for start position marker
            or beat_data.metadata.get("is_start_position", False)
            # Check beat number (0 = start position, 1+ = regular beats)
            or getattr(beat_data, "beat_number", 1) == 0
            # Check for start position letter (α, alpha, etc.)
            or getattr(beat_data, "letter", "") in ["α", "alpha", "start"]
            # Check for sequence start position in metadata
            or "sequence_start_position" in beat_data.metadata
            # REMOVED: Static motion type check - too broad, regular beats can be static
        )

        return "orientation" if is_start_position else "turns"

    def _show_orientation_picker(self, beat_data: BeatData | None):
        """
        Show the orientation picker panel and update it with beat data.

        Args:
            beat_data: Beat data to display
        """
        self._stacked_widget.setCurrentIndex(0)
        if self._orientation_picker:
            self._orientation_picker.set_beat_data(beat_data)

    def _show_turn_controls(self, beat_data: BeatData | None):
        """
        Show the turn controls panel and update it with beat data.

        Args:
            beat_data: Beat data to display
        """
        self._stacked_widget.setCurrentIndex(1)
        if self._turn_controls:
            self._turn_controls.set_beat_data(beat_data)

    def get_current_panel_mode(self) -> str:
        """
        Get the currently active panel mode.

        Returns:
            str: "orientation" or "turns" based on current panel
        """
        current_index = self._stacked_widget.currentIndex()
        return "orientation" if current_index == 0 else "turns"

    def force_orientation_mode(self):
        """Force the panel to show orientation picker regardless of beat type"""
        self._stacked_widget.setCurrentIndex(0)
        if self._orientation_picker and self._current_beat_data:
            self._orientation_picker.set_beat_data(self._current_beat_data)

    def force_turns_mode(self):
        """Force the panel to show turn controls regardless of beat type"""
        self._stacked_widget.setCurrentIndex(1)
        if self._turn_controls and self._current_beat_data:
            self._turn_controls.set_beat_data(self._current_beat_data)

    def get_orientation_picker(self) -> DualOrientationPicker | None:
        """
        Get the orientation picker component for direct access if needed.

        Returns:
            DualOrientationPicker: The orientation picker component
        """
        return self._orientation_picker

    def get_turn_controls(self) -> TurnAdjustmentControls | None:
        """
        Get the turn controls component for direct access if needed.

        Returns:
            TurnAdjustmentControls: The turn controls component
        """
        return self._turn_controls

    def get_current_beat_data(self) -> BeatData | None:
        """
        Get the currently set beat data.

        Returns:
            BeatData: Currently set beat data, or None if no beat is set
        """
        return self._current_beat_data

    def get_current_beat_index(self) -> int | None:
        """
        Get the currently set beat index.

        Returns:
            int: Currently set beat index, or None if no beat is set
        """
        return self._current_beat_index

    def clear_panels(self):
        """Clear both panels and reset to default state"""
        if self._orientation_picker:
            self._orientation_picker.set_beat_data(None)
        if self._turn_controls:
            self._turn_controls.set_beat_data(None)

        # Reset to orientation picker as default
        self._stacked_widget.setCurrentIndex(0)
        self._current_beat_data = None
        self._current_beat_index = None
