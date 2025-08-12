"""
Graph Editor Signal Coordinator - Simplified
============================================

Manages signal connections and coordination between graph editor components.
Simplified to remove over-engineered manager dependencies and complex routing.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


if TYPE_CHECKING:
    from desktop.modern.application.services.graph_editor_data_flow_service import (
        GraphEditorDataFlowService,
    )

    from ..graph_editor import GraphEditor

logger = logging.getLogger(__name__)


class GraphEditorSignalCoordinator(QObject):
    """
    Simple signal coordinator for the graph editor.

    Manages signal connections between components with straightforward
    signal routing. No over-engineering, just clean signal management.

    Responsibilities:
    - Connect internal component signals
    - Handle data flow service signals
    - Handle hotkey service signals
    - Coordinate signal emissions between components
    """

    # Re-exposed signals from graph editor (for external consumption)
    beat_modified = pyqtSignal(BeatData)
    arrow_selected = pyqtSignal(str)  # arrow_id
    visibility_changed = pyqtSignal(bool)  # is_visible

    def __init__(self, graph_editor: GraphEditor, parent: QObject | None = None):
        super().__init__(parent)
        self._graph_editor = graph_editor

        # Service references (will be set during initialization)
        self._data_flow_service = None
        self._hotkey_service = None
        self._layout_manager = None
        self._state_manager = None

        logger.info("Simple GraphEditorSignalCoordinator initialized")

    def set_dependencies(
        self,
        data_flow_service: GraphEditorDataFlowService,
        hotkey_service,
        layout_manager,
        state_manager,
    ) -> None:
        """Set component dependencies after initialization"""
        self._data_flow_service = data_flow_service
        self._hotkey_service = hotkey_service
        self._layout_manager = layout_manager
        self._state_manager = state_manager

        # Connect all signals now that dependencies are available
        self._connect_all_signals()

        logger.info("Dependencies set and signals connected")

    def _connect_all_signals(self) -> None:
        """Connect all component signals"""
        try:
            self._connect_data_flow_signals()
            self._connect_hotkey_signals()
            self._connect_ui_component_signals()
            logger.debug("All signals connected successfully")
        except Exception as e:
            logger.warning(f"Some signal connections failed: {e}")

    def _connect_data_flow_signals(self) -> None:
        """Connect data flow service signals to UI updates"""
        if self._data_flow_service:
            try:
                self._data_flow_service.beat_data_updated.connect(
                    self._on_beat_data_updated
                )
                self._data_flow_service.sequence_modified.connect(
                    self._on_sequence_modified
                )
                logger.debug("Data flow signals connected")
            except Exception as e:
                logger.warning(f"Failed to connect data flow signals: {e}")

    def _connect_hotkey_signals(self) -> None:
        """Connect hotkey service signals"""
        if self._hotkey_service:
            try:
                self._hotkey_service.arrow_moved.connect(self._on_arrow_moved)
                self._hotkey_service.rotation_override_requested.connect(
                    self._on_rotation_override
                )
                logger.debug("Hotkey signals connected")
            except Exception as e:
                logger.warning(f"Failed to connect hotkey signals: {e}")

    def _connect_ui_component_signals(self) -> None:
        """Connect UI component signals"""
        try:
            # Connect pictograph display signals if available
            if (
                hasattr(self._graph_editor, "_pictograph_display")
                and self._graph_editor._pictograph_display
            ):
                self._graph_editor._pictograph_display.pictograph_updated.connect(
                    self._on_pictograph_updated
                )

            # Connect adjustment panel signals if available
            if (
                hasattr(self._graph_editor, "_adjustment_panel")
                and self._graph_editor._adjustment_panel
            ):
                self._graph_editor._adjustment_panel.orientation_changed.connect(
                    self._on_orientation_changed
                )
                self._graph_editor._adjustment_panel.turn_amount_changed.connect(
                    self._on_turn_amount_changed
                )

            logger.debug("UI component signals connected")
        except Exception as e:
            logger.warning(f"Failed to connect UI component signals: {e}")

    # Simple signal handlers
    def _on_beat_data_updated(self, beat_data: BeatData, beat_index: int) -> None:
        """Handle beat data updates from data flow service (includes pictograph refresh)"""
        try:
            if self._state_manager:
                self._state_manager.set_selected_beat(beat_data, beat_index)
            self.beat_modified.emit(beat_data)

            # Handle pictograph refresh (consolidated from separate signal)
            if (
                hasattr(self._graph_editor, "_pictograph_display")
                and self._graph_editor._pictograph_display
            ):
                self._graph_editor._pictograph_display.refresh_display(beat_data)

            logger.debug(f"Beat data updated with pictograph refresh: {beat_index}")
        except Exception as e:
            logger.warning(f"Error handling beat data update: {e}")

    def _on_sequence_modified(self, sequence: SequenceData) -> None:
        """Handle sequence modification from data flow service"""
        try:
            if self._state_manager:
                self._state_manager.set_sequence(sequence)
            logger.debug(f"Sequence modified: {sequence.name}")
        except Exception as e:
            logger.warning(f"Error handling sequence modification: {e}")

    def _on_arrow_moved(self, arrow_id: str, delta_x: int, delta_y: int) -> None:
        """Handle arrow movement from hotkeys"""
        try:
            logger.debug(f"Arrow {arrow_id} moved by ({delta_x}, {delta_y})")
            # Simple arrow movement handling
        except Exception as e:
            logger.warning(f"Error handling arrow movement: {e}")

    def _on_rotation_override(self, arrow_id: str) -> None:
        """Handle rotation override (X key)"""
        try:
            logger.debug(f"Rotation override for arrow {arrow_id}")
            # Simple rotation override handling
        except Exception as e:
            logger.warning(f"Error handling rotation override: {e}")

    def _on_pictograph_updated(self, beat_index: int, beat_data: BeatData) -> None:
        """Handle pictograph updates"""
        try:
            self.beat_modified.emit(beat_data)
            logger.debug(f"Pictograph updated for beat {beat_index}")
        except Exception as e:
            logger.warning(f"Error handling pictograph update: {e}")

    def _on_orientation_changed(self, color: str, orientation) -> None:
        """Handle orientation changes"""
        try:
            # Convert enum to string for compatibility
            orientation_str = (
                orientation.value if hasattr(orientation, "value") else str(orientation)
            )

            orientation_data = {
                "color": color,
                "orientation": orientation_str,
                "type": "orientation_change",
            }
            self.arrow_selected.emit(str(orientation_data))
            logger.debug(f"{color} orientation changed to: {orientation_str}")
        except Exception as e:
            logger.warning(f"Error handling orientation change: {e}")

    def _on_turn_amount_changed(self, color: str, turn_amount: int) -> None:
        """Handle turn amount changes"""
        try:
            turn_data = {
                "color": color,
                "turn_amount": turn_amount,
                "type": "turn_change",
            }
            self.arrow_selected.emit(str(turn_data))
            logger.debug(f"{color} turn amount changed")
        except Exception as e:
            logger.warning(f"Error handling turn amount change: {e}")

    # Public methods for external signal emission
    def emit_beat_modified(self, beat_data: BeatData) -> None:
        """Emit beat modified signal"""
        self.beat_modified.emit(beat_data)

    def emit_arrow_selected(self, arrow_id: str) -> None:
        """Emit arrow selected signal"""
        self.arrow_selected.emit(arrow_id)

    def emit_visibility_changed(self, is_visible: bool) -> None:
        """Emit visibility changed signal"""
        self.visibility_changed.emit(is_visible)
