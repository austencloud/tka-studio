"""
UI Coordinator - Orchestrates UI State Management

Coordinates all UI state management components and provides a unified interface.
Replaces the monolithic UIStateManager with a composition of focused managers.
"""

import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from application.services.ui.settings.settings_manager import SettingsManager
from application.services.ui.state.component_visibility_manager import (
    ComponentVisibilityManager,
)
from application.services.ui.state.graph_editor_state_manager import (
    GraphEditorStateManager,
)
from application.services.ui.state.hotkey_registry import HotkeyRegistry
from application.services.ui.state.option_picker_state_manager import (
    OptionPickerStateManager,
)
from application.services.ui.state.tab_state_manager import TabStateManager
from application.services.ui.state.window_state_manager import WindowStateManager
from core.events.event_bus import UIEvent, get_event_bus
from core.interfaces.core_services import IUIStateManager
from core.interfaces.session_services import ISessionStateTracker

logger = logging.getLogger(__name__)


class UICoordinator(IUIStateManager):
    """
    UI state coordination service.

    Orchestrates focused UI state managers:
    - SettingsManager: Core settings operations
    - WindowStateManager: Window geometry and state
    - TabStateManager: Tab navigation and state
    - ComponentVisibilityManager: Component visibility
    - HotkeyRegistry: Hotkey bindings and handling

    Provides the same interface as the original UIStateManager but with
    better separation of concerns and focused responsibilities.
    """

    def __init__(self, session_service: Optional[ISessionStateTracker] = None):
        """Initialize UI coordinator with focused managers."""
        # Initialize focused managers
        self.settings = SettingsManager()
        self.window_state = WindowStateManager()
        self.tab_state = TabStateManager()
        self.component_visibility = ComponentVisibilityManager()
        self.graph_editor_state = GraphEditorStateManager()
        self.option_picker_state = OptionPickerStateManager()
        self.hotkey_registry = HotkeyRegistry()

        # Session service integration
        self._session_service = session_service

        # Event bus for coordination
        self._event_bus = get_event_bus()

        # State file for persistence
        modern_dir = Path(__file__).parent.parent.parent.parent.parent.parent
        self._state_file = modern_dir / "ui_state.json"

        # Load saved state
        self._load_state()

        # Setup event subscriptions for coordination
        self._setup_event_subscriptions()

    # Settings delegation
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.settings.get_setting(key, default)

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        self.settings.set_setting(key, value)

        # Trigger session auto-save for settings changes
        if self._session_service:
            self._session_service.mark_interaction()

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings."""
        return self.settings.get_all_settings()

    def clear_settings(self) -> None:
        """Clear all settings."""
        self.settings.clear_settings()

    # Tab state delegation
    def get_active_tab(self) -> str:
        """Get the active tab."""
        return self.tab_state.get_active_tab()

    def set_active_tab(self, tab_name: str) -> None:
        """Set the active tab."""
        self.tab_state.set_active_tab(tab_name)

        # Trigger session auto-save for tab changes
        if self._session_service:
            self._session_service.update_ui_state(
                active_tab=tab_name,
                beat_layout=self.tab_state.get_tab_state("beat_layout"),
                component_visibility=self.component_visibility.get_all_component_visibility(),
            )

    def get_tab_state(self, tab_name: str) -> Dict[str, Any]:
        """Get state for a specific tab."""
        return self.tab_state.get_tab_state(tab_name)

    def update_tab_state(self, tab_name: str, state: Dict[str, Any]) -> None:
        """Update state for a specific tab."""
        self.tab_state.update_tab_state(tab_name, state)

    # Window state delegation
    def get_window_geometry(self) -> Dict[str, int]:
        """Get window geometry."""
        return self.window_state.get_window_geometry()

    def set_window_geometry(self, geometry: Dict[str, int]) -> None:
        """Set window geometry."""
        self.window_state.set_window_geometry(geometry)

    def is_window_maximized(self) -> bool:
        """Check if window is maximized."""
        return self.window_state.is_window_maximized()

    def set_window_maximized(self, maximized: bool) -> None:
        """Set window maximized state."""
        self.window_state.set_window_maximized(maximized)

    # Component visibility delegation
    def is_component_visible(self, component: str) -> bool:
        """Check if component is visible."""
        return self.component_visibility.is_component_visible(component)

    def set_component_visibility(self, component: str, visible: bool) -> None:
        """Set component visibility."""
        self.component_visibility.set_component_visibility(component, visible)

    # Hotkey delegation
    def register_hotkey(self, key_combination: str, callback: Callable) -> None:
        """Register a hotkey binding."""
        self.hotkey_registry.register_hotkey(key_combination, callback)

    def handle_hotkey(self, key_combination: str) -> bool:
        """Handle hotkey press."""
        return self.hotkey_registry.handle_hotkey(key_combination)

    # Graph editor state delegation
    def get_graph_editor_state(self) -> Dict[str, Any]:
        """Get graph editor state."""
        return self.graph_editor_state.get_graph_editor_state()

    def toggle_graph_editor(self) -> bool:
        """Toggle graph editor visibility."""
        return self.graph_editor_state.toggle_graph_editor()

    def set_graph_editor_height(self, height: int) -> None:
        """Set graph editor height."""
        self.graph_editor_state.set_graph_editor_height(height)

    # Option picker state delegation
    def get_option_picker_state(self) -> Dict[str, Any]:
        """Get option picker state."""
        return self.option_picker_state.get_option_picker_state()

    def set_option_picker_selection(self, selection: Optional[str]) -> None:
        """Set option picker selection."""
        self.option_picker_state.set_option_picker_selection(selection)

    def update_option_picker_filters(self, filters: Dict[str, Any]) -> None:
        """Update option picker filters."""
        self.option_picker_state.update_option_picker_filters(filters)

    # Persistence operations
    def save_state(self) -> None:
        """Save state to persistent storage."""
        self._save_state()

    def load_state(self) -> None:
        """Load state from persistent storage."""
        self._load_state()

    def reset_to_defaults(self) -> None:
        """Reset all state to defaults."""
        self.settings.reset_to_defaults()
        self.window_state.reset_window_state()
        self.tab_state.reset_tab_states()
        self.component_visibility.reset_component_visibility()
        self.graph_editor_state.reset_graph_editor_state()
        self.option_picker_state.reset_option_picker_state()
        self.hotkey_registry.clear_all_hotkeys()

    def export_settings(self, file_path: Path) -> bool:
        """Export settings to file."""
        return self.settings.export_settings(file_path)

    def import_settings(self, file_path: Path) -> bool:
        """Import settings from file."""
        return self.settings.import_settings(file_path)

    def _load_state(self) -> None:
        """Load state from file."""
        try:
            if self._state_file.exists():
                with open(self._state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Load state into each manager
                if "window_state" in data:
                    self.window_state.load_state_from_persistence(data["window_state"])
                if "tab_state" in data:
                    self.tab_state.load_state_from_persistence(data["tab_state"])
                if "component_visibility" in data:
                    self.component_visibility.load_state_from_persistence(
                        data["component_visibility"]
                    )
                if "graph_editor_state" in data:
                    self.graph_editor_state.load_state_from_persistence(
                        data["graph_editor_state"]
                    )
                if "option_picker_state" in data:
                    self.option_picker_state.load_state_from_persistence(
                        data["option_picker_state"]
                    )
                if "hotkey_registry" in data:
                    self.hotkey_registry.load_state_from_persistence(
                        data["hotkey_registry"]
                    )

        except Exception as e:
            logger.error(f"Failed to load UI state: {e}")

    def _save_state(self) -> None:
        """Save state to file."""
        try:
            # Ensure directory exists
            self._state_file.parent.mkdir(parents=True, exist_ok=True)

            # Collect state from all managers
            state_data = {
                "window_state": self.window_state.get_state_for_persistence(),
                "tab_state": self.tab_state.get_state_for_persistence(),
                "component_visibility": self.component_visibility.get_state_for_persistence(),
                "graph_editor_state": self.graph_editor_state.get_state_for_persistence(),
                "option_picker_state": self.option_picker_state.get_state_for_persistence(),
                "hotkey_registry": self.hotkey_registry.get_state_for_persistence(),
            }

            with open(self._state_file, "w", encoding="utf-8") as f:
                json.dump(state_data, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to save UI state: {e}")

    def _setup_event_subscriptions(self) -> None:
        """Setup event subscriptions for coordination."""
        # Subscribe to events that require coordination between managers
        # This is where cross-cutting concerns are handled
        pass

    # Session integration methods (for backward compatibility)
    def set_session_service(self, session_service: ISessionStateTracker) -> None:
        """Set the session service for integration (used by DI container)."""
        self._session_service = session_service

    def update_current_sequence_with_session(
        self, sequence_data: Any, sequence_id: str
    ) -> None:
        """Update current sequence and save to session."""
        if self._session_service:
            self._session_service.update_current_sequence(sequence_data, sequence_id)

    def update_workbench_selection_with_session(
        self, beat_index: Optional[int], beat_data: Any, start_position: Any
    ) -> None:
        """Update workbench selection and save to session."""
        if self._session_service:
            self._session_service.update_workbench_selection(
                beat_index, beat_data, start_position
            )

    def update_graph_editor_with_session(
        self,
        visible: bool,
        beat_index: Optional[int] = None,
        beat_data: Any = None,
        start_position: Any = None,
    ) -> None:
        """Update graph editor state and save to session."""
        # Update local state
        self.graph_editor_state.set_graph_editor_visible(visible)

        # Update session
        if self._session_service:
            self._session_service.update_graph_editor(
                visible, beat_index, beat_data, start_position
            )

    def update_ui_state_with_session(
        self,
        active_tab: Optional[str] = None,
        beat_layout: Optional[Dict[str, Any]] = None,
        component_visibility: Optional[Dict[str, bool]] = None,
        graph_editor_visible: Optional[bool] = None,
        graph_editor_height: Optional[int] = None,
        option_picker_selection: Optional[str] = None,
        option_picker_filters: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Update UI state and save to session."""
        # Update local state
        if active_tab is not None:
            self.tab_state.set_active_tab(active_tab)
        if beat_layout is not None:
            self.tab_state.update_tab_state("beat_layout", beat_layout)
        if component_visibility is not None:
            self.component_visibility.set_multiple_component_visibility(
                component_visibility
            )
        if graph_editor_visible is not None:
            self.graph_editor_state.set_graph_editor_visible(graph_editor_visible)
        if graph_editor_height is not None:
            self.graph_editor_state.set_graph_editor_height(graph_editor_height)
        if option_picker_selection is not None:
            self.option_picker_state.set_option_picker_selection(
                option_picker_selection
            )
        if option_picker_filters is not None:
            self.option_picker_state.update_option_picker_filters(option_picker_filters)

        # Update session
        if self._session_service:
            self._session_service.update_ui_state(
                active_tab=active_tab,
                beat_layout=beat_layout,
                component_visibility=component_visibility,
            )

    def restore_session_on_startup(self) -> bool:
        """Restore session state on application startup."""
        if not self._session_service:
            return False

        try:
            session_data = self._session_service.get_session_data()
            if not session_data:
                return False

            # Restore UI state from session
            if "ui_state" in session_data:
                ui_state = session_data["ui_state"]
                self.update_ui_state_with_session(
                    active_tab=ui_state.get("active_tab"),
                    beat_layout=ui_state.get("beat_layout"),
                    component_visibility=ui_state.get("component_visibility"),
                )

            return True
        except Exception as e:
            logger.error(f"Failed to restore session on startup: {e}")
            return False
