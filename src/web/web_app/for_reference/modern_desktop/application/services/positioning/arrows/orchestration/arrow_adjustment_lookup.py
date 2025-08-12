"""
Arrow Adjustment Lookup Service

Focused service for handling special placement and default adjustment lookups.
Extracted from the god class ArrowAdjustmentCalculatorService.

RESPONSIBILITIES:
- Special placement lookup (stored adjustments)
- Default placement calculation fallback
- Key generation for lookups
- Error handling with Python exceptions

USAGE:
    lookup_service = ArrowAdjustmentLookupService(
        special_placement_service,
        default_placement_service,
        # ... other dependencies
    )

    adjustment = lookup_service.get_base_adjustment(pictograph_data, motion_data, letter)
"""

from __future__ import annotations

import logging

from shared.application.services.positioning.arrows.key_generators.placement_key_generator import (
    PlacementKeyGenerator,
)
from shared.application.services.positioning.arrows.key_generators.turns_tuple_key_generator import (
    TurnsTupleKeyGenerator,
)

# Import required services
from shared.application.services.positioning.arrows.placement.default_placement_service import (
    DefaultPlacementService,
)
from shared.application.services.positioning.arrows.placement.special_placement_ori_key_generator import (
    SpecialPlacementOriKeyGenerator,
)
from shared.application.services.positioning.arrows.placement.special_placement_service import (
    SpecialPlacementService,
)

from desktop.modern.application.services.positioning.arrows.key_generators.attribute_key_generator import (
    AttributeKeyGenerator,
)
from desktop.modern.core.types.coordinates import qpoint_to_point
from desktop.modern.core.types.geometry import Point
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData


logger = logging.getLogger(__name__)


class ArrowAdjustmentLookup:
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
        orientation_key_service: SpecialPlacementOriKeyGenerator,
        placement_key_service: PlacementKeyGenerator,
        turns_tuple_service: TurnsTupleKeyGenerator,
        attribute_key_service: AttributeKeyGenerator,
    ):
        """Initialize with required services for lookup operations."""
        self.special_placement_service = special_placement_service
        self.default_placement_service = default_placement_service
        self.orientation_key_service = orientation_key_service
        self.placement_key_service = placement_key_service
        self.turns_tuple_service = turns_tuple_service
        self.attribute_key_service = attribute_key_service

    def get_base_adjustment(
        self,
        pictograph_data: PictographData,
        motion_data: MotionData,
        letter: str,
        arrow_color: str = None,
    ) -> Point:
        """
        Get base adjustment using streamlined lookup logic.

        Args:
            pictograph_data: Pictograph data for context
            motion_data: Motion data containing type, rotation, and location info
            letter: Letter for special placement lookup
            arrow_color: Color of the arrow ('red' or 'blue')

        Returns:
            Point adjustment

        Raises:
            ValueError: If input data is invalid
            RuntimeError: If lookup fails
        """
        if not motion_data or not letter:
            raise ValueError("Missing motion or letter data for adjustment lookup")

        try:
            # Generate required keys for special placement lookup
            ori_key, turns_tuple, attr_key = self._generate_lookup_keys(
                pictograph_data, motion_data
            )

            logger.debug(
                f"Generated keys - ori: {ori_key}, turns: {turns_tuple}, attr: {attr_key}"
            )

            try:
                special_adjustment = self._lookup_special_placement(
                    motion_data, pictograph_data, arrow_color
                )
                return special_adjustment
            except ValueError:
                # No special placement found - fall back to default
                logger.debug("No special placement found, falling back to default")

            # STEP 2: Fall back to default calculation
            default_adjustment = self._calculate_default_adjustment(
                motion_data, pictograph_data
            )
            logger.debug(
                f"Using default adjustment: ({default_adjustment.x:.1f}, {default_adjustment.y:.1f})"
            )
            return default_adjustment

        except Exception as e:
            logger.error(f"Error in base adjustment lookup: {e}")
            raise RuntimeError(f"Arrow adjustment lookup failed: {e}") from e

    def _generate_lookup_keys(
        self, pictograph_data: PictographData, motion_data: MotionData
    ) -> tuple[str, str, str]:
        """Generate all required keys for special placement lookup."""
        try:
            # Create minimal pictograph data for legacy services that still need it

            ori_key = self.orientation_key_service.generate_orientation_key(
                motion_data, pictograph_data
            )
            turns_tuple = self.turns_tuple_service.generate_turns_tuple(pictograph_data)

            color = "blue"
            from desktop.modern.domain.models.arrow_data import ArrowData

            temp_arrow = ArrowData(color=color)
            attr_key = self.attribute_key_service.get_key_from_arrow(
                temp_arrow, pictograph_data
            )

            return (ori_key, turns_tuple, attr_key)

        except Exception as e:
            logger.error(f"Failed to generate lookup keys: {e}")
            raise RuntimeError(f"Key generation failed: {e}") from e

    def _lookup_special_placement(
        self,
        motion_data: MotionData,
        pictograph_data: PictographData,
        arrow_color: str = None,
    ) -> Point:
        """
        Look up special placement using exact legacy logic.

        Returns Point if found, raises ValueError if not found.
        """
        try:
            # Create minimal data for legacy service

            # This should return stored adjustment values if they exist
            adjustment = self.special_placement_service.get_special_adjustment(
                motion_data, pictograph_data, arrow_color
            )

            if adjustment:
                # Convert QPointF to Point
                point = qpoint_to_point(adjustment)
                return point

            # No special placement found
            raise ValueError("No special placement found")

        except Exception as e:
            if isinstance(e, ValueError):
                raise  # Re-raise ValueError as-is
            logger.error(f"Error in special placement lookup: {e}")
            raise RuntimeError(f"Special placement lookup failed: {e}") from e

    def _calculate_default_adjustment(
        self,
        motion_data: MotionData,
        pictograph_data: PictographData,
        grid_mode: str = "diamond",
    ) -> Point:
        """
        Calculate default adjustment using placement key and motion type.

        Returns Point adjustment.
        """
        try:
            # Create minimal pictograph data for legacy services

            # Get default placements for the grid mode and motion type
            default_placements = self.default_placement_service.all_defaults.get(
                grid_mode, {}
            ).get(motion_data.motion_type.value, {})

            # Generate placement key for default lookup
            placement_key = self.placement_key_service.generate_placement_key(
                motion_data, pictograph_data, default_placements, grid_mode
            )

            # Get adjustment from default placement service
            adjustment_point = self.default_placement_service.get_default_adjustment(
                motion_data, grid_mode="diamond", placement_key=placement_key
            )

            return adjustment_point

        except Exception as e:
            logger.error(f"Error calculating default adjustment: {e}")
            raise RuntimeError(f"Default adjustment calculation failed: {e}") from e
