"""
Service Locator for Desktop Modern Application

Provides convenient access to services registered in the DI container.
This is a façade pattern implementation that makes service access easier
without having to inject the container everywhere.
"""

from __future__ import annotations

import logging
from typing import TypeVar


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
        logger.exception(f"Failed to get sequence state manager: {e}")
        return None


def cleanup():
    """Clean up the service locator."""
    global _container
    _container = None
    logger.info("🧹 Service locator cleaned up")
