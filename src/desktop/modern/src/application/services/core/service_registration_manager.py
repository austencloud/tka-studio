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

REFACTORING NOTE:
This file is being refactored into specialized registrars following microservices architecture.
The goal is to split this large manager into focused, domain-specific registrars.
"""

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


# ============================================================================
# BASE REGISTRATION INFRASTRUCTURE
# ============================================================================


class IServiceRegistrar(ABC):
    """
    Interface for service registrars in the microservices registration architecture.

    Each registrar is responsible for registering a specific domain of services
    (e.g., positioning services, data services, etc.) following single responsibility principle.
    """

    @abstractmethod
    def register_services(self, container: "DIContainer") -> None:
        """Register all services for this domain in the DI container."""

    @abstractmethod
    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""

    @abstractmethod
    def get_registered_services(self) -> List[str]:
        """Get list of service names registered by this registrar."""

    @abstractmethod
    def is_critical(self) -> bool:
        """Return True if this registrar's services are critical for application startup."""


class BaseServiceRegistrar(IServiceRegistrar):
    """
    Base implementation for service registrars providing common functionality.

    Provides:
    - Progress tracking integration
    - Service availability tracking
    - Graceful degradation for optional services
    - Standardized error handling
    """

    def __init__(self, progress_callback: Optional[callable] = None):
        """Initialize with optional progress callback."""
        self.progress_callback = progress_callback
        self._service_availability: Dict[str, bool] = {}
        self._registered_services: List[str] = []

    def get_registered_services(self) -> List[str]:
        """Get list of service names registered by this registrar."""
        return self._registered_services.copy()

    def get_service_availability(self) -> Dict[str, bool]:
        """Get availability status of services in this domain."""
        return self._service_availability.copy()

    def _update_progress(self, message: str) -> None:
        """Update progress if callback is available."""
        if self.progress_callback:
            self.progress_callback(message)

    def _mark_service_available(self, service_name: str) -> None:
        """Mark a service as successfully registered."""
        self._service_availability[service_name] = True
        if service_name not in self._registered_services:
            self._registered_services.append(service_name)

    def _mark_service_unavailable(self, service_name: str) -> None:
        """Mark a service as failed to register."""
        self._service_availability[service_name] = False

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
        self._mark_service_unavailable(service_name)


# ============================================================================
# NEW REGISTRATION COORDINATOR (LIGHTWEIGHT)
# ============================================================================


class ServiceRegistrationCoordinator:
    """
    Lightweight coordinator for the new microservices registration architecture.

    Delegates registration to specialized registrars while maintaining:
    - Progress tracking across all registrars
    - Service availability monitoring
    - Graceful degradation for optional services
    - Dependency ordering

    This replaces the monolithic ServiceRegistrationManager with a clean,
    maintainable architecture following single responsibility principle.
    """

    def __init__(self, progress_callback: Optional[callable] = None):
        """Initialize coordinator with optional progress callback."""
        self.progress_callback = progress_callback
        self._registrars: List[IServiceRegistrar] = []
        self._initialize_registrars()

    def _initialize_registrars(self) -> None:
        """Initialize all specialized registrars in dependency order."""
        from .registrars import (
            AnimationServiceRegistrar,
            CoreServiceRegistrar,
            DataServiceRegistrar,
            EventSystemRegistrar,
            GraphEditorServiceRegistrar,
            MotionServiceRegistrar,
            OptionPickerServiceRegistrar,
            PictographServiceRegistrar,
            PositioningServiceRegistrar,
            SequenceServiceRegistrar,
            StartPositionServiceRegistrar,
            WorkbenchServiceRegistrar,
        )

        # Initialize registrars in dependency order
        # Critical services first, then optional services
        self._registrars = [
            # Phase 1: Foundation services (no dependencies)
            MotionServiceRegistrar(self.progress_callback),
            DataServiceRegistrar(self.progress_callback),
            # Phase 2: Core services (may depend on data/motion)
            CoreServiceRegistrar(self.progress_callback),
            SequenceServiceRegistrar(self.progress_callback),
            PictographServiceRegistrar(self.progress_callback),
            StartPositionServiceRegistrar(
                self.progress_callback
            ),  # Add start position services
            WorkbenchServiceRegistrar(self.progress_callback),
            # Phase 3: Complex services (depend on core services)
            PositioningServiceRegistrar(self.progress_callback),
            OptionPickerServiceRegistrar(self.progress_callback),
            # Phase 4: Optional services
            EventSystemRegistrar(self.progress_callback),
            GraphEditorServiceRegistrar(self.progress_callback),
            AnimationServiceRegistrar(self.progress_callback),
        ]

    def register_all_services(self, container: "DIContainer") -> None:
        """Register all services using specialized registrars."""
        self._update_progress("Configuring services with new registrar architecture...")

        critical_failures = []
        optional_failures = []

        for registrar in self._registrars:
            try:
                registrar.register_services(container)
                self._update_progress(f"{registrar.get_domain_name()} configured")

            except Exception as e:
                if registrar.is_critical():
                    critical_failures.append((registrar.get_domain_name(), e))
                else:
                    optional_failures.append((registrar.get_domain_name(), e))
                    logger.warning(
                        f"Optional service domain failed: {registrar.get_domain_name()}: {e}"
                    )

        # Report results
        if critical_failures:
            error_msg = f"Critical service registration failures: {critical_failures}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        if optional_failures:
            logger.warning(
                f"Optional service failures (application will continue): {optional_failures}"
            )

        self._update_progress("Services configured with new registrar architecture")

    def get_registration_status(self) -> dict:
        """Get comprehensive status of service registration across all registrars."""
        status = {
            "registrar_count": len(self._registrars),
            "registrars": {},
            "total_services": 0,
            "available_services": 0,
            "critical_registrars": 0,
            "optional_registrars": 0,
        }

        for registrar in self._registrars:
            domain_name = registrar.get_domain_name()
            registrar_services = registrar.get_registered_services()

            if hasattr(registrar, "get_service_availability"):
                availability = registrar.get_service_availability()
                available_count = sum(availability.values())
            else:
                available_count = len(registrar_services)
                availability = {service: True for service in registrar_services}

            status["registrars"][domain_name] = {
                "is_critical": registrar.is_critical(),
                "services": registrar_services,
                "service_count": len(registrar_services),
                "available_count": available_count,
                "availability": availability,
            }

            status["total_services"] += len(registrar_services)
            status["available_services"] += available_count

            if registrar.is_critical():
                status["critical_registrars"] += 1
            else:
                status["optional_registrars"] += 1

        return status

    def _update_progress(self, message: str) -> None:
        """Update progress if callback is available."""
        if self.progress_callback:
            self.progress_callback(message)


# ============================================================================
# LEGACY INTERFACE (BACKWARD COMPATIBILITY)
# ============================================================================


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
    BACKWARD COMPATIBILITY WRAPPER for the new microservices registration architecture.

    This class maintains the same interface as the original ServiceRegistrationManager
    but delegates to the new ServiceRegistrationCoordinator internally. This allows
    existing code to continue working without changes while benefiting from the new
    architecture.

    MIGRATION NOTE: New code should use ServiceRegistrationCoordinator directly.
    This wrapper will be deprecated once all consumers are migrated.
    """

    def __init__(self, progress_callback: Optional[callable] = None):
        """Initialize with optional progress callback."""
        self.progress_callback = progress_callback

        # Delegate to the new coordinator
        self._coordinator = ServiceRegistrationCoordinator(progress_callback)

        # Legacy service availability tracking for backward compatibility
        self._service_availability = {
            "event_system": False,
            "arrow_positioning": False,
            "prop_management": False,
            "prop_orchestration": False,
        }

    def register_all_services(self, container: "DIContainer") -> None:
        """
        Register all application services in the DI container.

        BACKWARD COMPATIBILITY: Delegates to the new ServiceRegistrationCoordinator
        while maintaining the same interface for existing code.
        """
        # Delegate to the new coordinator for most services
        self._coordinator.register_all_services(container)

        # Register remaining services that haven't been migrated to registrars yet
        self._register_remaining_legacy_services(container)

        self._update_progress("Services configured")

    def _register_remaining_legacy_services(self, container: "DIContainer") -> None:
        """Register services that haven't been migrated to specialized registrars yet."""
        # All services are now handled by specialized registrars!
        # This method is kept for backward compatibility but no longer needed.
        pass

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
        from application.services.sequence.sequence_restorer import (
            ISequenceRestorer,
            SequenceRestorer,
        )
        from application.services.ui.window_discovery_service import (
            IWindowDiscoveryService,
            WindowDiscoveryService,
        )

        # Register individual services
        container.register_singleton(IWindowManagementService, WindowManagementService)
        container.register_singleton(IWindowDiscoveryService, WindowDiscoveryService)
        container.register_singleton(ISequenceRestorer, SequenceRestorer)

        # Register session coordinator with sequence restoration service dependency
        def create_session_coordinator():
            sequence_service = container.resolve(ISequenceRestorer)
            return SessionRestorationCoordinator(sequence_service)

        container.register_factory(
            ISessionRestorationCoordinator, create_session_coordinator
        )

        # Register orchestrator with all dependencies
        def create_app_init_orchestrator():
            window_service = container.resolve(IWindowManagementService)
            session_coordinator = container.resolve(ISessionRestorationCoordinator)
            window_discovery_service = container.resolve(IWindowDiscoveryService)
            # Session service is optional and resolved by ApplicationOrchestrator
            return ApplicationInitializationOrchestrator(
                window_service, session_coordinator, window_discovery_service
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
        from application.services.pictograph.pictograph_position_matcher import (
            PictographCSVManager,
        )
        from application.services.pictograph_pool_manager import PictographPoolManager
        from core.interfaces.core_services import (
            IPictographBorderManager,
            IPictographContextDetector,
        )

        container.register_singleton(IPictographDataManager, PictographDataManager)
        container.register_singleton(PictographCSVManager, PictographCSVManager)
        container.register_singleton(IPictographBorderManager, PictographBorderManager)
        container.register_singleton(
            IPictographContextDetector, PictographContextDetector
        )
        # Register global visibility service as singleton to ensure all components use the same instance
        container.register_singleton(
            PictographVisibilityManager, PictographVisibilityManager
        )

        # Register pictograph pool manager as singleton for high-performance option picker
        # CRITICAL: Must be singleton so all components use the same initialized pool
        # Use factory registration but ensure singleton behavior by storing instance
        _pool_manager_instance = PictographPoolManager(container=container)
        container.register_instance(PictographPoolManager, _pool_manager_instance)

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
            from application.services.positioning.arrows.orchestration.arrow_adjustment_calculator import (
                ArrowAdjustmentCalculator,
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
                IArrowAdjustmentCalculator, ArrowAdjustmentCalculator
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
            # Register position matching service for option picker
            from application.services.positioning.arrows.utilities.pictograph_position_matcher import (
                PictographPositionMatcher,
            )

            container.register_singleton(
                PictographPositionMatcher, PictographPositionMatcher
            )
            self._service_availability["position_matching"] = True
        except ImportError as e:
            # GRACEFUL DEGRADATION: Position matching service not available - continue
            self._handle_service_unavailable(
                "Position matching service", e, "Option picker position matching"
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

            from application.services.positioning.props.orchestration.prop_orchestrator import (  # Register remaining orchestrators
                IPropOrchestrator,
                PropOrchestrator,
            )

            container.register_singleton(IPropOrchestrator, PropOrchestrator)

        except ImportError:
            # Orchestrators not available - continue
            pass

    def register_option_picker_services(self, container: "DIContainer") -> None:
        """Register the refactored option picker services and new microservices."""
        # Import existing services
        from application.services.option_picker.frame_pool_service import (
            FramePoolService,
        )
        from application.services.option_picker.option_configuration_service import (
            OptionConfigurationService,
        )
        from application.services.option_picker.option_loader import OptionLoader
        from application.services.option_picker.option_picker_size_calculator import (
            OptionPickerSizeCalculator,
        )
        from application.services.option_picker.option_pool_service import (
            OptionPoolService,
        )
        from application.services.option_picker.option_provider import OptionProvider

        # Import new microservices
        from application.services.option_picker.sequence_option_service import (
            SequenceOptionService,
        )
        from application.services.positioning.arrows.utilities.pictograph_position_matcher import (
            PictographPositionMatcher,
        )
        from core.interfaces.option_picker_interfaces import IOptionProvider

        # Register existing services
        container.register_singleton(IOptionProvider, OptionProvider)

        # Register PictographPositionMatcher (missing registration!)
        container.register_singleton(
            PictographPositionMatcher, PictographPositionMatcher
        )

        # Register new microservices with proper dependencies
        container.register_factory(
            SequenceOptionService,
            lambda c: SequenceOptionService(
                position_matcher=c.resolve(PictographPositionMatcher)
            ),
        )

        container.register_singleton(FramePoolService, FramePoolService)
        container.register_singleton(OptionPoolService, OptionPoolService)
        container.register_singleton(
            OptionConfigurationService, OptionConfigurationService
        )

        container.register_factory(
            OptionLoader,
            lambda c: OptionLoader(frame_pool_service=c.resolve(FramePoolService)),
        )

        container.register_singleton(
            OptionPickerSizeCalculator, OptionPickerSizeCalculator
        )

        # Register presentation component factories with injected services
        self._register_option_picker_component_factories(container)

    def _register_option_picker_component_factories(
        self, container: "DIContainer"
    ) -> None:
        """Register option picker component factories with proper dependency injection."""
        try:
            # Import components and services
            from application.services.option_picker.option_configuration_service import (
                OptionConfigurationService,
            )
            from application.services.option_picker.option_picker_size_calculator import (
                OptionPickerSizeCalculator,
            )
            from application.services.option_picker.option_pool_service import (
                OptionPoolService,
            )
            from application.services.option_picker.sequence_option_service import (
                SequenceOptionService,
            )

            # Import PictographPoolManager
            from application.services.pictograph_pool_manager import (
                PictographPoolManager,
            )
            from presentation.components.option_picker.components.option_picker_scroll import (
                OptionPickerScroll,
            )

            # Register OptionPickerScroll factory with injected microservices
            def create_option_picker_scroll(c):
                try:
                    from core.interfaces.animation_core_interfaces import (
                        IAnimationOrchestrator,
                    )

                    animation_orchestrator = c.resolve(IAnimationOrchestrator)
                except Exception:
                    # Animation system not available - continue without it
                    animation_orchestrator = None

                return OptionPickerScroll(
                    sequence_option_service=c.resolve(SequenceOptionService),
                    option_pool_service=c.resolve(OptionPoolService),
                    option_sizing_service=c.resolve(OptionPickerSizeCalculator),
                    option_config_service=c.resolve(OptionConfigurationService),
                    pictograph_pool_manager=c.resolve(PictographPoolManager),
                    animation_orchestrator=animation_orchestrator,
                )

            container.register_factory(OptionPickerScroll, create_option_picker_scroll)

            self._update_progress("Option picker component factories registered")

        except ImportError as e:
            # Components not available - continue without registration
            print(f"⚠️ Option picker components not available: {e}")

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

        BACKWARD COMPATIBILITY: Combines status from the new coordinator
        with legacy service availability tracking.
        """
        # Get status from the new coordinator
        coordinator_status = self._coordinator.get_registration_status()

        # Combine with legacy format for backward compatibility
        legacy_status = {
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

        # Merge coordinator status with legacy status
        legacy_status.update(
            {
                "coordinator_status": coordinator_status,
                "total_services_new_architecture": coordinator_status["total_services"],
                "available_services_new_architecture": coordinator_status[
                    "available_services"
                ],
            }
        )

        return legacy_status

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
