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

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


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
        # Service availability tracking for better debugging and monitoring
        self._service_availability = {
            "event_system": False,
            "arrow_positioning": False,
            "prop_management": False,
            "prop_orchestration": False,
        }

    def register_all_services(self, container: "DIContainer") -> None:
        """Register all application services in the DI container."""
        self._update_progress("Configuring services...")

        # Register services in dependency order
        self.register_event_system(container)
        self.register_core_services(
            container
        )  # Register core services including UI state management
        self.register_data_services(container)
        self.register_sequence_services(container)  # ✅ NEW - Sequence orchestration
        self.register_motion_services(container)
        self.register_layout_services(container)
        self.register_pictograph_services(container)
        self.register_positioning_services(container)
        self.register_option_picker_services(container)
        self.register_graph_editor_services(container)
        self.register_workbench_services(container)

        self._update_progress("Services configured")

    def register_event_system(self, container: "DIContainer") -> None:
        """
        Register event system and command infrastructure.

        SERVICE CRITICALITY: OPTIONAL
        - Application can run without event system for backward compatibility
        - Graceful degradation: reduced functionality but no crashes
        - Used for: inter-component communication, command processing
        """
        try:
            from core.commands import CommandProcessor
            from core.events import IEventBus, get_event_bus

            # Get or create event bus
            event_bus = get_event_bus()
            container.register_instance(IEventBus, event_bus)

            # Register command processor
            command_processor = CommandProcessor(event_bus)
            container.register_instance(CommandProcessor, command_processor)

            self._service_availability["event_system"] = True
            self._update_progress("Event system registered")

        except ImportError as e:
            print(f"⚠️ Event system not available: {e}")
            # GRACEFUL DEGRADATION: Continue without event system for backward compatibility
            # Impact: Reduced inter-component communication, but core functionality preserved

    def register_core_services(self, container: "DIContainer") -> None:
        """
        Register core services using pure dependency injection.

        SERVICE CRITICALITY: CRITICAL
        - These services are required for basic application functionality
        - No try-catch blocks: failures should cause application startup to fail
        - Used for: layout management, UI state coordination, lifecycle management
        """

        from application.services.layout.layout_manager import LayoutManager
        from application.services.ui.coordination.ui_coordinator import UICoordinator
        from core.interfaces.core_services import ILayoutService, IUIStateManager

        # Register service types with factory functions for proper DI
        def create_layout_service():
            event_bus = None
            try:
                from core.events import IEventBus

                event_bus = container.resolve(IEventBus)
            except Exception:
                # Event bus not available, continue without it
                pass
            return LayoutManager(event_bus=event_bus)

        # Register with factory functions for proper dependency resolution
        container.register_factory(ILayoutService, create_layout_service)

        # Register UI state service as singleton since it has no dependencies
        container.register_singleton(IUIStateManager, UICoordinator)

        # Register new lifecycle services
        self._register_lifecycle_services(container)

    def _register_lifecycle_services(self, container: "DIContainer") -> None:
        """Register the new refactored lifecycle services."""
        from application.services.core.application_initialization_orchestrator import (
            ApplicationInitializationOrchestrator,
            IApplicationInitializationOrchestrator,
        )
        from application.services.core.session_restoration_coordinator import (
            ISessionRestorationCoordinator,
            SessionRestorationCoordinator,
        )
        from application.services.core.window_management_service import (
            IWindowManagementService,
            WindowManagementService,
        )
        from application.services.sequence.sequence_restoration_service import (
            ISequenceRestorationService,
            SequenceRestorationService,
        )

        # Register individual services
        container.register_singleton(IWindowManagementService, WindowManagementService)
        container.register_singleton(
            ISequenceRestorationService, SequenceRestorationService
        )

        # Register session coordinator with sequence restoration service dependency
        def create_session_coordinator():
            sequence_service = container.resolve(ISequenceRestorationService)
            return SessionRestorationCoordinator(sequence_service)

        container.register_factory(
            ISessionRestorationCoordinator, create_session_coordinator
        )

        # Register orchestrator with all dependencies
        def create_app_init_orchestrator():
            window_service = container.resolve(IWindowManagementService)
            session_coordinator = container.resolve(ISessionRestorationCoordinator)
            # Session service is optional and resolved by ApplicationOrchestrator
            return ApplicationInitializationOrchestrator(
                window_service, session_coordinator
            )

        container.register_factory(
            IApplicationInitializationOrchestrator, create_app_init_orchestrator
        )

    def register_sequence_services(self, container: "DIContainer") -> None:
        """Register sequence services with interface bindings."""
        # Import sequence service interfaces and implementations
        from application.services.sequence.beat_factory import BeatFactory, IBeatFactory
        from application.services.sequence.loader import SequenceLoader
        from application.services.sequence.sequence_beat_operations import (
            SequenceBeatOperations,
        )
        from application.services.sequence.sequence_persister import (
            ISequencePersister,
            SequencePersister,
        )
        from application.services.sequence.sequence_repository import (
            ISequenceRepository,
            SequenceRepository,
        )
        from application.services.sequence.sequence_start_position_manager import (
            SequenceStartPositionManager,
        )
        from application.services.sequence.sequence_validator import (
            ISequenceValidator,
            SequenceValidator,
        )

        # Register sequence services with interfaces
        container.register_singleton(IBeatFactory, BeatFactory)
        container.register_singleton(ISequencePersister, SequencePersister)
        container.register_singleton(ISequenceRepository, SequenceRepository)
        container.register_singleton(ISequenceValidator, SequenceValidator)

        # Register services without interfaces yet
        container.register_singleton(SequenceLoader, SequenceLoader)
        container.register_singleton(SequenceBeatOperations, SequenceBeatOperations)
        container.register_singleton(
            SequenceStartPositionManager, SequenceStartPositionManager
        )

    def register_motion_services(self, container: "DIContainer") -> None:
        """Register motion services using pure dependency injection."""
        from application.services.motion.orientation_calculator import (
            IOrientationCalculator,
            OrientationCalculator,
        )

        container.register_singleton(IOrientationCalculator, OrientationCalculator)

    def register_layout_services(self, container: "DIContainer") -> None:
        """Register layout services."""
        from application.services.option_picker.section_layout_manager import (
            SectionLayoutManager,
        )

        container.register_singleton(SectionLayoutManager, SectionLayoutManager)

        # Note: Layout services have been consolidated into LayoutManagementService
        # which is already registered in register_core_services() as ILayoutService
        #
        # The old separate services (BeatLayoutService, ResponsiveLayoutService,
        # ComponentLayoutService) have been consolidated for better maintainability

    def register_pictograph_services(self, container: "DIContainer") -> None:
        """Register pictograph services using pure dependency injection."""
        from application.services.data.pictograph_data_service import (
            IPictographDataManager,
            PictographDataManager,
        )
        from application.services.pictograph.border_manager import (
            PictographBorderManager,
        )
        from application.services.pictograph.context_detection_service import (
            PictographContextDetector,
        )
        from application.services.pictograph.global_visibility_service import (
            PictographVisibilityManager,
        )
        from application.services.pictograph.pictograph_manager import PictographManager
        from core.interfaces.core_services import (
            IPictographBorderManager,
            IPictographContextDetector,
        )

        container.register_singleton(IPictographDataManager, PictographDataManager)
        container.register_singleton(PictographManager, PictographManager)
        container.register_singleton(IPictographBorderManager, PictographBorderManager)
        container.register_singleton(
            IPictographContextDetector, PictographContextDetector
        )
        # Register global visibility service as singleton to ensure all components use the same instance
        container.register_singleton(
            PictographVisibilityManager, PictographVisibilityManager
        )

    def register_workbench_services(self, container: "DIContainer") -> None:
        """Register workbench services."""
        from application.services.workbench.beat_selection_service import (
            BeatSelectionService,
        )
        from presentation.factories.workbench_factory import (
            configure_workbench_services,
        )

        # Register pure business services
        container.register_singleton(BeatSelectionService, BeatSelectionService)

        # Register presentation services
        configure_workbench_services(container)

    def register_positioning_services(self, container: "DIContainer") -> None:
        """
        Register microservices-based positioning services.

        SERVICE CRITICALITY: OPTIONAL (with specific impact warnings)
        - Application can run without positioning services but with reduced functionality
        - Graceful degradation: specific warnings about missing arrow positioning capabilities
        - Used for: arrow positioning, prop management, pictograph orchestration
        """
        try:
            # Import the individual calculator services with correct class names
            from application.services.positioning.arrows.calculation.arrow_location_calculator import (
                ArrowLocationCalculatorService,
            )
            from application.services.positioning.arrows.calculation.arrow_rotation_calculator import (
                ArrowRotationCalculatorService,
            )
            from application.services.positioning.arrows.coordinate_system.arrow_coordinate_system_service import (
                ArrowCoordinateSystemService,
            )
            from application.services.positioning.arrows.orchestration.arrow_adjustment_calculator_service import (
                ArrowAdjustmentCalculatorService,
            )
            from application.services.positioning.arrows.orchestration.arrow_positioning_orchestrator import (
                ArrowPositioningOrchestrator,
            )
            from core.interfaces.positioning_services import (
                IArrowAdjustmentCalculator,
                IArrowCoordinateSystemService,
                IArrowLocationCalculator,
                IArrowPositioningOrchestrator,
                IArrowRotationCalculator,
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

            # Register orchestrator (replaces monolith) with dependency injection
            def create_arrow_positioning_orchestrator():
                location_calculator = container.resolve(IArrowLocationCalculator)
                rotation_calculator = container.resolve(IArrowRotationCalculator)
                adjustment_calculator = container.resolve(IArrowAdjustmentCalculator)
                coordinate_system = container.resolve(IArrowCoordinateSystemService)

                return ArrowPositioningOrchestrator(
                    location_calculator=location_calculator,
                    rotation_calculator=rotation_calculator,
                    adjustment_calculator=adjustment_calculator,
                    coordinate_system=coordinate_system,
                )

            container.register_factory(
                IArrowPositioningOrchestrator, create_arrow_positioning_orchestrator
            )
            self._service_availability["arrow_positioning"] = True
        except ImportError as e:
            # GRACEFUL DEGRADATION: Some positioning services not available - continue
            self._handle_service_unavailable(
                "Arrow positioning services",
                e,
                "Arrow positioning calculations in pictographs",
            )

        try:
            # Register prop management services
            from application.services.positioning.props.orchestration.prop_management_service import (
                IPropManagementService,
                PropManagementService,
            )

            container.register_singleton(IPropManagementService, PropManagementService)
            self._service_availability["prop_management"] = True
        except ImportError as e:
            # GRACEFUL DEGRADATION: Prop management service not available - continue
            self._handle_service_unavailable(
                "Prop management service", e, "Prop positioning and management"
            )

        try:
            # Import existing prop orchestrator (keep if still needed)
            from application.services.pictograph.pictograph_orchestrator import (
                IPictographOrchestrator,
                PictographOrchestrator,
            )
            from application.services.positioning.props.orchestration.prop_orchestrator import (  # Register remaining orchestrators
                IPropOrchestrator,
                PropOrchestrator,
            )

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

        from application.services.option_picker.option_picker_display_manager import (
            OptionPickerDisplayManager,
        )
        from application.services.option_picker.option_picker_event_service import (
            OptionPickerEventService,
        )
        from application.services.option_picker.option_picker_initializer import (
            OptionPickerInitializer,
        )
        from application.services.option_picker.option_picker_orchestrator import (
            OptionPickerOrchestrator,
        )
        from application.services.option_picker.option_provider import OptionProvider
        from core.interfaces.option_picker_interfaces import (
            IOptionPickerDisplayService,
            IOptionPickerEventService,
            IOptionPickerInitializer,
            IOptionPickerOrchestrator,
            IOptionProvider,
        )

        # Register the refactored option picker services
        container.register_singleton(IOptionProvider, OptionProvider)
        container.register_singleton(IOptionPickerInitializer, OptionPickerInitializer)
        container.register_singleton(
            IOptionPickerDisplayService, OptionPickerDisplayManager
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
        from application.services.data.csv_reader import CSVReader, ICSVReader

        # Import the Phase 2 conversion services
        # Import the Phase 1 foundation data services
        from application.services.data.data_service import DataManager, IDataManager
        from application.services.data.dataset_query import DatasetQuery, IDatasetQuery
        from application.services.data.legacy_to_modern_converter import (
            LegacyToModernConverter,
        )
        from application.services.data.modern_to_legacy_converter import (
            ModernToLegacyConverter,
        )
        from application.services.data.pictograph_data_service import (
            IPictographDataManager,
            PictographDataManager,
        )
        from application.services.positioning.props.configuration.json_configuration_service import (
            IJSONConfigurator,
            JSONConfigurator,
        )

        # Register the existing data services
        container.register_singleton(ICSVReader, CSVReader)
        container.register_singleton(IJSONConfigurator, JSONConfigurator)
        container.register_singleton(IDataManager, DataManager)
        container.register_singleton(IDatasetQuery, DatasetQuery)
        container.register_singleton(IPictographDataManager, PictographDataManager)
        # Register microservices directly instead of facades
        container.register_singleton(LegacyToModernConverter, LegacyToModernConverter)
        container.register_singleton(ModernToLegacyConverter, ModernToLegacyConverter)

    def register_graph_editor_services(self, container: "DIContainer") -> None:
        """Register graph editor services using pure dependency injection."""
        from application.services.graph_editor.graph_editor_state_manager import (
            GraphEditorStateManager,
        )

        # Register graph editor state service as singleton for centralized state management
        container.register_singleton(GraphEditorStateManager, GraphEditorStateManager)

    def get_registration_status(self) -> dict:
        """
        Get comprehensive status of service registration.

        Returns detailed information about which services are available
        and which have failed to register for better debugging.
        """
        return {
            "event_system_available": self._service_availability["event_system"],
            "arrow_positioning_available": self._service_availability[
                "arrow_positioning"
            ],
            "prop_management_available": self._service_availability["prop_management"],
            "prop_orchestration_available": self._service_availability[
                "prop_orchestration"
            ],
            "services_registered": True,
            "availability_summary": {
                "total_optional_services": len(self._service_availability),
                "available_services": sum(self._service_availability.values()),
                "missing_services": [
                    service
                    for service, available in self._service_availability.items()
                    if not available
                ],
            },
        }

    def _update_progress(self, message: str) -> None:
        """Update progress if callback is available."""
        if self.progress_callback:
            self.progress_callback(message)

    def _handle_service_unavailable(
        self, service_name: str, error: Exception, functionality_impact: str
    ) -> None:
        """
        Standardized handling for unavailable optional services.

        Args:
            service_name: Name of the service that failed to register
            error: The exception that occurred
            functionality_impact: Description of what functionality is affected
        """
        logger.warning(f"{service_name} not available: {error}")
        logger.warning(f"Impact: {service_name} will not be available")
        logger.warning(f"Functionality affected: {functionality_impact}")

        # Update availability tracking
        service_key = service_name.lower().replace(" ", "_")
        if service_key in self._service_availability:
            self._service_availability[service_key] = False

    def get_service_availability_summary(self) -> str:
        """
        Get a human-readable summary of service availability.

        Useful for debugging and monitoring which optional services are available.
        """
        available = [
            name for name, status in self._service_availability.items() if status
        ]
        missing = [
            name for name, status in self._service_availability.items() if not status
        ]

        summary = f"Service Availability Summary:\n"
        summary += f"  Available ({len(available)}): {', '.join(available) if available else 'None'}\n"
        summary += (
            f"  Missing ({len(missing)}): {', '.join(missing) if missing else 'None'}\n"
        )
        summary += f"  Total optional services: {len(self._service_availability)}"

        return summary
