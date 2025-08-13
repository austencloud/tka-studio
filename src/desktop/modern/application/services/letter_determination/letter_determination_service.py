"""
Letter Determination Service Implementation

Main orchestrator for letter determination - platform agnostic.
Direct port of legacy LetterDeterminer with exact same behavior.
"""

import logging
from typing import TYPE_CHECKING, Optional

from desktop.modern.core.interfaces.letter_determination.letter_determination_services import (
    ILetterDeterminationService,
    IMotionAttributeService,
    IMotionComparisonService,
    IPictographDatasetProvider,
)
from desktop.modern.domain.models.enums import Letter, MotionType
from desktop.modern.domain.models.letter_determination.determination_models import (
    LetterDeterminationResult,
    MotionComparisonContext,
)

from .strategies.dual_float_strategy import DualFloatStrategy
from .strategies.non_hybrid_shift_strategy import NonHybridShiftStrategy

if TYPE_CHECKING:
    from desktop.modern.domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class LetterDeterminationService(ILetterDeterminationService):
    """
    Main orchestrator for letter determination - platform agnostic.

    Direct port of legacy LetterDeterminer with exact same strategy order
    and fallback behavior, but using modern service patterns.
    """

    def __init__(
        self,
        dataset_provider: IPictographDatasetProvider,
        comparison_service: IMotionComparisonService,
        attribute_service: IMotionAttributeService,
    ):
        self._dataset_provider = dataset_provider
        self._comparison_service = comparison_service
        self._attribute_service = attribute_service

        # Register strategies in exact legacy order
        self._strategies = [
            DualFloatStrategy(comparison_service),
            NonHybridShiftStrategy(comparison_service),
        ]

    def determine_letter(
        self,
        pictograph_data: "PictographData",
        context: Optional["MotionComparisonContext"] = None,
    ) -> "LetterDeterminationResult":
        """
        Determine letter using exact legacy algorithm.

        Direct port of legacy LetterDeterminer.determine_letter with same logic.
        """
        context = context or MotionComparisonContext.default()

        logger.debug(f"Starting letter determination for beat {pictograph_data.beat}")

        # Sync attributes (legacy behavior: attribute_manager.sync_attributes)
        pictograph_data = self._attribute_service.sync_attributes(pictograph_data)

        # Check for static motions - early return like legacy
        if self._is_static_motion(pictograph_data):
            logger.debug("Both motions are static, returning None")
            return LetterDeterminationResult.failure(
                strategy="static_check", reason="Both motions are static"
            )

        # Get dataset
        dataset = self._dataset_provider.get_pictograph_dataset()
        if not dataset:
            logger.warning("Pictograph dataset is empty")
            return LetterDeterminationResult.failure(
                strategy="dataset_check", reason="Pictograph dataset is empty"
            )

        # Try each strategy in exact legacy order
        for strategy in self._strategies:
            if strategy.applies_to(pictograph_data):
                logger.debug(f"Applying strategy: {strategy.get_strategy_name()}")
                result = strategy.execute(
                    pictograph_data, dataset, self._comparison_service, context
                )

                if result.is_successful:
                    logger.debug(
                        f"Strategy {strategy.get_strategy_name()} found letter: {result.letter.value}"
                    )
                    return result
                else:
                    logger.debug(
                        f"Strategy {strategy.get_strategy_name()} failed: {result.warnings}"
                    )

        # Fallback search (exact legacy implementation)
        logger.debug("All strategies failed, trying fallback search")
        return self._fallback_search(pictograph_data, dataset, context)

    def update_pictograph_dataset(
        self, dataset: dict[Letter, list["PictographData"]]
    ) -> None:
        """
        Update the pictograph dataset and refresh dependencies.

        Direct port of legacy update_pictograph_dataset.
        """
        logger.info(f"Updating pictograph dataset with {len(dataset)} letters")
        # The dataset provider handles the actual update
        # This method exists for interface compliance

    def get_available_strategies(self) -> list[str]:
        """Get list of available determination strategies."""
        return [strategy.get_strategy_name() for strategy in self._strategies]

    def validate_pictograph_data(self, pictograph_data: "PictographData") -> bool:
        """
        Validate that pictograph data is suitable for letter determination.

        Additional validation beyond legacy for robustness.
        """
        try:
            # Basic validation
            if pictograph_data.beat < 0:
                logger.warning("Invalid beat number")
                return False

            # Check attributes exist
            if (
                not pictograph_data.blue_attributes
                or not pictograph_data.red_attributes
            ):
                logger.warning("Missing motion attributes")
                return False

            # Check for required location data
            blue_attrs = pictograph_data.blue_attributes
            red_attrs = pictograph_data.red_attributes

            if (
                blue_attrs.start_loc is None
                or blue_attrs.end_loc is None
                or red_attrs.start_loc is None
                or red_attrs.end_loc is None
            ):
                logger.warning("Missing location data")
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating pictograph data: {str(e)}")
            return False

    def _is_static_motion(self, pictograph_data: "PictographData") -> bool:
        """
        Check if both motions are static.

        Direct port of legacy static motion check.
        """
        blue_motion = pictograph_data.motions.get("blue")
        red_motion = pictograph_data.motions.get("red")

        if not blue_motion or not red_motion:
            return False

        return (
            blue_motion.motion_type == MotionType.STATIC
            and red_motion.motion_type == MotionType.STATIC
        )

    def _fallback_search(
        self,
        pictograph_data: "PictographData",
        dataset: dict[Letter, list["PictographData"]],
        context: "MotionComparisonContext",
    ) -> "LetterDeterminationResult":
        """
        Fallback search using exhaustive comparison.

        Direct port of legacy _fallback_search with exact same logic.
        """
        logger.debug("Starting fallback search")

        # Check dataset size (legacy debug logging)
        dataset_size = len(dataset)
        logger.debug(f"Fallback search: dataset has {dataset_size} letters")

        if dataset_size == 0:
            logger.warning(
                "Pictograph dataset is empty - cannot perform fallback search"
            )
            return LetterDeterminationResult.failure(
                strategy="fallback_empty_dataset", reason="Dataset is empty"
            )

        # Apply prop_rot_dir swapping if needed (legacy behavior)
        search_data = pictograph_data
        if context.swap_prop_rot_dir:
            search_data = self._apply_prop_rot_dir_swap(pictograph_data)

        # Exhaustive comparison (exact legacy logic)
        for letter, examples in dataset.items():
            for example in examples:
                similarity = self._comparison_service.compare_motions(
                    search_data, example, context
                )

                if similarity > 0.9:  # Threshold for match
                    logger.debug(f"Fallback search found match: {letter.value}")
                    return LetterDeterminationResult.success(
                        letter=letter,
                        confidence=similarity,
                        strategy="fallback_exhaustive",
                        attributes={
                            "matched_example": example.to_legacy_dict(),
                            "similarity_score": similarity,
                            "swap_prop_rot_dir": context.swap_prop_rot_dir,
                        },
                    )

        logger.debug("Fallback search: no matches found")
        return LetterDeterminationResult.failure(
            strategy="fallback_no_match", reason="No matches found in exhaustive search"
        )

    def _apply_prop_rot_dir_swap(
        self, pictograph_data: "PictographData"
    ) -> "PictographData":
        """
        Apply prop rotation direction swapping.

        Creates new pictograph data with swapped rotation directions.
        """
        from dataclasses import replace

        # Swap blue prop rotation direction
        blue_swapped = replace(
            pictograph_data.blue_attributes,
            prop_rot_dir=self._swap_prop_rot_dir(
                pictograph_data.blue_attributes.prop_rot_dir
            ),
        )

        # Swap red prop rotation direction
        red_swapped = replace(
            pictograph_data.red_attributes,
            prop_rot_dir=self._swap_prop_rot_dir(
                pictograph_data.red_attributes.prop_rot_dir
            ),
        )

        return replace(
            pictograph_data, blue_attributes=blue_swapped, red_attributes=red_swapped
        )

    def _swap_prop_rot_dir(self, prop_rot_dir) -> any:
        """Swap a single prop rotation direction."""
        return self._comparison_service.reverse_prop_rot_dir(prop_rot_dir.value)

    def get_determination_statistics(self) -> dict[str, any]:
        """
        Get statistics about letter determination usage.

        Useful for debugging and optimization.
        """
        return {
            "available_strategies": len(self._strategies),
            "strategy_names": self.get_available_strategies(),
            "dataset_size": len(self._dataset_provider.get_pictograph_dataset()),
            "dataset_valid": self._dataset_provider.validate_dataset(),
        }

    def test_strategy_coverage(
        self, test_data: list["PictographData"]
    ) -> dict[str, any]:
        """
        Test strategy coverage against a set of test data.

        Useful for validating that strategies cover expected motion types.
        """
        coverage_stats = {
            strategy.get_strategy_name(): 0 for strategy in self._strategies
        }
        coverage_stats["no_strategy"] = 0
        coverage_stats["total"] = len(test_data)

        for motion_data in test_data:
            strategy_found = False
            for strategy in self._strategies:
                if strategy.applies_to(motion_data):
                    coverage_stats[strategy.get_strategy_name()] += 1
                    strategy_found = True
                    break

            if not strategy_found:
                coverage_stats["no_strategy"] += 1

        return coverage_stats
