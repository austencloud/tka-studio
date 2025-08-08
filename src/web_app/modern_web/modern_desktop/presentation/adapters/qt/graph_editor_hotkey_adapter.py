"""
Qt Adapter for Graph Editor Hotkey Service

This adapter wraps the pure GraphEditorHotkeyService to provide Qt-specific signal coordination.
"""

from __future__ import annotations

from collections.abc import Callable
import logging
from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import QObject, pyqtSignal
from shared.application.services.graph_editor.graph_editor_hotkey_service import (
    GraphEditorHotkeyService,
)


if TYPE_CHECKING:
    from desktop.modern.presentation.components.graph_editor.graph_editor import (
        GraphEditor,
    )

logger = logging.getLogger(__name__)


class QtGraphEditorHotkeyAdapter(QObject):
    """
    Qt adapter for GraphEditorHotkeyService.

    This adapter provides Qt signal coordination for the pure service.
    """

    # Qt signals for hotkey events
    arrow_moved = pyqtSignal(str, int, int)  # arrow_id, delta_x, delta_y
    hotkey_processed = pyqtSignal(str, dict)  # action, context

    # Qt signals for specific hotkey actions
    select_all_requested = pyqtSignal()
    copy_requested = pyqtSignal()
    paste_requested = pyqtSignal()
    delete_requested = pyqtSignal()
    undo_requested = pyqtSignal()
    redo_requested = pyqtSignal()

    def __init__(
        self,
        graph_editor_getter: Callable[[], GraphEditor] | None = None,
    ):
        super().__init__()

        # Create the pure service
        self.service = GraphEditorHotkeyService(graph_editor_getter)

        # Connect service callbacks to Qt signals
        self.service.add_arrow_moved_callback(self._on_arrow_moved)
        self.service.add_hotkey_processed_callback(self._on_hotkey_processed)

    def process_hotkey(
        self,
        hotkey: str,
        beat_data: object | None = None,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """
        Process a hotkey action.

        Args:
            hotkey: The hotkey string (e.g., "Ctrl+A", "Shift+Left")
            beat_data: Current beat data (if available)
            context: Additional context for the hotkey

        Returns:
            True if hotkey was processed, False otherwise
        """
        return self.service.process_hotkey(hotkey, beat_data, context)

    def move_arrow(
        self,
        arrow_id: str,
        delta_x: int,
        delta_y: int,
        beat_data: object | None = None,
    ) -> bool:
        """
        Move an arrow by the specified delta.

        Args:
            arrow_id: Identifier for the arrow
            delta_x: X-axis movement delta
            delta_y: Y-axis movement delta
            beat_data: Current beat data (if available)

        Returns:
            True if arrow was moved, False otherwise
        """
        return self.service.move_arrow(arrow_id, delta_x, delta_y, beat_data)

    def _on_arrow_moved(self, arrow_id: str, delta_x: int, delta_y: int):
        """Handle arrow moved callback from service."""
        self.arrow_moved.emit(arrow_id, delta_x, delta_y)

    def _on_hotkey_processed(self, action: str, context: dict[str, Any]):
        """Handle hotkey processed callback from service."""
        self.hotkey_processed.emit(action, context)

        # Emit specific action signals
        if action == "select_all":
            self.select_all_requested.emit()
        elif action == "copy":
            self.copy_requested.emit()
        elif action == "paste":
            self.paste_requested.emit()
        elif action == "delete":
            self.delete_requested.emit()
        elif action == "undo":
            self.undo_requested.emit()
        elif action == "redo":
            self.redo_requested.emit()

    # Pass-through methods for direct service access
    def add_arrow_moved_callback(self, callback: Callable[[str, int, int], None]):
        """Add callback for when an arrow is moved."""
        self.service.add_arrow_moved_callback(callback)

    def add_hotkey_processed_callback(
        self, callback: Callable[[str, dict[str, Any]], None]
    ):
        """Add callback for when a hotkey is processed."""
        self.service.add_hotkey_processed_callback(callback)
