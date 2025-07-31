"""
Motion Comparison Service Implementation

Pure business logic for motion comparison without UI dependencies.
Direct port of legacy MotionComparator logic with modern service patterns.
"""

import logging
from typing import TYPE_CHECKING, Optional

from desktop.modern.core.interfaces.letter_determination.letter_determination_services import (
    IMotionComparisonService,
    IPictographDatasetProvider,
)
from desktop.modern.domain.models.enums import MotionType, PropRotationDirection
from desktop.modern.domain.models.letter_determination.determination_models import (
    AttributeComparisonResult,
    MotionComparisonContext,
)

if TYPE_CHECKING:
    from desktop.modern.domain.models.motion.motion_attributes import MotionAttributes
    from desktop.modern.domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class MotionComparisonService(IMotionComparisonService):
    """
    Pure business logic for motion comparison without UI dependencies.

    Direct port of legacy MotionComparator.compare logic with exact same behavior
    but using modern service patterns and immutable domain models.
    """

    def __init__(self, dataset_provider: IPictographDatasetProvider):
        self._dataset_provider = dataset_provider

    def compare_motions(
        self,
        motion1: "PictographData",
        motion2: "PictographData",
        context: Optional["MotionComparisonContext"] = None,
    ) -> float:
        """
        Direct port of legacy MotionComparator.compare logic.

        Maintains exact legacy behavior including prefloat attribute handling
        and position/orientation matching.
        """
        context = context or MotionComparisonContext.default()

        # Get motion data from PictographData
        blue_attrs1 = motion1.motions.get("blue")
        red_attrs1 = motion1.motions.get("red")
        blue_attrs2 = motion2.motions.get("blue")
        red_attrs2 = motion2.motions.get("red")

        if not all([blue_attrs1, red_attrs1, blue_attrs2, red_attrs2]):
            return 0.0

        # Apply prefloat transformations (legacy: _update_prefloat_attrs)
        blue_attrs1 = self._update_prefloat_attrs(blue_attrs1, red_attrs1)
        red_attrs1 = self._update_prefloat_attrs(red_attrs1, blue_attrs1)
        blue_attrs2 = self._update_prefloat_attrs(blue_attrs2, red_attrs2)
        red_attrs2 = self._update_prefloat_attrs(red_attrs2, blue_attrs2)

        # Get effective motion types (legacy: _get_motion_type)
        blue_motion_type1 = self._get_motion_type(blue_attrs1)
        red_motion_type1 = self._get_motion_type(red_attrs1)
        blue_motion_type2 = self._get_motion_type(blue_attrs2)
        red_motion_type2 = self._get_motion_type(red_attrs2)

        # Position matching check (legacy: start_pos/end_pos comparison)
        if (
            motion1.start_position == motion2.start_position
            and motion1.end_position == motion2.end_position
        ):
            # Motion type matching (legacy: motion type comparison)
            if (
                blue_motion_type2 == blue_motion_type1
                and red_motion_type2 == red_motion_type1
            ):
                return 1.0

        # Full attribute comparison (legacy: exact attribute matching)
        blue_match = self._compare_motion_attributes_exact(
            blue_attrs2, blue_attrs1, context
        )
        red_match = self._compare_motion_attributes_exact(
            red_attrs2, red_attrs1, context
        )

        return 1.0 if (blue_match and red_match) else 0.0

    def compare_attributes(
        self,
        attrs1: "MotionAttributes",
        attrs2: "MotionAttributes",
        context: Optional["MotionComparisonContext"] = None,
    ) -> "AttributeComparisonResult":
        """
        Compare motion attributes with detailed breakdown.

        Provides detailed information about what matched and what didn't.
        """
        context = context or MotionComparisonContext.default()

        # Location comparison
        locations_match = (
            attrs1.start_loc == attrs2.start_loc and attrs1.end_loc == attrs2.end_loc
        )

        # Orientation comparison
        orientations_match = (
            attrs1.start_ori == attrs2.start_ori and attrs1.end_ori == attrs2.end_ori
        )

        # Motion type comparison (considering prefloat)
        motion_types_match = self._motion_types_match(attrs1, attrs2)

        # Prop rotation direction comparison (considering context)
        prop_rot_dirs_match = self._prop_rot_dirs_match(attrs1, attrs2, context)

        # Prefloat attributes comparison
        prefloat_match = self._prefloat_attributes_match(attrs1, attrs2)

        overall_match = (
            locations_match
            and orientations_match
            and motion_types_match
            and prop_rot_dirs_match
            and prefloat_match
        )

        return AttributeComparisonResult(
            locations_match=locations_match,
            orientations_match=orientations_match,
            motion_types_match=motion_types_match,
            prop_rot_dirs_match=prop_rot_dirs_match,
            prefloat_attributes_match=prefloat_match,
            overall_match=overall_match,
        )

    def reverse_prop_rot_dir(self, prop_rot_dir: str) -> str:
        """
        Direct port of legacy _reverse_prop_rot_dir method.
        """
        if prop_rot_dir == PropRotationDirection.CLOCKWISE.value:
            return PropRotationDirection.COUNTER_CLOCKWISE.value
        elif prop_rot_dir == PropRotationDirection.COUNTER_CLOCKWISE.value:
            return PropRotationDirection.CLOCKWISE.value
        return prop_rot_dir

    def apply_direction_inversion(self, direction: str, prop_rot_dir: str) -> str:
        """
        Apply direction-based prop rotation inversion.

        Direct port of legacy direction inversion logic from NonHybridShiftStrategy.
        """
        if direction == "opp":  # OPP direction
            return self.reverse_prop_rot_dir(prop_rot_dir)
        return prop_rot_dir

    def _update_prefloat_attrs(
        self, attrs: "MotionAttributes", other_attrs: "MotionAttributes"
    ) -> "MotionAttributes":
        """
        Update prefloat attributes based on other motion.

        Direct port of legacy _update_prefloat_attrs logic.
        """
        if attrs.motion_type == MotionType.FLOAT:
            # Create new attributes with prefloat information from other motion
            from dataclasses import replace

            return replace(
                attrs,
                prefloat_motion_type=other_attrs.motion_type,
                prefloat_prop_rot_dir=other_attrs.prop_rot_dir,
            )
        return attrs

    def _get_motion_type(self, attrs: "MotionAttributes") -> MotionType:
        """
        Get effective motion type considering prefloat state.

        Direct port of legacy _get_motion_type logic.
        """
        if attrs.motion_type == MotionType.FLOAT and attrs.prefloat_motion_type:
            return attrs.prefloat_motion_type
        return attrs.motion_type

    def _compare_motion_attributes_exact(
        self,
        attrs1: "MotionAttributes",
        attrs2: "MotionAttributes",
        context: "MotionComparisonContext",
    ) -> bool:
        """
        Exact attribute comparison for legacy compatibility.

        This performs the exact same comparison as the legacy system.
        """
        return (
            attrs1.start_loc == attrs2.start_loc
            and attrs1.end_loc == attrs2.end_loc
            and attrs1.start_ori == attrs2.start_ori
            and attrs1.end_ori == attrs2.end_ori
            and attrs1.motion_type == attrs2.motion_type
            and attrs1.prop_rot_dir == attrs2.prop_rot_dir
            and attrs1.turns == attrs2.turns
            and attrs1.prefloat_motion_type == attrs2.prefloat_motion_type
            and attrs1.prefloat_prop_rot_dir == attrs2.prefloat_prop_rot_dir
        )

    def _motion_types_match(
        self, attrs1: "MotionAttributes", attrs2: "MotionAttributes"
    ) -> bool:
        """
        Check if motion types match, considering prefloat states.

        Direct port of legacy _is_motion_type_matching logic.
        """
        type1 = self._get_motion_type(attrs1)
        type2 = self._get_motion_type(attrs2)
        return type1 == type2

    def _prop_rot_dirs_match(
        self,
        attrs1: "MotionAttributes",
        attrs2: "MotionAttributes",
        context: "MotionComparisonContext",
    ) -> bool:
        """
        Check if prop rotation directions match, considering context.

        Handles swapping and direction inversion as needed.
        """
        dir1 = attrs1.effective_prop_rot_dir.value
        dir2 = attrs2.effective_prop_rot_dir.value

        if context.swap_prop_rot_dir:
            dir2 = self.reverse_prop_rot_dir(dir2)

        return dir1 == dir2

    def _prefloat_attributes_match(
        self, attrs1: "MotionAttributes", attrs2: "MotionAttributes"
    ) -> bool:
        """
        Check if prefloat attributes match.

        Direct port of legacy _is_prefloat_matching logic.
        """
        if attrs1.prefloat_motion_type is None and attrs2.prefloat_motion_type is None:
            return True

        if attrs1.prefloat_motion_type != attrs2.prefloat_motion_type:
            return False

        if attrs1.prefloat_prop_rot_dir != attrs2.prefloat_prop_rot_dir:
            return False

        return True

    def compare_motion_to_example(
        self,
        motion_attrs: "MotionAttributes",
        example_attrs: "MotionAttributes",
        swap_prop_rot_dir: bool = False,
    ) -> bool:
        """
        Direct port of legacy compare_motion_to_example method.

        Used by strategies for specific motion comparison scenarios.
        """
        expected_prop_rot_dir = self._get_expected_prop_rot_dir(
            example_attrs.prop_rot_dir.value, swap_prop_rot_dir
        )

        return (
            motion_attrs.start_loc == example_attrs.start_loc
            and motion_attrs.end_loc == example_attrs.end_loc
            and self._is_motion_type_matching_for_example(motion_attrs, example_attrs)
            and motion_attrs.prop_rot_dir.value == expected_prop_rot_dir
        )

    def _get_expected_prop_rot_dir(self, prop_rot_dir: str, swap: bool) -> str:
        """Direct port of legacy _get_expected_prop_rot_dir."""
        return self.reverse_prop_rot_dir(prop_rot_dir) if swap else prop_rot_dir

    def _is_motion_type_matching_for_example(
        self, motion_attrs: "MotionAttributes", example_attrs: "MotionAttributes"
    ) -> bool:
        """Direct port of legacy _is_motion_type_matching for examples."""
        return (
            example_attrs.motion_type == motion_attrs.motion_type
            or example_attrs.motion_type == motion_attrs.prefloat_motion_type
        )

    def compare_with_prefloat(
        self,
        target: "PictographData",
        example: "PictographData",
        swap_prop_rot_dir: bool = False,
    ) -> float:
        """
        Direct port of legacy compare_with_prefloat method.

        Used for complex float-shift hybrid comparisons.
        """
        float_attr, shift_attr = self._get_float_and_shift_attrs(target)
        example_float, example_shift = self._get_float_and_shift_attrs(example)

        if not float_attr or not example_float:
            return 0.0

        float_expected_rot_dir = self._get_expected_prop_rot_dir(
            example_float.prop_rot_dir.value, swap_prop_rot_dir
        )

        float_match = (
            float_attr.start_loc == example_float.start_loc
            and float_attr.end_loc == example_float.end_loc
            and float_expected_rot_dir
            == self.reverse_prop_rot_dir(
                float_attr.prefloat_prop_rot_dir.value
                if float_attr.prefloat_prop_rot_dir
                else ""
            )
            and example_float.motion_type == float_attr.prefloat_motion_type
        )

        shift_match = (
            shift_attr.start_loc == example_shift.start_loc
            and shift_attr.end_loc == example_shift.end_loc
            and shift_attr.prop_rot_dir == example_shift.prop_rot_dir
            and shift_attr.motion_type == example_shift.motion_type
        )

        return 1.0 if float_match and shift_match else 0.0

    def _get_float_and_shift_attrs(self, data: "PictographData") -> tuple:
        """Get float and shift attributes from pictograph data."""
        if data.blue_attributes.motion_type == MotionType.FLOAT:
            return data.blue_attributes, data.red_attributes
        return data.red_attributes, data.blue_attributes
