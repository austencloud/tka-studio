"""
Option Picker State Manager - Option Picker Specific State

Handles option picker selection, filters, and other option picker specific state.
Uses Qt signals for clean communication.
"""

import logging
from typing import Any, Optional

from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)


class OptionPickerStateManager(QObject):
    """
    Option picker state management using Qt signals.

    Handles:
    - Option picker selection
    - Option picker filters via Qt signals
    - Option picker specific settings
    - Option picker state persistence
    """

    # Qt signals for option picker state changes
    selection_changed = pyqtSignal(str)  # selection
    filter_changed = pyqtSignal(str, object)  # filter_name, filter_value
    state_reset = pyqtSignal()  # state reset

    def __init__(self):
        """Initialize option picker state manager."""
        super().__init__()

        # Option picker state
        self._option_picker_selection: Optional[str] = None
        self._option_picker_filters: dict[str, Any] = {}

    def get_option_picker_selection(self) -> Optional[str]:
        """Get option picker selection."""
        return self._option_picker_selection

    def set_option_picker_selection(self, selection: Optional[str]) -> None:
        """Set option picker selection."""
        previous_selection = self._option_picker_selection
        self._option_picker_selection = selection

        # Emit Qt signal for selection change
        if previous_selection != selection and selection is not None:
            self.selection_changed.emit(selection)

    def clear_option_picker_selection(self) -> None:
        """Clear option picker selection."""
        self.set_option_picker_selection(None)

    def get_option_picker_filters(self) -> dict[str, Any]:
        """Get option picker filters."""
        return self._option_picker_filters.copy()

    def update_option_picker_filters(self, filters: dict[str, Any]) -> None:
        """Update option picker filters."""
        previous_filters = self._option_picker_filters.copy()
        self._option_picker_filters.update(filters)

        # Emit Qt signals for each filter change
        for filter_key, filter_value in filters.items():
            self.filter_changed.emit(filter_key, filter_value)

    def set_option_picker_filter(self, filter_key: str, filter_value: Any) -> None:
        """Set a specific option picker filter."""
        self.update_option_picker_filters({filter_key: filter_value})

    def remove_option_picker_filter(self, filter_key: str) -> bool:
        """Remove a specific option picker filter."""
        if filter_key in self._option_picker_filters:
            previous_value = self._option_picker_filters.pop(filter_key)

            # Emit Qt signal for filter removal (set to None)
            self.filter_changed.emit(filter_key, None)

            return True
        return False

    def clear_option_picker_filters(self) -> None:
        """Clear all option picker filters."""
        previous_filters = self._option_picker_filters.copy()
        self._option_picker_filters.clear()

        # Emit Qt signal for state reset (covers filter clearing)
        self.state_reset.emit()

    def get_option_picker_state(self) -> dict[str, Any]:
        """Get complete option picker state."""
        return {
            "selection": self._option_picker_selection,
            "filters": self._option_picker_filters.copy(),
        }

    def set_option_picker_state(self, state: dict[str, Any]) -> None:
        """Set complete option picker state."""
        if "selection" in state:
            self.set_option_picker_selection(state["selection"])
        if "filters" in state:
            self._option_picker_filters = state["filters"].copy()

    def reset_option_picker_state(self) -> None:
        """Reset option picker state to defaults."""
        self._option_picker_selection = None
        self._option_picker_filters.clear()

        # Emit Qt signal for state reset
        self.state_reset.emit()

    def get_state_for_persistence(self) -> dict[str, Any]:
        """Get state data for persistence."""
        return {
            "option_picker_selection": self._option_picker_selection,
            "option_picker_filters": self._option_picker_filters.copy(),
        }

    def load_state_from_persistence(self, state: dict[str, Any]) -> None:
        """Load state from persistence data."""
        if "option_picker_selection" in state:
            self._option_picker_selection = state["option_picker_selection"]
        if "option_picker_filters" in state:
            self._option_picker_filters = state["option_picker_filters"].copy()
