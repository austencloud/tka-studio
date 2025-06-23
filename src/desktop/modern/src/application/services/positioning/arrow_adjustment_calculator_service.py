"""
Refactored Arrow Adjustment Calculator Service

Orchestrates arrow position adjustments using focused service components.

This service coordinates:
- Default placement calculations
- Special placement lookups
- Orientation calculations
- Key generation
- Quadrant adjustments

Replaces the monolithic ArrowAdjustmentCalculatorService with a clean composition.
"""

import logging
from typing import Optional

from core.interfaces.positioning_services import IArrowAdjustmentCalculator
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

from core.types.geometry import Point

from .default_placement_service import DefaultPlacementService
from .orientation_calculation_service import OrientationCalculationService
from .placement_key_generation_service import PlacementKeyGenerationService
from .placement_key_service import PlacementKeyService
from .quadrant_adjustment_service import QuadrantAdjustmentService
from .special_placement_service import SpecialPlacementService
from .special_placement_orientation_service import SpecialPlacementOrientationService
from .turns_tuple_generation_service import TurnsTupleGenerationService
from .attribute_key_generation_service import AttributeKeyGenerationService
from .directional_tuple_service import DirectionalTupleService
from .quadrant_index_service import QuadrantIndexService

logger = logging.getLogger(__name__)


class ArrowAdjustmentCalculatorService(IArrowAdjustmentCalculator):
    """
    Clean, focused service for calculating arrow position adjustments.

    Uses composition of focused services to handle the complete adjustment pipeline:
    1. Default adjustments based on motion type and placement key
    2. Special adjustments for specific letters and configurations
    3. Orientation calculations using legacy logic
    4. Quadrant-based directional adjustments    No UI dependencies, completely testable in isolation.
    """

    def __init__(
        self,
        default_placement_service: Optional[DefaultPlacementService] = None,
        special_placement_service: Optional[SpecialPlacementService] = None,
        orientation_service: Optional[OrientationCalculationService] = None,
        key_generation_service: Optional[PlacementKeyGenerationService] = None,
        placement_key_service: Optional[PlacementKeyService] = None,
        quadrant_service: Optional[QuadrantAdjustmentService] = None,
        orientation_key_service: Optional[SpecialPlacementOrientationService] = None,
        turns_tuple_service: Optional[TurnsTupleGenerationService] = None,
        attribute_key_service: Optional[AttributeKeyGenerationService] = None,
        directional_tuple_service: Optional[DirectionalTupleService] = None,
        quadrant_index_service: Optional[QuadrantIndexService] = None,
    ):
        """
        Initialize with service dependencies.

        Args:
            default_placement_service: Handles default placement calculations
            special_placement_service: Handles special placement lookups
            orientation_service: Handles orientation calculations
            key_generation_service: Handles placement key generation
            placement_key_service: Handles placement key creation
            quadrant_service: Handles quadrant adjustments (legacy compatibility)
            orientation_key_service: Handles orientation key generation
            turns_tuple_service: Handles turns tuple generation
            attribute_key_service: Handles attribute key generation
            directional_tuple_service: Handles directional tuple generation (CRITICAL FIX)
            quadrant_index_service: Handles quadrant index calculation (CRITICAL FIX)
        """
        self.default_placement_service = (
            default_placement_service or DefaultPlacementService()
        )
        self.special_placement_service = (
            special_placement_service or SpecialPlacementService()
        )
        self.orientation_service = (
            orientation_service or OrientationCalculationService()
        )
        self.key_generation_service = (
            key_generation_service or PlacementKeyGenerationService()
        )
        self.placement_key_service = placement_key_service or PlacementKeyService()
        self.quadrant_service = quadrant_service or QuadrantAdjustmentService()
        self.orientation_key_service = (
            orientation_key_service or SpecialPlacementOrientationService()
        )
        self.turns_tuple_service = turns_tuple_service or TurnsTupleGenerationService()
        self.attribute_key_service = (
            attribute_key_service or AttributeKeyGenerationService()
        )
        # NEW: Core directional tuple services for quadrant-based positioning
        self.directional_tuple_service = (
            directional_tuple_service or DirectionalTupleService()
        )
        self.quadrant_index_service = quadrant_index_service or QuadrantIndexService()

    def calculate_adjustment(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Point:
        """
        Calculate position adjustment for arrow using the complete pipeline.

        Pipeline:
        1. Try special placement lookup first (highest priority)
        2. Fall back to default placement calculations
        3. Apply quadrant adjustments
        4. Apply position-specific fine-tuning

        Args:
            arrow_data: Arrow data with motion and color information
            pictograph_data: Pictograph context with letter and sequence data

        Returns:
            Final position adjustment as Point
        """
        logger.info(
            f"Calculating adjustment for {arrow_data.color} arrow in letter {pictograph_data.letter}"
        )  # Step 1: Try special placement lookup
        special_adjustment = self._get_special_adjustment(arrow_data, pictograph_data)
        if special_adjustment is not None:
            logger.info(
                f"Using special adjustment: ({special_adjustment.x()}, {special_adjustment.y()})"
            )
            final_qpoint = self._apply_final_adjustments(
                special_adjustment, arrow_data, pictograph_data
            )
            # Convert back to Point to match interface
            return Point(
                final_qpoint.x(), final_qpoint.y()
            )  # Step 2: Fall back to default placement
        default_adjustment = self._get_default_adjustment(arrow_data)
        logger.info(
            f"Using default adjustment: ({default_adjustment.x}, {default_adjustment.y})"
        )

        # Convert Point to QPointF for consistency with quadrant service
        default_qpoint = QPointF(
            default_adjustment.x, default_adjustment.y
        )  # Step 3: Apply final adjustments
        final_qpoint = self._apply_final_adjustments(
            default_qpoint, arrow_data, pictograph_data
        )

        # Convert back to Point to match interface
        return Point(final_qpoint.x(), final_qpoint.y())

    def _get_special_adjustment(
        self, arrow_data: ArrowData, pictograph_data: PictographData
    ) -> Optional[QPointF]:
        """
        Attempt to get special adjustment using placement lookup.

        Args:
            arrow_data: Arrow data with motion and color
            pictograph_data: Pictograph context

        Returns:
            Special adjustment if found, None otherwise
        """
        motion = arrow_data.motion_data
        letter = pictograph_data.letter

        if not motion or not letter:
            logger.debug("Missing motion or letter data for special placement")
            return None

        try:  # Generate keys using the appropriate services
            ori_key = self.orientation_key_service.generate_orientation_key(
                motion, pictograph_data
            )
            turns_tuple = self.turns_tuple_service.generate_turns_tuple(pictograph_data)
            attr_key = self.attribute_key_service.get_key_from_arrow(
                arrow_data, pictograph_data
            )

            logger.debug(
                f"Generated keys - ori: {ori_key}, turns: {turns_tuple}, attr: {attr_key}"
            )  # Look up special placement
            adjustment = self.special_placement_service.get_special_adjustment(
                arrow_data, pictograph_data
            )

            if adjustment:
                logger.info(
                    f"Found special adjustment: ({adjustment.x()}, {adjustment.y()})"
                )
                return adjustment

            logger.debug("No special adjustment found")
            return None

        except Exception as e:
            logger.error(f"Error in special placement lookup: {e}")
            return None

    def _get_default_adjustment(self, arrow_data: ArrowData) -> QPointF:
        """
        Get default adjustment using placement key and motion type.

        Args:
            arrow_data: Arrow data with motion information

        Returns:
            Default adjustment as QPointF
        """
        motion = arrow_data.motion_data

        if not motion:
            logger.warning("No motion data for default placement")
            return QPointF(0, 0)

        # Generate placement key
        placement_key = self.placement_key_service.generate_placement_key(motion)

        # Get adjustment from default placement service
        adjustment = self.default_placement_service.get_default_adjustment(
            motion, grid_mode="diamond", placement_key=placement_key
        )

        return adjustment

    def _apply_final_adjustments(
        self,
        base_adjustment: QPointF,
        arrow_data: ArrowData,
        pictograph_data: PictographData,
    ) -> QPointF:
        """
        Apply final adjustments using legacy-style directional tuple logic.

        This is the CRITICAL FIX that was missing from the modern version.
        It replicates the legacy quadrant adjustment strategy exactly.

        Args:
            base_adjustment: Base adjustment from placement lookup
            arrow_data: Arrow data with motion and color
            pictograph_data: Pictograph context

        Returns:
            Final adjusted position with directional tuple applied
        """
        motion = arrow_data.motion_data

        if not motion or not motion.start_loc or not motion.end_loc:
            # Can't apply directional adjustments without location data
            logger.debug("No motion or location data, returning base adjustment")
            return base_adjustment

        # STEP 1: Generate directional tuples using legacy rotation matrices
        directional_tuples = self.directional_tuple_service.generate_directional_tuples(
            motion, base_adjustment.x(), base_adjustment.y()
        )

        # STEP 2: Calculate arrow location (where the arrow will be positioned)
        from .arrow_location_calculator_service import ArrowLocationCalculatorService

        location_calculator = ArrowLocationCalculatorService()
        arrow_location = location_calculator.calculate_location(motion, pictograph_data)

        # STEP 3: Get quadrant index based on motion and arrow location
        quadrant_index = self.quadrant_index_service.get_quadrant_index(
            motion, arrow_location
        )

        # STEP 4: Select the correct directional adjustment from the tuple array
        if directional_tuples and 0 <= quadrant_index < len(directional_tuples):
            selected_tuple = directional_tuples[quadrant_index]
            final_adjustment = QPointF(selected_tuple[0], selected_tuple[1])
        else:
            logger.warning(
                f"Invalid quadrant index {quadrant_index} for {len(directional_tuples)} tuples"
            )
            final_adjustment = QPointF(0, 0)

        logger.info(
            f"🎯 DIRECTIONAL TUPLE ADJUSTMENT: "
            f"base=({base_adjustment.x():.1f}, {base_adjustment.y():.1f}) -> "
            f"tuples={directional_tuples} -> "
            f"index={quadrant_index} -> "
            f"final=({final_adjustment.x():.1f}, {final_adjustment.y():.1f})"
        )

        return final_adjustment
