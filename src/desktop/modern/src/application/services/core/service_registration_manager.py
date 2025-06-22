"""
Service Registration Manager

Pure service for managing dependency injection service registration.
Extracted from KineticConstructorModern to follow single responsibility principle.

PROVIDES:
- Core service registration
- Motion service registration
- Layout service registration
- Pictograph service registration
- Event system registration
"""

from typing import Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from core.dependency_injection.di_container import DIContainer

try:
    from core.events import IEventBus
except ImportError:
    IEventBus = None


class IServiceRegistrationManager(ABC):
    """Interface for service registration operations."""

    @abstractmethod
    def register_all_services(self, container: "DIContainer") -> None:
        """Register all application services in the DI container."""
        pass

    @abstractmethod
    def register_event_system(self, container: "DIContainer") -> None:
        """Register event system and command infrastructure."""
        pass

    @abstractmethod
    def register_core_services(self, container: "DIContainer") -> None:
        """Register core services using pure dependency injection."""
        pass

    @abstractmethod
    def register_motion_services(self, container: "DIContainer") -> None:
        """Register motion services using pure dependency injection."""
        pass


class ServiceRegistrationManager(IServiceRegistrationManager):
    """
    Pure service for managing dependency injection service registration.
    
    Handles all service registration without external dependencies.
    Uses clean dependency injection patterns following TKA architecture.
    """

    def __init__(self, progress_callback: Optional[callable] = None):
        """Initialize with optional progress callback."""
        self.progress_callback = progress_callback

    def register_all_services(self, container: "DIContainer") -> None:
        """Register all application services in the DI container."""
        self._update_progress("Configuring services...")

        # Register services in dependency order
        self.register_event_system(container)
        self.register_core_services(container)
        self.register_motion_services(container)
        self.register_layout_services(container)
        self.register_pictograph_services(container)
        self.register_workbench_services(container)

        self._update_progress("Services configured")

    def register_event_system(self, container: "DIContainer") -> None:
        """Register event system and command infrastructure."""
        try:
            from core.events import IEventBus, get_event_bus
            from core.commands import CommandProcessor

            # Get or create event bus
            event_bus = get_event_bus()
            container.register_instance(IEventBus, event_bus)

            # Register command processor
            command_processor = CommandProcessor(event_bus)
            container.register_instance(CommandProcessor, command_processor)

            self._update_progress("Event system registered")

        except ImportError as e:
            print(f"⚠️ Event system not available: {e}")
            # Continue without event system for backward compatibility

    def register_core_services(self, container: "DIContainer") -> None:
        """Register core services using pure dependency injection."""
        from application.services.layout.layout_management_service import (
            LayoutManagementService,
        )
        from application.services.ui.ui_state_management_service import (
            UIStateManagementService,
        )
        from core.interfaces.core_services import (
            IUIStateManagementService,
            ILayoutService,
        )

        # Register service types with factory functions for proper DI
        def create_layout_service():
            event_bus = None
            try:
                if IEventBus:
                    event_bus = container.resolve(IEventBus)
            except Exception:
                # Event bus not available, continue without it
                pass
            return LayoutManagementService(event_bus=event_bus)

        def create_ui_state_service():
            return UIStateManagementService()

        # Register with factory functions for proper dependency resolution
        container.register_factory(ILayoutService, create_layout_service)
        container.register_factory(
            IUIStateManagementService, create_ui_state_service
        )

    def register_motion_services(self, container: "DIContainer") -> None:
        """Register motion services using pure dependency injection."""
        from application.services.motion.motion_validation_service import (
            MotionValidationService,
            IMotionValidationService,
        )
        from application.services.motion.motion_orientation_service import (
            MotionOrientationService,
            IMotionOrientationService,
        )

        # Register service types, not instances - pure DI
        container.register_singleton(
            IMotionValidationService, MotionValidationService
        )
        container.register_singleton(
            IMotionOrientationService, MotionOrientationService
        )

    def register_layout_services(self, container: "DIContainer") -> None:
        """Register layout services."""
        # Note: Layout services have been consolidated into LayoutManagementService
        # which is already registered in register_core_services() as ILayoutService
        #
        # The old separate services (BeatLayoutService, ResponsiveLayoutService,
        # ComponentLayoutService) have been consolidated for better maintainability
        pass

    def register_pictograph_services(self, container: "DIContainer") -> None:
        """Register pictograph services using pure dependency injection."""
        from application.services.data.pictograph_data_service import (
            PictographDataService,
            IPictographDataService,
        )
        from src.application.services.core.pictograph_management_service import (
            PictographManagementService,
        )

        # Register service types, not instances - pure DI
        container.register_singleton(IPictographDataService, PictographDataService)
        container.register_singleton(
            PictographManagementService, PictographManagementService
        )

    def register_workbench_services(self, container: "DIContainer") -> None:
        """Register workbench services."""
        from presentation.factories.workbench_factory import configure_workbench_services

        configure_workbench_services(container)

    def register_positioning_services(self, container: "DIContainer") -> None:
        """Register the new refactored positioning services."""
        # Import the new orchestrators
        from application.services.positioning.arrow_orchestrator import (
            ArrowPositioningOrchestrator,
            IArrowPositioningOrchestrator,
        )
        from application.services.positioning.prop_orchestrator import (
            PropOrchestrator,
            IPropOrchestrator,
        )
        from application.services.core.pictograph_orchestrator import (
            PictographOrchestrator,
            IPictographOrchestrator,
        )

        # Register the orchestrators
        container.register_singleton(
            IArrowPositioningOrchestrator, ArrowPositioningOrchestrator
        )
        container.register_singleton(IPropOrchestrator, PropOrchestrator)
        container.register_singleton(IPictographOrchestrator, PictographOrchestrator)

    def register_data_services(self, container: "DIContainer") -> None:
        """Register the new refactored data services."""
        # Import the new data services
        from application.services.data.csv_data_service import (
            CSVDataService,
            ICSVDataService,
        )
        from application.services.positioning.json_configuration_service import (
            JSONConfigurationService,
            IJSONConfigurationService,
        )

        # Register the data services
        container.register_singleton(ICSVDataService, CSVDataService)
        container.register_singleton(IJSONConfigurationService, JSONConfigurationService)

    def get_registration_status(self) -> dict:
        """Get status of service registration."""
        return {
            "event_system_available": IEventBus is not None,
            "services_registered": True,  # Could be enhanced to track actual registration
        }

    def _update_progress(self, message: str) -> None:
        """Update progress if callback is available."""
        if self.progress_callback:
            self.progress_callback(message)
