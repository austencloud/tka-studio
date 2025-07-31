"""
Non-Hybrid Shift Strategy Implementation

Direct port of legacy NonHybridShiftStrategy with exact same logic
including complex direction-aware prefloat matching.
"""

import logging
from typing import TYPE_CHECKING, Optional

from desktop.modern.core.interfaces.letter_determination.letter_determination_services import (
    ILetterDeterminationStrategy,
    IMotionComparisonService,
)
from desktop.modern.domain.models.enums import Letter, MotionType, PropRotationDirection
from desktop.modern.domain.models.letter_determination.determination_models import (
    LetterDeterminationResult,
    MotionComparisonContext,
)
from desktop.modern.domain.models.pictograph_data import PictographData

if TYPE_CHECKING:
    from desktop.modern.domain.models.motion.motion_attributes import MotionAttributes

logger = logging.getLogger(__name__)


class NonHybridShiftStrategy(ILetterDeterminationStrategy):
    """
    Direct port of legacy NonHybridShiftStrategy.

    Handles cases where one motion is FLOAT and the other is PRO/ANTI.
    Includes complex direction-aware matching and prefloat attribute handling.
    """

    def __init__(self, comparison_service: IMotionComparisonService):
        self._comparison_service = comparison_service

    def _get_motions(self, pictograph_data: "PictographData"):
        """
        Helper method to get blue and red motions from PictographData.

        Args:
            pictograph_data: PictographData instance

        Returns:
            Tuple of (blue_motion, red_motion)
        """
        return pictograph_data.motions.get("blue"), pictograph_data.motions.get("red")

    def applies_to(self, pictograph_data) -> bool:
        """
        Check if this strategy applies - one motion FLOAT, other PRO/ANTI.

        Direct port of legacy applies_to logic.
        """
        blue_motion, red_motion = self._get_motions(pictograph_data)

        if not blue_motion or not red_motion:
            return False

        blue_is_float = blue_motion.motion_type == MotionType.FLOAT
        red_is_float = red_motion.motion_type == MotionType.FLOAT
        blue_is_shift = blue_motion.motion_type in [
            MotionType.PRO,
            MotionType.ANTI,
        ]
        red_is_shift = red_motion.motion_type in [
            MotionType.PRO,
            MotionType.ANTI,
        ]

        return (blue_is_float and red_is_shift) or (red_is_float and blue_is_shift)

    def execute(
        self,
        motion_data: "PictographData",
        dataset: dict[Letter, list["PictographData"]],
        comparison_service: IMotionComparisonService,
        context: Optional["MotionComparisonContext"] = None,
    ) -> "LetterDeterminationResult":
        """
        Execute non-hybrid shift strategy with direction-aware matching.

        Direct port of legacy execute method with exact same logic.
        """
        context = context or MotionComparisonContext.default()

        if not self.applies_to(motion_data):
            return LetterDeterminationResult.failure(
                strategy=self.get_strategy_name(),
                reason="Strategy does not apply to this motion data",
            )

        logger.debug(
            f"Executing non-hybrid shift strategy for motion at beat {motion_data.beat}"
        )

        # Identify float and shift components (legacy: _identify_components)
        float_attrs, non_float_attrs, float_color = self._identify_components(
            motion_data
        )

        if not float_attrs or not non_float_attrs:
            return LetterDeterminationResult.failure(
                strategy=self.get_strategy_name(),
                reason="Could not identify float and shift components",
            )

        # Apply direction-based transformations (legacy: _update_prefloat_attributes)
        transformed_data = self._apply_direction_transformations(
            motion_data, float_attrs, non_float_attrs, float_color
        )

        # Find matching letter with prefloat-aware comparison (legacy: _find_matching_letter)
        result = self._find_matching_letter(
            transformed_data, float_attrs, non_float_attrs, dataset
        )

        return result

    def get_strategy_name(self) -> str:
        """Get the name of this strategy."""
        return "non_hybrid_shift"

    def _identify_components(
        self, data: "PictographData"
    ) -> tuple[Optional["MotionAttributes"], Optional["MotionAttributes"], str]:
        """
        Identify float and shift attributes.

        Direct port of legacy _identify_components method.
        """
        blue_attrs = data.motions["blue"]
        red_attrs = data.motions["red"]

        # Find float motion
        float_attrs = None
        non_float_attrs = None
        float_color = ""

        if blue_attrs.motion_type == MotionType.FLOAT:
            float_attrs = blue_attrs
            non_float_attrs = red_attrs
            float_color = "blue"
        elif red_attrs.motion_type == MotionType.FLOAT:
            float_attrs = red_attrs
            non_float_attrs = blue_attrs
            float_color = "red"

        return float_attrs, non_float_attrs, float_color

    def _apply_direction_transformations(
        self,
        pictograph_data: "PictographData",
        float_attr: "MotionAttributes",
        non_float_attrs: "MotionAttributes",
        color: str,
    ) -> "PictographData":
        """
        Apply direction-based transformations to prefloat attributes.

        Direct port of legacy _update_prefloat_attributes method with direction handling.
        """
        from dataclasses import replace

        # Get base rotation (legacy: _get_base_rotation)
        base_rotation = self._get_base_rotation(float_attr, non_float_attrs)

        # Apply direction inversion (legacy: _apply_direction_inversion)
        final_rotation = self._apply_direction_inversion(
            pictograph_data.direction.value, base_rotation
        )

        # Update float attributes with prefloat information
        updated_float_attr = replace(
            float_attr,
            prefloat_motion_type=non_float_attrs.motion_type,
            prefloat_prop_rot_dir=PropRotationDirection(final_rotation),
        )

        # Create updated pictograph data
        updated_motions = pictograph_data.motions.copy()
        if color == "blue":
            updated_motions["blue"] = updated_float_attr
        else:
            updated_motions["red"] = updated_float_attr

        return replace(pictograph_data, motions=updated_motions)

    def _get_base_rotation(
        self, float_attrs: "MotionAttributes", non_float_attrs: "MotionAttributes"
    ) -> str:
        """
        Resolve rotation source based on motion state.

        Direct port of legacy _get_base_rotation logic.
        """
        if float_attrs.prop_rot_dir == PropRotationDirection.NO_ROT:
            return non_float_attrs.prop_rot_dir.value
        return float_attrs.prop_rot_dir.value

    def _apply_direction_inversion(self, direction: str, prop_rot_dir: str) -> str:
        """
        Handle OPP direction inversion.

        Direct port of legacy _apply_direction_inversion logic.
        """
        if direction == "opp":  # OPP direction
            if prop_rot_dir == PropRotationDirection.CLOCKWISE.value:
                return PropRotationDirection.COUNTER_CLOCKWISE.value
            elif prop_rot_dir == PropRotationDirection.COUNTER_CLOCKWISE.value:
                return PropRotationDirection.CLOCKWISE.value
        return prop_rot_dir

    def _find_matching_letter(
        self,
        pictograph: "PictographData",
        float_attrs: "MotionAttributes",
        non_float_attrs: "MotionAttributes",
        dataset: dict[Letter, list["PictographData"]],
    ) -> "LetterDeterminationResult":
        """
        Match using prefloat-aware comparison.

        Direct port of legacy _find_matching_letter method.
        """
        for letter, examples in dataset.items():
            for example in examples:
                if self._matches_example(
                    pictograph, float_attrs, non_float_attrs, example
                ):
                    logger.debug(f"Non-hybrid shift match found: {letter.value}")
                    return LetterDeterminationResult.success(
                        letter=letter,
                        confidence=1.0,
                        strategy=self.get_strategy_name(),
                        attributes={
                            "matched_example": example.to_legacy_dict(),
                            "float_color": (
                                "blue"
                                if pictograph.motions["blue"].motion_type
                                == MotionType.FLOAT
                                else "red"
                            ),
                            "prefloat_motion_type": (
                                float_attrs.prefloat_motion_type.value
                                if float_attrs.prefloat_motion_type
                                else None
                            ),
                            "prefloat_prop_rot_dir": (
                                float_attrs.prefloat_prop_rot_dir.value
                                if float_attrs.prefloat_prop_rot_dir
                                else None
                            ),
                            "direction": pictograph.direction.value,
                        },
                    )

        logger.debug("No non-hybrid shift match found")
        return LetterDeterminationResult.failure(
            strategy=self.get_strategy_name(),
            reason="No matching non-hybrid shift pattern found in dataset",
        )

    def _matches_example(
        self,
        pictograph: "PictographData",
        float_attrs: "MotionAttributes",
        non_float_attrs: "MotionAttributes",
        example: "PictographData",
    ) -> bool:
        """
        Corrected comparison logic that avoids searching for FLOAT in examples.

        Direct port of legacy _matches_example with exact same logic.
        """
        # Get example components (neither will be FLOAT in examples)
        example_blue = example.motions["blue"]
        example_red = example.motions["red"]

        # Identify which example attribute to compare against which motion
        # Since example won't have FLOAT, we need to match based on position/role
        if float_attrs == pictograph.motions["blue"]:
            # Blue is float, so compare against example blue
            reference_for_float = example_blue
            reference_for_non_float = example_red
        else:
            # Red is float, so compare against example red
            reference_for_float = example_red
            reference_for_non_float = example_blue

        # Match float motion against example using prefloat attributes
        float_match = (
            float_attrs.start_loc == reference_for_float.start_loc
            and float_attrs.end_loc == reference_for_float.end_loc
            and float_attrs.prefloat_prop_rot_dir == reference_for_float.prop_rot_dir
            and float_attrs.prefloat_motion_type == reference_for_float.motion_type
        )

        # Match non-float motion with potential direction inversion
        expected_prop_rot_dir = self._apply_direction_inversion(
            pictograph.direction.value, reference_for_non_float.prop_rot_dir.value
        )

        non_float_match = (
            non_float_attrs.start_loc == reference_for_non_float.start_loc
            and non_float_attrs.end_loc == reference_for_non_float.end_loc
            and non_float_attrs.prop_rot_dir.value == expected_prop_rot_dir
            and non_float_attrs.motion_type == reference_for_non_float.motion_type
        )

        return float_match and non_float_match

    def get_debug_info(self, motion_data: "PictographData") -> dict[str, any]:
        """
        Get debug information for this strategy.

        Useful for troubleshooting complex matching scenarios.
        """
        float_attrs, non_float_attrs, float_color = self._identify_components(
            motion_data
        )

        debug_info = {
            "strategy": self.get_strategy_name(),
            "applies_to": self.applies_to(motion_data),
            "blue_motion_type": motion_data.motions["blue"].motion_type.value,
            "red_motion_type": motion_data.motions["red"].motion_type.value,
            "float_color": float_color,
            "direction": motion_data.direction.value,
        }

        if float_attrs:
            debug_info.update(
                {
                    "float_start_loc": float_attrs.start_loc.value,
                    "float_end_loc": float_attrs.end_loc.value,
                    "float_prop_rot_dir": float_attrs.prop_rot_dir.value,
                    "prefloat_motion_type": (
                        float_attrs.prefloat_motion_type.value
                        if float_attrs.prefloat_motion_type
                        else None
                    ),
                    "prefloat_prop_rot_dir": (
                        float_attrs.prefloat_prop_rot_dir.value
                        if float_attrs.prefloat_prop_rot_dir
                        else None
                    ),
                }
            )

        if non_float_attrs:
            debug_info.update(
                {
                    "non_float_start_loc": non_float_attrs.start_loc.value,
                    "non_float_end_loc": non_float_attrs.end_loc.value,
                    "non_float_prop_rot_dir": non_float_attrs.prop_rot_dir.value,
                    "non_float_motion_type": non_float_attrs.motion_type.value,
                }
            )

        return debug_info
