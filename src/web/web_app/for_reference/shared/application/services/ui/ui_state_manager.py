"""
UI State Management Service - Unified UI State Operations

Consolidates all UI state-related services into a single cohesive service:
- Core settings management (settings_service)
- Settings dialog coordination (settings_dialog_service)
- Tab-specific settings (tab_settings_services)
- Option picker state management (option_picker_state_service)
- Graph editor state (graph_editor_service)
- Graph editor hotkeys (graph_editor_hotkey_service)

This service provides a clean, unified interface for all UI state operations
while maintaining the proven algorithms from the individual services.
Uses Qt signals for clean inter-component communication.
"""

import json
from abc import ABCMeta
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

from desktop.modern.core.interfaces.core_services import IUIStateManager
from desktop.modern.core.interfaces.session_services import ISessionStateTracker


class QObjectABCMeta(type(QObject), ABCMeta):
    """Metaclass that combines QObject's metaclass with ABCMeta."""


class UIComponent(Enum):
    """UI component types."""

    MAIN_WINDOW = "main_window"
    SEQUENCE_EDITOR = "sequence_editor"
    GRAPH_EDITOR = "graph_editor"
    OPTION_PICKER = "option_picker"
    SETTINGS_DIALOG = "settings_dialog"
    BEAT_FRAME = "beat_frame"
    DICTIONARY_BROWSER = "dictionary_browser"


class TabType(Enum):
    """Tab types in the application."""

    SEQUENCE_BUILDER = "sequence_builder"
    DICTIONARY = "dictionary"
    LEARN = "learn"
    WRITE = "write"
    SETTINGS = "settings"


@dataclass
class UIState:
    """Complete UI state representation."""

    # Window state
    window_geometry: dict[str, int] = field(default_factory=dict)
    window_maximized: bool = False

    # Component visibility
    component_visibility: dict[str, bool] = field(default_factory=dict)

    # Tab states
    active_tab: str = "sequence_builder"
    tab_states: dict[str, dict[str, Any]] = field(default_factory=dict)

    # Option picker state
    option_picker_selection: str | None = None
    option_picker_filters: dict[str, Any] = field(default_factory=dict)

    # Settings
    user_settings: dict[str, Any] = field(default_factory=dict)


class UIStateManager(QObject, IUIStateManager, metaclass=QObjectABCMeta):
    """
    Unified UI state management service consolidating all UI state operations.

    Provides comprehensive UI state management including:
    - Settings management (get, set, save, load)
    - Tab state coordination
    - Component visibility management
    - Graph editor state management
    - Option picker state management
    - Qt signal-driven state synchronization
    """

    # Qt Signals for state changes
    setting_changed = pyqtSignal(str, object)  # key, value
    tab_state_changed = pyqtSignal(str, dict)  # tab_name, state
    tab_switched = pyqtSignal(str, str)  # previous_tab, new_tab
    ui_state_changed = pyqtSignal(str, object)  # component, state_data
    component_visibility_changed = pyqtSignal(str, bool)  # component, visible
    hotkey_triggered = pyqtSignal(str)  # hotkey_name
    window_geometry_changed = pyqtSignal(dict)  # geometry

    def __init__(self, session_service: ISessionStateTracker | None = None):
        QObject.__init__(self)

        # Core state
        self._ui_state = UIState()

        # Settings file path - use modern directory
        # Navigate from: src/application/services/ui/ -> modern/
        modern_dir = Path(__file__).parent.parent.parent.parent.parent
        self._settings_file = modern_dir / "user_settings.json"

        # Session service integration (optional for backward compatibility)
        self._session_service = session_service

        # Default settings
        self._default_settings = self._load_default_settings()

        # Hotkey bindings
        self._hotkey_bindings: dict[str, Callable] = {}

        # Load saved state
        self._load_state()

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self._ui_state.user_settings.get(
            key, self._default_settings.get(key, default)
        )

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        self._ui_state.user_settings[key] = value
        self._save_state()

        # Trigger session auto-save for settings changes
        if self._session_service:
            self._session_service.mark_interaction()

        # Emit Qt signal for setting change
        self.setting_changed.emit(key, value)

    def get_tab_state(self, tab_name: str) -> dict[str, Any]:
        """Get state for a specific tab."""
        return self._ui_state.tab_states.get(tab_name, {})

    def get_all_settings(self) -> dict[str, Any]:
        """Get all settings."""
        return self._ui_state.user_settings.copy()

    def clear_settings(self) -> None:
        """Clear all settings."""
        self._ui_state.user_settings.clear()
        self._save_state()

    def save_state(self) -> None:
        """Save current state to persistent storage."""
        self._save_state()

    def load_state(self) -> None:
        """Load state from persistent storage."""
        self._load_state()

    def toggle_graph_editor(self) -> bool:
        """Toggle graph editor visibility."""
        current_visibility = self._ui_state.component_visibility.get(
            "graph_editor", False
        )
        new_visibility = not current_visibility
        self._ui_state.component_visibility["graph_editor"] = new_visibility
        self.component_visibility_changed.emit("graph_editor", new_visibility)
        self._save_state()
        return new_visibility

    def update_tab_state(self, tab_name: str, state: dict[str, Any]) -> None:
        """Update state for a specific tab."""
        if tab_name not in self._ui_state.tab_states:
            self._ui_state.tab_states[tab_name] = {}

        self._ui_state.tab_states[tab_name].update(state)
        self._save_state()

        # Emit Qt signal for tab state change
        self.tab_state_changed.emit(tab_name, state)

    def set_active_tab(self, tab_name: str) -> None:
        """Set the active tab."""
        previous_tab = self._ui_state.active_tab
        self._ui_state.active_tab = tab_name
        self._save_state()

        # Trigger session auto-save for tab changes
        if self._session_service:
            self._session_service.update_ui_state(
                active_tab=tab_name,
                beat_layout=self._ui_state.tab_states.get("beat_layout", {}),
                component_visibility=self._ui_state.component_visibility,
            )

        # Emit Qt signal for tab switch
        self.tab_switched.emit(previous_tab, tab_name)

    def get_active_tab(self) -> str:
        """Get the current active tab."""
        return self._ui_state.active_tab

    def set_component_visibility(self, component_name: str, visible: bool) -> None:
        """Set visibility state for a component."""
        self._ui_state.component_visibility[component_name] = visible
        self._save_state()

        # Trigger session auto-save for visibility changes
        if self._session_service:
            self._session_service.mark_interaction()

        # Emit Qt signal for visibility change
        self.component_visibility_changed.emit(component_name, visible)

    def get_component_visibility(
        self, component_name: str, default: bool = True
    ) -> bool:
        """Get visibility state for a component."""
        return self._ui_state.component_visibility.get(component_name, default)

    def toggle_component_visibility(self, component_name: str) -> bool:
        """Toggle visibility for a component and return new state."""
        current_visibility = self.get_component_visibility(component_name)
        new_visibility = not current_visibility
        self.set_component_visibility(component_name, new_visibility)
        return new_visibility

    def set_option_picker_selection(self, selection: str) -> None:
        """Set option picker selection."""
        self._ui_state.option_picker_selection = selection
        self._save_state()

    def get_option_picker_selection(self) -> str | None:
        """Get option picker selection."""
        return self._ui_state.option_picker_selection

    def set_option_picker_filter(self, filter_name: str, filter_value: Any) -> None:
        """Set an option picker filter."""
        self._ui_state.option_picker_filters[filter_name] = filter_value
        self._save_state()

    def get_option_picker_filter(self, filter_name: str, default: Any = None) -> Any:
        """Get an option picker filter value."""
        return self._ui_state.option_picker_filters.get(filter_name, default)

    def register_hotkey(self, hotkey_name: str, callback: Callable) -> None:
        """Register a hotkey callback."""
        self._hotkey_bindings[hotkey_name] = callback

    def trigger_hotkey(self, hotkey_name: str) -> bool:
        """Trigger a hotkey callback."""
        if hotkey_name in self._hotkey_bindings:
            try:
                self._hotkey_bindings[hotkey_name]()
                # Emit Qt signal for hotkey trigger
                self.hotkey_triggered.emit(hotkey_name)
                return True
            except Exception as e:
                print(f"Error executing hotkey {hotkey_name}: {e}")
        return False

    def get_window_geometry(self) -> dict[str, int]:
        """Get window geometry."""
        return self._ui_state.window_geometry.copy()

    def set_window_geometry(self, geometry: dict[str, int]) -> None:
        """Set window geometry."""
        self._ui_state.window_geometry.update(geometry)
        self._save_state()

        # Emit Qt signal for window geometry change
        self.window_geometry_changed.emit(geometry)

    def get_ui_state(self, key: str = None):
        """Get UI state or specific key."""
        if key:
            return getattr(self._ui_state, key, None)
        return self._ui_state

    def set_ui_state(self, key: str, value):
        """Set UI state value."""
        if hasattr(self._ui_state, key):
            setattr(self._ui_state, key, value)
            self._save_state()

    def update_ui_state(self, updates: dict):
        """Update multiple UI state values."""
        for key, value in updates.items():
            if hasattr(self._ui_state, key):
                setattr(self._ui_state, key, value)
        self._save_state()

    def reset_ui_state(self):
        """Reset UI state to defaults."""
        self._ui_state = UIState()
        self._save_state()

    def save_ui_state(self) -> bool:
        """Save UI state to file."""
        return self._save_state()

    def load_ui_state(self) -> bool:
        """Load UI state from file."""
        return self._load_state()

    def update_ui_state_with_session(
        self,
        active_tab: str | None = None,
        beat_layout: dict[str, Any] | None = None,
        component_visibility: dict[str, bool] | None = None,
    ) -> None:
        """Update UI state and save to session."""
        if active_tab:
            self._ui_state.active_tab = active_tab

        if beat_layout:
            self._ui_state.tab_states.setdefault("beat_layout", {}).update(beat_layout)

        if component_visibility:
            self._ui_state.component_visibility.update(component_visibility)

        self._save_state()

        # Trigger session auto-save
        if self._session_service:
            self._session_service.mark_interaction()

    def restore_session_on_startup(self) -> bool:
        """Restore session state on application startup."""
        try:
            # Load state from file
            loaded = self._load_state()

            # Restore session state if available
            if self._session_service and loaded:
                self._session_service.update_ui_state(
                    active_tab=self._ui_state.active_tab,
                    beat_layout=self._ui_state.tab_states.get("beat_layout", {}),
                    component_visibility=self._ui_state.component_visibility,
                )

            return loaded
        except Exception as e:
            print(f"Error restoring session on startup: {e}")
            return False

    def set_session_service(self, session_service: ISessionStateTracker) -> None:
        """Set the session service for integration (used by DI container)."""
        self._session_service = session_service

    def _load_default_settings(self) -> dict[str, Any]:
        """Load default settings configuration."""
        return {
            "theme": "default",
            "language": "en",
            "auto_save": True,
            "auto_save_interval": 300,  # 5 minutes
            "show_tooltips": True,
            "window_opacity": 1.0,
            "sequence_builder": {
                "grid_size": 50,
                "snap_to_grid": True,
                "show_grid": True,
            },
            "dictionary": {"filter_mode": "all", "sort_order": "alphabetical"},
        }

    def _load_state(self) -> bool:
        """Load UI state from file."""
        try:
            if self._settings_file.exists():
                with open(self._settings_file, encoding="utf-8") as f:
                    data = json.load(f)

                # Update state with loaded data
                if "window_geometry" in data:
                    self._ui_state.window_geometry = data["window_geometry"]
                if "window_maximized" in data:
                    self._ui_state.window_maximized = data["window_maximized"]
                if "component_visibility" in data:
                    self._ui_state.component_visibility = data["component_visibility"]
                if "active_tab" in data:
                    self._ui_state.active_tab = data["active_tab"]
                if "tab_states" in data:
                    self._ui_state.tab_states = data["tab_states"]
                if "option_picker_selection" in data:
                    self._ui_state.option_picker_selection = data[
                        "option_picker_selection"
                    ]
                if "option_picker_filters" in data:
                    self._ui_state.option_picker_filters = data["option_picker_filters"]
                if "user_settings" in data:
                    self._ui_state.user_settings = data["user_settings"]

                return True
            else:
                # No saved state, use defaults
                self._ui_state.user_settings = self._default_settings.copy()
                return False

        except Exception as e:
            print(f"Error loading UI state: {e}")
            # Use defaults on error
            self._ui_state.user_settings = self._default_settings.copy()
            return False

    def _save_state(self) -> bool:
        """Save current UI state to file."""
        try:
            # Ensure directory exists
            self._settings_file.parent.mkdir(parents=True, exist_ok=True)

            # Prepare data for serialization
            data = {
                "window_geometry": self._ui_state.window_geometry,
                "window_maximized": self._ui_state.window_maximized,
                "component_visibility": self._ui_state.component_visibility,
                "active_tab": self._ui_state.active_tab,
                "tab_states": self._ui_state.tab_states,
                "option_picker_selection": self._ui_state.option_picker_selection,
                "option_picker_filters": self._ui_state.option_picker_filters,
                "user_settings": self._ui_state.user_settings,
            }

            # Write to file
            with open(self._settings_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"Error saving UI state: {e}")
            return False
