"""
Option Picker State Manager - Option Picker Specific State

Handles option picker selection, filters, and other option picker specific state.
Extracted from UIStateManager to follow single responsibility principle.
"""

import logging
from typing import Any, Dict, Optional

from core.events.event_bus import UIEvent, get_event_bus

logger = logging.getLogger(__name__)


class OptionPickerStateManager:
    """
    Option picker state management.
    
    Handles:
    - Option picker selection
    - Option picker filters
    - Option picker specific settings
    - Option picker state persistence
    """

    def __init__(self):
        """Initialize option picker state manager."""
        # Event bus for notifications
        self._event_bus = get_event_bus()

        # Option picker state
        self._option_picker_selection: Optional[str] = None
        self._option_picker_filters: Dict[str, Any] = {}

    def get_option_picker_selection(self) -> Optional[str]:
        """Get option picker selection."""
        return self._option_picker_selection

    def set_option_picker_selection(self, selection: Optional[str]) -> None:
        """Set option picker selection."""
        previous_selection = self._option_picker_selection
        self._option_picker_selection = selection

        # Publish option picker selection change event
        event = UIEvent(
            component="option_picker",
            action="selection_changed",
            state_data={
                "selection": selection,
                "previous_selection": previous_selection,
            },
            source="option_picker_state_manager",
        )
        self._event_bus.publish(event)

    def clear_option_picker_selection(self) -> None:
        """Clear option picker selection."""
        self.set_option_picker_selection(None)

    def get_option_picker_filters(self) -> Dict[str, Any]:
        """Get option picker filters."""
        return self._option_picker_filters.copy()

    def update_option_picker_filters(self, filters: Dict[str, Any]) -> None:
        """Update option picker filters."""
        previous_filters = self._option_picker_filters.copy()
        self._option_picker_filters.update(filters)

        # Publish option picker filters change event
        event = UIEvent(
            component="option_picker",
            action="filters_updated",
            state_data={
                "filters": filters,
                "all_filters": self._option_picker_filters.copy(),
                "previous_filters": previous_filters,
            },
            source="option_picker_state_manager",
        )
        self._event_bus.publish(event)

    def set_option_picker_filter(self, filter_key: str, filter_value: Any) -> None:
        """Set a specific option picker filter."""
        self.update_option_picker_filters({filter_key: filter_value})

    def remove_option_picker_filter(self, filter_key: str) -> bool:
        """Remove a specific option picker filter."""
        if filter_key in self._option_picker_filters:
            previous_value = self._option_picker_filters.pop(filter_key)

            # Publish option picker filter removed event
            event = UIEvent(
                component="option_picker",
                action="filter_removed",
                state_data={
                    "filter_key": filter_key,
                    "previous_value": previous_value,
                },
                source="option_picker_state_manager",
            )
            self._event_bus.publish(event)

            return True
        return False

    def clear_option_picker_filters(self) -> None:
        """Clear all option picker filters."""
        previous_filters = self._option_picker_filters.copy()
        self._option_picker_filters.clear()

        # Publish option picker filters cleared event
        event = UIEvent(
            component="option_picker",
            action="filters_cleared",
            state_data={
                "previous_filters": previous_filters,
            },
            source="option_picker_state_manager",
        )
        self._event_bus.publish(event)

    def get_option_picker_state(self) -> Dict[str, Any]:
        """Get complete option picker state."""
        return {
            "selection": self._option_picker_selection,
            "filters": self._option_picker_filters.copy(),
        }

    def set_option_picker_state(self, state: Dict[str, Any]) -> None:
        """Set complete option picker state."""
        if "selection" in state:
            self.set_option_picker_selection(state["selection"])
        if "filters" in state:
            self._option_picker_filters = state["filters"].copy()

    def reset_option_picker_state(self) -> None:
        """Reset option picker state to defaults."""
        self._option_picker_selection = None
        self._option_picker_filters.clear()

        # Publish option picker state reset event
        event = UIEvent(
            component="option_picker",
            action="state_reset",
            state_data={},
            source="option_picker_state_manager",
        )
        self._event_bus.publish(event)

    def get_state_for_persistence(self) -> Dict[str, Any]:
        """Get state data for persistence."""
        return {
            "option_picker_selection": self._option_picker_selection,
            "option_picker_filters": self._option_picker_filters.copy(),
        }

    def load_state_from_persistence(self, state: Dict[str, Any]) -> None:
        """Load state from persistence data."""
        if "option_picker_selection" in state:
            self._option_picker_selection = state["option_picker_selection"]
        if "option_picker_filters" in state:
            self._option_picker_filters = state["option_picker_filters"].copy()
