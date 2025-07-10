"""
Global service locator for accessing core services in event-driven architecture.

This provides centralized access to the event bus, command processor, and state manager
without requiring dependency injection in every component.
"""

from typing import Optional
import logging

# Import core services
try:
    from .events.event_bus import TypeSafeEventBus
    from .commands.command_system import CommandProcessor
    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    EVENT_SYSTEM_AVAILABLE = False
    TypeSafeEventBus = None
    CommandProcessor = None

logger = logging.getLogger(__name__)

# Global service instances
_event_bus: Optional[TypeSafeEventBus] = None
_command_processor: Optional[CommandProcessor] = None
_sequence_state_manager: Optional[object] = None  # Will be imported later to avoid circular imports
_data_conversion_service: Optional[object] = None

def initialize_services():
    """Initialize all core services - call this at app startup"""
    global _event_bus, _command_processor, _sequence_state_manager
    
    if not EVENT_SYSTEM_AVAILABLE:
        logger.error("Event system not available - cannot initialize services")
        return False
    
    try:
        # Initialize event bus
        _event_bus = TypeSafeEventBus()
        logger.info("✅ Event bus initialized")
        
        # Initialize command processor
        _command_processor = CommandProcessor(_event_bus)
        logger.info("✅ Command processor initialized")
        
        # Initialize sequence state manager (import here to avoid circular imports)
        from application.services.core.sequence_state_manager import SequenceStateManager
        _sequence_state_manager = SequenceStateManager(_event_bus, _command_processor)
        logger.info("✅ Sequence state manager initialized")
        
        # Initialize event logger for debugging
        try:
            from core.debugging.event_logger import setup_event_logger
            event_logger = setup_event_logger(_event_bus)
            logger.info("✅ Event logger initialized")
            
            # Optionally enable event logging for debugging
            # Uncomment the next line to enable detailed event logging
            # event_logger.enable()
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize event logger: {e}")
        
        logger.info("🎯 All core services initialized successfully")
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
        logger.warning("Command processor not initialized - call initialize_services() first")
    return _command_processor

def get_sequence_state_manager():
    """Get the global sequence state manager instance"""
    if _sequence_state_manager is None:
        logger.warning("Sequence state manager not initialized - call initialize_services() first")
    return _sequence_state_manager

def get_data_conversion_service():
    """Get the data conversion service instance"""
    global _data_conversion_service  # Declare global before use
    
    if _data_conversion_service is None:
        # Lazy initialize data conversion service
        try:
            from presentation.tabs.construct.data_conversion_service import DataConversionService
            _data_conversion_service = DataConversionService()
            logger.info("✅ Data conversion service initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize data conversion service: {e}")
    return _data_conversion_service

def cleanup_services():
    """Cleanup all services - call this at app shutdown"""
    global _event_bus, _command_processor, _sequence_state_manager, _data_conversion_service
    
    try:
        if _sequence_state_manager and hasattr(_sequence_state_manager, 'cleanup'):
            _sequence_state_manager.cleanup()
            
        if _command_processor and hasattr(_command_processor, 'clear_history'):
            _command_processor.clear_history()
            
        if _event_bus and hasattr(_event_bus, 'shutdown'):
            _event_bus.shutdown()
            
        _event_bus = None
        _command_processor = None
        _sequence_state_manager = None
        _data_conversion_service = None
        
        logger.info("🧹 All services cleaned up")
        
    except Exception as e:
        logger.error(f"❌ Error during service cleanup: {e}")

def is_initialized() -> bool:
    """Check if core services are initialized"""
    return all([
        _event_bus is not None,
        _command_processor is not None,
        _sequence_state_manager is not None
    ])
