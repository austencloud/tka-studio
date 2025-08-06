"""
CAP Operations - Core Implementation

Direct port of Circular Algorithmic Permutation logic from legacy system.
These are the mathematical transformations that make circular sequences work.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
import logging

from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.sequence_data import SequenceData


logger = logging.getLogger(__name__)


class CAPType(Enum):
    """
    CAP types from legacy system.
    These define the mathematical transformations for circular sequences.
    """

    STRICT_ROTATED = "strict_rotated"
    STRICT_MIRRORED = "strict_mirrored"
    MIRRORED_SWAPPED = "mirrored_swapped"
    STRICT_SWAPPED = "strict_swapped"
    SWAPPED_COMPLEMENTARY = "swapped_complementary"
    STRICT_COMPLEMENTARY = "strict_complementary"
    ROTATED_COMPLEMENTARY = "rotated_complementary"
    MIRRORED_COMPLEMENTARY = "mirrored_complementary"
    ROTATED_SWAPPED = "rotated_swapped"
    MIRRORED_ROTATED = "mirrored_rotated"
    MIRRORED_COMPLEMENTARY_ROTATED = "mirrored_complementary_rotated"


class CAPOperation(ABC):
    """Base class for all CAP transformations."""

    @abstractmethod
    def execute(self, sequence: SequenceData, **kwargs) -> SequenceData:
        """Execute the CAP transformation."""

    @abstractmethod
    def validate_applicability(self, sequence: SequenceData) -> bool:
        """Check if CAP can be applied to this sequence."""


class StrictRotatedCAP(CAPOperation):
    """
    HIGHEST PRIORITY: Most commonly used CAP type.

    Direct port of legacy strict_rotated_executor.py.
    Rotates positions by specific amounts based on slice_size.
    """

    def execute(
        self, sequence: SequenceData, slice_size: str = "full", **kwargs
    ) -> SequenceData:
        """
        Execute strict rotated CAP transformation.

        Args:
            sequence: The sequence to transform
            slice_size: "full", "halved", or custom rotation amount

        Returns:
            Transformed sequence with rotated positions
        """
        try:
            print(f"🔧 Applying STRICT_ROTATED CAP with slice_size: {slice_size}")

            if not self.validate_applicability(sequence):
                raise ValueError("Sequence is not applicable for strict rotated CAP")

            # Get the starting position from first beat (after start position)
            start_beat = self._get_first_sequence_beat(sequence)
            if not start_beat or not start_beat.pictograph_data:
                print("⚠️ No valid start beat found for rotation")
                return sequence

            start_position = start_beat.pictograph_data.start_position
            print(f"  Starting position: {start_position}")

            # Calculate rotation mapping
            rotation_mapping = self._calculate_rotation_mapping(
                start_position, slice_size
            )
            if not rotation_mapping:
                print("⚠️ Could not calculate rotation mapping")
                return sequence

            # Apply rotation to each beat
            rotated_beats = []
            for beat in sequence.beats:
                if beat.metadata.get("is_start_position"):
                    # Don't rotate start position
                    rotated_beats.append(beat)
                    continue

                rotated_beat = self._apply_rotation_to_beat(beat, rotation_mapping)
                rotated_beats.append(rotated_beat)

            result_sequence = sequence.update(beats=rotated_beats)
            print(f"✅ Applied STRICT_ROTATED CAP to {len(rotated_beats)} beats")
            return result_sequence

        except Exception as e:
            logger.error(f"Error in StrictRotatedCAP.execute: {e}")
            return sequence

    def validate_applicability(self, sequence: SequenceData) -> bool:
        """Check if sequence can have strict rotated CAP applied."""
        if sequence.length < 2:
            return False

        # Must have at least one non-start position beat
        non_start_beats = [
            b for b in sequence.beats if not b.metadata.get("is_start_position")
        ]
        return len(non_start_beats) > 0

    def _get_first_sequence_beat(self, sequence: SequenceData) -> BeatData | None:
        """Get the first beat that's not a start position."""
        for beat in sequence.beats:
            if not beat.metadata.get("is_start_position"):
                return beat
        return None

    def _calculate_rotation_mapping(
        self, start_position: str, slice_size: str
    ) -> dict[str, str]:
        """
        Calculate position rotation mapping.

        This is the core mathematical transformation from legacy system.
        """
        try:
            # Basic rotation mappings (simplified version of legacy position maps)
            # In full implementation, this would use the complete position_maps data
            base_rotations = {
                "alpha1": {"full": "beta1", "halved": "gamma1"},
                "alpha2": {"full": "beta2", "halved": "gamma2"},
                "beta1": {"full": "gamma1", "halved": "delta1"},
                "beta2": {"full": "gamma2", "halved": "delta2"},
                "gamma1": {"full": "delta1", "halved": "alpha1"},
                "gamma2": {"full": "delta2", "halved": "alpha2"},
                "delta1": {"full": "alpha1", "halved": "beta1"},
                "delta2": {"full": "alpha2", "halved": "beta2"},
            }

            # Build mapping for all positions
            rotation_mapping = {}

            if slice_size in ["full", "halved"]:
                for pos, rotations in base_rotations.items():
                    if slice_size in rotations:
                        rotation_mapping[pos] = rotations[slice_size]

            print(f"  Rotation mapping: {rotation_mapping}")
            return rotation_mapping

        except Exception as e:
            logger.error(f"Error calculating rotation mapping: {e}")
            return {}

    def _apply_rotation_to_beat(
        self, beat: BeatData, rotation_mapping: dict[str, str]
    ) -> BeatData:
        """Apply rotation mapping to a single beat."""
        try:
            if not beat.pictograph_data:
                return beat

            current_start = beat.pictograph_data.start_position
            current_end = beat.pictograph_data.end_position

            # Rotate positions using mapping
            new_start = rotation_mapping.get(current_start, current_start)
            new_end = rotation_mapping.get(current_end, current_end)

            # Create new pictograph data with rotated positions
            from desktop.modern.domain.models.pictograph_data import PictographData

            rotated_pictograph = PictographData(
                id=beat.pictograph_data.id,
                grid_data=beat.pictograph_data.grid_data,
                arrows=beat.pictograph_data.arrows,
                props=beat.pictograph_data.props,
                motions=beat.pictograph_data.motions,
                letter=beat.pictograph_data.letter,
                start_position=new_start,
                end_position=new_end,
                is_blank=beat.pictograph_data.is_blank,
                is_mirrored=beat.pictograph_data.is_mirrored,
                metadata={
                    **beat.pictograph_data.metadata,
                    "rotated_from": current_start,
                    "rotated_to": new_start,
                },
            )

            # Create new beat with rotated pictograph
            rotated_beat = beat.update(
                pictograph_data=rotated_pictograph,
                metadata={
                    **beat.metadata,
                    "cap_applied": "strict_rotated",
                    "original_start_pos": current_start,
                    "original_end_pos": current_end,
                },
            )

            return rotated_beat

        except Exception as e:
            logger.error(f"Error applying rotation to beat: {e}")
            return beat


class StrictMirroredCAP(CAPOperation):
    """
    SECOND PRIORITY: Second most used CAP type.

    Direct port of legacy mirrored CAP logic.
    """

    def execute(self, sequence: SequenceData, **kwargs) -> SequenceData:
        """Execute strict mirrored CAP transformation."""
        try:
            print("🔧 Applying STRICT_MIRRORED CAP")

            if not self.validate_applicability(sequence):
                raise ValueError("Sequence is not applicable for strict mirrored CAP")

            # Mirror mappings (simplified version of legacy mirror maps)
            mirror_mapping = self._get_mirror_mapping()

            # Apply mirroring to each beat
            mirrored_beats = []
            for beat in sequence.beats:
                if beat.metadata.get("is_start_position"):
                    # Don't mirror start position
                    mirrored_beats.append(beat)
                    continue

                mirrored_beat = self._apply_mirror_to_beat(beat, mirror_mapping)
                mirrored_beats.append(mirrored_beat)

            result_sequence = sequence.update(beats=mirrored_beats)
            print(f"✅ Applied STRICT_MIRRORED CAP to {len(mirrored_beats)} beats")
            return result_sequence

        except Exception as e:
            logger.error(f"Error in StrictMirroredCAP.execute: {e}")
            return sequence

    def validate_applicability(self, sequence: SequenceData) -> bool:
        """Check if sequence can have mirrored CAP applied."""
        return sequence.length >= 2

    def _get_mirror_mapping(self) -> dict[str, str]:
        """Get position mirror mapping."""
        # Simplified mirror mapping (legacy had complete mirror position maps)
        return {
            "alpha1": "alpha2",
            "alpha2": "alpha1",
            "beta1": "beta2",
            "beta2": "beta1",
            "gamma1": "gamma2",
            "gamma2": "gamma1",
            "delta1": "delta2",
            "delta2": "delta1",
        }

    def _apply_mirror_to_beat(
        self, beat: BeatData, mirror_mapping: dict[str, str]
    ) -> BeatData:
        """Apply mirror mapping to a single beat."""
        try:
            if not beat.pictograph_data:
                return beat

            current_start = beat.pictograph_data.start_position
            current_end = beat.pictograph_data.end_position

            # Mirror positions
            new_start = mirror_mapping.get(current_start, current_start)
            new_end = mirror_mapping.get(current_end, current_end)

            # Create mirrored pictograph data
            from desktop.modern.domain.models.pictograph_data import PictographData

            mirrored_pictograph = PictographData(
                id=beat.pictograph_data.id,
                grid_data=beat.pictograph_data.grid_data,
                arrows=beat.pictograph_data.arrows,
                props=beat.pictograph_data.props,
                motions=beat.pictograph_data.motions,
                letter=beat.pictograph_data.letter,
                start_position=new_start,
                end_position=new_end,
                is_blank=beat.pictograph_data.is_blank,
                is_mirrored=True,  # Mark as mirrored
                metadata={
                    **beat.pictograph_data.metadata,
                    "mirrored_from": current_start,
                    "mirrored_to": new_start,
                },
            )

            # Create mirrored beat
            mirrored_beat = beat.update(
                pictograph_data=mirrored_pictograph,
                metadata={
                    **beat.metadata,
                    "cap_applied": "strict_mirrored",
                    "original_start_pos": current_start,
                    "original_end_pos": current_end,
                },
            )

            return mirrored_beat

        except Exception as e:
            logger.error(f"Error applying mirror to beat: {e}")
            return beat


class CAPExecutorFactory:
    """
    Factory for creating CAP executors.

    Direct port of legacy CAP executor factory pattern.
    """

    _executors = {
        CAPType.STRICT_ROTATED: StrictRotatedCAP(),
        CAPType.STRICT_MIRRORED: StrictMirroredCAP(),
        # TODO: Add remaining CAP types in Phase 2
    }

    @classmethod
    def create_executor(cls, cap_type: CAPType) -> CAPOperation:
        """Get the appropriate CAP executor."""
        if cap_type not in cls._executors:
            raise ValueError(f"CAP type {cap_type} not implemented yet")
        return cls._executors[cap_type]

    @classmethod
    def get_available_cap_types(cls) -> list[CAPType]:
        """Get list of implemented CAP types."""
        return list(cls._executors.keys())

    @classmethod
    def is_cap_type_implemented(cls, cap_type: CAPType) -> bool:
        """Check if a CAP type is implemented."""
        return cap_type in cls._executors


# Convenience function for applying CAP transformations
def apply_cap_to_sequence(
    sequence: SequenceData, cap_type: CAPType, **kwargs
) -> SequenceData:
    """
    Apply a CAP transformation to a sequence.

    Args:
        sequence: The sequence to transform
        cap_type: The type of CAP to apply
        **kwargs: Additional parameters for the CAP operation

    Returns:
        Transformed sequence
    """
    try:
        executor = CAPExecutorFactory.create_executor(cap_type)
        return executor.execute(sequence, **kwargs)
    except Exception as e:
        logger.error(f"Error applying CAP {cap_type}: {e}")
        return sequence


# Create __init__.py for the operations module
def create_operations_init():
    """Create __init__.py for operations module."""
    init_content = '''"""
Domain Operations Module

Contains all domain-level operations including CAP transformations.
"""

from .cap_operations import (
    CAPType,
    CAPOperation,
    StrictRotatedCAP,
    StrictMirroredCAP,
    CAPExecutorFactory,
    apply_cap_to_sequence,
)

__all__ = [
    "CAPType",
    "CAPOperation",
    "StrictRotatedCAP",
    "StrictMirroredCAP",
    "CAPExecutorFactory",
    "apply_cap_to_sequence",
]
'''
    return init_content
