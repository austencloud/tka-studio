"""
Pictograph Dataset Provider Implementation

Provides access to pictograph reference datasets for letter determination.
Converts existing pictograph data to letter determination format.
"""

import logging

from desktop.modern.core.interfaces.letter_determination.letter_determination_services import (
    IPictographDatasetProvider,
)
from desktop.modern.domain.models.enums import Letter
from desktop.modern.domain.models.motion.letter_determination_pictograph_data import (
    LetterDeterminationPictographData,
)
from desktop.modern.domain.models.pictograph_data import PictographData

logger = logging.getLogger(__name__)


class PictographDatasetProvider(IPictographDatasetProvider):
    """
    Implementation of IPictographDatasetProvider that works with existing data sources.

    Converts existing pictograph data to letter determination format using
    the established PictographCSVManager and DatasetQuery services.
    """

    def __init__(self):
        """Initialize with dependency injection."""
        from desktop.modern.application.services.data.dataset_query import IDatasetQuery
        from desktop.modern.application.services.pictograph.pictograph_csv_manager import (
            IPictographCSVManager,
        )
        from desktop.modern.core.dependency_injection.di_container import get_container

        container = get_container()
        self._csv_manager = container.resolve(IPictographCSVManager)
        self._dataset_query = container.resolve(IDatasetQuery)

        self._cached_dataset: (
            dict[Letter, list[LetterDeterminationPictographData]] | None
        ) = None
        self._dataset_metadata: dict[str, any] = {}

    def get_pictograph_dataset(
        self,
    ) -> dict[Letter, list[PictographData]]:
        """
        Get the complete pictograph dataset for letter matching.

        Returns:
            Dictionary mapping letters to example pictographs
        """
        if self._cached_dataset is not None:
            return self._cached_dataset

        try:
            logger.info("Loading pictograph dataset for letter determination...")

            # Get available letters from dataset
            available_letters = self._dataset_query.get_available_letters()
            logger.info(f"Found {len(available_letters)} letters in dataset")

            dataset = {}
            total_pictographs = 0

            for letter_str in available_letters:
                try:
                    # Convert string to Letter enum
                    letter = Letter(letter_str)

                    # Get beat data for this letter
                    beat_data_list = self._dataset_query.find_pictographs_by_letter(
                        letter_str
                    )

                    # Convert to LetterDeterminationPictographData
                    letter_pictographs = []
                    for beat_data in beat_data_list:
                        if beat_data.has_pictograph:
                            try:
                                from dataclasses import replace

                                # Set letter determination fields directly on PictographData
                                letter_data = replace(
                                    beat_data.pictograph_data,
                                    beat=beat_data.beat_number,
                                    letter=letter.value,
                                    timing=getattr(beat_data, "timing", None),
                                    direction=getattr(beat_data, "direction", None),
                                )
                                letter_pictographs.append(letter_data)
                            except Exception as e:
                                logger.warning(
                                    f"Failed to process pictograph for letter {letter_str}: {e}"
                                )
                                continue

                    if letter_pictographs:
                        dataset[letter] = letter_pictographs
                        total_pictographs += len(letter_pictographs)
                        logger.debug(
                            f"Loaded {len(letter_pictographs)} pictographs for letter {letter_str}"
                        )

                except ValueError:
                    logger.warning(f"Unknown letter in dataset: {letter_str}")
                    continue
                except Exception as e:
                    logger.error(f"Error processing letter {letter_str}: {e}")
                    continue

            # Cache the dataset
            self._cached_dataset = dataset

            # Update metadata
            self._dataset_metadata = {
                "total_letters": len(dataset),
                "total_pictographs": total_pictographs,
                "letters": list(dataset.keys()),
                "source": "PictographCSVManager + DatasetQuery",
            }

            logger.info(
                f"Successfully loaded dataset: {total_pictographs} pictographs across {len(dataset)} letters"
            )
            return dataset

        except Exception as e:
            logger.error(f"Failed to load pictograph dataset: {e}")
            return {}

    def reload_dataset(self) -> None:
        """Reload dataset from storage."""
        logger.info("Reloading pictograph dataset...")
        self._cached_dataset = None
        self._dataset_metadata = {}

        # Force reload of underlying data
        try:
            self._csv_manager._csv_data = None  # Clear CSV cache
            self._dataset_query._cached_dataset = None  # Clear query cache if it exists
        except AttributeError:
            pass  # Cache attributes may not exist

        # Reload dataset
        self.get_pictograph_dataset()

    def get_dataset_metadata(self) -> dict[str, any]:
        """
        Get metadata about the current dataset.

        Returns:
            Dictionary containing dataset information
        """
        if not self._dataset_metadata:
            # Trigger dataset load to populate metadata
            self.get_pictograph_dataset()

        return self._dataset_metadata.copy()

    def validate_dataset(self) -> bool:
        """
        Validate the current dataset integrity.

        Returns:
            True if dataset is valid and complete
        """
        try:
            dataset = self.get_pictograph_dataset()

            if not dataset:
                logger.warning("Dataset is empty")
                return False

            # Check that we have data for common letters
            required_letters = [Letter.A, Letter.B, Letter.C]  # Basic validation
            for letter in required_letters:
                if letter not in dataset or not dataset[letter]:
                    logger.warning(f"Missing data for required letter: {letter}")
                    return False

            # Check that pictographs have valid data
            total_checked = 0
            for letter, pictographs in dataset.items():
                for pictograph in pictographs[:5]:  # Check first 5 of each letter
                    if not pictograph.pictograph_data:
                        logger.warning(f"Invalid pictograph data for letter {letter}")
                        return False
                    total_checked += 1

            logger.info(
                f"Dataset validation passed: {len(dataset)} letters, {total_checked} pictographs checked"
            )
            return True

        except Exception as e:
            logger.error(f"Dataset validation failed: {e}")
            return False
