"""
Start Position Service Registrar

Handles registration of start position services following microservices architecture.
This registrar manages start position data, selection, UI, and orchestration services.

Services Registered:
- StartPositionDataService: Data retrieval and caching
- StartPositionSelectionService: Selection business logic
- StartPositionUIService: UI state and layout management
- StartPositionOrchestrator: Service coordination and workflows
"""

import logging
from typing import TYPE_CHECKING

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class StartPositionServiceRegistrar(BaseServiceRegistrar):
    """
    Registrar for start position services.

    Medium complexity registrar handling start position operations including
    data access, selection logic, UI management, and service orchestration.
    """

    # Class-level flag to prevent duplicate registrations across all instances
    _SERVICES_REGISTERED = False

    def __init__(self, progress_callback=None):
        super().__init__(progress_callback)

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Start Position Services"

    def is_critical(self) -> bool:
        """Start position services are critical for construct tab functionality."""
        return True

    def register_services(self, container: "DIContainer") -> None:
        """Register start position services using pure dependency injection."""
        # Prevent duplicate registration using class-level flag
        if StartPositionServiceRegistrar._SERVICES_REGISTERED:
            logger.debug(
                "Start position services already registered globally, skipping"
            )
            return

        self._update_progress("Registering start position services...")

        # Register core start position services
        self._register_core_start_position_services(container)

        # Mark as registered globally
        StartPositionServiceRegistrar._SERVICES_REGISTERED = True

        self._update_progress("Start position services registered successfully")

    def _register_core_start_position_services(self, container: "DIContainer") -> None:
        """Register core start position services with proper dependency injection."""
        try:
            # Import service interfaces and implementations

            from desktop.modern.application.services.start_position.start_position_orchestrator import (
                StartPositionOrchestrator,
            )
            from desktop.modern.application.services.start_position.start_position_ui_service import (
                StartPositionUIService,
            )
            from desktop.modern.core.interfaces.start_position_services import (
                IStartPositionDataService,
                IStartPositionOrchestrator,
                IStartPositionSelectionService,
                IStartPositionUIService,
            )
            from shared.application.services.start_position.start_position_data_service import (
                StartPositionDataService,
            )
            from shared.application.services.start_position.start_position_selection_service import (
                StartPositionSelectionService,
            )

            # Register data service (no dependencies)
            container.register_singleton(
                IStartPositionDataService, StartPositionDataService
            )
            self._mark_service_available("StartPositionDataService")

            # Register selection service (no dependencies)
            container.register_singleton(
                IStartPositionSelectionService, StartPositionSelectionService
            )
            self._mark_service_available("StartPositionSelectionService")

            # Register UI service (no dependencies)
            container.register_singleton(
                IStartPositionUIService, StartPositionUIService
            )
            self._mark_service_available("StartPositionUIService")

            # Register new UI-agnostic services (no dependencies)

            # Register orchestrator service with dependencies
            def create_orchestrator():
                data_service = container.resolve(IStartPositionDataService)
                selection_service = container.resolve(IStartPositionSelectionService)
                ui_service = container.resolve(IStartPositionUIService)
                return StartPositionOrchestrator(
                    data_service, selection_service, ui_service
                )

            container.register_factory(IStartPositionOrchestrator, create_orchestrator)
            self._mark_service_available("StartPositionOrchestrator")

            # Remove duplicate log message - it's now in the main register_services method

        except ImportError as e:
            error_msg = f"Failed to register start position services: {e}"
            logger.error(error_msg)

            # Start position services are critical for construct tab
            if self.is_critical():
                raise ImportError(
                    f"Critical start position services unavailable: {e}"
                ) from e

    @classmethod
    def reset_registration_state(cls):
        """Reset the global registration state (for testing purposes)."""
        cls._SERVICES_REGISTERED = False
        logger.debug("Start position service registration state reset")
