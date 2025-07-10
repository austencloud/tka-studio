"""
Dependency injection for TKA API.
Provides all service dependencies for FastAPI endpoints.
"""

import logging
from typing import Optional

from application.services.sequences.sequence_management_service import (
    SequenceManagementService,
    ISequenceManagementService,
)
from core.interfaces.positioning_services import IArrowPositioningOrchestrator
from core.commands import CommandProcessor
from core.dependency_injection.di_container import (
    DIContainer,
    get_container,
)
from core.events import IEventBus, get_event_bus
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

# Global service instances (initialized at startup)
_container: Optional[DIContainer] = None
_event_bus: Optional[IEventBus] = None
_command_processor: Optional[CommandProcessor] = None
_sequence_service: Optional[SequenceManagementService] = None
_arrow_service: Optional[IArrowPositioningOrchestrator] = None


def initialize_services():
    """
    Initialize all services and dependencies.

    This function is called during application startup to initialize
    all required services and their dependencies.

    Raises:
        Exception: If service initialization fails
    """
    global _container, _event_bus, _command_processor, _sequence_service, _arrow_service

    try:
        logger.info("Initializing API services...")

        # Initialize DI container and event bus
        _container = get_container()
        _event_bus = get_event_bus()

        # Initialize command processor
        _command_processor = CommandProcessor(_event_bus)

        # Resolve services from DI container instead of direct instantiation
        _sequence_service = _container.resolve(ISequenceManagementService)
        _arrow_service = _container.resolve(IArrowPositioningOrchestrator)

        logger.info("All API services initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize API services: {e}")
        raise


def cleanup_services():
    """
    Cleanup services during application shutdown.

    This function is called during application shutdown to properly
    cleanup resources and close connections.
    """
    global _arrow_service

    try:
        logger.info("Cleaning up API services...")

        # Cleanup services that require it
        if _arrow_service and hasattr(_arrow_service, "cleanup"):
            _arrow_service.cleanup()

        logger.info("API services cleanup complete")

    except Exception as e:
        logger.error(f"Error during service cleanup: {e}")


# Dependency injection functions for FastAPI


def get_sequence_service() -> SequenceManagementService:
    """
    Get sequence management service dependency.

    Returns:
        SequenceManagementService: The sequence management service

    Raises:
        HTTPException: If service is not available (503)
    """
    if _sequence_service is None:
        logger.error("Sequence service not available")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Sequence service not available",
        )
    return _sequence_service


def get_arrow_service() -> IArrowPositioningOrchestrator:
    """
    Get arrow management service dependency.

    Returns:
        IArrowPositioningOrchestrator: The arrow positioning orchestrator

    Raises:
        HTTPException: If service is not available (503)
    """
    if _arrow_service is None:
        logger.error("Arrow service not available")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Arrow service not available",
        )
    return _arrow_service


def get_command_processor() -> CommandProcessor:
    """
    Get command processor dependency.

    Returns:
        CommandProcessor: The command processor

    Raises:
        HTTPException: If service is not available (503)
    """
    if _command_processor is None:
        logger.error("Command processor not available")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Command processor not available",
        )
    return _command_processor


def get_event_bus_dependency() -> IEventBus:
    """
    Get event bus dependency.

    Returns:
        IEventBus: The event bus

    Raises:
        HTTPException: If service is not available (503)
    """
    if _event_bus is None:
        logger.error("Event bus not available")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Event bus not available",
        )
    return _event_bus


def get_di_container() -> DIContainer:
    """
    Get dependency injection container.

    Returns:
        DIContainer: The DI container

    Raises:
        HTTPException: If container is not available (503)
    """
    if _container is None:
        logger.error("DI container not available")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="DI container not available",
        )
    return _container


def check_service_health() -> dict:
    """
    Check the health status of all services.

    Returns:
        dict: Service health status mapping
    """
    return {
        "sequence_service": _sequence_service is not None,
        "arrow_service": _arrow_service is not None,
        "command_processor": _command_processor is not None,
        "event_bus": _event_bus is not None,
        "di_container": _container is not None,
    }


def are_all_services_healthy() -> bool:
    """
    Check if all services are healthy.

    Returns:
        bool: True if all services are available, False otherwise
    """
    health_status = check_service_health()
    return all(health_status.values())
