"""
Graph Editor State Manager - Graph Editor Specific State

Handles graph editor visibility, height, and other graph editor specific state.
Uses Qt signals for clean communication.
"""

import logging
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)


class GraphEditorStateManager(QObject):
    """
    Graph editor state management using Qt signals.

    Handles:
    - Graph editor visibility
    - Graph editor height
    - Graph editor specific settings
    - Graph editor state persistence
    """

    # Qt signals for graph editor state changes
    visibility_changed = pyqtSignal(bool)  # visible
    height_changed = pyqtSignal(int)  # height
    state_reset = pyqtSignal()  # state reset

    def __init__(self):
        """Initialize graph editor state manager."""
        super().__init__()

        # Graph editor state
        self._graph_editor_visible: bool = False
        self._graph_editor_height: int = 300

    def is_graph_editor_visible(self) -> bool:
        """Check if graph editor is visible."""
        return self._graph_editor_visible

    def set_graph_editor_visible(self, visible: bool) -> None:
        """Set graph editor visibility."""
        previous_state = self._graph_editor_visible
        self._graph_editor_visible = visible

        # Only emit signal if state actually changed
        if previous_state != visible:
            self.visibility_changed.emit(visible)

    def toggle_graph_editor(self) -> bool:
        """Toggle graph editor visibility and return new state."""
        new_state = not self._graph_editor_visible
        self.set_graph_editor_visible(new_state)
        return new_state

    def get_graph_editor_height(self) -> int:
        """Get graph editor height."""
        return self._graph_editor_height

    def set_graph_editor_height(self, height: int) -> None:
        """Set graph editor height with bounds checking."""
        # Clamp height between reasonable bounds
        clamped_height = max(100, min(800, height))
        previous_height = self._graph_editor_height
        self._graph_editor_height = clamped_height

        # Only emit signal if height actually changed
        if previous_height != clamped_height:
            self.height_changed.emit(clamped_height)

    def get_graph_editor_state(self) -> dict[str, Any]:
        """Get complete graph editor state."""
        return {
            "visible": self._graph_editor_visible,
            "height": self._graph_editor_height,
        }

    def set_graph_editor_state(self, state: dict[str, Any]) -> None:
        """Set complete graph editor state."""
        if "visible" in state:
            self.set_graph_editor_visible(state["visible"])
        if "height" in state:
            self.set_graph_editor_height(state["height"])

    def reset_graph_editor_state(self) -> None:
        """Reset graph editor state to defaults."""
        self._graph_editor_visible = False
        self._graph_editor_height = 300

        # Emit signal for state reset
        self.state_reset.emit()

    def get_state_for_persistence(self) -> dict[str, Any]:
        """Get state data for persistence."""
        return {
            "graph_editor_visible": self._graph_editor_visible,
            "graph_editor_height": self._graph_editor_height,
        }

    def load_state_from_persistence(self, state: dict[str, Any]) -> None:
        """Load state from persistence data."""
        if "graph_editor_visible" in state:
            self._graph_editor_visible = state["graph_editor_visible"]
        if "graph_editor_height" in state:
            self._graph_editor_height = state["graph_editor_height"]
