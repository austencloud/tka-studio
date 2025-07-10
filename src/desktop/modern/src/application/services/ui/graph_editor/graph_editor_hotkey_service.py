"""
Graph Editor Hotkey Service Implementation

Real hotkey service implementation for graph editor with WASD movement,
Shift/Ctrl modifiers, and X/Z/C special commands, replacing the placeholder implementation.
"""

from typing import Optional, TYPE_CHECKING
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QKeyEvent

if TYPE_CHECKING:
    from core.interfaces.workbench_services import IGraphEditorService


class GraphEditorHotkeyService(QObject):
    """Real hotkey service implementation for graph editor"""

    # Signals for hotkey actions
    arrow_moved = pyqtSignal(str, int, int)  # arrow_id, delta_x, delta_y
    rotation_override_requested = pyqtSignal(str)  # arrow_id
    special_placement_removal_requested = pyqtSignal(str)  # arrow_id
    prop_placement_override_requested = pyqtSignal(str)  # arrow_id

    def __init__(self, graph_service: "IGraphEditorService", parent=None):
        super().__init__(parent)
        self.graph_service = graph_service

        # Movement increment settings (from legacy)
        self.base_increment = 5
        self.shift_increment = 20
        self.ctrl_shift_increment = 200

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
        elif key == Qt.Key.Key_X:
            self.rotation_override_requested.emit(selected_arrow)
            return True
        elif key == Qt.Key.Key_Z:
            self.special_placement_removal_requested.emit(selected_arrow)
            return True
        elif key == Qt.Key.Key_C:
            self.prop_placement_override_requested.emit(selected_arrow)
            return True

        return False

    def _get_selected_arrow(self) -> Optional[str]:
        """Get the currently selected arrow from the graph service"""
        # TODO: Add method to graph service interface to get selected arrow
        # For now, assume we have a selected arrow if we have a selected beat
        if hasattr(self.graph_service, "get_selected_beat"):
            beat = self.graph_service.get_selected_beat()
            if beat:
                # Default to blue arrow for now
                return "blue"
        return None

    def _handle_arrow_movement(
        self, key: Qt.Key, modifiers: Qt.KeyboardModifier, arrow_id: str
    ) -> bool:
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
            self.arrow_moved.emit(arrow_id, delta_x, delta_y)
            return True

        return False

    def _get_movement_delta(self, key: Qt.Key, increment: int) -> tuple[int, int]:
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
__all__ = ["GraphEditorHotkeyService"]
