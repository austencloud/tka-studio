"""
Hotkey Registry - Hotkey Binding and Handling

Manages hotkey bindings and handles hotkey events throughout the application.
Extracted from UIStateManager to follow single responsibility principle.
"""

import logging
from typing import Callable, Dict

from core.events.event_bus import UIEvent, get_event_bus

logger = logging.getLogger(__name__)


class HotkeyRegistry:
    """
    Hotkey binding and handling registry.
    
    Handles:
    - Hotkey binding registration
    - Hotkey event handling
    - Hotkey binding management
    - Hotkey state persistence
    """

    def __init__(self):
        """Initialize hotkey registry."""
        # Event bus for notifications
        self._event_bus = get_event_bus()

        # Hotkey bindings storage
        self._hotkey_bindings: Dict[str, Callable] = {}

    def register_hotkey(self, key_combination: str, callback: Callable) -> None:
        """Register a hotkey binding."""
        self._hotkey_bindings[key_combination] = callback
        
        logger.debug(f"Registered hotkey: {key_combination}")

        # Publish hotkey registered event
        event = UIEvent(
            component="hotkey",
            action="registered",
            state_data={"key_combination": key_combination},
            source="hotkey_registry",
        )
        self._event_bus.publish(event)

    def unregister_hotkey(self, key_combination: str) -> bool:
        """Unregister a hotkey binding."""
        if key_combination in self._hotkey_bindings:
            del self._hotkey_bindings[key_combination]
            
            logger.debug(f"Unregistered hotkey: {key_combination}")

            # Publish hotkey unregistered event
            event = UIEvent(
                component="hotkey",
                action="unregistered",
                state_data={"key_combination": key_combination},
                source="hotkey_registry",
            )
            self._event_bus.publish(event)
            
            return True
        return False

    def handle_hotkey(self, key_combination: str) -> bool:
        """Handle hotkey press."""
        if key_combination in self._hotkey_bindings:
            try:
                callback = self._hotkey_bindings[key_combination]
                callback()
                
                logger.debug(f"Executed hotkey: {key_combination}")

                # Publish hotkey executed event
                event = UIEvent(
                    component="hotkey",
                    action="executed",
                    state_data={"key_combination": key_combination},
                    source="hotkey_registry",
                )
                self._event_bus.publish(event)
                
                return True
            except Exception as e:
                logger.error(f"Error executing hotkey {key_combination}: {e}")
                
                # Publish hotkey error event
                event = UIEvent(
                    component="hotkey",
                    action="error",
                    state_data={"key_combination": key_combination, "error": str(e)},
                    source="hotkey_registry",
                )
                self._event_bus.publish(event)
                
                return False
        return False

    def is_hotkey_registered(self, key_combination: str) -> bool:
        """Check if a hotkey is registered."""
        return key_combination in self._hotkey_bindings

    def get_all_hotkeys(self) -> Dict[str, str]:
        """Get all registered hotkeys (returns key combinations and callback names)."""
        return {
            key: callback.__name__ if hasattr(callback, '__name__') else str(callback)
            for key, callback in self._hotkey_bindings.items()
        }

    def clear_all_hotkeys(self) -> None:
        """Clear all hotkey bindings."""
        self._hotkey_bindings.clear()

        # Publish hotkeys cleared event
        event = UIEvent(
            component="hotkey",
            action="cleared",
            state_data={},
            source="hotkey_registry",
        )
        self._event_bus.publish(event)

    def get_hotkey_count(self) -> int:
        """Get the number of registered hotkeys."""
        return len(self._hotkey_bindings)

    def register_multiple_hotkeys(self, hotkey_bindings: Dict[str, Callable]) -> None:
        """Register multiple hotkeys at once."""
        for key_combination, callback in hotkey_bindings.items():
            self.register_hotkey(key_combination, callback)

    def get_state_for_persistence(self) -> Dict[str, str]:
        """Get state data for persistence (only key combinations, not callbacks)."""
        # Note: We can't persist callbacks, only the key combinations
        return {
            key: callback.__name__ if hasattr(callback, '__name__') else str(callback)
            for key, callback in self._hotkey_bindings.items()
        }

    def load_state_from_persistence(self, state: Dict[str, str]) -> None:
        """Load state from persistence data."""
        # Note: This method is mainly for documentation purposes
        # Hotkey callbacks need to be re-registered by the application
        # since we can't serialize/deserialize function objects
        logger.info(f"Hotkey registry state loaded: {len(state)} hotkeys to be re-registered")
        # The actual re-registration should be done by the application startup code
