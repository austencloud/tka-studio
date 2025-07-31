"""
Component Visibility Manager - UI Component Visibility State

Handles visibility state for various UI components throughout the application.
Uses Qt signals for communication instead of event bus.
"""

import logging

from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)


class ComponentVisibilityManager(QObject):
    """
    Component visibility management using Qt signals.

    Handles:
    - Component visibility state tracking
    - Visibility state changes via Qt signals
    - Component show/hide operations
    - Visibility state persistence
    """

    # Qt signals for component visibility changes
    component_visibility_changed = pyqtSignal(str, bool)  # component, visible
    component_shown = pyqtSignal(str)  # component
    component_hidden = pyqtSignal(str)  # component
    visibility_reset = pyqtSignal()  # all reset

    def __init__(self):
        """Initialize component visibility manager."""
        super().__init__()

        # Component visibility state
        self._component_visibility: dict[str, bool] = {}

    def is_component_visible(self, component: str) -> bool:
        """Check if component is visible."""
        return self._component_visibility.get(component, True)  # Default to visible

    def set_component_visibility(self, component: str, visible: bool) -> None:
        """Set component visibility."""
        previous_state = self._component_visibility.get(component, True)
        self._component_visibility[component] = visible

        # Only emit signal if state actually changed
        if previous_state != visible:
            # Emit Qt signal for component visibility change
            self.component_visibility_changed.emit(component, visible)

            if visible:
                self.component_shown.emit(component)
            else:
                self.component_hidden.emit(component)

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

    def get_all_component_visibility(self) -> dict[str, bool]:
        """Get visibility state for all components."""
        return self._component_visibility.copy()

    def set_multiple_component_visibility(
        self, visibility_states: dict[str, bool]
    ) -> None:
        """Set visibility for multiple components at once."""
        for component, visible in visibility_states.items():
            self.set_component_visibility(component, visible)

    def reset_component_visibility(self) -> None:
        """Reset all component visibility to defaults (all visible)."""
        self._component_visibility.clear()

        # Emit Qt signal for component visibility reset
        self.visibility_reset.emit()

    def get_state_for_persistence(self) -> dict[str, bool]:
        """Get state data for persistence."""
        return self._component_visibility.copy()

    def load_state_from_persistence(self, state: dict[str, bool]) -> None:
        """Load state from persistence data."""
        if isinstance(state, dict):
            self._component_visibility = state.copy()
        else:
            logger.warning("Invalid component visibility state format")
            self._component_visibility = {}
