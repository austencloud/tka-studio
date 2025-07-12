"""
Option data service for loading pictographs by letter type.

This service provides pictograph data for option picker sections,
filtering by letter types (Type1, Type2, etc.) and converting
between BeatData and PictographData as needed.
"""

import logging
from typing import List, Optional

from application.services.data.dataset_query import IDatasetQuery
from core.dependency_injection.di_container import DIContainer
from domain.models.beat_data import BeatData
from domain.models.pictograph_data import PictographData
from presentation.components.option_picker.types.letter_types import LetterType

logger = logging.getLogger(__name__)


class OptionDataService:
    """Service for loading pictograph data for option picker sections."""

    def __init__(self, container: DIContainer):
        """Initialize with dependency injection container."""
        self.container = container
        self._dataset_query_service: Optional[IDatasetQuery] = None

    @property
    def dataset_query_service(self) -> IDatasetQuery:
        """Lazy-loaded dataset query service."""
        if self._dataset_query_service is None:
            try:
                self._dataset_query_service = self.container.resolve(IDatasetQuery)
            except Exception as e:
                logger.warning(f"Failed to resolve DatasetQuery: {e}")
                # For testing/fallback, return None and handle in _get_pictographs_for_letter
                return None
        return self._dataset_query_service

    def get_pictographs_for_letter_type(
        self, letter_type: str, max_count: int = 12
    ) -> List[PictographData]:
        """
        Get pictographs for a specific letter type.

        Args:
            letter_type: Letter type (Type1, Type2, etc.)
            max_count: Maximum number of pictographs to return

        Returns:
            List of PictographData objects for the letter type
        """
        try:
            # Get letters for this type
            letters = self._get_letters_for_type(letter_type)
            if not letters:
                logger.warning(f"No letters found for letter type: {letter_type}")
                return []

            pictographs = []
            per_letter_count = max(1, max_count // len(letters))

            # Get pictographs for each letter in this type
            for letter in letters:
                letter_pictographs = self._get_pictographs_for_letter(
                    letter, per_letter_count
                )
                pictographs.extend(letter_pictographs)

                # Stop if we have enough
                if len(pictographs) >= max_count:
                    break

            # Trim to exact count
            return pictographs[:max_count]

        except Exception as e:
            logger.error(
                f"Error getting pictographs for letter type {letter_type}: {e}"
            )
            return []

    def _get_letters_for_type(self, letter_type: str) -> List[str]:
        """Get the letters that belong to a specific letter type."""
        letter_mappings = {
            LetterType.TYPE1: [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "J",
                "K",
                "L",
                "M",
                "N",
                "O",
                "P",
                "Q",
                "R",
                "S",
                "T",
                "U",
                "V",
            ],
            LetterType.TYPE2: ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"],
            LetterType.TYPE3: ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"],
            LetterType.TYPE4: ["Φ", "Ψ", "Λ"],
            LetterType.TYPE5: ["Φ-", "Ψ-", "Λ-"],
            LetterType.TYPE6: ["α", "β", "Γ"],
        }
        return letter_mappings.get(letter_type, [])

    def _get_pictographs_for_letter(
        self, letter: str, max_count: int
    ) -> List[PictographData]:
        """Get pictographs for a specific letter."""
        try:
            # Get beat data from dataset
            beat_data_list = self.dataset_query_service.find_pictographs_by_letter(
                letter, grid_mode="diamond"
            )

            # Convert to PictographData
            pictographs = []
            for beat_data in beat_data_list[:max_count]:
                if beat_data.has_pictograph:
                    pictographs.append(beat_data.pictograph_data)

            return pictographs

        except Exception as e:
            logger.error(f"Error getting pictographs for letter {letter}: {e}")
            # For testing/fallback, create mock pictographs
            return self._create_mock_pictographs(letter, max_count)

    def _create_mock_pictographs(self, letter: str, count: int) -> List[PictographData]:
        """Create mock pictographs for testing when real data is not available."""
        from domain.models.grid_data import GridData

        mock_pictographs = []
        for i in range(count):
            # Create a simple mock pictograph
            mock_pictograph = PictographData(
                letter=letter,
                grid_data=GridData(),
                arrows={},
                props={},
                motions={},
                metadata={"mock": True, "index": i},
            )
            mock_pictographs.append(mock_pictograph)

        logger.info(
            f"Created {len(mock_pictographs)} mock pictographs for letter {letter}"
        )
        return mock_pictographs

    def get_total_available_pictographs(self) -> int:
        """Get total count of available pictographs across all types."""
        total = 0
        for letter_type in LetterType.ALL_TYPES:
            letters = self._get_letters_for_type(letter_type)
            for letter in letters:
                try:
                    beat_data_list = (
                        self.dataset_query_service.find_pictographs_by_letter(
                            letter, grid_mode="diamond"
                        )
                    )
                    total += len(beat_data_list)
                except Exception:
                    continue
        return total
