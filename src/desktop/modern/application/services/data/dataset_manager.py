"""
Dataset Management Service

Pure service for managing pictograph datasets and caching.
Extracted from PictographManagementService to follow single responsibility principle.

PROVIDES:
- In-memory dataset caching
- Category-based organization
- Search and filtering operations
- Dataset indexing
"""

import uuid
from typing import Any

from desktop.modern.application.services.pictograph.pictograph_csv_manager import (
    PictographSearchQuery,
)
from desktop.modern.core.interfaces.data_services import IDatasetManager
from desktop.modern.domain.models.pictograph_data import PictographData

from .cache_manager import DataCacheManager


class DatasetManager(IDatasetManager):
    """
    Pure service for dataset management operations.

    Handles in-memory caching and organization without external dependencies.
    Uses immutable data patterns following TKA architecture.
    """

    def __init__(self, cache_manager: DataCacheManager = None):
        """Initialize dataset management service with unified cache."""
        # Use unified cache manager for pictograph caching
        self.cache_manager = cache_manager or DataCacheManager()
        self._dataset_index: dict[str, list[str]] = {}

    def add_to_dataset(
        self, pictograph: PictographData, category: str = "user_created"
    ) -> str:
        """Add pictograph to dataset."""
        pictograph_id = str(uuid.uuid4())

        # Cache the pictograph
        self.cache_manager.set_pictograph_cache(pictograph_id, pictograph)

        # Update dataset index
        if category not in self._dataset_index:
            self._dataset_index[category] = []
        self._dataset_index[category].append(pictograph_id)

        return pictograph_id

    def search_dataset(self, query: PictographSearchQuery) -> list[PictographData]:
        """Search pictograph dataset with query."""
        results = []

        # Extract search criteria with proper type handling
        max_results = query.get("max_results", 50)
        if max_results is None:
            max_results = 50

        # Search through cached pictographs
        # Note: We need to iterate through dataset index since cache manager doesn't expose iteration
        for category, pictograph_ids in self._dataset_index.items():
            for pictograph_id in pictograph_ids:
                pictograph = self.cache_manager.get_pictograph_cache(pictograph_id)
                if pictograph and self._matches_query(pictograph, query):
                    results.append(pictograph)

                    if len(results) >= max_results:
                        break

            if len(results) >= max_results:
                break

        return results

    def get_dataset_categories(self) -> list[str]:
        """Get all available dataset categories."""
        return list(self._dataset_index.keys())

    def get_pictographs_by_category(self, category: str) -> list[PictographData]:
        """Get all pictographs in a category."""
        pictograph_ids = self._dataset_index.get(category, [])
        results = []
        for pid in pictograph_ids:
            pictograph = self.cache_manager.get_pictograph_cache(pid)
            if pictograph:
                results.append(pictograph)
        return results

    def get_pictograph_by_id(self, pictograph_id: str) -> PictographData | None:
        """Get pictograph by ID."""
        return self.cache_manager.get_pictograph_cache(pictograph_id)

    def remove_from_dataset(self, pictograph_id: str) -> bool:
        """Remove pictograph from dataset."""
        # Check if pictograph exists in cache
        if not self.cache_manager.get_pictograph_cache(pictograph_id):
            return False

        # Remove from cache (cache manager handles this internally)
        # Note: DataCacheManager doesn't have a remove method, so we'll need to clear and rebuild
        # For now, we'll just remove from index and let cache expire naturally

        # Remove from all category indices
        for ids in self._dataset_index.values():
            if pictograph_id in ids:
                ids.remove(pictograph_id)

        return True

    def update_pictograph(
        self, pictograph_id: str, updated_pictograph: PictographData
    ) -> bool:
        """Update pictograph in dataset."""
        if not self.cache_manager.get_pictograph_cache(pictograph_id):
            return False

        self.cache_manager.set_pictograph_cache(pictograph_id, updated_pictograph)
        return True

    def clear_dataset(self) -> None:
        """Clear all dataset data."""
        self.cache_manager.clear_pictograph_cache()
        self._dataset_index.clear()

    def get_dataset_stats(self) -> dict[str, Any]:
        """Get dataset statistics."""
        # Count total pictographs from index
        total_pictographs = sum(len(ids) for ids in self._dataset_index.values())
        categories = self.get_dataset_categories()

        category_counts = {
            category: len(self._dataset_index[category]) for category in categories
        }

        return {
            "total_pictographs": total_pictographs,
            "total_categories": len(categories),
            "categories": categories,
            "category_counts": category_counts,
        }

    def _matches_query(
        self, pictograph: PictographData, query: PictographSearchQuery
    ) -> bool:
        """Check if pictograph matches search query."""
        # Letter matching
        if "letter" in query and query["letter"]:
            letter = pictograph.metadata.get("letter", "").lower()
            query_letter = query["letter"].lower()
            if query_letter not in letter:
                return False

        # Motion type matching
        if "motion_type" in query and query["motion_type"]:
            query_motion_type = query["motion_type"]
            has_matching_motion = False

            for motion in pictograph.motions.values():
                if motion and motion.motion_type.value == query_motion_type:
                    has_matching_motion = True
                    break

            if not has_matching_motion:
                return False

        # Start position matching
        if "start_position" in query and query["start_position"]:
            start_position = pictograph.start_position
            if not start_position or query["start_position"] not in start_position:
                return False

        # Category matching
        if "categories" in query and query["categories"]:
            pictograph_categories = pictograph.metadata.get("categories", [])
            if not any(cat in pictograph_categories for cat in query["categories"]):
                return False

        return True
