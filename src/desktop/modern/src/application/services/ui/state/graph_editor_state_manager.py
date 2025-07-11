"""
Graph Editor State Manager - Graph Editor Specific State

Handles graph editor visibility, height, and other graph editor specific state.
Extracted from UIStateManager to follow single responsibility principle.
"""

import logging
from typing import Any, Dict

from core.events.event_bus import UIEvent, get_event_bus

logger = logging.getLogger(__name__)


class GraphEditorStateManager:
    """
    Graph editor state management.
    
    Handles:
    - Graph editor visibility
    - Graph editor height
    - Graph editor specific settings
    - Graph editor state persistence
    """

    def __init__(self):
        """Initialize graph editor state manager."""
        # Event bus for notifications
        self._event_bus = get_event_bus()

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

        # Only publish event if state actually changed
        if previous_state != visible:
            # Publish graph editor visibility change event
            event = UIEvent(
                component="graph_editor",
                action="visibility_changed",
                state_data={
                    "visible": visible,
                    "previous_state": previous_state,
                },
                source="graph_editor_state_manager",
            )
            self._event_bus.publish(event)

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

        # Only publish event if height actually changed
        if previous_height != clamped_height:
            # Publish graph editor height change event
            event = UIEvent(
                component="graph_editor",
                action="height_changed",
                state_data={
                    "height": clamped_height,
                    "previous_height": previous_height,
                },
                source="graph_editor_state_manager",
            )
            self._event_bus.publish(event)

    def get_graph_editor_state(self) -> Dict[str, Any]:
        """Get complete graph editor state."""
        return {
            "visible": self._graph_editor_visible,
            "height": self._graph_editor_height,
        }

    def set_graph_editor_state(self, state: Dict[str, Any]) -> None:
        """Set complete graph editor state."""
        if "visible" in state:
            self.set_graph_editor_visible(state["visible"])
        if "height" in state:
            self.set_graph_editor_height(state["height"])

    def reset_graph_editor_state(self) -> None:
        """Reset graph editor state to defaults."""
        self._graph_editor_visible = False
        self._graph_editor_height = 300

        # Publish graph editor state reset event
        event = UIEvent(
            component="graph_editor",
            action="state_reset",
            state_data={},
            source="graph_editor_state_manager",
        )
        self._event_bus.publish(event)

    def get_state_for_persistence(self) -> Dict[str, Any]:
        """Get state data for persistence."""
        return {
            "graph_editor_visible": self._graph_editor_visible,
            "graph_editor_height": self._graph_editor_height,
        }

    def load_state_from_persistence(self, state: Dict[str, Any]) -> None:
        """Load state from persistence data."""
        if "graph_editor_visible" in state:
            self._graph_editor_visible = state["graph_editor_visible"]
        if "graph_editor_height" in state:
            self._graph_editor_height = state["graph_editor_height"]
