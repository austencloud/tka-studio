"""
Sequence Card Cache Service Implementation

Multi-level LRU caching with memory management.
"""

import gc
import logging
from pathlib import Path
from typing import Optional

from desktop.modern.core.interfaces.sequence_card_services import (
    CacheLevel,
    CacheStats,
    ISequenceCardCacheService,
)

logger = logging.getLogger(__name__)


class LRUCache:
    """Least Recently Used cache implementation."""

    def __init__(self, max_size: int):
        self.max_size = max_size
        self.cache: dict[str, any] = {}
        self.access_order = []

    def get(self, key: str) -> Optional[any]:
        if key in self.cache:
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None

    def put(self, key: str, value: any) -> None:
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            oldest = self.access_order.pop(0)
            del self.cache[oldest]

        self.cache[key] = value
        self.access_order.append(key)

    def clear(self) -> None:
        self.cache.clear()
        self.access_order.clear()

    def size(self) -> int:
        return len(self.cache)


class SequenceCardCacheService(ISequenceCardCacheService):
    """Implementation of sequence card caching."""

    def __init__(self, max_raw_cache_size: int = 100, max_scaled_cache_size: int = 500):
        self.raw_cache = LRUCache(max_raw_cache_size)
        self.scaled_cache = LRUCache(max_scaled_cache_size)
        self.stats = CacheStats()
        self.memory_limit_mb = 500  # 500MB limit
        self._last_memory_check = 0
        self._memory_check_interval = 5.0  # Check memory every 5 seconds max

    def get_cached_image(self, path: Path, scale: float = 1.0) -> Optional[bytes]:
        """Get cached image data."""
        cache_key = self._get_cache_key(path, scale)

        if scale == 1.0:
            # Check raw cache
            result = self.raw_cache.get(cache_key)
            if result:
                self.stats.raw_cache_hits += 1
                return result
            else:
                self.stats.raw_cache_misses += 1
        else:
            # Check scaled cache
            result = self.scaled_cache.get(cache_key)
            if result:
                self.stats.scaled_cache_hits += 1
                return result
            else:
                self.stats.scaled_cache_misses += 1

        return None

    def cache_image(self, path: Path, image_data: bytes, scale: float = 1.0) -> None:
        """Cache image data."""
        cache_key = self._get_cache_key(path, scale)

        # Check memory usage periodically (not on every call)
        import time

        current_time = time.time()
        if current_time - self._last_memory_check > self._memory_check_interval:
            self._check_memory_usage()
            self._last_memory_check = current_time

        if scale == 1.0:
            self.raw_cache.put(cache_key, image_data)
        else:
            self.scaled_cache.put(cache_key, image_data)

    def clear_cache(self, cache_level: Optional[CacheLevel] = None) -> None:
        """Clear cache."""
        if cache_level is None:
            self.raw_cache.clear()
            self.scaled_cache.clear()
        elif cache_level == CacheLevel.RAW_IMAGE:
            self.raw_cache.clear()
        elif cache_level == CacheLevel.SCALED_IMAGE:
            self.scaled_cache.clear()

        # Reset stats
        self.stats = CacheStats()
        gc.collect()

    def get_cache_stats(self) -> CacheStats:
        """Get cache performance statistics."""
        self.stats.cache_size = self.raw_cache.size() + self.scaled_cache.size()
        self.stats.total_memory_usage = self._estimate_memory_usage()
        return self.stats

    def optimize_memory_usage(self) -> None:
        """Optimize memory usage."""
        try:
            import psutil

            current_memory = psutil.Process().memory_info().rss / 1024 / 1024

            if current_memory > self.memory_limit_mb:
                # Clear oldest entries first
                if self.scaled_cache.size() > 0:
                    # Clear 25% of scaled cache
                    clear_count = max(1, self.scaled_cache.size() // 4)
                    for _ in range(clear_count):
                        if self.scaled_cache.access_order:
                            oldest = self.scaled_cache.access_order.pop(0)
                            del self.scaled_cache.cache[oldest]

                gc.collect()
                logger.info(
                    f"Memory optimization: cleared cache entries, memory: {current_memory:.1f}MB"
                )
        except ImportError:
            # psutil not available, just do basic cleanup
            if self.scaled_cache.size() > 100:
                clear_count = 25
                for _ in range(clear_count):
                    if self.scaled_cache.access_order:
                        oldest = self.scaled_cache.access_order.pop(0)
                        del self.scaled_cache.cache[oldest]
            gc.collect()

    def _get_cache_key(self, path: Path, scale: float) -> str:
        """Generate cache key."""
        return f"{path}_{scale}"

    def _check_memory_usage(self) -> None:
        """Check and manage memory usage."""
        try:
            import psutil

            current_memory = psutil.Process().memory_info().rss / 1024 / 1024
            if current_memory > self.memory_limit_mb * 0.8:  # 80% threshold
                self.optimize_memory_usage()
        except ImportError:
            # Fallback without psutil - basic size-based cleanup
            total_cache_size = self.raw_cache.size() + self.scaled_cache.size()
            if total_cache_size > 400:  # Arbitrary threshold
                self.optimize_memory_usage()

    def _estimate_memory_usage(self) -> int:
        """Estimate current memory usage in bytes."""
        # Rough estimation - in real implementation would be more accurate
        return (
            (self.raw_cache.size() + self.scaled_cache.size()) * 1024 * 1024
        )  # 1MB per image estimate
