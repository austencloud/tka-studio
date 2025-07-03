"""
Arrow Adjustment Lookup Service

Focused service for handling special placement and default adjustment lookups.
Extracted from the god class ArrowAdjustmentCalculatorService.

RESPONSIBILITIES:
- Special placement lookup (stored adjustments)
- Default placement calculation fallback
- Key generation for lookups
- Error handling with Result types

USAGE:
    lookup_service = ArrowAdjustmentLookupService(
        special_placement_service,
        default_placement_service,
        # ... other dependencies
    )
    
    result = lookup_service.get_base_adjustment(arrow_data, pictograph_data)
    if result.is_success():
        adjustment = result.value
    else:
        logger.error(f"Lookup failed: {result.error}")
"""

import logging

from core.types.result import Result, AppError, ErrorType, success, failure, app_error
from core.types.coordinates import PositionResult, qpoint_to_point
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
from ...arrows.placement.default_placement_service import DefaultPlacementService
from ...arrows.placement.special_placement_service import SpecialPlacementService
from ...arrows.placement.special_placement_orientation_service import SpecialPlacementOrientationService
from ...arrows.keys.placement_key_service import PlacementKeyService
from ...arrows.keys.turns_tuple_generation_service import TurnsTupleGenerationService
from ...arrows.keys.attribute_key_generation_service import AttributeKeyGenerationService

logger = logging.getLogger(__name__)


class ArrowAdjustmentLookupService:
    """
    Focused service for arrow adjustment lookups.
    
    Handles the lookup phase of arrow positioning:
    1. Try special placement lookup (stored values)
    2. Fall back to default calculation
    3. Return proper Result types with error handling
    """

    def __init__(
        self,
        special_placement_service: SpecialPlacementService,
        default_placement_service: DefaultPlacementService,
        orientation_key_service: SpecialPlacementOrientationService,
        placement_key_service: PlacementKeyService,
        turns_tuple_service: TurnsTupleGenerationService,
        attribute_key_service: AttributeKeyGenerationService,
    ):
        """Initialize with required services for lookup operations."""
        self.special_placement_service = special_placement_service
        self.default_placement_service = default_placement_service
        self.orientation_key_service = orientation_key_service
        self.placement_key_service = placement_key_service
        self.turns_tuple_service = turns_tuple_service
        self.attribute_key_service = attribute_key_service

    def get_base_adjustment(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> PositionResult:
        """
        Get base adjustment using legacy-compatible lookup logic.
        
        Args:
            arrow_data: Arrow data with motion and color information
            pictograph_data: Pictograph context with letter and sequence data
            
        Returns:
            Result containing Point adjustment or AppError
        """
        motion = arrow_data.motion_data
        letter = pictograph_data.letter

        if not motion or not letter:
            return failure(app_error(
                ErrorType.VALIDATION_ERROR,
                "Missing motion or letter data for adjustment lookup",
                {"has_motion": motion is not None, "has_letter": letter is not None}
            ))

        try:
            # Generate required keys for special placement lookup
            key_result = self._generate_lookup_keys(arrow_data, pictograph_data)
            if key_result.is_failure():
                return failure(key_result.error)
            
            ori_key, turns_tuple, attr_key = key_result.value

            logger.debug(
                f"Generated keys - ori: {ori_key}, turns: {turns_tuple}, attr: {attr_key}"
            )

            # STEP 1: Try special placement lookup (stored adjustments)
            special_result = self._lookup_special_placement(
                arrow_data, pictograph_data, ori_key, turns_tuple, attr_key
            )

            if special_result.is_success():
                logger.info(
                    f"Using special placement: ({special_result.value.x:.1f}, {special_result.value.y:.1f})"
                )
                return special_result

            # STEP 2: Fall back to default calculation
            default_result = self._calculate_default_adjustment(arrow_data, pictograph_data)
            if default_result.is_success():
                logger.info(
                    f"Using default calculation: ({default_result.value.x:.1f}, {default_result.value.y:.1f})"
                )
                return default_result
            
            return failure(default_result.error)

        except Exception as e:
            return failure(app_error(
                ErrorType.POSITIONING_ERROR,
                f"Error in base adjustment lookup: {e}",
                {"arrow_color": arrow_data.color, "letter": pictograph_data.letter},
                e
            ))

    def _generate_lookup_keys(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Result[tuple[str, str, str], AppError]:
        """Generate all required keys for special placement lookup."""
        try:
            motion = arrow_data.motion_data
            
            ori_key = self.orientation_key_service.generate_orientation_key(
                motion, pictograph_data
            )
            turns_tuple = self.turns_tuple_service.generate_turns_tuple(pictograph_data)
            attr_key = self.attribute_key_service.get_key_from_arrow(
                arrow_data, pictograph_data
            )
            
            return success((ori_key, turns_tuple, attr_key))
            
        except Exception as e:
            return failure(app_error(
                ErrorType.SERVICE_OPERATION_ERROR,
                f"Failed to generate lookup keys: {e}",
                {"arrow_color": arrow_data.color, "letter": pictograph_data.letter},
                e
            ))

    def _lookup_special_placement(
        self,
        arrow_data: ArrowData,
        pictograph_data: PictographData,
        ori_key: str,
        turns_tuple: str,
        attr_key: str,
    ) -> PositionResult:
        """
        Look up special placement using exact legacy logic.
        
        Returns Result[Point, AppError] instead of Optional[QPointF].
        """
        try:
            # This should return stored adjustment values if they exist
            adjustment = self.special_placement_service.get_special_adjustment(
                arrow_data, pictograph_data
            )

            if adjustment:
                # Convert QPointF to Point
                point = qpoint_to_point(adjustment)
                return success(point)

            # No special placement found - this is not an error, just means fallback to default
            return failure(app_error(
                ErrorType.DATA_ERROR,
                "No special placement found",
                {
                    "ori_key": ori_key,
                    "turns_tuple": turns_tuple,
                    "attr_key": attr_key,
                    "arrow_color": arrow_data.color,
                    "letter": pictograph_data.letter
                }
            ))

        except Exception as e:
            return failure(app_error(
                ErrorType.POSITIONING_ERROR,
                f"Error in special placement lookup: {e}",
                {
                    "ori_key": ori_key,
                    "turns_tuple": turns_tuple,
                    "attr_key": attr_key,
                    "arrow_color": arrow_data.color
                },
                e
            ))

    def _calculate_default_adjustment(
        self,
        arrow_data: ArrowData,
        pictograph_data: PictographData,
        grid_mode: str = "diamond",
    ) -> PositionResult:
        """
        Calculate default adjustment using placement key and motion type.
        
        Returns Result[Point, AppError] instead of QPointF.
        """
        motion = arrow_data.motion_data

        if not motion:
            return failure(app_error(
                ErrorType.VALIDATION_ERROR,
                "No motion data for default calculation",
                {"arrow_color": arrow_data.color, "letter": pictograph_data.letter}
            ))

        try:
            # Get default placements for the grid mode and motion type
            grid_mode = pictograph_data.grid_data.grid_mode.value
            default_placements = self.default_placement_service.all_defaults.get(
                grid_mode, {}
            ).get(motion.motion_type.value, {})

            # Generate placement key for default lookup
            placement_key = self.placement_key_service.generate_placement_key(
                motion, pictograph_data, default_placements, grid_mode
            )

            # Get adjustment from default placement service
            adjustment_point = self.default_placement_service.get_default_adjustment(
                motion, grid_mode="diamond", placement_key=placement_key
            )

            return success(adjustment_point)

        except Exception as e:
            return failure(app_error(
                ErrorType.POSITIONING_ERROR,
                f"Error calculating default adjustment: {e}",
                {
                    "arrow_color": arrow_data.color,
                    "letter": pictograph_data.letter,
                    "grid_mode": grid_mode,
                    "motion_type": motion.motion_type.value if motion else "None"
                },
                e
            ))
