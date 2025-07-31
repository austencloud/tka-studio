"""
Core Service Registrar

Handles registration of core application services following microservices architecture.
This registrar manages critical foundation services required for basic application functionality.

Services Registered:
- LayoutManager: Layout management and coordination
- UICoordinator: UI state management
- ApplicationInitializationOrchestrator: Application startup coordination
- SessionRestorationCoordinator: Session restoration management
- WindowManagementService: Window lifecycle management
- WindowDiscoveryService: Window discovery and management
- SequenceRestorationService: Sequence restoration operations
"""

import logging
from typing import TYPE_CHECKING

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class CoreServiceRegistrar(BaseServiceRegistrar):
    """
    Registrar for core application services.

    Medium complexity registrar handling critical foundation services required
    for basic application functionality including layout, UI coordination, and
    lifecycle management.
    """

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Core Services"

    def is_critical(self) -> bool:
        """Core services are critical for application functionality."""
        return True

    def register_services(self, container: "DIContainer") -> None:
        """Register core services using pure dependency injection."""
        self._update_progress("Registering core services...")

        # Register basic core services
        self._register_basic_core_services(container)

        # Register lifecycle services
        self._register_lifecycle_services(container)

        self._update_progress("Core services registered successfully")

    def _register_basic_core_services(self, container: "DIContainer") -> None:
        """Register basic core services (layout, UI coordination)."""
        try:
            from desktop.modern.core.interfaces.core_services import (
                ILayoutService,
                IUIStateManager,
            )
            from desktop.modern.core.interfaces.layout_services import (
                IBeatLayoutCalculator,
            )
            from desktop.modern.core.interfaces.ui_services import (
                IThumbnailGenerationService,
            )
            from shared.application.services.layout.beat_layout_calculator import (
                BeatLayoutCalculator,
            )
            from shared.application.services.layout.layout_manager import LayoutManager
            from shared.application.services.ui.coordination.ui_coordinator import (
                UICoordinator,
            )
            from shared.application.services.ui.thumbnail_generation_service import (
                ThumbnailGenerationService,
            )
            from shared.application.services.ui.ui_state_manager import UIStateManager

            # Register service types with factory functions for proper DI
            def create_layout_service():
                event_bus = None
                try:
                    from desktop.modern.core.events import IEventBus

                    event_bus = container.resolve(IEventBus)
                except Exception:
                    # Event bus not available, continue without it
                    pass
                return LayoutManager(event_bus=event_bus)

            # Register with factory functions for proper dependency resolution
            container.register_factory(ILayoutService, create_layout_service)
            self._mark_service_available("LayoutManager")

            # Register UI state service as singleton since it has no dependencies
            container.register_singleton(IUIStateManager, UICoordinator)
            self._mark_service_available("UICoordinator")

            # Register modern UI state manager
            container.register_singleton(UIStateManager, UIStateManager)
            self._mark_service_available("UIStateManager")

            # Register window resize coordinator for pictograph re-scaling
            from desktop.modern.application.services.ui.window_resize_coordinator import (
                WindowResizeCoordinator,
            )

            container.register_singleton(
                WindowResizeCoordinator, WindowResizeCoordinator
            )
            self._mark_service_available("WindowResizeCoordinator")

            # Register thumbnail generation service
            container.register_singleton(
                ThumbnailGenerationService, ThumbnailGenerationService
            )
            container.register_singleton(
                IThumbnailGenerationService, ThumbnailGenerationService
            )
            self._mark_service_available("ThumbnailGenerationService")
            self._mark_service_available("IThumbnailGenerationService")

            # Register beat layout calculator
            container.register_singleton(IBeatLayoutCalculator, BeatLayoutCalculator)
            self._mark_service_available("BeatLayoutCalculator")

        except ImportError as e:
            error_msg = f"Failed to register basic core services: {e}"
            logger.error(error_msg)

            # Core services are critical, so re-raise the error
            if self.is_critical():
                raise ImportError(f"Critical core services unavailable: {e}") from e

    def _register_lifecycle_services(self, container: "DIContainer") -> None:
        """Register the lifecycle management services."""
        try:
            from desktop.modern.application.services.core.application_initialization_orchestrator import (
                ApplicationInitializationOrchestrator,
                IApplicationInitializationOrchestrator,
            )
            from desktop.modern.application.services.core.window_management_service import (
                IWindowManagementService,
                WindowManagementService,
            )
            from desktop.modern.application.services.ui.window_discovery_service import (
                IWindowDiscoveryService,
                WindowDiscoveryService,
            )
            from shared.application.services.core.session_restoration_coordinator import (
                ISessionRestorationCoordinator,
                SessionRestorationCoordinator,
            )
            from shared.application.services.sequence.sequence_restorer import (
                ISequenceRestorer,
                SequenceRestorer,
            )

            # Register individual services
            container.register_singleton(
                IWindowManagementService, WindowManagementService
            )
            self._mark_service_available("WindowManagementService")

            container.register_singleton(
                IWindowDiscoveryService, WindowDiscoveryService
            )
            self._mark_service_available("WindowDiscoveryService")

            container.register_singleton(ISequenceRestorer, SequenceRestorer)
            self._mark_service_available("SequenceRestorationService")

            # Register session coordinator with sequence restoration service dependency
            def create_session_coordinator():
                sequence_service = container.resolve(ISequenceRestorer)
                return SessionRestorationCoordinator(sequence_service)

            container.register_factory(
                ISessionRestorationCoordinator, create_session_coordinator
            )
            self._mark_service_available("SessionRestorationCoordinator")

            # Register orchestrator with all dependencies
            def create_app_init_orchestrator():
                window_service = container.resolve(IWindowManagementService)
                session_coordinator = container.resolve(ISessionRestorationCoordinator)
                window_discovery_service = container.resolve(IWindowDiscoveryService)
                return ApplicationInitializationOrchestrator(
                    window_service, session_coordinator, window_discovery_service
                )

            container.register_factory(
                IApplicationInitializationOrchestrator, create_app_init_orchestrator
            )
            self._mark_service_available("ApplicationInitializationOrchestrator")

        except ImportError as e:
            error_msg = f"Failed to register lifecycle services: {e}"
            logger.error(error_msg)

            # Lifecycle services are critical, so re-raise the error
            if self.is_critical():
                raise ImportError(
                    f"Critical lifecycle services unavailable: {e}"
                ) from e
