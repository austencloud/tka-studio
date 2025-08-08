"""
Circular Generator - Practical Generation Architecture

Handles circular sequence generation with direct CAP transformation methods.
No over-engineered strategy patterns - around 200 lines.
"""

from __future__ import annotations

import logging

from desktop.modern.core.interfaces.generation_services import CAPType, SliceSize
from desktop.modern.domain.models.generation_models import GenerationConfig
from desktop.modern.domain.models.pictograph_data import PictographData

from .freeform_generator import FreeformGenerator


logger = logging.getLogger(__name__)


class CircularGenerator:
    """
    Practical circular sequence generator with direct CAP transformations.

    Uses the freeform generator to create base patterns, then applies
    CAP transformations using direct methods (no strategy pattern).
    """

    def __init__(self, workbench_manager=None):
        self.freeform_generator = FreeformGenerator(workbench_manager)

    def generate_sequence(self, config: GenerationConfig) -> list[PictographData]:
        """
        Generate a circular sequence with CAP transformations.

        Args:
            config: Generation configuration with CAP type and slice size

        Returns:
            List of generated PictographData objects
        """
        # Validate circular-specific requirements
        if not self._validate_circular_config(config):
            return []

        logger.info(
            f"🎯 Starting circular generation: CAP={config.cap_type.value}, slice={config.slice_size.value}"
        )

        # Calculate word length based on slice size
        word_length = self._calculate_word_length(config.length, config.slice_size)

        # Generate base pattern using freeform generator
        # The freeform generator will establish its own start position
        base_config = self._create_base_config(config, word_length)
        base_pattern = self.freeform_generator.generate_sequence(base_config)

        if not base_pattern:
            logger.error("Failed to generate base pattern")
            return []

        logger.info(f"✅ Generated base pattern with {len(base_pattern)} beats")

        # Apply CAP transformation
        transformed_pattern = self._apply_cap_transformation(
            base_pattern, config.cap_type
        )

        if not transformed_pattern:
            logger.error("Failed to apply CAP transformation")
            return base_pattern

        logger.info(
            f"✅ Applied {config.cap_type.value} transformation: {len(transformed_pattern)} beats"
        )

        # Combine base + transformed patterns
        full_sequence = base_pattern + transformed_pattern

        # Trim to requested length
        final_sequence = full_sequence[: config.length]

        logger.info(f"🎉 Generated circular sequence with {len(final_sequence)} beats")
        return final_sequence

    def _validate_circular_config(self, config: GenerationConfig) -> bool:
        """Simple validation for circular generation."""
        if not config.cap_type:
            logger.error("CAP type is required for circular generation")
            return False

        if not config.slice_size:
            logger.error("Slice size is required for circular generation")
            return False

        if config.length < 2:
            logger.error("Circular sequences must be at least 2 beats long")
            return False

        return True

    def _calculate_word_length(self, total_length: int, slice_size: SliceSize) -> int:
        """Calculate the word length based on slice size."""
        if slice_size == SliceSize.HALVED:
            return max(1, total_length // 2)
        if slice_size == SliceSize.QUARTERED:
            return max(1, total_length // 4)
        # Default to halved
        return max(1, total_length // 2)

    def _create_base_config(
        self, original_config: GenerationConfig, word_length: int
    ) -> GenerationConfig:
        """Create configuration for base pattern generation."""
        return GenerationConfig(
            mode=original_config.mode,
            length=word_length,
            level=original_config.level,
            turn_intensity=original_config.turn_intensity,
            letter_types=original_config.letter_types,
            prop_continuity=original_config.prop_continuity,
        )

    def _apply_cap_transformation(
        self, base_pattern: list[PictographData], cap_type: CAPType
    ) -> list[PictographData]:
        """
        Apply CAP transformation using direct methods.
        No over-engineered strategy pattern - just direct transformation logic.
        """
        if cap_type == CAPType.STRICT_ROTATED:
            return self._apply_rotated_transformation(base_pattern)
        if cap_type == CAPType.STRICT_MIRRORED:
            return self._apply_mirrored_transformation(base_pattern)
        if cap_type == CAPType.STRICT_SWAPPED:
            return self._apply_swapped_transformation(base_pattern)
        if cap_type in (CAPType.STRICT_COMPLEMENTARY, CAPType.SWAPPED_COMPLEMENTARY):
            return self._apply_complementary_transformation(base_pattern)
        logger.error(f"Unknown CAP type: {cap_type}")
        return []

    def _apply_rotated_transformation(
        self, pattern: list[PictographData]
    ) -> list[PictographData]:
        """Apply 180-degree rotation transformation."""
        transformed = []

        for i, beat in enumerate(pattern):
            try:
                rotated_beat = PictographData(
                    letter=beat.letter,
                    start_position=self._rotate_position_180(beat.start_position),
                    end_position=self._rotate_position_180(beat.end_position),
                    beat=beat.beat + len(pattern),
                    motions=self._rotate_motions(beat.motions),
                    metadata=beat.metadata,
                )
                transformed.append(rotated_beat)

            except Exception as e:
                logger.exception(f"Failed to rotate beat {i}: {e}")
                continue

        logger.debug(f"Rotated {len(transformed)} beats")
        return transformed

    def _apply_mirrored_transformation(
        self, pattern: list[PictographData]
    ) -> list[PictographData]:
        """Apply horizontal mirror transformation."""
        transformed = []

        for i, beat in enumerate(pattern):
            try:
                mirrored_beat = PictographData(
                    letter=beat.letter,
                    start_position=self._mirror_position_horizontal(
                        beat.start_position
                    ),
                    end_position=self._mirror_position_horizontal(beat.end_position),
                    beat=beat.beat + len(pattern),
                    motions=self._mirror_motions(beat.motions),
                    metadata=beat.metadata,
                )
                transformed.append(mirrored_beat)

            except Exception as e:
                logger.exception(f"Failed to mirror beat {i}: {e}")
                continue

        logger.debug(f"Mirrored {len(transformed)} beats")
        return transformed

    def _apply_swapped_transformation(
        self, pattern: list[PictographData]
    ) -> list[PictographData]:
        """Apply blue/red prop swap transformation."""
        transformed = []

        for i, beat in enumerate(pattern):
            try:
                swapped_motions = {}

                # Swap blue and red motions
                if "blue" in beat.motions:
                    swapped_motions["red"] = beat.motions["blue"]
                if "red" in beat.motions:
                    swapped_motions["blue"] = beat.motions["red"]

                swapped_beat = PictographData(
                    letter=beat.letter,
                    start_position=beat.start_position,
                    end_position=beat.end_position,
                    beat=beat.beat + len(pattern),
                    motions=swapped_motions,
                    metadata=beat.metadata,
                )
                transformed.append(swapped_beat)

            except Exception as e:
                logger.exception(f"Failed to swap beat {i}: {e}")
                continue

        logger.debug(f"Swapped {len(transformed)} beats")
        return transformed

    def _apply_complementary_transformation(
        self, pattern: list[PictographData]
    ) -> list[PictographData]:
        """Apply complementary transformation (combination of rotated + mirrored)."""
        # First apply rotation
        rotated = self._apply_rotated_transformation(pattern)

        # Then apply mirroring to the rotated pattern
        complementary = self._apply_mirrored_transformation(rotated)

        logger.debug(
            f"Applied complementary transformation: {len(complementary)} beats"
        )
        return complementary

    def _rotate_position_180(self, position: str) -> str:
        """Rotate position 180 degrees."""
        # Simplified rotation mapping
        rotation_map = {
            "alpha1": "gamma5",
            "alpha3": "gamma7",
            "alpha5": "gamma1",
            "alpha7": "gamma3",
            "alpha2": "gamma6",
            "alpha4": "gamma8",
            "alpha6": "gamma2",
            "alpha8": "gamma4",
            "beta1": "beta5",
            "beta3": "beta7",
            "beta5": "beta1",
            "beta7": "beta3",
            "beta2": "beta6",
            "beta4": "beta8",
            "beta6": "beta2",
            "beta8": "beta4",
            "gamma1": "alpha5",
            "gamma3": "alpha7",
            "gamma5": "alpha1",
            "gamma7": "alpha3",
            "gamma2": "alpha6",
            "gamma4": "alpha8",
            "gamma6": "alpha2",
            "gamma8": "alpha4",
        }
        return rotation_map.get(position, position)

    def _mirror_position_horizontal(self, position: str) -> str:
        """Mirror position horizontally."""
        # Simplified mirror mapping
        mirror_map = {
            "alpha1": "alpha7",
            "alpha3": "alpha5",
            "alpha5": "alpha3",
            "alpha7": "alpha1",
            "alpha2": "alpha8",
            "alpha4": "alpha6",
            "alpha6": "alpha4",
            "alpha8": "alpha2",
            "beta1": "beta7",
            "beta3": "beta5",
            "beta5": "beta3",
            "beta7": "beta1",
            "beta2": "beta8",
            "beta4": "beta6",
            "beta6": "beta4",
            "beta8": "beta2",
            "gamma1": "gamma7",
            "gamma3": "gamma5",
            "gamma5": "gamma3",
            "gamma7": "gamma1",
            "gamma2": "gamma8",
            "gamma4": "gamma6",
            "gamma6": "gamma4",
            "gamma8": "gamma2",
        }
        return mirror_map.get(position, position)

    def _rotate_motions(self, motions: dict) -> dict:
        """Rotate motion data 180 degrees."""
        # Simplified - would need proper motion rotation logic
        return motions

    def _mirror_motions(self, motions: dict) -> dict:
        """Mirror motion data horizontally."""
        # Simplified - would need proper motion mirroring logic
        return motions

    def set_workbench_manager(self, workbench_manager) -> None:
        """Set the workbench manager for UI integration."""
        self.freeform_generator.set_workbench_manager(workbench_manager)
        logger.debug("Updated workbench manager for circular generation")
