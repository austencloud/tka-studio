"""
Service Locator for Desktop Modern Application

Provides convenient access to services registered in the DI container.
This is a façade pattern implementation that makes service access easier
without having to inject the container everywhere.
"""

import logging
from typing import Optional, TypeVar

logger = logging.getLogger(__name__)

# Global container reference
_container = None

T = TypeVar("T")


def initialize_service_locator(container):
    """Initialize the service locator with a DI container."""
    global _container
    _container = container
    logger.info("🔧 Service locator initialized")


def get_container():
    """Get the DI container instance."""
    return _container


def is_initialized() -> bool:
    """Check if the service locator has been initialized."""
    return _container is not None


def get_service(service_type: type[T]) -> Optional[T]:
    """
    Get a service from the DI container.

    Args:
        service_type: The type of service to resolve

    Returns:
        The service instance or None if not available
    """
    if not _container:
        logger.warning(
            "Service locator not initialized - call initialize_service_locator() first"
        )
        return None

    try:
        return _container.resolve(service_type)
    except Exception as e:
        logger.error(f"Failed to resolve service {service_type.__name__}: {e}")
        return None


def get_sequence_state_manager():
    """
    Get the sequence state manager (tracker) service.

    Returns:
        QtSequenceStateTrackerAdapter instance or None if not available
    """
    if not _container:
        logger.warning(
            "Sequence state manager not initialized - call initialize_services() first"
        )
        return None

    try:
        from desktop.modern.presentation.adapters.qt.sequence_state_tracker_adapter import (
            QtSequenceStateTrackerAdapter,
        )

        return _container.resolve(QtSequenceStateTrackerAdapter)
    except Exception as e:
        logger.error(f"Failed to get sequence state manager: {e}")
        return None


def cleanup():
    """Clean up the service locator."""
    global _container
    _container = None
    logger.info("🧹 Service locator cleaned up")
