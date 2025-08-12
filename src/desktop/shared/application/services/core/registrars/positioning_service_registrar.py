"""
Positioning Service Registrar

Handles registration of positioning-related services following microservices architecture.
This is a complex registrar managing arrow positioning, prop management, and orchestration
services with graceful degradation for optional components.

Services Registered:
- ArrowLocationCalculatorService: Arrow location calculations
- ArrowRotationCalculatorService: Arrow rotation calculations
- ArrowAdjustmentCalculatorService: Arrow adjustment calculations
- ArrowCoordinateSystemService: Arrow coordinate system management
- ArrowPositioningOrchestrator: Arrow positioning orchestration
- PictographPositionMatcher: Position matching for option picker
- PropManagementService: Prop management operations
- PropOrchestrator: Prop orchestration
- PictographOrchestrator: Pictograph orchestration
"""

import logging
from typing import TYPE_CHECKING

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class PositioningServiceRegistrar(BaseServiceRegistrar):
    """
    Registrar for positioning-related services.

    Complex registrar handling arrow positioning, prop management, and orchestration
    services. Uses graceful degradation for optional services while ensuring
    critical positioning functionality is available.
    """

    def get_domain_name(self) -> str:
        """Get the name of the service domain this registrar handles."""
        return "Positioning Services"

    def is_critical(self) -> bool:
        """Positioning services are critical for arrow positioning."""
        return True

    def register_services(self, container: "DIContainer") -> None:
        """Register positioning services with graceful degradation."""
        self._update_progress("Registering positioning services...")
        print(
            "🔧 [POSITIONING_REGISTRAR] Starting positioning services registration..."
        )

        # Register arrow positioning services
        self._register_arrow_positioning_services(container)

        # Register arrow placement services (special placement, default placement, etc.)
        self._register_arrow_placement_services(container)

        # Register position matching service
        self._register_position_matching_service(container)

        # Register prop management services
        self._register_prop_management_services(container)

        # Register orchestration services
        self._register_orchestration_services(container)

        self._update_progress("Positioning services registered successfully")

    def _register_arrow_positioning_services(self, container: "DIContainer") -> None:
        """Register arrow positioning microservices."""
        print("🔧 [POSITIONING_REGISTRAR] Registering arrow positioning services...")
        try:
            from desktop.modern.application.services.positioning.arrows.orchestration.arrow_positioning_orchestrator import (
                ArrowPositioningOrchestrator,
            )
            from desktop.modern.core.interfaces.positioning_services import (
                IArrowAdjustmentCalculator,
                IArrowCoordinateSystemService,
                IArrowLocationCalculator,
                IArrowPositioningOrchestrator,
                IArrowRotationCalculator,
            )
            from shared.application.services.positioning.arrows.calculation.arrow_location_calculator import (
                ArrowLocationCalculatorService,
            )
            from shared.application.services.positioning.arrows.calculation.arrow_rotation_calculator import (
                ArrowRotationCalculatorService,
            )
            from shared.application.services.positioning.arrows.coordinate_system.arrow_coordinate_system_service import (
                ArrowCoordinateSystemService,
            )
            from shared.application.services.positioning.arrows.orchestration.arrow_adjustment_calculator import (
                ArrowAdjustmentCalculator,
            )

            # Register calculator microservices
            container.register_singleton(
                IArrowLocationCalculator, ArrowLocationCalculatorService
            )
            self._mark_service_available("ArrowLocationCalculator")

            container.register_singleton(
                IArrowRotationCalculator, ArrowRotationCalculatorService
            )
            self._mark_service_available("ArrowRotationCalculator")

            container.register_singleton(
                IArrowAdjustmentCalculator, ArrowAdjustmentCalculator
            )
            self._mark_service_available("ArrowAdjustmentCalculator")

            container.register_singleton(
                IArrowCoordinateSystemService, ArrowCoordinateSystemService
            )
            self._mark_service_available("ArrowCoordinateSystemService")

            # Register orchestrator as singleton using direct registration
            # First resolve all dependencies
            location_calculator = container.resolve(IArrowLocationCalculator)
            rotation_calculator = container.resolve(IArrowRotationCalculator)
            adjustment_calculator = container.resolve(IArrowAdjustmentCalculator)
            coordinate_system = container.resolve(IArrowCoordinateSystemService)

            # Create the orchestrator instance
            orchestrator_instance = ArrowPositioningOrchestrator(
                location_calculator=location_calculator,
                rotation_calculator=rotation_calculator,
                adjustment_calculator=adjustment_calculator,
                coordinate_system=coordinate_system,
            )

            # Register the instance directly as singleton
            container.register_instance(
                IArrowPositioningOrchestrator, orchestrator_instance
            )
            self._mark_service_available("ArrowPositioningOrchestrator")
            print(
                "✅ [POSITIONING_REGISTRAR] Arrow positioning orchestrator registered successfully"
            )

        except ImportError as e:
            print(f"❌ [POSITIONING_REGISTRAR] Import error: {e}")
            self._handle_service_unavailable(
                "Arrow positioning services",
                e,
                "Arrow positioning calculations in pictographs",
            )
        except Exception as e:
            print(f"❌ [POSITIONING_REGISTRAR] Registration error: {e}")
            import traceback

            traceback.print_exc()
            raise

    def _register_arrow_placement_services(self, container: "DIContainer") -> None:
        """Register arrow placement services (special placement, default placement, etc.)."""
        try:
            # Import arrow placement services
            from desktop.modern.application.services.positioning.arrows.placement.special_placement_service import (
                SpecialPlacementService,
            )
            from shared.application.services.positioning.arrows.key_generators.attribute_key_generator import (
                AttributeKeyGenerator,
            )
            from shared.application.services.positioning.arrows.key_generators.placement_key_generator import (
                PlacementKeyGenerator,
            )
            from shared.application.services.positioning.arrows.key_generators.turns_tuple_key_generator import (
                TurnsTupleKeyGenerator,
            )
            from shared.application.services.positioning.arrows.placement.default_placement_service import (
                DefaultPlacementService,
            )
            from shared.application.services.positioning.arrows.placement.special_placement_ori_key_generator import (
                SpecialPlacementOriKeyGenerator,
            )

            # Register placement services as singletons
            container.register_singleton(
                SpecialPlacementService, SpecialPlacementService
            )
            container.register_singleton(
                DefaultPlacementService, DefaultPlacementService
            )
            container.register_singleton(
                SpecialPlacementOriKeyGenerator, SpecialPlacementOriKeyGenerator
            )
            container.register_singleton(PlacementKeyGenerator, PlacementKeyGenerator)
            container.register_singleton(TurnsTupleKeyGenerator, TurnsTupleKeyGenerator)
            container.register_singleton(AttributeKeyGenerator, AttributeKeyGenerator)

            # Register arrow adjustment services that depend on placement services
            from desktop.modern.application.services.positioning.arrows.orchestration.arrow_adjustment_lookup import (
                ArrowAdjustmentLookup,
            )
            from shared.application.services.positioning.arrows.orchestration.arrow_adjustment_calculator import (
                ArrowAdjustmentCalculator,
            )
            from shared.application.services.positioning.arrows.orchestration.directional_tuple_processor import (
                DirectionalTupleProcessor,
            )

            # Register the adjustment services (now that dependencies are available)
            container.register_factory(
                ArrowAdjustmentLookup,
                lambda c: ArrowAdjustmentLookup(
                    special_placement_service=c.resolve(SpecialPlacementService),
                    default_placement_service=c.resolve(DefaultPlacementService),
                    orientation_key_service=c.resolve(SpecialPlacementOriKeyGenerator),
                    placement_key_service=c.resolve(PlacementKeyGenerator),
                    turns_tuple_service=c.resolve(TurnsTupleKeyGenerator),
                    attribute_key_service=c.resolve(AttributeKeyGenerator),
                ),
            )
            container.register_singleton(
                DirectionalTupleProcessor, DirectionalTupleProcessor
            )
            container.register_singleton(
                ArrowAdjustmentCalculator, ArrowAdjustmentCalculator
            )

            self._mark_service_available("ArrowPlacementServices")

        except ImportError as e:
            self._handle_service_unavailable(
                "Arrow placement services",
                e,
                "Special placement and default placement calculations",
            )

    def _register_position_matching_service(self, container: "DIContainer") -> None:
        """Register position matching service for option picker."""
        try:
            from shared.application.services.positioning.arrows.utilities.pictograph_position_matcher import (
                PictographPositionMatcher,
            )

            container.register_singleton(
                PictographPositionMatcher, PictographPositionMatcher
            )
            self._mark_service_available("PictographPositionMatcher")

        except ImportError as e:
            self._handle_service_unavailable(
                "Position matching service", e, "Option picker position matching"
            )

    def _register_prop_management_services(self, container: "DIContainer") -> None:
        """Register prop management services."""
        try:
            # Register legacy PropManagementService for backward compatibility
            from shared.application.services.positioning.props.orchestration.prop_management_service import (
                IPropManagementService,
                PropManagementService,
            )

            container.register_singleton(IPropManagementService, PropManagementService)
            self._mark_service_available("PropManagementService")

            # Register new modular PropPositioningOrchestrator
            from shared.application.services.positioning.props.orchestration.prop_positioning_orchestrator import (
                IPropPositioningOrchestrator,
                PropPositioningOrchestrator,
            )

            container.register_singleton(
                IPropPositioningOrchestrator, PropPositioningOrchestrator
            )
            self._mark_service_available("PropPositioningOrchestrator")

            # Register individual modular services
            self._register_prop_detection_services(container)
            self._register_prop_calculation_services(container)
            self._register_prop_specialization_services(container)
            self._register_prop_event_services(container)

        except ImportError as e:
            self._handle_service_unavailable(
                "Prop management service", e, "Prop positioning and management"
            )

    def _register_orchestration_services(self, container: "DIContainer") -> None:
        """Register orchestration services."""
        try:
            # Note: PropOrchestrator has Qt dependencies and remains in desktop location
            # Using PropPositioningOrchestrator instead which is framework-agnostic
            from shared.application.services.positioning.props.orchestration.prop_positioning_orchestrator import (
                IPropPositioningOrchestrator,
                PropPositioningOrchestrator,
            )

            container.register_singleton(
                IPropPositioningOrchestrator, PropPositioningOrchestrator
            )
            self._mark_service_available("PropPositioningOrchestrator")

            self._mark_service_available("PictographOrchestrator")

        except ImportError as e:
            self._handle_service_unavailable(
                "Orchestration services", e, "Prop and pictograph orchestration"
            )

    def _register_prop_detection_services(self, container: "DIContainer") -> None:
        """Register prop detection services."""
        try:
            from shared.application.services.positioning.props.detection import (
                BetaPositioningDetector,
                IBetaPositioningDetector,
                IPropOverlapDetector,
                PropOverlapDetector,
            )

            container.register_singleton(
                IBetaPositioningDetector, BetaPositioningDetector
            )
            container.register_singleton(IPropOverlapDetector, PropOverlapDetector)
            self._mark_service_available("PropDetectionServices")

        except ImportError as e:
            self._handle_service_unavailable(
                "Prop detection services", e, "Beta positioning and overlap detection"
            )

    def _register_prop_calculation_services(self, container: "DIContainer") -> None:
        """Register prop calculation services."""
        try:
            from shared.application.services.positioning.props.calculation import (
                DirectionCalculationService,
                IDirectionCalculationService,
                IOffsetCalculationService,
                IPropClassificationService,
                IPropRotationCalculator,
                OffsetCalculationService,
                PropClassificationService,
                PropRotationCalculator,
            )

            container.register_singleton(
                IDirectionCalculationService, DirectionCalculationService
            )
            container.register_singleton(
                IOffsetCalculationService, OffsetCalculationService
            )
            container.register_singleton(
                IPropClassificationService, PropClassificationService
            )
            container.register_singleton(
                IPropRotationCalculator, PropRotationCalculator
            )
            self._mark_service_available("PropCalculationServices")

        except ImportError as e:
            self._handle_service_unavailable(
                "Prop calculation services",
                e,
                "Direction, offset, and rotation calculations",
            )

    def _register_prop_specialization_services(self, container: "DIContainer") -> None:
        """Register prop specialization services."""
        try:
            from shared.application.services.positioning.props.specialization import (
                ILetterIPositioningService,
                ISpecialPlacementOverrideService,
                LetterIPositioningService,
                SpecialPlacementOverrideService,
            )

            container.register_singleton(
                ILetterIPositioningService, LetterIPositioningService
            )
            container.register_singleton(
                ISpecialPlacementOverrideService, SpecialPlacementOverrideService
            )
            self._mark_service_available("PropSpecializationServices")

        except ImportError as e:
            self._handle_service_unavailable(
                "Prop specialization services",
                e,
                "Letter I positioning and special overrides",
            )

    def _register_prop_event_services(self, container: "DIContainer") -> None:
        """Register prop event services."""
        try:
            from shared.application.services.positioning.props.events import (
                IPropPositioningEventPublisher,
                PropPositioningEventPublisher,
            )

            container.register_singleton(
                IPropPositioningEventPublisher, PropPositioningEventPublisher
            )
            self._mark_service_available("PropEventServices")

        except ImportError as e:
            self._handle_service_unavailable(
                "Prop event services", e, "Prop positioning event publishing"
            )
