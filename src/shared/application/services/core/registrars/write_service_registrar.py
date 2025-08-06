"""
Write Service Registrar

Specialized registrar for Write Tab services following the microservices
registration architecture pattern.
"""

import logging
from typing import TYPE_CHECKING, Optional

from ..service_registration_manager import IServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class WriteServiceRegistrar(IServiceRegistrar):
    """
    Registrar for Write Tab services.

    Handles registration of all write-related services including:
    - Act data management and persistence
    - Music player integration
    - Act editing operations
    - Layout calculation services  
    - Write tab coordinator
    - UI components
    """

    def __init__(self, progress_callback: Optional[callable] = None):
        """Initialize Write service registrar."""
        self.progress_callback = progress_callback

    def register_services(self, container: "DIContainer") -> None:
        """Register all Write Tab services."""
        try:
            self._update_progress("Registering Write Tab services...")

            # Import and register Write services
            from desktop.modern.core.dependency_injection.write_service_registration import (
                register_write_services,
            )

            register_write_services(container)

            self._update_progress("Write Tab services registered successfully")

        except Exception as e:
            logger.error(f"Failed to register Write Tab services: {e}")
            raise

    def get_domain_name(self) -> str:
        """Get the domain name for this registrar."""
        return "Write Tab Services"

    def get_registered_services(self) -> list[str]:
        """Get list of service names registered by this registrar."""
        return [
            "IActDataService",
            "IActEditingService", 
            "IActLayoutService",
            "IMusicPlayerService",
            "IWriteTabCoordinator",
            "WriteTab",
        ]

    def is_critical(self) -> bool:
        """
        Determine if Write Tab services are critical.

        Returns:
            False - Write Tab is optional functionality
        """
        return False

    def get_service_dependencies(self) -> list[str]:
        """
        Get list of service domains this registrar depends on.

        Returns:
            List of dependency domain names
        """
        return [
            "Core Services",  # For basic infrastructure
        ]

    def _update_progress(self, message: str) -> None:
        """Update progress if callback is available."""
        if self.progress_callback:
            self.progress_callback(message)
        logger.debug(message)
