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
from typing import TYPE_CHECKING, List

from ..service_registration_manager import BaseServiceRegistrar

if TYPE_CHECKING:
    from core.dependency_injection.di_container import DIContainer

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
        """Positioning services are optional with graceful degradation."""
        return False

    def register_services(self, container: "DIContainer") -> None:
        """Register positioning services with graceful degradation."""
        self._update_progress("Registering positioning services...")

        # Register arrow positioning services
        self._register_arrow_positioning_services(container)

        # Register position matching service
        self._register_position_matching_service(container)

        # Register prop management services
        self._register_prop_management_services(container)

        # Register orchestration services
        self._register_orchestration_services(container)

        self._update_progress("Positioning services registered successfully")

    def _register_arrow_positioning_services(self, container: "DIContainer") -> None:
        """Register arrow positioning microservices."""
        try:
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
            self._mark_service_available("ArrowLocationCalculator")

            container.register_singleton(
                IArrowRotationCalculator, ArrowRotationCalculatorService
            )
            self._mark_service_available("ArrowRotationCalculator")

            container.register_singleton(
                IArrowAdjustmentCalculator, ArrowAdjustmentCalculatorService
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

        except ImportError as e:
            self._handle_service_unavailable(
                "Arrow positioning services",
                e,
                "Arrow positioning calculations in pictographs",
            )

    def _register_position_matching_service(self, container: "DIContainer") -> None:
        """Register position matching service for option picker."""
        try:
            from application.services.positioning.arrows.utilities.pictograph_position_matcher import (
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
            from application.services.positioning.props.orchestration.prop_management_service import (
                IPropManagementService,
                PropManagementService,
            )

            container.register_singleton(IPropManagementService, PropManagementService)
            self._mark_service_available("PropManagementService")

        except ImportError as e:
            self._handle_service_unavailable(
                "Prop management service", e, "Prop positioning and management"
            )

    def _register_orchestration_services(self, container: "DIContainer") -> None:
        """Register orchestration services."""
        try:

            from application.services.positioning.props.orchestration.prop_orchestrator import (
                IPropOrchestrator,
                PropOrchestrator,
            )

            container.register_singleton(IPropOrchestrator, PropOrchestrator)
            self._mark_service_available("PropOrchestrator")

            self._mark_service_available("PictographOrchestrator")

        except ImportError as e:
            self._handle_service_unavailable(
                "Orchestration services", e, "Prop and pictograph orchestration"
            )
