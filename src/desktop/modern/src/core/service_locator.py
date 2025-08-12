"""
Global service locator for accessing core services in event-driven architecture.

This provides centralized access to the event bus, command processor, and state manager
without requiring dependency injection in every component.
"""
from __future__ import annotations

import logging


# Import core services
try:
    from .commands.command_system import CommandProcessor
    from .events.event_bus import TypeSafeEventBus

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    EVENT_SYSTEM_AVAILABLE = False
    TypeSafeEventBus = None
    CommandProcessor = None

logger = logging.getLogger(__name__)

# Global service instances
_event_bus: TypeSafeEventBus | None = None
_command_processor: CommandProcessor | None = None
_sequence_state_manager: object | None = (
    None  # Will be imported later to avoid circular imports
)
_data_conversion_service: object | None = None


def initialize_services():
    """Initialize all core services - call this at app startup"""
    global _event_bus, _command_processor, _sequence_state_manager

    if not EVENT_SYSTEM_AVAILABLE:
        logger.error("Event system not available - cannot initialize services")
        return False

    try:
        # Initialize event bus
        _event_bus = TypeSafeEventBus()

        # Initialize command processor
        _command_processor = CommandProcessor(_event_bus)

        # Initialize sequence state manager (import here to avoid circular imports)
        from desktop.modern.application.services.sequence.sequence_state_tracker import (
            SequenceStateTracker,
        )

        _sequence_state_manager = SequenceStateTracker(_event_bus, _command_processor)

        # Initialize event logger for debugging
        try:
            from desktop.modern.core.debugging.event_logger import setup_event_logger

            setup_event_logger(_event_bus)

            # Optionally enable event logging for debugging
            # Uncomment the next line to enable detailed event logging
            # event_logger.enable()
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize event logger: {e}")

        return True

    except Exception as e:
        logger.exception(f"❌ Failed to initialize services: {e}")
        return False


def get_event_bus() -> TypeSafeEventBus | None:
    """Get the global event bus instance"""
    if _event_bus is None:
        logger.warning("Event bus not initialized - call initialize_services() first")
    return _event_bus


def get_command_processor() -> CommandProcessor | None:
    """Get the global command processor instance"""
    if _command_processor is None:
        logger.warning(
            "Command processor not initialized - call initialize_services() first"
        )
    return _command_processor


def get_sequence_state_manager() -> object | None:
    """Get the global sequence state manager instance"""
    if _sequence_state_manager is None:
        logger.warning(
            "Sequence state manager not initialized - call initialize_services() first"
        )
    return _sequence_state_manager


def get_data_conversion_service():
    """Get the data conversion service instance"""
    global _data_conversion_service  # Declare global before use

    if _data_conversion_service is None:
        # Lazy initialize data conversion service
        try:
            from desktop.modern.application.services.data.data_converter import (
                DataConverter,
            )

            _data_conversion_service = DataConverter()
            logger.info("✅ Data conversion service initialized")
        except Exception as e:
            logger.exception(f"❌ Failed to initialize data conversion service: {e}")
    return _data_conversion_service


def cleanup_services():
    """Cleanup all services - call this at app shutdown"""
    global _event_bus, _command_processor, _sequence_state_manager, _data_conversion_service

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
        _data_conversion_service = None

        logger.info("🧹 All services cleaned up")

    except Exception as e:
        logger.exception(f"❌ Error during service cleanup: {e}")


def is_initialized() -> bool:
    """Check if core services are initialized"""
    return all(
        [
            _event_bus is not None,
            _command_processor is not None,
            _sequence_state_manager is not None,
        ]
    )
