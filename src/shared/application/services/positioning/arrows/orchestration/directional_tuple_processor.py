"""
Directional Tuple Processor Service

Focused service for handling directional tuple generation and quadrant-based selection.
Extracted from the god class ArrowAdjustmentCalculatorService.

RESPONSIBILITIES:
- Generate directional tuples using rotation matrices
- Calculate quadrant indices for selection
- Select final adjustment from tuples
- Error handling with Result types

USAGE:
    processor = DirectionalTupleProcessor(
        directional_tuple_service,
        quadrant_index_service
    )

    try:
        final_adjustment = processor.process_directional_tuples(base_adjustment, motion_data, location)
    except Exception as e:
        logger.error(f"Processing failed: {e}")
"""

import logging

from desktop.modern.core.types.coordinates import point_to_qpoint
from desktop.modern.core.types.geometry import Point
from desktop.modern.domain.models.enums import Location
from desktop.modern.domain.models.motion_data import MotionData

# Import required services
from ...arrows.calculation.directional_tuple_calculator import (
    DirectionalTupleCalculator,
)
from ..calculation.quadrant_index_calculator import QuadrantIndexCalculator

logger = logging.getLogger(__name__)


class DirectionalTupleProcessor:
    """
    Focused service for directional tuple processing.

    Handles the tuple generation and selection phase of arrow positioning:
    1. Generate directional tuples using rotation matrices
    2. Calculate quadrant index for selection
    3. Select final adjustment from tuples
    4. Return proper Result types with error handling
    """

    def __init__(
        self,
        directional_tuple_service: DirectionalTupleCalculator,
        quadrant_index_service: QuadrantIndexCalculator,
    ):
        """Initialize with required services for tuple processing."""
        self.directional_tuple_service = directional_tuple_service
        self.quadrant_index_service = quadrant_index_service

    def process_directional_tuples(
        self,
        base_adjustment: Point,
        motion_data: MotionData,
        location: Location,
    ) -> Point:
        """
        Process directional tuples to get final adjustment.

        Args:
            base_adjustment: Base adjustment point from lookup
            motion_data: Motion data containing type, rotation, and location info
            location: Pre-calculated arrow location
        """

        try:
            # STEP 1: Generate directional tuples using base adjustment
            directional_tuples = self._generate_directional_tuples(
                motion_data, base_adjustment
            )

            # STEP 2: Get quadrant index for selection using pre-calculated location
            quadrant_index = self._get_quadrant_index(motion_data, location)

            # STEP 3: Select final adjustment from directional tuples
            final_adjustment = self._select_from_tuples(
                directional_tuples, quadrant_index
            )

            return final_adjustment

        except Exception as e:
            logger.error(f"Error processing directional tuples: {e}")
            raise RuntimeError(f"Directional tuple processing failed: {e}") from e

    def _generate_directional_tuples(
        self, motion: MotionData, base_adjustment: Point
    ) -> list[tuple[int, int]]:
        """
        Generate directional tuples using rotation matrices.

        Returns Result[List[Tuple[int, int]], AppError] instead of list with fallback.
        """
        try:
            # Convert Point to QPointF for legacy service compatibility
            base_qpoint = point_to_qpoint(base_adjustment)

            directional_tuples = (
                self.directional_tuple_service.generate_directional_tuples(
                    motion, base_qpoint.x(), base_qpoint.y()
                )
            )

            if not directional_tuples:
                raise ValueError("Directional tuple service returned empty tuples")

            return directional_tuples

        except Exception as e:
            logger.error(f"Error generating directional tuples: {e}")
            raise RuntimeError(f"Directional tuple generation failed: {e}") from e

    def _get_quadrant_index(self, motion_data: MotionData, location: Location) -> int:
        """
        Get quadrant index for directional tuple selection using pre-calculated location.
        """
        try:
            # Use pre-calculated location instead of recalculating
            quadrant_index = self.quadrant_index_service.get_quadrant_index(
                motion_data, location
            )

            # Validate quadrant index
            if quadrant_index < 0:
                raise ValueError(f"Invalid negative quadrant index: {quadrant_index}")

            return quadrant_index

        except Exception as e:
            logger.error(f"Error calculating quadrant index: {e}")
            raise RuntimeError(f"Quadrant index calculation failed: {e}") from e

    def _select_from_tuples(
        self, directional_tuples: list[tuple[int, int]], quadrant_index: int
    ) -> Point:
        """
        Select final adjustment from directional tuples using quadrant index.
        """
        try:
            if not directional_tuples:
                raise ValueError("Cannot select from empty directional tuples")

            if quadrant_index >= len(directional_tuples):
                raise ValueError(
                    f"Quadrant index {quadrant_index} out of range for {len(directional_tuples)} tuples"
                )

            selected_tuple = directional_tuples[quadrant_index]
            final_point = Point(float(selected_tuple[0]), float(selected_tuple[1]))

            return final_point

        except Exception as e:
            logger.error(f"Error selecting from directional tuples: {e}")
            raise RuntimeError(f"Tuple selection failed: {e}") from e
