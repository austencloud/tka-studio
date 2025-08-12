"""
Pictograph Data Service - Focused Pictograph CRUD Operations

Handles all core pictograph data operations including:
- Pictograph creation and manipulation
- Dataset management and querying
- Pictograph caching and indexing
- Category-based organization

This service provides a clean, focused interface for pictograph data operations
while maintaining the proven data management algorithms.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from desktop.modern.core.interfaces.pictograph_services import IPictographDataManager
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import GridMode
from desktop.modern.domain.models.grid_data import GridData
from desktop.modern.domain.models.pictograph_data import PictographData

from .cache_manager import DataCacheManager
from .dataset_query import IDatasetQuery

logger = logging.getLogger(__name__)


class PictographDataManager(IPictographDataManager):
    """
    Handles all core pictograph data operations.

    Provides a clean interface for creating, updating, and querying pictographs
    while maintaining efficient caching and indexing.
    """

    def __init__(self, cache_manager: DataCacheManager):
        self.cache_manager = cache_manager


class IPictographDataManager(ABC):
    """Interface for pictograph data operations."""

    @abstractmethod
    def create_pictograph(
        self, grid_mode: GridMode = GridMode.DIAMOND
    ) -> PictographData:
        """Create a new blank pictograph."""

    @abstractmethod
    def create_from_beat(self, beat_data: BeatData) -> PictographData:
        """Create pictograph from beat data."""


class PictographDataManager(IPictographDataManager):
    """
    Focused pictograph data service.

    Provides comprehensive pictograph data management including:
    - Pictograph creation and manipulation
    - Dataset management and querying
    - Pictograph caching and indexing
    - Category-based organization
    """

    def __init__(
        self,
        cache_manager: DataCacheManager = None,
        dataset_query: IDatasetQuery = None,
    ):
        # Use unified cache manager for pictograph caching
        self.cache_manager = cache_manager or DataCacheManager()
        self._dataset_index: dict[str, list[str]] = {}
        self._dataset_query = dataset_query
        self._pictograph_cache: dict[str, Any] = {}
        self._dataset_cache: dict[str, list[dict[str, Any]]] | None = None

    def create_pictograph(
        self, grid_mode: GridMode = GridMode.DIAMOND
    ) -> PictographData:
        """Create a new blank pictograph."""
        grid_data = GridData(
            grid_mode=grid_mode,
        )

        return PictographData(
            grid_data=grid_data,
            arrows={},
            props={},
            is_blank=True,
            metadata={"created_by": "pictograph_data_service"},
        )

    def create_from_beat(self, beat_data: BeatData) -> PictographData | None:
        """Get pictograph data from beat (returns embedded pictograph if available)."""
        if beat_data.has_pictograph:
            # Return the embedded pictograph data directly
            return beat_data.pictograph_data

        # Fallback: create empty pictograph for beats without embedded data
        return self.create_pictograph().update(
            is_blank=True,
            metadata={
                "created_from_beat": beat_data.beat_number,
                "letter": beat_data.letter or "?",
            },
        )

    def get_dataset_categories(self) -> list[str]:
        """Get all available dataset categories."""
        return list(self._dataset_index.keys())

    def get_pictographs_by_category(self, category: str) -> list[PictographData]:
        """Get all pictographs in a category."""
        pictograph_ids = self._dataset_index.get(category, [])
        return [
            self._pictograph_cache[pid]
            for pid in pictograph_ids
            if pid in self._pictograph_cache
        ]

    def get_pictograph_by_id(self, pictograph_id: str) -> PictographData | None:
        """Get pictograph by ID."""
        return self._pictograph_cache.get(pictograph_id)

    def remove_from_dataset(self, pictograph_id: str) -> bool:
        """Remove pictograph from dataset."""
        if pictograph_id not in self._pictograph_cache:
            return False

        # Remove from cache
        del self._pictograph_cache[pictograph_id]

        # Remove from all categories
        for category, ids in self._dataset_index.items():
            if pictograph_id in ids:
                ids.remove(pictograph_id)

        return True

    def get_dataset_stats(self) -> dict[str, Any]:
        """Get dataset statistics."""
        return {
            "total_pictographs": len(self._pictograph_cache),
            "categories": {
                category: len(ids) for category, ids in self._dataset_index.items()
            },
            "cache_size": len(self._pictograph_cache),
        }

    def clear_cache(self) -> None:
        """Clear the pictograph cache."""
        self._pictograph_cache.clear()
        self._dataset_index.clear()

    def get_pictograph_data(self, pictograph_id: str) -> PictographData | None:
        """
        Get pictograph data by ID.

        Args:
            pictograph_id: Unique identifier for pictograph

        Returns:
            PictographData object or None if not found
        """
        try:
            # Check cache first
            if pictograph_id in self._pictograph_cache:
                return self._pictograph_cache[pictograph_id]

            # If we have a dataset query service, try to get real data
            if self._dataset_query:
                # For Learn Tab, pictograph_id format is "letter_index" (e.g., "A_0", "B_1")
                if "_" in pictograph_id:
                    letter, index_str = pictograph_id.split("_", 1)
                    try:
                        index = int(index_str)
                        beat_data_list = self._dataset_query.find_pictographs_by_letter(
                            letter
                        )

                        if index < len(beat_data_list):
                            beat_data = beat_data_list[index]
                            if beat_data.has_pictograph:
                                pictograph_data = beat_data.pictograph_data
                                # Cache the result
                                self._pictograph_cache[pictograph_id] = pictograph_data
                                return pictograph_data
                    except (ValueError, IndexError):
                        pass

            # Fallback to cache lookup
            return self.get_pictograph_by_id(pictograph_id)

        except Exception as e:
            logger.error(f"Failed to get pictograph data for {pictograph_id}: {e}")
            return None

    def get_pictograph_dataset(self) -> dict[str, list[dict[str, Any]]]:
        """
        Get the complete pictograph dataset for question generation.

        Returns:
            Dictionary mapping letters to lists of pictograph data dictionaries
        """
        try:
            # Use cached dataset if available
            if self._dataset_cache is not None:
                return self._dataset_cache

            if not self._dataset_query:
                logger.warning(
                    "No dataset query service available - returning empty dataset"
                )
                return {}

            logger.info("Building pictograph dataset from TKA data...")

            # Get all available letters from the dataset
            available_letters = self._dataset_query.get_available_letters()
            logger.info(f"Found {len(available_letters)} letters in dataset")

            dataset = {}
            total_pictographs = 0

            for letter in available_letters:
                pictographs = self._get_pictographs_by_letter(letter)
                if pictographs:
                    dataset[letter] = pictographs
                    total_pictographs += len(pictographs)
                    logger.debug(f"Letter {letter}: {len(pictographs)} pictographs")

            logger.info(
                f"Built dataset with {len(dataset)} letters and {total_pictographs} total pictographs"
            )

            # Cache the result
            self._dataset_cache = dataset
            return dataset

        except Exception as e:
            logger.error(f"Failed to build pictograph dataset: {e}")
            # Return empty dataset to prevent crashes
            return {}

    def _get_pictographs_by_letter(self, letter: str) -> list[dict[str, Any]]:
        """
        Get pictographs for a specific letter.

        Args:
            letter: Letter to search for

        Returns:
            List of pictograph data dictionaries
        """
        try:
            if not self._dataset_query:
                return []

            beat_data_list = self._dataset_query.find_pictographs_by_letter(letter)

            pictographs = []
            for i, beat_data in enumerate(beat_data_list):
                if beat_data.has_pictograph:
                    pictograph_dict = {
                        "id": f"{letter}_{i}",
                        "letter": letter,
                        "type": "real",
                        "data": beat_data.pictograph_data,
                        "beat_data": beat_data,  # Include full beat data for rendering
                    }
                    pictographs.append(pictograph_dict)

            logger.debug(f"Found {len(pictographs)} pictographs for letter {letter}")
            return pictographs

        except Exception as e:
            logger.error(f"Failed to get pictographs for letter {letter}: {e}")
            return []

    # Private helper methods

    def _matches_query(self, pictograph: PictographData, query: dict[str, Any]) -> bool:
        """Check if pictograph matches search query."""
        # Letter matching
        if "letter" in query:
            letter = pictograph.metadata.get("letter", "").lower()
            query_letter = query["letter"].lower()
            if query_letter not in letter:
                return False

        # Motion type matching
        if "motion_type" in query:
            query_motion_type = query["motion_type"]
            has_matching_motion = False

            for arrow in pictograph.arrows.values():
                if (
                    arrow.motion_data
                    and arrow.motion_data.motion_type == query_motion_type
                ):
                    has_matching_motion = True
                    break

            if not has_matching_motion:
                return False

        # Start position matching
        if "start_position" in query:
            query_start_position = query["start_position"]
            has_matching_start = False

            for arrow in pictograph.arrows.values():
                if (
                    arrow.motion_data
                    and arrow.motion_data.start_loc == query_start_position
                ):
                    has_matching_start = True
                    break

            if not has_matching_start:
                return False

        return True
