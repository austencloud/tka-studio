"""
Letter Determination Service Interfaces

Defines the contracts for letter determination services using the existing modern architecture.
These interfaces work with the enhanced PictographData and MotionData models.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from desktop.modern.domain.models.enums import Letter
    from desktop.modern.domain.models.letter_determination.determination_models import (
        AttributeComparisonResult,
        LetterDeterminationResult,
        MotionComparisonContext,
    )
    from desktop.modern.domain.models.motion_data import MotionData
    from desktop.modern.domain.models.pictograph_data import PictographData


class ILetterDeterminationService(ABC):
    """
    Main interface for letter determination operations.

    This service coordinates the entire letter determination process,
    using strategies and comparison services to identify letters from motion data.
    """

    @abstractmethod
    def determine_letter(
        self,
        pictograph_data: PictographData,
        context: Optional[MotionComparisonContext] = None,
    ) -> LetterDeterminationResult:
        """
        Determine the letter for given pictograph motion data.

        Args:
            pictograph_data: The motion data to analyze
            context: Optional context for comparison behavior

        Returns:
            Result containing the determined letter and metadata
        """

    @abstractmethod
    def update_pictograph_dataset(
        self, dataset: dict[Letter, list[PictographData]]
    ) -> None:
        """
        Update the reference dataset used for letter matching.

        Args:
            dataset: Dictionary mapping letters to example pictographs
        """

    @abstractmethod
    def get_available_strategies(self) -> list[str]:
        """
        Get list of available determination strategies.

        Returns:
            List of strategy names
        """

    @abstractmethod
    def validate_pictograph_data(self, pictograph_data: PictographData) -> bool:
        """
        Validate that pictograph data is suitable for letter determination.

        Args:
            pictograph_data: The motion data to validate

        Returns:
            True if data is valid for determination
        """


class IMotionComparisonService(ABC):
    """
    Interface for comparing motion data between pictographs.

    Handles the low-level comparison logic including prefloat states,
    direction inversions, and other complex motion relationships.
    """

    @abstractmethod
    def compare_motions(
        self,
        motion1: PictographData,
        motion2: PictographData,
        context: Optional[MotionComparisonContext] = None,
    ) -> float:
        """
        Compare two complete motion pictographs.

        Args:
            motion1: First motion to compare
            motion2: Second motion to compare
            context: Optional comparison context

        Returns:
            Similarity score between 0.0 and 1.0
        """

    @abstractmethod
    def compare_attributes(
        self,
        attrs1: MotionData,
        attrs2: MotionData,
        context: Optional[MotionComparisonContext] = None,
    ) -> AttributeComparisonResult:
        """
        Compare motion attributes with detailed breakdown.

        Args:
            attrs1: First motion attributes
            attrs2: Second motion attributes
            context: Optional comparison context

        Returns:
            Detailed comparison result
        """

    @abstractmethod
    def reverse_prop_rot_dir(self, prop_rot_dir: str) -> str:
        """
        Reverse a prop rotation direction.

        Args:
            prop_rot_dir: Original rotation direction

        Returns:
            Reversed rotation direction
        """

    @abstractmethod
    def apply_direction_inversion(self, direction: str, prop_rot_dir: str) -> str:
        """
        Apply direction-based prop rotation inversion.

        Args:
            direction: Movement direction ('same' or 'opp')
            prop_rot_dir: Original prop rotation direction

        Returns:
            Potentially inverted prop rotation direction
        """


class ILetterDeterminationStrategy(ABC):
    """
    Interface for letter determination strategies.

    Each strategy handles a specific type of motion pattern
    (e.g., dual float, shift-float hybrid, etc.).
    """

    @abstractmethod
    def applies_to(self, motion_data: PictographData) -> bool:
        """
        Check if this strategy applies to the given motion data.

        Args:
            motion_data: The motion data to check

        Returns:
            True if this strategy should be used for the motion
        """

    @abstractmethod
    def execute(
        self,
        motion_data: PictographData,
        dataset: dict[Letter, list[PictographData]],
        comparison_service: IMotionComparisonService,
        context: Optional[MotionComparisonContext] = None,
    ) -> LetterDeterminationResult:
        """
        Execute the letter determination strategy.

        Args:
            motion_data: The motion data to analyze
            dataset: Reference dataset for comparison
            comparison_service: Service for motion comparison
            context: Optional comparison context

        Returns:
            Result of the determination attempt
        """

    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Get the name of this strategy.

        Returns:
            Strategy name for logging/debugging
        """


class IMotionAttributeService(ABC):
    """
    Interface for motion attribute processing and synchronization.

    Handles attribute updates, prefloat transformations, and validation.
    """

    @abstractmethod
    def sync_attributes(self, pictograph_data: PictographData) -> PictographData:
        """
        Synchronize and validate motion attributes.

        Args:
            pictograph_data: Motion data to synchronize

        Returns:
            Motion data with synchronized attributes
        """

    @abstractmethod
    def apply_prefloat_transformations(
        self, attributes: MotionData, reference_attributes: MotionData
    ) -> MotionData:
        """
        Apply prefloat motion transformations.

        Args:
            attributes: Attributes to transform
            reference_attributes: Reference for prefloat state

        Returns:
            Transformed attributes with prefloat information
        """

    @abstractmethod
    def validate_attribute_consistency(
        self, blue_attrs: MotionData, red_attrs: MotionData
    ) -> bool:
        """
        Validate consistency between blue and red attributes.

        Args:
            blue_attrs: Blue motion attributes
            red_attrs: Red motion attributes

        Returns:
            True if attributes are consistent
        """

    @abstractmethod
    def extract_prefloat_attributes(
        self, pictograph_data: PictographData
    ) -> dict[str, MotionData]:
        """
        Extract prefloat attributes from pictograph data.

        Args:
            pictograph_data: Motion data to analyze

        Returns:
            Dictionary of color -> prefloat attributes
        """


class IPictographDatasetProvider(ABC):
    """
    Interface for accessing pictograph reference datasets.

    Provides access to the pictograph examples used for letter matching.
    """

    @abstractmethod
    def get_pictograph_dataset(self) -> dict[Letter, list[PictographData]]:
        """
        Get the complete pictograph dataset for letter matching.

        Returns:
            Dictionary mapping letters to example pictographs
        """

    @abstractmethod
    def reload_dataset(self) -> None:
        """
        Reload dataset from storage.
        """

    @abstractmethod
    def get_dataset_metadata(self) -> dict[str, any]:
        """
        Get metadata about the current dataset.

        Returns:
            Dictionary containing dataset information
        """

    @abstractmethod
    def validate_dataset(self) -> bool:
        """
        Validate the current dataset integrity.

        Returns:
            True if dataset is valid and complete
        """
