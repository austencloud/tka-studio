"""
Browse State Service - State Persistence Logic

Handles state saving/loading for browse tab settings, filters, and selections.
Based on Legacy audit showing complex state management that needs careful porting.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from desktop.modern.domain.models.browse_models import (
    BrowseState,
    FilterType,
    NavigationMode,
    SortMethod,
)


class BrowseStateService:
    """
    REPLACES: Complex state persistence scattered throughout legacy code

    Handles all browse tab state persistence - this was identified as genuinely
    complex in the legacy audit due to multiple state types that must survive restarts.
    """

    def __init__(self, settings_file: Path):
        """Initialize with settings file path."""
        self.settings_file = settings_file
        self._current_state: BrowseState | None = None

    def load_browse_state(self) -> BrowseState:
        """Load browse state from persistent storage."""
        if self._current_state is not None:
            return self._current_state

        # Try to load from settings file
        if self.settings_file.exists():
            try:
                with open(self.settings_file) as f:
                    data = json.load(f)
                    browse_data = data.get("browse_tab", {})

                self._current_state = BrowseState(
                    filter_type=browse_data.get("filter_type"),
                    filter_values=browse_data.get("filter_values"),
                    selected_sequence=browse_data.get("selected_sequence"),
                    selected_variation=browse_data.get("selected_variation"),
                    navigation_mode=browse_data.get(
                        "navigation_mode", NavigationMode.FILTER_SELECTION.value
                    ),
                    sort_method=browse_data.get(
                        "sort_method", SortMethod.ALPHABETICAL.value
                    ),
                )
            except Exception as e:
                print(f"Error loading browse state: {e}")
                self._current_state = BrowseState()
        else:
            self._current_state = BrowseState()

        return self._current_state

    def save_browse_state(self, state: BrowseState) -> None:
        """Save browse state to persistent storage."""
        self._current_state = state

        # Load existing settings or create new
        settings_data = {}
        if self.settings_file.exists():
            try:
                with open(self.settings_file) as f:
                    settings_data = json.load(f)
            except Exception:
                settings_data = {}

        # Update browse tab section
        settings_data["browse_tab"] = {
            "filter_type": state.filter_type,
            "filter_values": state.filter_values,
            "selected_sequence": state.selected_sequence,
            "selected_variation": state.selected_variation,
            "navigation_mode": state.navigation_mode,
            "sort_method": state.sort_method,
        }

        # Save back to file
        try:
            # Ensure parent directory exists
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.settings_file, "w") as f:
                json.dump(settings_data, f, indent=2)
        except Exception as e:
            print(f"Error saving browse state: {e}")

    def set_filter(self, filter_type: FilterType, filter_values: Any) -> None:
        """Update current filter and save state."""
        current_state = self.load_browse_state()
        updated_state = BrowseState(
            filter_type=filter_type.value if filter_type else None,
            filter_values=filter_values,
            selected_sequence=current_state.selected_sequence,
            selected_variation=current_state.selected_variation,
            navigation_mode=current_state.navigation_mode,
            sort_method=current_state.sort_method,
        )
        self.save_browse_state(updated_state)

    def set_selected_sequence(
        self, sequence_id: str | None, variation: int | None = None
    ) -> None:
        """Update selected sequence and save state."""
        current_state = self.load_browse_state()
        updated_state = BrowseState(
            filter_type=current_state.filter_type,
            filter_values=current_state.filter_values,
            selected_sequence=sequence_id,
            selected_variation=variation,
            navigation_mode=current_state.navigation_mode,
            sort_method=current_state.sort_method,
        )
        self.save_browse_state(updated_state)

    def set_sort_method(self, sort_method: SortMethod) -> None:
        """Update sort method and save state."""
        current_state = self.load_browse_state()
        updated_state = BrowseState(
            filter_type=current_state.filter_type,
            filter_values=current_state.filter_values,
            selected_sequence=current_state.selected_sequence,
            selected_variation=current_state.selected_variation,
            navigation_mode=current_state.navigation_mode,
            sort_method=sort_method.value,
        )
        self.save_browse_state(updated_state)

    def get_current_sort_method(self) -> SortMethod:
        """Get current sort method."""
        state = self.load_browse_state()
        try:
            return SortMethod(state.sort_method)
        except ValueError:
            return SortMethod.ALPHABETICAL

    def get_sort_order(self) -> str:
        """Get current sort order as string (compatibility method)."""
        sort_method = self.get_current_sort_method()
        # Convert SortMethod enum to string format expected by components
        sort_mapping = {
            SortMethod.ALPHABETICAL: "alphabetical",
            SortMethod.SEQUENCE_LENGTH: "length",
            SortMethod.DIFFICULTY_LEVEL: "level",
            SortMethod.DATE_ADDED: "date_added",
        }
        return sort_mapping.get(sort_method, "alphabetical")

    def clear_selection(self) -> None:
        """Clear selected sequence."""
        self.set_selected_sequence(None, None)
