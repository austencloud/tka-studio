"""
Arrow Adjustment Calculator Service - Refactored with Result Types

Clean, focused coordinator service that delegates to specialized components.
Implements proper error handling with Result types instead of silent failures.

ARCHITECTURE:
- ArrowAdjustmentLookupService: Handles special/default placement lookups
- DirectionalTupleProcessor: Handles tuple generation and selection
- This service: Coordinates the pipeline with proper error propagation

USAGE:
    calculator = ArrowAdjustmentCalculatorService(lookup_service, tuple_processor)
    result = calculator.calculate_adjustment(arrow_data, pictograph_data)
    if result.is_success():
        adjustment = result.value
    else:
        logger.error(f"Calculation failed: {result.error}")
"""

import logging

from core.interfaces.positioning_services import IArrowAdjustmentCalculator
from core.types.result import (
    ErrorType,
    success,
    failure,
    app_error,
)
from core.types.coordinates import (
    PositionResult,
    get_default_point,
)
from core.types.geometry import Point
from domain.models.pictograph_models import ArrowData, PictographData

# Import the focused services
from .arrow_adjustment_lookup_service import ArrowAdjustmentLookupService
from .directional_tuple_processor import DirectionalTupleProcessor

# Legacy service imports for backward compatibility
from ...arrows.placement.default_placement_service import DefaultPlacementService
from ...arrows.placement.special_placement_service import SpecialPlacementService
from ...arrows.placement.special_placement_orientation_service import (
    SpecialPlacementOrientationService,
)
from ...arrows.keys.placement_key_service import PlacementKeyService
from ...arrows.keys.turns_tuple_generation_service import TurnsTupleGenerationService
from ...arrows.keys.attribute_key_generation_service import (
    AttributeKeyGenerationService,
)
from ...arrows.calculation.directional_tuple_calculator import (
    DirectionalTupleCalculator,
)
from ...arrows.calculation.quadrant_index_service import QuadrantIndexService

logger = logging.getLogger(__name__)


class ArrowAdjustmentCalculatorService(IArrowAdjustmentCalculator):
    """
    Clean coordinator service for arrow positioning with proper error handling.

    Delegates to focused services:
    - ArrowAdjustmentLookupService: Special/default placement lookups
    - DirectionalTupleProcessor: Tuple generation and selection

    Provides both new Result-based API and legacy Point-based API for compatibility.
    """

    def __init__(
        self,
        lookup_service: ArrowAdjustmentLookupService = None,
        tuple_processor: DirectionalTupleProcessor = None,
    ):
        """
        Initialize with focused services.

        Args:
            lookup_service: Service for adjustment lookups
            tuple_processor: Service for directional tuple processing
        """
        # Use provided services or create with default dependencies
        if lookup_service is None:
            lookup_service = self._create_default_lookup_service()
        if tuple_processor is None:
            tuple_processor = self._create_default_tuple_processor()

        self.lookup_service = lookup_service
        self.tuple_processor = tuple_processor

    def _create_default_lookup_service(self) -> ArrowAdjustmentLookupService:
        """Create lookup service with default dependencies."""
        return ArrowAdjustmentLookupService(
            special_placement_service=SpecialPlacementService(),
            default_placement_service=DefaultPlacementService(),
            orientation_key_service=SpecialPlacementOrientationService(),
            placement_key_service=PlacementKeyService(),
            turns_tuple_service=TurnsTupleGenerationService(),
            attribute_key_service=AttributeKeyGenerationService(),
        )

    def _create_default_tuple_processor(self) -> DirectionalTupleProcessor:
        """Create tuple processor with default dependencies."""
        return DirectionalTupleProcessor(
            directional_tuple_service=DirectionalTupleCalculator(),
            quadrant_index_service=QuadrantIndexService(),
        )

    def calculate_adjustment(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Point:
        """
        Calculate arrow position adjustment (legacy API for compatibility).

        This method maintains the original Point return type for backward compatibility.
        For new code, use calculate_adjustment_result() which returns Result types.

        Args:
            arrow_data: Arrow data with motion and color information
            pictograph_data: Pictograph context with letter and sequence data

        Returns:
            Final position adjustment as Point (to be added to initial position)
        """
        result = self.calculate_adjustment_result(arrow_data, pictograph_data)
        if result.is_success():
            return result.value

        # Log error and return default for backward compatibility
        logger.error(f"Adjustment calculation failed: {result.error}")
        return get_default_point()

    def calculate_adjustment_result(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> PositionResult:
        """
        Calculate arrow position adjustment with proper error handling.

        New Result-based API that provides explicit error handling.

        Args:
            arrow_data: Arrow data with motion and color information
            pictograph_data: Pictograph context with letter and sequence data

        Returns:
            Result containing Point adjustment or AppError
        """
        logger.info(
            f"🎯 Calculating adjustment for {arrow_data.color} arrow in letter {pictograph_data.letter}"
        )

        motion = arrow_data.motion_data
        if not motion:
            return failure(
                app_error(
                    ErrorType.VALIDATION_ERROR,
                    "No motion data available for adjustment calculation",
                    {"arrow_color": arrow_data.color, "letter": pictograph_data.letter},
                )
            )

        try:
            # STEP 1: Look up base adjustment (special → default)
            lookup_result = self.lookup_service.get_base_adjustment(
                arrow_data, pictograph_data
            )
            if lookup_result.is_failure():
                return failure(lookup_result.error)

            base_adjustment = lookup_result.value
            logger.info(
                f"   Step 1 - Base adjustment: ({base_adjustment.x:.1f}, {base_adjustment.y:.1f})"
            )

            # STEP 2: Process directional tuples
            tuple_result = self.tuple_processor.process_directional_tuples(
                base_adjustment, arrow_data, pictograph_data
            )
            if tuple_result.is_failure():
                return failure(tuple_result.error)

            final_adjustment = tuple_result.value
            logger.info(
                f"   Final adjustment: ({final_adjustment.x:.1f}, {final_adjustment.y:.1f})"
            )

            return success(final_adjustment)

        except Exception as e:
            return failure(
                app_error(
                    ErrorType.POSITIONING_ERROR,
                    f"Unexpected error in adjustment calculation: {e}",
                    {"arrow_color": arrow_data.color, "letter": pictograph_data.letter},
                    e,
                )
            )
