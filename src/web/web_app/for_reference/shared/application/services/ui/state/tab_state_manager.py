"""
Tab State Manager - Tab-specific State Management

Handles tab-specific state including active tab, tab configuration, and persistence.
Uses Qt signals for clean communication.
"""

import logging
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

# Event bus removed - using Qt signals instead

logger = logging.getLogger(__name__)


class TabStateManager(QObject):
    """
    Tab state management using Qt signals.

    Handles:
    - Active tab tracking
    - Tab switching logic via Qt signals
    - Tab-specific state storage
    - Tab state persistence

    Note: Implements IUIStateManager interface methods but doesn't inherit
    to avoid metaclass conflicts with QObject.
    """

    # Qt signals for tab state changes
    tab_switched = pyqtSignal(str, str)  # new_tab, previous_tab
    tab_state_changed = pyqtSignal(str, dict)  # tab_name, state
    tab_state_updated = pyqtSignal(str, dict)  # tab_name, updates
    state_save_requested = pyqtSignal(dict)  # state_data
    state_load_requested = pyqtSignal()

    def __init__(self):
        """Initialize tab state manager."""
        super().__init__()

        # Tab state
        self._active_tab: str = "sequence_builder"
        self._tab_states: dict[str, dict[str, Any]] = {}

    def get_active_tab(self) -> str:
        """Get the active tab."""
        return self._active_tab

    def set_active_tab(self, tab_name: str) -> None:
        """Set the active tab."""
        previous_tab = self._active_tab
        self._active_tab = tab_name

        # Emit Qt signal for tab change
        if previous_tab != tab_name:
            self.tab_switched.emit(tab_name, previous_tab)

    def get_tab_state(self, tab_name: str) -> dict[str, Any]:
        """Get state for a specific tab."""
        return self._tab_states.get(tab_name, {})

    def update_tab_state(self, tab_name: str, state: dict[str, Any]) -> None:
        """Update state for a specific tab."""
        if tab_name not in self._tab_states:
            self._tab_states[tab_name] = {}

        self._tab_states[tab_name].update(state)

        # Emit Qt signal for tab state change
        self.tab_state_updated.emit(tab_name, state)
        # self._event_bus.publish(event)  # Converted to Qt signals

    def clear_tab_state(self, tab_name: str) -> None:
        """Clear state for a specific tab."""
        if tab_name in self._tab_states:
            del self._tab_states[tab_name]

        # Emit Qt signal for tab state cleared
        self.tab_state_changed.emit(tab_name, {})
        # self._event_bus.publish(event)  # Converted to Qt signals

    def get_all_tab_states(self) -> dict[str, dict[str, Any]]:
        """Get all tab states."""
        return self._tab_states.copy()

    def reset_tab_states(self) -> None:
        """Reset all tab states."""
        self._tab_states.clear()
        self._active_tab = "sequence_builder"

        # Emit Qt signal for tab states reset
        self.tab_state_changed.emit("all", {})
        # self._event_bus.publish(event)  # Converted to Qt signals

    def get_state_for_persistence(self) -> dict[str, Any]:
        """Get state data for persistence."""
        return {
            "active_tab": self._active_tab,
            "tab_states": self._tab_states,
        }

    def load_state_from_persistence(self, state: dict[str, Any]) -> None:
        """Load state from persistence data."""
        if "active_tab" in state:
            self._active_tab = state["active_tab"]
        if "tab_states" in state:
            self._tab_states = state["tab_states"]

    # Interface implementation methods
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value (interface implementation)."""
        return self._tab_states.get(self._active_tab, {}).get(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value (interface implementation)."""
        if self._active_tab not in self._tab_states:
            self._tab_states[self._active_tab] = {}
        self._tab_states[self._active_tab][key] = value

    def get_all_settings(self) -> dict[str, Any]:
        """Get all settings (interface implementation)."""
        return self._tab_states.copy()

    def clear_settings(self) -> None:
        """Clear all settings (interface implementation)."""
        self._tab_states.clear()

    def save_state(self) -> None:
        """Save current state to persistent storage (interface implementation)."""
        state_data = {"active_tab": self._active_tab, "tab_states": self._tab_states}
        # Emit Qt signal for save request
        self.state_save_requested.emit(state_data)

    def load_state(self) -> None:
        """Load state from persistent storage (interface implementation)."""
        # Emit Qt signal for load request
        self.state_load_requested.emit()

    def toggle_graph_editor(self) -> bool:
        """Toggle graph editor visibility (interface implementation)."""
        current_state = self.get_setting("graph_editor_visible", False)
        new_state = not current_state
        self.set_setting("graph_editor_visible", new_state)
        return new_state
