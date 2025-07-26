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

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from desktop.modern.core.interfaces.pictograph_services import IPictographDataManager
from desktop.modern.domain.models.beat_data import BeatData
from desktop.modern.domain.models.enums import GridMode
from desktop.modern.domain.models.grid_data import GridData
from desktop.modern.domain.models.pictograph_data import PictographData

from .cache_manager import DataCacheManager


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

    def __init__(self, cache_manager: DataCacheManager = None):
        # Use unified cache manager for pictograph caching
        self.cache_manager = cache_manager or DataCacheManager()
        self._dataset_index: Dict[str, List[str]] = {}

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

    def create_from_beat(self, beat_data: BeatData) -> Optional[PictographData]:
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

    def get_dataset_categories(self) -> List[str]:
        """Get all available dataset categories."""
        return list(self._dataset_index.keys())

    def get_pictographs_by_category(self, category: str) -> List[PictographData]:
        """Get all pictographs in a category."""
        pictograph_ids = self._dataset_index.get(category, [])
        return [
            self._pictograph_cache[pid]
            for pid in pictograph_ids
            if pid in self._pictograph_cache
        ]

    def get_pictograph_by_id(self, pictograph_id: str) -> Optional[PictographData]:
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

    def get_dataset_stats(self) -> Dict[str, Any]:
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

    # Private helper methods

    def _matches_query(self, pictograph: PictographData, query: Dict[str, Any]) -> bool:
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
