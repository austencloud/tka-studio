"""
Graph Editor Hotkey Service Implementation

Real hotkey service implementation for graph editor with WASD movement,
Shift/Ctrl modifiers, and X/Z/C special commands.

This is a pure service implementation that follows TKA testing patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent


if TYPE_CHECKING:
    from desktop.modern.core.interfaces.workbench_services import IGraphEditorService


class GraphEditorHotkeyManager:
    """
    Graph editor hotkey service with reliable testing support.

    Uses callback pattern for communication instead of Qt signals,
    making it easier to test and more service-layer appropriate.
    """

    def __init__(self, graph_service: IGraphEditorService, callback_handler=None):
        self.graph_service = graph_service

        # Movement increment settings
        self.base_increment = 5
        self.shift_increment = 20
        self.ctrl_shift_increment = 200

        # Set up callback handlers
        if callback_handler:
            self.on_arrow_moved = getattr(callback_handler, "on_arrow_moved", None)
            self.on_rotation_override = getattr(
                callback_handler, "on_rotation_override_requested", None
            )
            self.on_special_placement_removal = getattr(
                callback_handler, "on_special_placement_removal_requested", None
            )
            self.on_prop_placement_override = getattr(
                callback_handler, "on_prop_placement_override_requested", None
            )
        else:
            # Callback handlers (set externally)
            self.on_arrow_moved = None
            self.on_rotation_override = None
            self.on_special_placement_removal = None
            self.on_prop_placement_override = None

    def handle_key_event(self, event: QKeyEvent) -> bool:
        """Handle keyboard events and return True if handled"""
        key = event.key()
        modifiers = event.modifiers()

        # Check if we have a selected arrow
        selected_arrow = self._get_selected_arrow()
        if not selected_arrow:
            return False

        # WASD movement
        if key in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            return self._handle_arrow_movement(key, modifiers, selected_arrow)

        # Special commands
        if key == Qt.Key.Key_X:
            if self.on_rotation_override:
                self.on_rotation_override(selected_arrow)
            return True
        if key == Qt.Key.Key_Z:
            if self.on_special_placement_removal:
                self.on_special_placement_removal(selected_arrow)
            return True
        if key == Qt.Key.Key_C:
            if self.on_prop_placement_override:
                self.on_prop_placement_override(selected_arrow)
            return True

        return False

    def _get_selected_arrow(self) -> str | None:
        """Get the currently selected arrow from the graph service"""
        # TODO: Add method to graph service interface to get selected arrow
        # For now, return a default arrow since the interface doesn't have selection methods yet
        # This will need to be updated when the interface is extended
        return "blue"  # Default to blue arrow for now

    def _handle_arrow_movement(self, key, modifiers, arrow_id: str) -> bool:
        """Handle WASD arrow movement with modifier support"""
        # Calculate increment based on modifiers
        increment = self.base_increment
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            if modifiers & Qt.KeyboardModifier.ControlModifier:
                increment = self.ctrl_shift_increment  # Shift+Ctrl = 200px
            else:
                increment = self.shift_increment  # Shift = 20px

        # Calculate movement delta
        delta_x, delta_y = self._get_movement_delta(key, increment)

        if delta_x != 0 or delta_y != 0:
            if self.on_arrow_moved:
                self.on_arrow_moved(arrow_id, delta_x, delta_y)
            return True

        return False

    def _get_movement_delta(self, key, increment: int) -> tuple[int, int]:
        """Convert key to movement delta"""
        movement_map = {
            Qt.Key.Key_W: (0, -increment),  # Up
            Qt.Key.Key_A: (-increment, 0),  # Left
            Qt.Key.Key_S: (0, increment),  # Down
            Qt.Key.Key_D: (increment, 0),  # Right
        }
        return movement_map.get(key, (0, 0))

    def set_movement_increments(
        self, base: int = 5, shift: int = 20, ctrl_shift: int = 200
    ):
        """Set custom movement increments"""
        self.base_increment = base
        self.shift_increment = shift
        self.ctrl_shift_increment = ctrl_shift

    def get_movement_increments(self) -> tuple[int, int, int]:
        """Get current movement increments"""
        return (self.base_increment, self.shift_increment, self.ctrl_shift_increment)


# Export the service class
__all__ = ["GraphEditorHotkeyManager"]
