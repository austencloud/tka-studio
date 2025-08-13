"""
Hotkey Registry - Hotkey Binding and Handling

Manages hotkey bindings and handles hotkey events throughout the application.
Uses Qt signals for clean communication.
"""

import logging
from collections.abc import Callable

from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)


class HotkeyRegistry(QObject):
    """
    Hotkey binding and handling registry using Qt signals.

    Handles:
    - Hotkey binding registration
    - Hotkey event handling via Qt signals
    - Hotkey binding management
    - Hotkey state persistence
    """

    # Qt signals for hotkey events
    hotkey_triggered = pyqtSignal(str)  # key_combination
    hotkey_registered = pyqtSignal(str)  # key_combination
    hotkey_unregistered = pyqtSignal(str)  # key_combination

    def __init__(self):
        """Initialize hotkey registry."""
        super().__init__()

        # Hotkey bindings storage
        self._hotkey_bindings: dict[str, Callable] = {}

    def register_hotkey(self, key_combination: str, callback: Callable) -> None:
        """Register a hotkey binding."""
        self._hotkey_bindings[key_combination] = callback

        logger.debug(f"Registered hotkey: {key_combination}")

        # Emit Qt signal for hotkey registered
        self.hotkey_registered.emit(key_combination)

    def unregister_hotkey(self, key_combination: str) -> bool:
        """Unregister a hotkey binding."""
        if key_combination in self._hotkey_bindings:
            del self._hotkey_bindings[key_combination]

            logger.debug(f"Unregistered hotkey: {key_combination}")

            # Emit Qt signal for hotkey unregistered
            self.hotkey_unregistered.emit(key_combination)

            return True
        return False

    def handle_hotkey(self, key_combination: str) -> bool:
        """Handle hotkey press."""
        if key_combination in self._hotkey_bindings:
            try:
                callback = self._hotkey_bindings[key_combination]
                callback()

                logger.debug(f"Executed hotkey: {key_combination}")

                # Emit Qt signal for hotkey executed
                self.hotkey_triggered.emit(key_combination)

                return True
            except Exception as e:
                logger.error(f"Error executing hotkey {key_combination}: {e}")

                # For errors, we could add an error signal if needed
                # For now, just log the error

                return False
        return False

    def is_hotkey_registered(self, key_combination: str) -> bool:
        """Check if a hotkey is registered."""
        return key_combination in self._hotkey_bindings

    def get_all_hotkeys(self) -> dict[str, str]:
        """Get all registered hotkeys (returns key combinations and callback names)."""
        return {
            key: callback.__name__ if hasattr(callback, "__name__") else str(callback)
            for key, callback in self._hotkey_bindings.items()
        }

    def clear_all_hotkeys(self) -> None:
        """Clear all hotkey bindings."""
        self._hotkey_bindings.clear()

        # For now, we don't need a specific signal for clearing all hotkeys
        # Individual unregister signals would be emitted if needed

    def get_hotkey_count(self) -> int:
        """Get the number of registered hotkeys."""
        return len(self._hotkey_bindings)

    def register_multiple_hotkeys(self, hotkey_bindings: dict[str, Callable]) -> None:
        """Register multiple hotkeys at once."""
        for key_combination, callback in hotkey_bindings.items():
            self.register_hotkey(key_combination, callback)

    def get_state_for_persistence(self) -> dict[str, str]:
        """Get state data for persistence (only key combinations, not callbacks)."""
        # Note: We can't persist callbacks, only the key combinations
        return {
            key: callback.__name__ if hasattr(callback, "__name__") else str(callback)
            for key, callback in self._hotkey_bindings.items()
        }

    def load_state_from_persistence(self, state: dict[str, str]) -> None:
        """Load state from persistence data."""
        # Note: This method is mainly for documentation purposes
        # Hotkey callbacks need to be re-registered by the application
        # since we can't serialize/deserialize function objects
        logger.info(
            f"Hotkey registry state loaded: {len(state)} hotkeys to be re-registered"
        )
        # The actual re-registration should be done by the application startup code
