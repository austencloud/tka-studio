"""
Global service locator for accessing core services in event-driven architecture.

This provides centralized access to the event bus, command processor, and state manager
without requiring dependency injection in every component.
"""

import logging
from typing import Optional

from .commands.command_system import CommandProcessor
from .events.event_bus import TypeSafeEventBus

logger = logging.getLogger(__name__)

# Global service instances
_event_bus: Optional[TypeSafeEventBus] = None
_command_processor: Optional[CommandProcessor] = None
_sequence_state_manager: Optional[object] = (
    None  # Will be imported later to avoid circular imports
)
_services: dict = {}  # Additional services registry


class ServiceLocator:
    """Legacy service locator for backward compatibility."""

    @staticmethod
    def get_service(service_name: str):
        """Get a service by name - used for backward compatibility."""
        return _services.get(service_name)

    @staticmethod
    def register_service(service_name: str, service_instance):
        """Register a service - used for backward compatibility."""
        _services[service_name] = service_instance


def initialize_services():
    """Initialize all core services - call this at app startup"""
    global _event_bus, _command_processor, _sequence_state_manager
    try:
        # Initialize event bus
        _event_bus = TypeSafeEventBus()

        # Initialize command processor
        _command_processor = CommandProcessor(_event_bus)

        # Initialize sequence state manager (import here to avoid circular imports)
        from desktop.modern.presentation.adapters.qt.sequence_state_tracker_adapter import (
            QtSequenceStateTrackerAdapter,
        )

        _sequence_state_manager = QtSequenceStateTrackerAdapter(
            _event_bus, _command_processor
        )

        # Initialize event logger for debugging
        try:
            from desktop.modern.core.debugging.event_logger import setup_event_logger

            event_logger = setup_event_logger(_event_bus)

            # Optionally enable event logging for debugging
            # Uncomment the next line to enable detailed event logging
            # event_logger.enable()
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize event logger: {e}")

        return True

    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {e}")
        return False


def get_event_bus() -> Optional[TypeSafeEventBus]:
    """Get the global event bus instance"""
    if _event_bus is None:
        logger.warning("Event bus not initialized - call initialize_services() first")
    return _event_bus


def get_command_processor() -> Optional[CommandProcessor]:
    """Get the global command processor instance"""
    if _command_processor is None:
        logger.warning(
            "Command processor not initialized - call initialize_services() first"
        )
    return _command_processor


def get_sequence_state_manager() -> Optional[object]:
    """Get the global sequence state manager instance"""
    if _sequence_state_manager is None:
        logger.warning(
            "Sequence state manager not initialized - call initialize_services() first"
        )
    return _sequence_state_manager


def cleanup_services():
    """Cleanup all services - call this at app shutdown"""
    global _event_bus, _command_processor, _sequence_state_manager

    try:
        if _sequence_state_manager and hasattr(_sequence_state_manager, "cleanup"):
            _sequence_state_manager.cleanup()

        if _command_processor and hasattr(_command_processor, "clear_history"):
            _command_processor.clear_history()

        if _event_bus and hasattr(_event_bus, "shutdown"):
            _event_bus.shutdown()

        _event_bus = None
        _command_processor = None
        _sequence_state_manager = None

        logger.info("🧹 All services cleaned up")

    except Exception as e:
        logger.error(f"❌ Error during service cleanup: {e}")


def is_initialized() -> bool:
    """Check if core services are initialized"""
    return all(
        [
            _event_bus is not None,
            _command_processor is not None,
            _sequence_state_manager is not None,
        ]
    )
