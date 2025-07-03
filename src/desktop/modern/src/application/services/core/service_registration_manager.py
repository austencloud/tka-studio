"""
Service Registration Manager

Pure service for managing dependency injection service registration.
Extracted from KineticConstructorModern to follow single responsibility principle.

```
Option 2: Create a pylintrc configuration file

Alternatively, you can create a `.pylintrc` file in your project root with the following content:
```ini
[MASTER]
extension-pkg-whitelist=PyQt6

[TYPECHECK]
generated-members=PyQt6.*
PROVIDES:
- Core service registration
- Motion service registration
- Layout service registration
- Pictograph service registration
- Event system registration
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

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

    @abstractmethod
    def register_event_system(self, container: "DIContainer") -> None:
        """Register event system and command infrastructure."""

    @abstractmethod
    def register_core_services(self, container: "DIContainer") -> None:
        """Register core services using pure dependency injection."""

    @abstractmethod
    def register_motion_services(self, container: "DIContainer") -> None:
        """Register motion services using pure dependency injection."""


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
        self.register_core_services(
            container
        )  # Register core services including UI state management
        self.register_data_services(container)
        self.register_motion_services(container)
        self.register_layout_services(container)
        self.register_pictograph_services(container)
        self.register_positioning_services(container)
        self.register_option_picker_services(container)
        self.register_workbench_services(container)

        self._update_progress("Services configured")

    def register_event_system(self, container: "DIContainer") -> None:
        """Register event system and command infrastructure."""
        try:
            from core.commands import CommandProcessor
            from core.events import IEventBus, get_event_bus

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
            ILayoutService,
            IUIStateManagementService,
        )

        # Register service types with factory functions for proper DI
        def create_layout_service():
            event_bus = None
            try:
                from core.events import IEventBus

                event_bus = container.resolve(IEventBus)
            except Exception:
                # Event bus not available, continue without it
                pass
            return LayoutManagementService(event_bus=event_bus)

        # Register with factory functions for proper dependency resolution
        container.register_factory(ILayoutService, create_layout_service)

        # Register UI state service as singleton since it has no dependencies
        container.register_singleton(
            IUIStateManagementService, UIStateManagementService
        )

    def register_motion_services(self, container: "DIContainer") -> None:
        """Register motion services using pure dependency injection."""
        from application.services.motion.motion_orientation_service import (
            IMotionOrientationService,
            MotionOrientationService,
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

    def register_pictograph_services(self, container: "DIContainer") -> None:
        """Register pictograph services using pure dependency injection."""
        from application.services.data.pictograph_data_service import (
            IPictographDataService,
            PictographDataService,
        )
        from application.services.core.pictograph_management_service import (
            PictographManagementService,
        )
        from core.interfaces.core_services import IPictographContextService
        from application.services.ui.pictograph_context_service import (
            PictographContextService,
        )

        # Register service types, not instances - pure DI
        container.register_singleton(IPictographDataService, PictographDataService)
        container.register_singleton(
            PictographManagementService, PictographManagementService
        )

        # Register pictograph context service for robust context detection
        container.register_singleton(
            IPictographContextService, PictographContextService
        )
        print("🔧 [SERVICE_REGISTRATION] Registered IPictographContextService")

        # Debug: Verify service can be resolved immediately after registration
        try:
            test_service = container.resolve(IPictographContextService)
            print(
                f"✅ [SERVICE_REGISTRATION] IPictographContextService resolved successfully: {type(test_service).__name__}"
            )
        except Exception as e:
            print(
                f"❌ [SERVICE_REGISTRATION] Failed to resolve IPictographContextService: {e}"
            )

    def register_workbench_services(self, container: "DIContainer") -> None:
        """Register workbench services."""
        from presentation.factories.workbench_factory import (
            configure_workbench_services,
        )

        configure_workbench_services(container)

    def register_positioning_services(self, container: "DIContainer") -> None:
        """Register microservices-based positioning services."""
        try:
            # Import the individual calculator services with correct class names
            from application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service import (
                ArrowAdjustmentCalculatorService,
            )
            from application.services.positioning.arrows.coordinate_system.arrow_coordinate_system_service import (
                ArrowCoordinateSystemService,
            )
            from application.services.positioning.arrows.calculation.arrow_location_calculator import (
                ArrowLocationCalculatorService,
            )
            from application.services.positioning.arrows.calculation.arrow_rotation_calculator import (
                ArrowRotationCalculatorService,
            )
            from application.services.positioning.arrows.orchestration.arrow_positioning_orchestrator import (
                ArrowPositioningOrchestrator,
            )
            from core.interfaces.positioning_services import (
                IArrowAdjustmentCalculator,
                IArrowCoordinateSystemService,
                IArrowLocationCalculator,
                IArrowRotationCalculator,
                IArrowPositioningOrchestrator,
            )

            # Register calculator microservices
            container.register_singleton(
                IArrowLocationCalculator, ArrowLocationCalculatorService
            )
            container.register_singleton(
                IArrowRotationCalculator, ArrowRotationCalculatorService
            )
            container.register_singleton(
                IArrowAdjustmentCalculator, ArrowAdjustmentCalculatorService
            )
            container.register_singleton(
                IArrowCoordinateSystemService, ArrowCoordinateSystemService
            )

            # Register orchestrator (replaces monolith)
            container.register_singleton(
                IArrowPositioningOrchestrator, ArrowPositioningOrchestrator
            )
        except ImportError as e:
            # Some positioning services not available - continue
            print(f"⚠️ Failed to import positioning services: {e}")
            print(f"   This means IArrowPositioningOrchestrator will not be available")

        try:
            # Register prop management services
            from application.services.positioning.props.orchestration.prop_management_service import (
                PropManagementService,
                IPropManagementService,
            )

            container.register_singleton(IPropManagementService, PropManagementService)
        except ImportError:
            # Prop management service not available - continue
            pass

        try:
            # Import existing prop orchestrator (keep if still needed)
            from application.services.core.pictograph_orchestrator import (
                IPictographOrchestrator,
                PictographOrchestrator,
            )
            from application.services.positioning.props.orchestration.prop_orchestrator import (
                IPropOrchestrator,
                PropOrchestrator,
            )  # Register remaining orchestrators

            container.register_singleton(IPropOrchestrator, PropOrchestrator)
            container.register_singleton(
                IPictographOrchestrator, PictographOrchestrator
            )
        except ImportError:
            # Orchestrators not available - continue
            pass

    def register_option_picker_services(self, container: "DIContainer") -> None:
        """Register the refactored option picker services."""
        # Import the refactored option picker services
        from application.services.option_picker.data_service import (
            OptionPickerDataService,
        )
        from application.services.option_picker.display_service import (
            OptionPickerDisplayService,
        )
        from application.services.option_picker.event_service import (
            OptionPickerEventService,
        )
        from application.services.option_picker.initialization_service import (
            OptionPickerInitializationService,
        )
        from application.services.option_picker.orchestrator import (
            OptionPickerOrchestrator,
        )
        from core.interfaces.option_picker_services import (
            IOptionPickerDataService,
            IOptionPickerDisplayService,
            IOptionPickerEventService,
            IOptionPickerInitializationService,
            IOptionPickerOrchestrator,
        )

        # Register the refactored option picker services
        container.register_singleton(
            IOptionPickerInitializationService, OptionPickerInitializationService
        )
        container.register_singleton(IOptionPickerDataService, OptionPickerDataService)
        container.register_singleton(
            IOptionPickerDisplayService, OptionPickerDisplayService
        )
        container.register_singleton(
            IOptionPickerEventService, OptionPickerEventService
        )
        container.register_singleton(
            IOptionPickerOrchestrator, OptionPickerOrchestrator
        )

    def register_data_services(self, container: "DIContainer") -> None:
        """Register the new refactored data services."""
        # Import the new data services
        from application.services.data.csv_data_service import (
            CSVDataService,
            ICSVDataService,
        )
        from application.services.positioning.props.configuration.json_configuration_service import (
            IJSONConfigurationService,
            JSONConfigurationService,
        )

        # Register the data services
        container.register_singleton(ICSVDataService, CSVDataService)
        container.register_singleton(
            IJSONConfigurationService, JSONConfigurationService
        )

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
