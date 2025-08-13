"""
Pure Sequence State Tracker Service - Platform Agnostic

This service tracks sequence state without any Qt dependencies.
Qt-specific signal coordination is handled by adapters in the presentation layer.
"""

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


# Simple event dataclasses to replace missing event bus events
@dataclass
class CommandExecutedEvent:
    command_type: str
    command_data: dict[str, Any]
    timestamp: float = 0.0


@dataclass
class CommandUndoneEvent:
    command_type: str
    command_data: dict[str, Any]
    timestamp: float = 0.0


@dataclass
class CommandRedoneEvent:
    command_type: str
    command_data: dict[str, Any]
    timestamp: float = 0.0


logger = logging.getLogger(__name__)


class SequenceStateTrackerService:
    """
    Pure service for tracking sequence and start position state.

    This service is platform-agnostic and does not depend on Qt.
    Signal coordination is handled by Qt adapters in the presentation layer.

    Responsibilities:
    - Track current sequence and start position state
    - React to command execution events
    - Manage persistence coordination
    - Provide clean API for state access
    """

    def __init__(self, event_bus, command_processor):
        self.event_bus = event_bus
        self.command_processor = command_processor

        # Current state (single source of truth)
        self.current_sequence: SequenceData | None = None
        self.start_position: BeatData | None = None

        # Platform-agnostic event callbacks
        self._sequence_updated_callbacks: list[
            Callable[[SequenceData | None], None]
        ] = []
        self._start_position_updated_callbacks: list[
            Callable[[BeatData | None], None]
        ] = []
        self._state_changed_callbacks: list[Callable[[], None]] = []

        # Event bus subscriptions removed - using direct Qt signals instead

    def add_sequence_updated_callback(
        self, callback: Callable[[SequenceData | None], None]
    ):
        """Add callback for when sequence is updated."""
        self._sequence_updated_callbacks.append(callback)

    def add_start_position_updated_callback(
        self, callback: Callable[[BeatData | None], None]
    ):
        """Add callback for when start position is updated."""
        self._start_position_updated_callbacks.append(callback)

    def add_state_changed_callback(self, callback: Callable[[], None]):
        """Add callback for when state changes."""
        self._state_changed_callbacks.append(callback)

    def _update_sequence(self, new_sequence: SequenceData | None):
        """Update the current sequence and notify callbacks"""
        if self.current_sequence != new_sequence:
            self.current_sequence = new_sequence
            self._notify_sequence_updated(new_sequence)
            self._notify_state_changed()
            logger.debug(
                f"📊 Sequence updated: {new_sequence.length if new_sequence else 'None'} beats"
            )

    def _update_start_position(self, new_start_position: BeatData | None):
        """Update the start position and notify callbacks"""
        if self.start_position != new_start_position:
            self.start_position = new_start_position
            self._notify_start_position_updated(new_start_position)
            self._notify_state_changed()
            logger.debug(
                f"🎯 Start position updated: {new_start_position.letter if new_start_position else 'None'}"
            )

    def _clear_all_state(self):
        """Clear all state"""
        self.current_sequence = None
        self.start_position = None
        self._notify_sequence_updated(None)
        self._notify_start_position_updated(None)
        self._notify_state_changed()
        logger.info("🗑️ All state cleared")

    def _refresh_state_from_persistence(self):
        """Refresh state from persistence (for undo/redo scenarios)"""
        try:
            # Load current state from persistence
            # Note: This would need to be injected as dependencies to avoid direct imports
            # For now, keeping the same pattern as the original
            from desktop.modern.application.services.sequence.sequence_persister import (
                SequencePersister,
            )

            persistence_service = SequencePersister()

            # Load sequence (this will need to be converted from legacy format)
            # For now, we'll just refresh what we have
            # TODO: Implement proper persistence loading

            logger.debug("🔄 State refreshed from persistence")

        except Exception as e:
            logger.error(f"❌ Error refreshing state from persistence: {e}")

    # Public API for accessing current state
    def get_sequence(self) -> SequenceData | None:
        """Get the current sequence"""
        return self.current_sequence

    def get_start_position(self) -> BeatData | None:
        """Get the current start position"""
        return self.start_position

    def has_sequence(self) -> bool:
        """Check if there's a current sequence"""
        return self.current_sequence is not None and self.current_sequence.length > 0

    def has_start_position(self) -> bool:
        """Check if there's a start position set"""
        return self.start_position is not None

    def is_empty(self) -> bool:
        """Check if both sequence and start position are empty"""
        return not self.has_sequence() and not self.has_start_position()

    # Direct state setting methods (for non-command scenarios like loading)
    def set_sequence_direct(self, sequence: SequenceData | None):
        """Set sequence directly (for loading scenarios, bypasses commands)"""
        self._update_sequence(sequence)

    def set_start_position_direct(self, start_position: BeatData | None):
        """Set start position directly (for loading scenarios, bypasses commands)"""
        self._update_start_position(start_position)

    def get_state_summary(self) -> dict[str, Any]:
        """Get a summary of current state."""
        return {
            "has_sequence": self.has_sequence(),
            "has_start_position": self.has_start_position(),
            "sequence_length": (
                self.current_sequence.length if self.current_sequence else 0
            ),
            "start_position_letter": (
                self.start_position.letter if self.start_position else None
            ),
            "is_empty": self.is_empty(),
        }

    def cleanup(self):
        """Cleanup resources when the state manager is being destroyed"""
        try:
            # Unsubscribe from events
            if self.event_bus:
                # The event bus should handle cleanup of subscriptions
                pass

            # Clear callbacks
            self._sequence_updated_callbacks.clear()
            self._start_position_updated_callbacks.clear()
            self._state_changed_callbacks.clear()

            logger.info("🧹 SequenceStateTrackerService cleaned up")

        except Exception as e:
            logger.error(f"❌ Error during SequenceStateTrackerService cleanup: {e}")

    def _notify_sequence_updated(self, sequence: SequenceData | None):
        """Notify callbacks that sequence was updated."""
        for callback in self._sequence_updated_callbacks:
            callback(sequence)

    def _notify_start_position_updated(self, start_position: BeatData | None):
        """Notify callbacks that start position was updated."""
        for callback in self._start_position_updated_callbacks:
            callback(start_position)

    def _notify_state_changed(self):
        """Notify callbacks that state changed."""
        for callback in self._state_changed_callbacks:
            callback()
