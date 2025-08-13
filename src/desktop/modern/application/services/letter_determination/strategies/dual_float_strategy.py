"""
Dual Float Strategy Implementation

Direct port of legacy DualFloatStrategy with exact same logic
but using modern service patterns and immutable domain models.
"""

import logging
from typing import TYPE_CHECKING, Optional

from desktop.modern.core.interfaces.letter_determination.letter_determination_services import (
    ILetterDeterminationStrategy,
    IMotionComparisonService,
)
from desktop.modern.domain.models.enums import Letter, MotionType
from desktop.modern.domain.models.letter_determination.determination_models import (
    LetterDeterminationResult,
    MotionComparisonContext,
)

if TYPE_CHECKING:
    from desktop.modern.domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class DualFloatStrategy(ILetterDeterminationStrategy):
    """
    Direct port of legacy DualFloatStrategy.

    Handles cases where both blue and red motions are in FLOAT state.
    Uses exact matching against the dataset for letter determination.
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
        Check if this strategy applies to the given motion data.

        Direct port of legacy applies_to logic with additional validation.
        """
        blue_motion, red_motion = self._get_motions(pictograph_data)

        if not blue_motion or not red_motion:
            return False

        return (
            blue_motion.motion_type == MotionType.FLOAT
            and red_motion.motion_type == MotionType.FLOAT
            and blue_motion.start_loc is not None
            and red_motion.start_loc is not None
        )

    def execute(
        self,
        pictograph_data: "PictographData",
        dataset: dict[Letter, list["PictographData"]],
        comparison_service: IMotionComparisonService,
        context: Optional["MotionComparisonContext"] = None,
    ) -> "LetterDeterminationResult":
        """
        Execute dual float strategy using exact legacy algorithm.

        Direct port of legacy execute method with same matching logic.
        """
        context = context or MotionComparisonContext.default()

        if not self.applies_to(pictograph_data):
            return LetterDeterminationResult.failure(
                strategy=self.get_strategy_name(),
                reason="Strategy does not apply to this pictograph data",
            )

        # Direct port of legacy _match_exact logic
        for letter, examples in dataset.items():
            for example in examples:
                # Use comparison service for exact matching (legacy: comparator.compare)
                similarity = comparison_service.compare_motions(
                    pictograph_data, example, context
                )

                if similarity > 0.9:  # Threshold for exact match
                    logger.debug(f"Dual float match found: {letter.value}")
                    return LetterDeterminationResult.success(
                        letter=letter,
                        confidence=similarity,
                        strategy=self.get_strategy_name(),
                        attributes={
                            "matched_example": example.to_dict(),
                            "similarity_score": similarity,
                            "blue_motion_type": self._get_motions(pictograph_data)[
                                0
                            ].motion_type.value,
                            "red_motion_type": self._get_motions(pictograph_data)[
                                1
                            ].motion_type.value,
                        },
                    )

        logger.debug("No dual float match found")
        return LetterDeterminationResult.failure(
            strategy=self.get_strategy_name(),
            reason="No matching dual float pattern found in dataset",
        )

    def get_strategy_name(self) -> str:
        """Get the name of this strategy."""
        return "dual_float"

    def _is_dual_float(self, pictograph_data) -> bool:
        """
        Check if pictograph has dual float motion.

        Direct port of legacy _is_dual_float method.
        """
        blue_motion, red_motion = self._get_motions(pictograph_data)

        if not blue_motion or not red_motion:
            return False

        return (
            blue_motion.motion_type == MotionType.FLOAT
            and red_motion.motion_type == MotionType.FLOAT
        )

    def _validate_float_attributes(self, motion_data) -> bool:
        """
        Validate that float attributes are complete and valid.

        Additional validation beyond legacy for robustness.
        """
        blue_attrs, red_attrs = self._get_motions(motion_data)

        if not blue_attrs or not red_attrs:
            return False

        # Check that float motions have required prefloat attributes
        if blue_attrs.motion_type == MotionType.FLOAT:
            if not blue_attrs.prefloat_motion_type:
                logger.warning("Blue float motion missing prefloat_motion_type")
                return False

        if red_attrs.motion_type == MotionType.FLOAT:
            if not red_attrs.prefloat_motion_type:
                logger.warning("Red float motion missing prefloat_motion_type")
                return False

        # Check that locations are valid
        if blue_attrs.start_loc is None or red_attrs.start_loc is None:
            logger.warning("Float motion missing start locations")
            return False

        return True

    def get_debug_info(self, motion_data) -> dict[str, any]:
        """
        Get debug information for this strategy.

        Useful for troubleshooting why strategy did or didn't apply.
        """
        blue_motion, red_motion = self._get_motions(motion_data)

        return {
            "strategy": self.get_strategy_name(),
            "applies_to": self.applies_to(motion_data),
            "blue_motion_type": blue_motion.motion_type.value if blue_motion else None,
            "red_motion_type": red_motion.motion_type.value if red_motion else None,
            "blue_start_loc": (
                blue_motion.start_loc.value
                if blue_motion and blue_motion.start_loc
                else None
            ),
            "red_start_loc": (
                red_motion.start_loc.value
                if red_motion and red_motion.start_loc
                else None
            ),
            "is_dual_float": self._is_dual_float(motion_data),
            "has_valid_attributes": self._validate_float_attributes(motion_data),
        }
