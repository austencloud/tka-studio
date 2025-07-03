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
    
    result = processor.process_directional_tuples(base_adjustment, arrow_data, pictograph_data)
    if result.is_success():
        final_adjustment = result.value
    else:
        logger.error(f"Processing failed: {result.error}")
"""

import logging
from typing import List, Tuple

from core.types.result import Result, AppError, ErrorType, success, failure, app_error
from core.types.coordinates import PositionResult, point_to_qpoint
from core.types.geometry import Point
from domain.models.pictograph_models import ArrowData, PictographData

# Conditional PyQt6 imports for testing compatibility
try:
    from PyQt6.QtCore import QPointF
    QT_AVAILABLE = True
except ImportError:
    # Create mock QPointF for testing when Qt is not available
    class QPointF:
        def __init__(self, x=0.0, y=0.0):
            self._x = x
            self._y = y

        def x(self):
            return self._x

        def y(self):
            return self._y
    
    QT_AVAILABLE = False

# Import required services
from ...arrows.calculation.directional_tuple_calculator import DirectionalTupleCalculator
from ...arrows.calculation.quadrant_index_service import QuadrantIndexService

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
        quadrant_index_service: QuadrantIndexService,
    ):
        """Initialize with required services for tuple processing."""
        self.directional_tuple_service = directional_tuple_service
        self.quadrant_index_service = quadrant_index_service

    def process_directional_tuples(
        self,
        base_adjustment: Point,
        arrow_data: ArrowData,
        pictograph_data: PictographData,
    ) -> PositionResult:
        """
        Process directional tuples to get final adjustment.
        
        Args:
            base_adjustment: Base adjustment point from lookup
            arrow_data: Arrow data with motion and color information
            pictograph_data: Pictograph context with letter and sequence data
            
        Returns:
            Result containing final Point adjustment or AppError
        """
        motion = arrow_data.motion_data
        if not motion:
            return failure(app_error(
                ErrorType.VALIDATION_ERROR,
                "No motion data for directional tuple processing",
                {"arrow_color": arrow_data.color, "letter": pictograph_data.letter}
            ))

        try:
            # STEP 1: Generate directional tuples using base adjustment
            tuples_result = self._generate_directional_tuples(motion, base_adjustment)
            if tuples_result.is_failure():
                return failure(tuples_result.error)
            
            directional_tuples = tuples_result.value
            logger.info(f"Generated directional tuples: {directional_tuples}")

            # STEP 2: Get quadrant index for selection
            quadrant_result = self._get_quadrant_index(arrow_data, pictograph_data)
            if quadrant_result.is_failure():
                return failure(quadrant_result.error)
            
            quadrant_index = quadrant_result.value
            logger.info(f"Quadrant index: {quadrant_index}")

            # STEP 3: Select final adjustment from directional tuples
            selection_result = self._select_from_tuples(directional_tuples, quadrant_index)
            if selection_result.is_failure():
                return failure(selection_result.error)
            
            final_adjustment = selection_result.value
            logger.info(
                f"Final adjustment: ({final_adjustment.x:.1f}, {final_adjustment.y:.1f})"
            )
            
            return success(final_adjustment)

        except Exception as e:
            return failure(app_error(
                ErrorType.POSITIONING_ERROR,
                f"Error processing directional tuples: {e}",
                {
                    "arrow_color": arrow_data.color,
                    "letter": pictograph_data.letter,
                    "base_adjustment": f"({base_adjustment.x:.1f}, {base_adjustment.y:.1f})"
                },
                e
            ))

    def _generate_directional_tuples(
        self, motion, base_adjustment: Point
    ) -> Result[List[Tuple[int, int]], AppError]:
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
                return failure(app_error(
                    ErrorType.POSITIONING_ERROR,
                    "Directional tuple service returned empty tuples",
                    {
                        "motion_type": motion.motion_type.value if motion else "None",
                        "base_x": base_adjustment.x,
                        "base_y": base_adjustment.y
                    }
                ))
            
            return success(directional_tuples)

        except Exception as e:
            return failure(app_error(
                ErrorType.POSITIONING_ERROR,
                f"Error generating directional tuples: {e}",
                {
                    "motion_type": motion.motion_type.value if motion else "None",
                    "base_x": base_adjustment.x,
                    "base_y": base_adjustment.y
                },
                e
            ))

    def _get_quadrant_index(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Result[int, AppError]:
        """
        Get quadrant index for directional tuple selection.
        
        Returns Result[int, AppError] instead of int with fallback.
        """
        try:
            # Calculate arrow location for quadrant determination
            from ...arrows.calculation.arrow_location_calculator import (
                ArrowLocationCalculatorService,
            )

            location_calculator = ArrowLocationCalculatorService()
            arrow_location = location_calculator.calculate_location(
                arrow_data.motion_data, pictograph_data
            )

            # Get quadrant index
            quadrant_index = self.quadrant_index_service.get_quadrant_index(
                arrow_data.motion_data, arrow_location
            )

            # Validate quadrant index
            if quadrant_index < 0:
                return failure(app_error(
                    ErrorType.POSITIONING_ERROR,
                    f"Invalid negative quadrant index: {quadrant_index}",
                    {
                        "arrow_color": arrow_data.color,
                        "letter": pictograph_data.letter,
                        "arrow_location": str(arrow_location)
                    }
                ))

            return success(quadrant_index)

        except Exception as e:
            return failure(app_error(
                ErrorType.POSITIONING_ERROR,
                f"Error calculating quadrant index: {e}",
                {"arrow_color": arrow_data.color, "letter": pictograph_data.letter},
                e
            ))

    def _select_from_tuples(
        self, directional_tuples: List[Tuple[int, int]], quadrant_index: int
    ) -> PositionResult:
        """
        Select final adjustment from directional tuples using quadrant index.
        
        Returns Result[Point, AppError] instead of QPointF with fallback.
        """
        try:
            if not directional_tuples:
                return failure(app_error(
                    ErrorType.POSITIONING_ERROR,
                    "Cannot select from empty directional tuples",
                    {"quadrant_index": quadrant_index}
                ))

            if quadrant_index >= len(directional_tuples):
                return failure(app_error(
                    ErrorType.POSITIONING_ERROR,
                    f"Quadrant index {quadrant_index} out of range for {len(directional_tuples)} tuples",
                    {
                        "quadrant_index": quadrant_index,
                        "tuple_count": len(directional_tuples),
                        "available_tuples": directional_tuples
                    }
                ))

            selected_tuple = directional_tuples[quadrant_index]
            final_point = Point(float(selected_tuple[0]), float(selected_tuple[1]))
            
            return success(final_point)

        except Exception as e:
            return failure(app_error(
                ErrorType.POSITIONING_ERROR,
                f"Error selecting from directional tuples: {e}",
                {
                    "quadrant_index": quadrant_index,
                    "tuple_count": len(directional_tuples),
                    "tuples": directional_tuples
                },
                e
            ))
