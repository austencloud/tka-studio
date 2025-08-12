"""
Data Cache Manager - Unified caching for all data services

Centralizes cache management across the data services layer to eliminate
duplicate cache implementations and provide consistent cache behavior.
"""

import logging
from typing import Any

from desktop.modern.core.interfaces.data_services import IDataCacheManager

logger = logging.getLogger(__name__)


class DataCacheManager(IDataCacheManager):
    """
    Unified cache manager for all data service caching needs.

    Provides separate cache namespaces for different data types while
    maintaining a single interface and eviction policy.
    """

    def __init__(self, max_size: int = 100):
        """
        Initialize the cache manager.

        Args:
            max_size: Maximum number of items per cache namespace
        """
        self.max_size = max_size
        self._position_cache: dict[str, Any] = {}
        self._sequence_cache: dict[str, Any] = {}
        self._pictograph_cache: dict[str, Any] = {}
        self._conversion_cache: dict[str, Any] = {}

        # Track access order for LRU eviction
        self._position_access_order: list[str] = []
        self._sequence_access_order: list[str] = []
        self._pictograph_access_order: list[str] = []
        self._conversion_access_order: list[str] = []

        logger.info(f"DataCacheManager initialized with max_size={max_size}")

    def get_position_cache(self, key: str) -> Any | None:
        """Get item from position cache."""
        return self._get_from_cache(
            self._position_cache, self._position_access_order, key, "position"
        )

    def set_position_cache(self, key: str, value: Any) -> None:
        """Set item in position cache."""
        self._set_in_cache(
            self._position_cache, self._position_access_order, key, value, "position"
        )

    def get_sequence_cache(self, key: str) -> Any | None:
        """Get item from sequence cache."""
        return self._get_from_cache(
            self._sequence_cache, self._sequence_access_order, key, "sequence"
        )

    def set_sequence_cache(self, key: str, value: Any) -> None:
        """Set item in sequence cache."""
        self._set_in_cache(
            self._sequence_cache, self._sequence_access_order, key, value, "sequence"
        )

    def get_pictograph_cache(self, key: str) -> Any | None:
        """Get item from pictograph cache."""
        return self._get_from_cache(
            self._pictograph_cache, self._pictograph_access_order, key, "pictograph"
        )

    def set_pictograph_cache(self, key: str, value: Any) -> None:
        """Set item in pictograph cache."""
        self._set_in_cache(
            self._pictograph_cache,
            self._pictograph_access_order,
            key,
            value,
            "pictograph",
        )

    def get_conversion_cache(self, key: str) -> Any | None:
        """Get item from conversion cache."""
        return self._get_from_cache(
            self._conversion_cache, self._conversion_access_order, key, "conversion"
        )

    def set_conversion_cache(self, key: str, value: Any) -> None:
        """Set item in conversion cache."""
        self._set_in_cache(
            self._conversion_cache,
            self._conversion_access_order,
            key,
            value,
            "conversion",
        )

    def clear_all(self) -> None:
        """Clear all caches."""
        self._position_cache.clear()
        self._sequence_cache.clear()
        self._pictograph_cache.clear()
        self._conversion_cache.clear()

        self._position_access_order.clear()
        self._sequence_access_order.clear()
        self._pictograph_access_order.clear()
        self._conversion_access_order.clear()

        logger.info("All caches cleared")

    def clear_position_cache(self) -> None:
        """Clear only position cache."""
        self._position_cache.clear()
        self._position_access_order.clear()
        logger.info("Position cache cleared")

    def clear_sequence_cache(self) -> None:
        """Clear only sequence cache."""
        self._sequence_cache.clear()
        self._sequence_access_order.clear()
        logger.info("Sequence cache cleared")

    def clear_pictograph_cache(self) -> None:
        """Clear only pictograph cache."""
        self._pictograph_cache.clear()
        self._pictograph_access_order.clear()
        logger.info("Pictograph cache cleared")

    def clear_conversion_cache(self) -> None:
        """Clear only conversion cache."""
        self._conversion_cache.clear()
        self._conversion_access_order.clear()
        logger.info("Conversion cache cleared")

    def get_cache_stats(self) -> dict[str, Any]:
        """
        Return comprehensive cache statistics.

        Returns:
            Dictionary with cache sizes, hit rates, and other metrics
        """
        return {
            "position_cache_size": len(self._position_cache),
            "sequence_cache_size": len(self._sequence_cache),
            "pictograph_cache_size": len(self._pictograph_cache),
            "conversion_cache_size": len(self._conversion_cache),
            "total_items": (
                len(self._position_cache)
                + len(self._sequence_cache)
                + len(self._pictograph_cache)
                + len(self._conversion_cache)
            ),
            "max_size_per_cache": self.max_size,
            "position_keys": list(self._position_cache.keys()),
            "sequence_keys": list(self._sequence_cache.keys()),
            "pictograph_keys": list(self._pictograph_cache.keys()),
            "conversion_keys": list(self._conversion_cache.keys()),
        }

    def _get_from_cache(
        self, cache: dict[str, Any], access_order: list[str], key: str, cache_type: str
    ) -> Any | None:
        """Internal method to get from a specific cache with LRU tracking."""
        if key in cache:
            # Move to end of access order (most recently used)
            if key in access_order:
                access_order.remove(key)
            access_order.append(key)

            logger.debug(f"Cache hit for {cache_type}: {key}")
            return cache[key]

        logger.debug(f"Cache miss for {cache_type}: {key}")
        return None

    def _set_in_cache(
        self,
        cache: dict[str, Any],
        access_order: list[str],
        key: str,
        value: Any,
        cache_type: str,
    ) -> None:
        """Internal method to set in a specific cache with LRU eviction."""
        # If already exists, update and move to end
        if key in cache:
            cache[key] = value
            if key in access_order:
                access_order.remove(key)
            access_order.append(key)
            logger.debug(f"Updated {cache_type} cache: {key}")
            return

        # If at capacity, evict least recently used
        if len(cache) >= self.max_size:
            lru_key = access_order.pop(0)
            del cache[lru_key]
            logger.debug(f"Evicted LRU from {cache_type} cache: {lru_key}")

        # Add new item
        cache[key] = value
        access_order.append(key)
        logger.debug(f"Added to {cache_type} cache: {key}")
