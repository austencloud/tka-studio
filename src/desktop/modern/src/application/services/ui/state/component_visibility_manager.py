"""
Component Visibility Manager - UI Component Visibility State

Handles visibility state for various UI components throughout the application.
Extracted from UIStateManager to follow single responsibility principle.
"""

import logging
from typing import Dict

from core.events.event_bus import UIEvent, get_event_bus

logger = logging.getLogger(__name__)


class ComponentVisibilityManager:
    """
    Component visibility management.
    
    Handles:
    - Component visibility state tracking
    - Visibility state changes
    - Component show/hide operations
    - Visibility state persistence
    """

    def __init__(self):
        """Initialize component visibility manager."""
        # Event bus for notifications
        self._event_bus = get_event_bus()

        # Component visibility state
        self._component_visibility: Dict[str, bool] = {}

    def is_component_visible(self, component: str) -> bool:
        """Check if component is visible."""
        return self._component_visibility.get(component, True)  # Default to visible

    def set_component_visibility(self, component: str, visible: bool) -> None:
        """Set component visibility."""
        previous_state = self._component_visibility.get(component, True)
        self._component_visibility[component] = visible

        # Only publish event if state actually changed
        if previous_state != visible:
            # Publish component visibility change event
            event = UIEvent(
                component="component_visibility",
                action="changed",
                state_data={
                    "component": component,
                    "visible": visible,
                    "previous_state": previous_state,
                },
                source="component_visibility_manager",
            )
            self._event_bus.publish(event)

    def show_component(self, component: str) -> None:
        """Show a component."""
        self.set_component_visibility(component, True)

    def hide_component(self, component: str) -> None:
        """Hide a component."""
        self.set_component_visibility(component, False)

    def toggle_component_visibility(self, component: str) -> bool:
        """Toggle component visibility and return new state."""
        current_state = self.is_component_visible(component)
        new_state = not current_state
        self.set_component_visibility(component, new_state)
        return new_state

    def get_all_component_visibility(self) -> Dict[str, bool]:
        """Get visibility state for all components."""
        return self._component_visibility.copy()

    def set_multiple_component_visibility(self, visibility_states: Dict[str, bool]) -> None:
        """Set visibility for multiple components at once."""
        for component, visible in visibility_states.items():
            self.set_component_visibility(component, visible)

    def reset_component_visibility(self) -> None:
        """Reset all component visibility to defaults (all visible)."""
        self._component_visibility.clear()

        # Publish component visibility reset event
        event = UIEvent(
            component="component_visibility",
            action="reset",
            state_data={},
            source="component_visibility_manager",
        )
        self._event_bus.publish(event)

    def get_state_for_persistence(self) -> Dict[str, bool]:
        """Get state data for persistence."""
        return self._component_visibility.copy()

    def load_state_from_persistence(self, state: Dict[str, bool]) -> None:
        """Load state from persistence data."""
        if isinstance(state, dict):
            self._component_visibility = state.copy()
        else:
            logger.warning("Invalid component visibility state format")
            self._component_visibility = {}
