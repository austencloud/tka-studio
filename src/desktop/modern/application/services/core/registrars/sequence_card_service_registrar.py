"""
Sequence Card Service Registrar

Specialized registrar for Sequence Card Tab services following the microservices
registration architecture pattern.
"""

import logging
from typing import TYPE_CHECKING, Optional

from ..service_registration_manager import IServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class SequenceCardServiceRegistrar(IServiceRegistrar):
    """
    Registrar for Sequence Card Tab services.

    Handles registration of all sequence card-related services including:
    - Data loading and caching
    - Layout calculation services
    - Display coordination
    - Export functionality
    - Settings management
    - UI components
    """

    def __init__(self, progress_callback: Optional[callable] = None):
        """Initialize Sequence Card service registrar."""
        self.progress_callback = progress_callback

    def register_services(self, container: "DIContainer") -> None:
        """Register all Sequence Card Tab services."""
        try:
            self._update_progress("Registering Sequence Card Tab services...")

            # Import and register Sequence Card services
            from desktop.modern.core.dependency_injection.sequence_card_service_registration import (
                register_sequence_card_services,
            )

            register_sequence_card_services(container)

            self._update_progress("Sequence Card Tab services registered successfully")

        except Exception as e:
            logger.error(f"Failed to register Sequence Card Tab services: {e}")
            raise

    def get_domain_name(self) -> str:
        """Get the domain name for this registrar."""
        return "Sequence Card Tab Services"

    def get_registered_services(self) -> list[str]:
        """Get list of service names registered by this registrar."""
        return [
            "ISequenceCardDataService",
            "ISequenceCardCacheService", 
            "ISequenceCardLayoutService",
            "ISequenceCardDisplayService",
            "ISequenceCardExportService",
            "ISequenceCardSettingsService",
            "SequenceCardDisplayAdaptor",
            "SequenceCardTab",
        ]

    def is_critical(self) -> bool:
        """
        Determine if Sequence Card Tab services are critical.

        Returns:
            False - Sequence Card Tab is optional functionality
        """
        return False

    def get_service_dependencies(self) -> list[str]:
        """
        Get list of service domains this registrar depends on.

        Returns:
            List of dependency domain names
        """
        return [
            "Data Services",  # For file system and data access
            "Core Services",  # For basic infrastructure
        ]

    def _update_progress(self, message: str) -> None:
        """Update progress if callback is available."""
        if self.progress_callback:
            self.progress_callback(message)
        logger.debug(message)
