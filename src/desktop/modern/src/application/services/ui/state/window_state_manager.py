"""
Window State Manager - Window Geometry and State Management

Handles window-specific state including geometry, maximized state, and positioning.
Extracted from UIStateManager to follow single responsibility principle.
"""

import logging
from typing import Dict

from core.events.event_bus import UIEvent, get_event_bus

logger = logging.getLogger(__name__)


class WindowStateManager:
    """
    Window state management service.

    Handles:
    - Window geometry (position and size)
    - Window maximized state
    - Window state persistence
    """

    def __init__(self):
        """Initialize window state service."""
        # Event bus for notifications
        self._event_bus = get_event_bus()

        # Window state
        self._window_geometry: Dict[str, int] = {}
        self._window_maximized: bool = False

    def get_window_geometry(self) -> Dict[str, int]:
        """Get window geometry."""
        return self._window_geometry.copy()

    def set_window_geometry(self, geometry: Dict[str, int]) -> None:
        """Set window geometry."""
        self._window_geometry = geometry.copy()

        # Publish window geometry change event
        event = UIEvent(
            component="window",
            action="geometry_changed",
            state_data={"geometry": geometry},
            source="window_state_service",
        )
        self._event_bus.publish(event)

    def is_window_maximized(self) -> bool:
        """Check if window is maximized."""
        return self._window_maximized

    def set_window_maximized(self, maximized: bool) -> None:
        """Set window maximized state."""
        self._window_maximized = maximized

        # Publish window maximized state change event
        event = UIEvent(
            component="window",
            action="maximized_changed",
            state_data={"maximized": maximized},
            source="window_state_service",
        )
        self._event_bus.publish(event)

    def get_window_state(self) -> Dict[str, any]:
        """Get complete window state."""
        return {
            "geometry": self.get_window_geometry(),
            "maximized": self.is_window_maximized(),
        }

    def set_window_state(self, state: Dict[str, any]) -> None:
        """Set complete window state."""
        if "geometry" in state:
            self.set_window_geometry(state["geometry"])
        if "maximized" in state:
            self.set_window_maximized(state["maximized"])

    def reset_window_state(self) -> None:
        """Reset window state to defaults."""
        self._window_geometry = {}
        self._window_maximized = False

        # Publish window state reset event
        event = UIEvent(
            component="window",
            action="state_reset",
            state_data={},
            source="window_state_service",
        )
        self._event_bus.publish(event)

    def get_state_for_persistence(self) -> Dict[str, any]:
        """Get state data for persistence."""
        return {
            "window_geometry": self._window_geometry,
            "window_maximized": self._window_maximized,
        }

    def load_state_from_persistence(self, state: Dict[str, any]) -> None:
        """Load state from persistence data."""
        if "window_geometry" in state:
            self._window_geometry = state["window_geometry"]
        if "window_maximized" in state:
            self._window_maximized = state["window_maximized"]
