"""
Tab State Manager - Tab Navigation and State Management

Handles tab-specific state including active tab, tab switching, and tab-specific data.
Extracted from UIStateManager to follow single responsibility principle.
"""

import logging
from typing import Any, Dict

from core.events.event_bus import EventPriority, UIEvent, get_event_bus

logger = logging.getLogger(__name__)


class TabStateManager:
    """
    Tab state management.
    
    Handles:
    - Active tab tracking
    - Tab switching logic
    - Tab-specific state storage
    - Tab state persistence
    """

    def __init__(self):
        """Initialize tab state manager."""
        # Event bus for notifications
        self._event_bus = get_event_bus()

        # Tab state
        self._active_tab: str = "sequence_builder"
        self._tab_states: Dict[str, Dict[str, Any]] = {}

    def get_active_tab(self) -> str:
        """Get the active tab."""
        return self._active_tab

    def set_active_tab(self, tab_name: str) -> None:
        """Set the active tab."""
        previous_tab = self._active_tab
        self._active_tab = tab_name

        # Publish tab change event
        event = UIEvent(
            component="tab",
            action="changed",
            state_data={"previous_tab": previous_tab, "new_tab": tab_name},
            source="tab_state_manager",
            priority=EventPriority.HIGH,
        )
        self._event_bus.publish(event)

    def get_tab_state(self, tab_name: str) -> Dict[str, Any]:
        """Get state for a specific tab."""
        return self._tab_states.get(tab_name, {})

    def update_tab_state(self, tab_name: str, state: Dict[str, Any]) -> None:
        """Update state for a specific tab."""
        if tab_name not in self._tab_states:
            self._tab_states[tab_name] = {}

        self._tab_states[tab_name].update(state)

        # Publish tab state change event
        event = UIEvent(
            component="tab",
            action="state_updated",
            state_data={"tab_name": tab_name, "state": state},
            source="tab_state_manager",
        )
        self._event_bus.publish(event)

    def clear_tab_state(self, tab_name: str) -> None:
        """Clear state for a specific tab."""
        if tab_name in self._tab_states:
            del self._tab_states[tab_name]

        # Publish tab state cleared event
        event = UIEvent(
            component="tab",
            action="state_cleared",
            state_data={"tab_name": tab_name},
            source="tab_state_manager",
        )
        self._event_bus.publish(event)

    def get_all_tab_states(self) -> Dict[str, Dict[str, Any]]:
        """Get all tab states."""
        return self._tab_states.copy()

    def reset_tab_states(self) -> None:
        """Reset all tab states."""
        self._tab_states.clear()
        self._active_tab = "sequence_builder"

        # Publish tab states reset event
        event = UIEvent(
            component="tab",
            action="states_reset",
            state_data={},
            source="tab_state_manager",
        )
        self._event_bus.publish(event)

    def get_state_for_persistence(self) -> Dict[str, Any]:
        """Get state data for persistence."""
        return {
            "active_tab": self._active_tab,
            "tab_states": self._tab_states,
        }

    def load_state_from_persistence(self, state: Dict[str, Any]) -> None:
        """Load state from persistence data."""
        if "active_tab" in state:
            self._active_tab = state["active_tab"]
        if "tab_states" in state:
            self._tab_states = state["tab_states"]
