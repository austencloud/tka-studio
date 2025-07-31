"""
State Manager for TKA Unified Launcher.
Manages application state and window state persistence.
"""

from typing import Any, Dict

from PyQt6.QtCore import QObject, pyqtSignal


class StateManager(QObject):
    """Manages launcher state and persistence."""

    # Signals
    state_changed = pyqtSignal(str, object)  # key, value

    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self._state: Dict[str, Any] = {}

        # Load initial state
        self._load_state()

    def _load_state(self):
        """Load state from settings."""
        # Load window state
        window_state = self.settings_manager.get_window_state()
        self._state.update(window_state)

        # Load other persistent state
        self._state.update(
            {
                "last_launched_app": self.settings_manager.get(
                    "last_launched_app", None
                ),
                "launch_count": self.settings_manager.get("launch_count", 0),
                "first_run": self.settings_manager.get("first_run", True),
            }
        )

    def get(self, key: str, default: Any = None) -> Any:
        """Get a state value."""
        return self._state.get(key, default)

    def set(self, key: str, value: Any, persist: bool = True):
        """Set a state value."""
        old_value = self._state.get(key)
        self._state[key] = value

        # Persist to settings if requested
        if persist:
            self.settings_manager.set(key, value)

        # Emit change signal
        if old_value != value:
            self.state_changed.emit(key, value)

    def increment(self, key: str, amount: int = 1, persist: bool = True):
        """Increment a numeric state value."""
        current = self.get(key, 0)
        self.set(key, current + amount, persist)

    def get_window_state(self) -> Dict[str, Any]:
        """Get current window state."""
        return {
            "mode": self.get("mode", "window"),
            "window_geometry": self.get("window_geometry"),
            "dock_geometry": self.get("dock_geometry"),
            "target_screen": self.get("target_screen", 0),
            "dock_screen": self.get("dock_screen", 0),
        }

    def save_window_state(
        self, geometry: Dict[str, int], mode: str, screen_index: int = 0
    ):
        """Save window state."""
        self.set("mode", mode)
        self.set("target_screen", screen_index)

        if mode == "window":
            self.set("window_geometry", geometry)
        elif mode == "docked":
            self.set("dock_geometry", geometry)
            self.set("dock_screen", screen_index)

    def mark_app_launched(self, app_id: str):
        """Mark an application as launched."""
        self.set("last_launched_app", app_id)
        self.increment("launch_count")

        # Mark as not first run
        if self.get("first_run"):
            self.set("first_run", False)

    def is_first_run(self) -> bool:
        """Check if this is the first run."""
        return self.get("first_run", True)

    def get_launch_count(self) -> int:
        """Get total launch count."""
        return self.get("launch_count", 0)

    def reset_state(self):
        """Reset all state to defaults."""
        self._state.clear()
        self.settings_manager.reset_to_defaults()
        self._load_state()
