"""
Graph Editor Hotkey Qt Adapter

Qt-specific adapter for the GraphEditorHotkeyService that handles PyQt signals
while keeping the core service logic framework-agnostic.

This adapter implements the Adapter Pattern to bridge between Qt signals
and the pure service layer, maintaining proper service separation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QKeyEvent

from .graph_editor_hotkey_manager import GraphEditorHotkeyManager


if TYPE_CHECKING:
    from desktop.modern.core.interfaces.workbench_services import IGraphEditorService


class GraphEditorHotkeyAdapter(QObject):
    """
    Qt adapter for GraphEditorHotkeyService.

    This adapter handles Qt signals while delegating actual hotkey logic
    to the framework-agnostic service layer.
    """

    # Qt signals for external components
    arrow_moved = pyqtSignal(str, int, int)  # arrow_id, delta_x, delta_y
    rotation_override_requested = pyqtSignal(str)  # arrow_id
    special_placement_removal_requested = pyqtSignal(str)  # arrow_id
    prop_placement_override_requested = pyqtSignal(str)  # arrow_id

    def __init__(self, graph_service: IGraphEditorService, parent=None):
        super().__init__(parent)

        # Create callback handler that bridges to Qt signals
        callback_handler = HotkeyCallbackHandler(self)

        # Initialize the pure service with callbacks
        self.service = GraphEditorHotkeyManager(graph_service, callback_handler)

    def handle_key_event(self, event: QKeyEvent) -> bool:
        """Handle keyboard events by delegating to service"""
        return self.service.handle_key_event(event)

    def set_movement_increments(
        self, base: int = 5, shift: int = 20, ctrl_shift: int = 200
    ):
        """Set custom movement increments"""
        self.service.set_movement_increments(base, shift, ctrl_shift)

    def get_movement_increments(self) -> tuple[int, int, int]:
        """Get current movement increments"""
        return self.service.get_movement_increments()


class HotkeyCallbackHandler:
    """
    Callback handler that bridges service callbacks to Qt signals.

    This class implements the IHotkeyCallbacks protocol and converts
    service callbacks into PyQt signals.
    """

    def __init__(self, adapter: GraphEditorHotkeyAdapter):
        self.adapter = adapter

    def on_arrow_moved(self, arrow_id: str, delta_x: int, delta_y: int) -> None:
        """Called when arrow movement is requested"""
        self.adapter.arrow_moved.emit(arrow_id, delta_x, delta_y)

    def on_rotation_override_requested(self, arrow_id: str) -> None:
        """Called when rotation override is requested"""
        self.adapter.rotation_override_requested.emit(arrow_id)

    def on_special_placement_removal_requested(self, arrow_id: str) -> None:
        """Called when special placement removal is requested"""
        self.adapter.special_placement_removal_requested.emit(arrow_id)

    def on_prop_placement_override_requested(self, arrow_id: str) -> None:
        """Called when prop placement override is requested"""
        self.adapter.prop_placement_override_requested.emit(arrow_id)


# Export the adapter as the main interface
__all__ = ["GraphEditorHotkeyAdapter"]
