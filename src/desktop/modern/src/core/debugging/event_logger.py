"""
Event Logger for debugging event-driven architecture.

This provides comprehensive logging of all events and commands for debugging purposes.
"""
from __future__ import annotations

import logging
from typing import Any

from desktop.modern.core.events.domain_events import (
    CommandExecutedEvent,
    CommandRedoneEvent,
    CommandUndoneEvent,
)
from desktop.modern.core.events.event_bus import BaseEvent


logger = logging.getLogger(__name__)


class EventLogger:
    """
    Logs all events for debugging purposes.

    This makes debugging trivial by providing a complete audit trail
    of all events that occur in the system.
    """

    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.enabled = False
        self._event_count = 0

        # Subscribe to all event types for logging
        self._setup_subscriptions()

    def _setup_subscriptions(self):
        """Subscribe to all events for logging"""
        try:
            # Subscribe to command events
            self.event_bus.subscribe("command.executed", self._log_command_executed)
            self.event_bus.subscribe("command.undone", self._log_command_undone)
            self.event_bus.subscribe("command.redone", self._log_command_redone)

            # Subscribe to sequence events
            self.event_bus.subscribe("sequence.beat_added", self._log_sequence_event)
            self.event_bus.subscribe("sequence.beat_removed", self._log_sequence_event)
            self.event_bus.subscribe("sequence.beat_updated", self._log_sequence_event)

            # Subscribe to start position events (if we add them)
            self.event_bus.subscribe(
                "sequence.start_position_set", self._log_sequence_event
            )

        except Exception as e:
            logger.exception(f"❌ Error setting up EventLogger subscriptions: {e}")

    def enable(self):
        """Enable event logging"""
        self.enabled = True
        logger.info("🔍 Event logging ENABLED - all events will be logged")

    def disable(self):
        """Disable event logging"""
        self.enabled = False
        logger.info("🔇 Event logging DISABLED")

    def _log_command_executed(self, event: CommandExecutedEvent):
        """Log command execution events"""
        if not self.enabled:
            return

        self._event_count += 1
        logger.info(f"📝 EVENT #{self._event_count}: COMMAND EXECUTED")
        logger.info(f"   Command: {event.command_type}")
        logger.info(f"   Description: {event.command_description}")
        logger.info(f"   Can Undo: {event.can_undo}")
        logger.info(f"   Can Redo: {event.can_redo}")
        logger.info(f"   Source: {event.source}")
        logger.info(f"   Timestamp: {event.timestamp}")

    def _log_command_undone(self, event: CommandUndoneEvent):
        """Log command undo events"""
        if not self.enabled:
            return

        self._event_count += 1
        logger.info(f"↩️ EVENT #{self._event_count}: COMMAND UNDONE")
        logger.info(f"   Command: {event.command_type}")
        logger.info(f"   Description: {event.command_description}")
        logger.info(f"   Can Undo: {event.can_undo}")
        logger.info(f"   Can Redo: {event.can_redo}")

    def _log_command_redone(self, event: CommandRedoneEvent):
        """Log command redo events"""
        if not self.enabled:
            return

        self._event_count += 1
        logger.info(f"↪️ EVENT #{self._event_count}: COMMAND REDONE")
        logger.info(f"   Command: {event.command_type}")
        logger.info(f"   Description: {event.command_description}")
        logger.info(f"   Can Undo: {event.can_undo}")
        logger.info(f"   Can Redo: {event.can_redo}")

    def _log_sequence_event(self, event: BaseEvent):
        """Log sequence-related events"""
        if not self.enabled:
            return

        self._event_count += 1
        logger.info(f"🎵 EVENT #{self._event_count}: {event.event_type.upper()}")
        logger.info(f"   Source: {event.source}")
        logger.info(f"   Timestamp: {event.timestamp}")

        # Log event-specific data
        if hasattr(event, "sequence_id"):
            logger.info(f"   Sequence ID: {event.sequence_id}")
        if hasattr(event, "beat_position"):
            logger.info(f"   Beat Position: {event.beat_position}")
        if hasattr(event, "total_beats"):
            logger.info(f"   Total Beats: {event.total_beats}")
        if hasattr(event, "position_key"):
            logger.info(f"   Position Key: {event.position_key}")

    def get_event_count(self) -> int:
        """Get the total number of events logged"""
        return self._event_count

    def reset_count(self):
        """Reset the event counter"""
        self._event_count = 0
        logger.info("🔄 Event counter reset")


# Global event logger instance
_event_logger: Any = None


def setup_event_logger(event_bus):
    """Setup the global event logger"""
    global _event_logger
    _event_logger = EventLogger(event_bus)
    return _event_logger


def get_event_logger():
    """Get the global event logger"""
    return _event_logger


def enable_event_logging():
    """Enable event logging globally"""
    if _event_logger:
        _event_logger.enable()
    else:
        logger.warning(
            "⚠️ Event logger not initialized - call setup_event_logger() first"
        )


def disable_event_logging():
    """Disable event logging globally"""
    if _event_logger:
        _event_logger.disable()
    else:
        logger.warning("⚠️ Event logger not initialized")


def log_debug_info():
    """Log current system state for debugging"""
    logger.info("🔍 DEBUG INFO - Current System State:")

    try:
        from desktop.modern.core.service_locator import (
            get_command_processor,
            get_sequence_state_manager,
        )

        # Log state manager info
        state_manager = get_sequence_state_manager()
        if state_manager:
            sequence = state_manager.get_sequence()
            start_pos = state_manager.get_start_position()
            logger.info(f"   Sequence: {sequence.length if sequence else 0} beats")
            logger.info(
                f"   Start Position: {start_pos.letter if start_pos else 'None'}"
            )
        else:
            logger.info("   State Manager: Not available")

        # Log command processor info
        command_processor = get_command_processor()
        if command_processor:
            logger.info(f"   Can Undo: {command_processor.can_undo()}")
            logger.info(f"   Can Redo: {command_processor.can_redo()}")

            if command_processor.can_undo():
                logger.info(
                    f"   Undo Description: {command_processor.get_undo_description()}"
                )
            if command_processor.can_redo():
                logger.info(
                    f"   Redo Description: {command_processor.get_redo_description()}"
                )
        else:
            logger.info("   Command Processor: Not available")

        # Log event count
        if _event_logger:
            logger.info(f"   Events Logged: {_event_logger.get_event_count()}")

    except Exception as e:
        logger.exception(f"❌ Error logging debug info: {e}")
