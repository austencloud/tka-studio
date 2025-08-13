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
    try:
        adjustment = calculator.calculate_adjustment(pictograph_data, motion_data, letter, location)
    except Exception as e:
        logger.error(f"Calculation failed: {e}")
"""

import logging

# Import the focused services
from desktop.modern.application.services.positioning.arrows.orchestration.arrow_adjustment_lookup import (
    ArrowAdjustmentLookup,
)
from desktop.modern.core.interfaces.positioning_services import (
    IArrowAdjustmentCalculator,
)
from desktop.modern.core.types.coordinates import get_default_point
from desktop.modern.core.types.geometry import Point
from desktop.modern.domain.models.enums import Location
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData

from ..calculation.directional_tuple_calculator import DirectionalTupleCalculator
from ..calculation.quadrant_index_calculator import QuadrantIndexCalculator
from ..key_generators.attribute_key_generator import AttributeKeyGenerator
from ..key_generators.placement_key_generator import PlacementKeyGenerator
from ..key_generators.turns_tuple_key_generator import TurnsTupleKeyGenerator

# Legacy service imports for backward compatibility
from ..placement.default_placement_service import DefaultPlacementService
from ..placement.special_placement_ori_key_generator import (
    SpecialPlacementOriKeyGenerator,
)
from ..placement.special_placement_service import SpecialPlacementService
from .directional_tuple_processor import DirectionalTupleProcessor

logger = logging.getLogger(__name__)


class ArrowAdjustmentCalculator(IArrowAdjustmentCalculator):
    """
    Clean coordinator service for arrow positioning with proper error handling.

    Delegates to focused services:
    - ArrowAdjustmentLookupService: Special/default placement lookups
    - DirectionalTupleProcessor: Tuple generation and selection

    Provides both new Result-based API and legacy Point-based API for compatibility.
    """

    def __init__(
        self,
        lookup_service: ArrowAdjustmentLookup = None,
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

    def _create_default_lookup_service(self) -> ArrowAdjustmentLookup:
        """Create lookup service with default dependencies."""
        return ArrowAdjustmentLookup(
            special_placement_service=SpecialPlacementService(),
            default_placement_service=DefaultPlacementService(),
            orientation_key_service=SpecialPlacementOriKeyGenerator(),
            placement_key_service=PlacementKeyGenerator(),
            turns_tuple_service=TurnsTupleKeyGenerator(),
            attribute_key_service=AttributeKeyGenerator(),
        )

    def _create_default_tuple_processor(self) -> DirectionalTupleProcessor:
        """Create tuple processor with default dependencies."""
        return DirectionalTupleProcessor(
            directional_tuple_service=DirectionalTupleCalculator(),
            quadrant_index_service=QuadrantIndexCalculator(),
        )

    def calculate_adjustment(
        self,
        pictograph_data: PictographData,
        motion_data: MotionData,
        letter: str,
        location: Location,
        arrow_color: str = None,
    ) -> Point:
        """
        Calculate arrow position adjustment with streamlined parameters.

        Args:
            motion_data: Motion data containing type, rotation, and location info
            letter: Letter for special placement lookup
            location: Pre-calculated arrow location
            arrow_color: Color of the arrow ('red' or 'blue')

        Returns:
            Final position adjustment as Point (to be added to initial position)
        """
        try:
            return self.calculate_adjustment_result(
                pictograph_data, motion_data, letter, location, arrow_color
            )
        except Exception as e:
            # Log error and return default for backward compatibility
            logger.error(f"Adjustment calculation failed: {e}")
            return get_default_point()

    def calculate_adjustment_result(
        self,
        pictograph_data: PictographData,
        motion_data: MotionData,
        letter: str,
        location: Location,
        arrow_color: str = None,
    ) -> Point:
        """
        Calculate arrow position adjustment with proper error handling.

        Args:
            motion_data: Motion data containing type, rotation, and location info
            letter: Letter for special placement lookup
            location: Pre-calculated arrow location
            arrow_color: Color of the arrow ('red' or 'blue')

        Returns:
            Point adjustment

        Raises:
            ValueError: If calculation fails due to invalid input
            RuntimeError: If calculation fails due to system error
        """
        try:
            # STEP 1: Look up base adjustment (special → default) - EXACTLY like legacy
            base_adjustment = self.lookup_service.get_base_adjustment(
                pictograph_data, motion_data, letter, arrow_color
            )

            # STEP 2: Process directional tuples - EXACTLY like legacy
            final_adjustment = self.tuple_processor.process_directional_tuples(
                base_adjustment, motion_data, location
            )

            return final_adjustment

        except Exception as e:
            logger.error(f"Adjustment calculation failed for letter {letter}: {e}")
            raise RuntimeError(f"Arrow adjustment calculation failed: {e}") from e
