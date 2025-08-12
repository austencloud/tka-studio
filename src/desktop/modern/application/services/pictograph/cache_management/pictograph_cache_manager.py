"""
Cache management microservice for pictograph rendering.

This service handles:
- QSvgRenderer caching with memory management
- SVG data caching
- Cache eviction strategies
- Memory usage monitoring
- Cache performance statistics
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtSvg import QSvgRenderer

from desktop.modern.core.interfaces.pictograph_rendering_services import (
    IPictographCacheManager,
)


logger = logging.getLogger(__name__)


class PictographCacheManager(IPictographCacheManager):
    """
    Microservice for managing pictograph rendering caches.

    Provides:
    - QSvgRenderer caching with LRU eviction
    - SVG data caching
    - Memory usage monitoring
    - Cache performance statistics
    - Configurable cache limits
    """

    def __init__(
        self, max_renderers: int = 50, max_svg_data: int = 100, max_memory_mb: int = 50
    ):
        """Initialize the cache manager with configurable limits."""
        # Cache configuration
        self._config = {
            "max_renderers": max_renderers,
            "max_svg_data": max_svg_data,
            "max_memory_mb": max_memory_mb,
        }

        # Renderer caches by category
        self._grid_renderer_cache: dict[str, QSvgRenderer] = {}
        self._prop_renderer_cache: dict[str, QSvgRenderer] = {}
        self._glyph_renderer_cache: dict[str, QSvgRenderer] = {}
        self._arrow_renderer_cache: dict[str, QSvgRenderer] = {}

        # SVG data cache
        self._svg_data_cache: dict[str, str] = {}

        # Access tracking for LRU eviction
        self._renderer_access_order: list[str] = []
        self._svg_access_order: list[str] = []

        # Performance statistics
        self._stats = {
            "cache_hits": 0,
            "cache_misses": 0,
            "renderers_created": 0,
            "evictions_performed": 0,
            "memory_warnings": 0,
        }

    def get_renderer(self, cache_key: str) -> QSvgRenderer | None:
        """Get cached renderer by key."""
        # Check all renderer caches
        for cache in [
            self._grid_renderer_cache,
            self._prop_renderer_cache,
            self._glyph_renderer_cache,
            self._arrow_renderer_cache,
        ]:
            if cache_key in cache:
                self._stats["cache_hits"] += 1
                self._update_renderer_access(cache_key)
                return cache[cache_key]

        self._stats["cache_misses"] += 1
        return None

    def store_renderer(self, cache_key: str, renderer: QSvgRenderer) -> None:
        """Store renderer in appropriate cache based on key prefix."""
        if not renderer or not renderer.isValid():
            logger.warning(
                f"⚠️ [CACHE_MANAGER] Attempted to cache invalid renderer: {cache_key}"
            )
            return

        # Determine cache based on key prefix
        if cache_key.startswith("grid_"):
            target_cache = self._grid_renderer_cache
        elif cache_key.startswith("staff_") or cache_key.startswith("prop_"):
            target_cache = self._prop_renderer_cache
        elif cache_key.startswith("glyph_"):
            target_cache = self._glyph_renderer_cache
        elif cache_key.startswith("arrow_"):
            target_cache = self._arrow_renderer_cache
        else:
            logger.warning(f"⚠️ [CACHE_MANAGER] Unknown cache key prefix: {cache_key}")
            target_cache = self._prop_renderer_cache  # Default fallback

        # Check if we need to evict before storing
        total_renderers = sum(
            len(cache)
            for cache in [
                self._grid_renderer_cache,
                self._prop_renderer_cache,
                self._glyph_renderer_cache,
                self._arrow_renderer_cache,
            ]
        )

        if total_renderers >= self._config["max_renderers"]:
            self._evict_least_used_renderer()

        target_cache[cache_key] = renderer
        self._update_renderer_access(cache_key)
        self._stats["renderers_created"] += 1

        logger.debug(f"🗄️ [CACHE_MANAGER] Cached renderer: {cache_key}")

    def get_svg_data(self, cache_key: str) -> str | None:
        """Get cached SVG data by key."""
        if cache_key in self._svg_data_cache:
            self._stats["cache_hits"] += 1
            self._update_svg_access(cache_key)
            return self._svg_data_cache[cache_key]

        self._stats["cache_misses"] += 1
        return None

    def store_svg_data(self, cache_key: str, svg_data: str) -> None:
        """Store SVG data in cache."""
        if len(self._svg_data_cache) >= self._config["max_svg_data"]:
            self._evict_least_used_svg()

        self._svg_data_cache[cache_key] = svg_data
        self._update_svg_access(cache_key)

        logger.debug(f"🗄️ [CACHE_MANAGER] Cached SVG data: {cache_key}")

    def evict_least_used(self) -> None:
        """Evict least recently used items from all caches."""
        self._evict_least_used_renderer()
        self._evict_least_used_svg()

    def _evict_least_used_renderer(self) -> None:
        """Evict the least recently used renderer."""
        if not self._renderer_access_order:
            return

        # Find the oldest accessed renderer that still exists
        for cache_key in self._renderer_access_order:
            for cache in [
                self._grid_renderer_cache,
                self._prop_renderer_cache,
                self._glyph_renderer_cache,
                self._arrow_renderer_cache,
            ]:
                if cache_key in cache:
                    del cache[cache_key]
                    self._renderer_access_order.remove(cache_key)
                    self._stats["evictions_performed"] += 1
                    logger.debug(f"🗑️ [CACHE_MANAGER] Evicted renderer: {cache_key}")
                    return

    def _evict_least_used_svg(self) -> None:
        """Evict the least recently used SVG data."""
        if not self._svg_access_order:
            return

        cache_key = self._svg_access_order.pop(0)
        if cache_key in self._svg_data_cache:
            del self._svg_data_cache[cache_key]
            self._stats["evictions_performed"] += 1
            logger.debug(f"🗑️ [CACHE_MANAGER] Evicted SVG data: {cache_key}")

    def _update_renderer_access(self, cache_key: str) -> None:
        """Update renderer access order for LRU tracking."""
        if cache_key in self._renderer_access_order:
            self._renderer_access_order.remove(cache_key)
        self._renderer_access_order.append(cache_key)

    def _update_svg_access(self, cache_key: str) -> None:
        """Update SVG access order for LRU tracking."""
        if cache_key in self._svg_access_order:
            self._svg_access_order.remove(cache_key)
        self._svg_access_order.append(cache_key)

    def get_memory_usage(self) -> int:
        """Get estimated memory usage in bytes."""
        # Rough estimation based on cache sizes
        renderer_memory = (
            sum(
                len(cache)
                for cache in [
                    self._grid_renderer_cache,
                    self._prop_renderer_cache,
                    self._glyph_renderer_cache,
                    self._arrow_renderer_cache,
                ]
            )
            * 1024
        )  # Estimate 1KB per renderer

        svg_memory = sum(len(svg_data) for svg_data in self._svg_data_cache.values())

        total_memory = renderer_memory + svg_memory

        # Check if we're approaching memory limits
        max_memory_bytes = self._config["max_memory_mb"] * 1024 * 1024
        if total_memory > max_memory_bytes * 0.8:  # 80% threshold
            self._stats["memory_warnings"] += 1
            logger.warning(
                f"⚠️ [CACHE_MANAGER] Memory usage approaching limit: {total_memory / 1024 / 1024:.1f}MB"
            )

        return total_memory

    def clear_all_caches(self) -> None:
        """Clear all caches."""
        self._grid_renderer_cache.clear()
        self._prop_renderer_cache.clear()
        self._glyph_renderer_cache.clear()
        self._arrow_renderer_cache.clear()
        self._svg_data_cache.clear()
        self._renderer_access_order.clear()
        self._svg_access_order.clear()

        # Reset stats
        self._stats = {
            "cache_hits": 0,
            "cache_misses": 0,
            "renderers_created": 0,
            "evictions_performed": 0,
            "memory_warnings": 0,
        }

        logger.info("🧹 [CACHE_MANAGER] Cleared all caches")

    def get_cache_stats(self) -> dict[str, Any]:
        """Get comprehensive cache statistics."""
        total_requests = self._stats["cache_hits"] + self._stats["cache_misses"]
        hit_rate = (
            (self._stats["cache_hits"] / total_requests * 100)
            if total_requests > 0
            else 0
        )

        return {
            "cache_hits": self._stats["cache_hits"],
            "cache_misses": self._stats["cache_misses"],
            "hit_rate_percent": round(hit_rate, 2),
            "renderers_created": self._stats["renderers_created"],
            "evictions_performed": self._stats["evictions_performed"],
            "memory_warnings": self._stats["memory_warnings"],
            "grid_renderers_cached": len(self._grid_renderer_cache),
            "prop_renderers_cached": len(self._prop_renderer_cache),
            "glyph_renderers_cached": len(self._glyph_renderer_cache),
            "arrow_renderers_cached": len(self._arrow_renderer_cache),
            "svg_data_cached": len(self._svg_data_cache),
            "estimated_memory_bytes": self.get_memory_usage(),
        }

    def get_cache_info(self) -> str:
        """Get detailed cache information for debugging."""
        stats = self.get_cache_stats()
        memory_mb = stats["estimated_memory_bytes"] / 1024 / 1024

        return (
            f"PictographCacheManager Stats:\n"
            f"  Cache Hits: {stats['cache_hits']}\n"
            f"  Cache Misses: {stats['cache_misses']}\n"
            f"  Hit Rate: {stats['hit_rate_percent']}%\n"
            f"  Renderers Created: {stats['renderers_created']}\n"
            f"  Grid Renderers: {stats['grid_renderers_cached']}\n"
            f"  Prop Renderers: {stats['prop_renderers_cached']}\n"
            f"  Glyph Renderers: {stats['glyph_renderers_cached']}\n"
            f"  Arrow Renderers: {stats['arrow_renderers_cached']}\n"
            f"  SVG Data Cached: {stats['svg_data_cached']}\n"
            f"  Memory Usage: {memory_mb:.1f}MB\n"
            f"  Evictions: {stats['evictions_performed']}"
        )
