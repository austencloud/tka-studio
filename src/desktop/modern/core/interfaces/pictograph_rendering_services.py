"""
Interfaces for pictograph rendering services.

Defines contracts for shared rendering services that provide cached,
high-performance rendering of pictograph elements.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene

from desktop.modern.domain.models import MotionData, PictographData


class IPictographRenderingService(ABC):
    """
    Interface for shared pictograph rendering service.

    Provides cached, high-performance rendering of all pictograph elements:
    - Grids (diamond, box modes)
    - Props (staff in various colors)
    - Arrows (via existing arrow rendering service)
    - Glyphs (letters, elemental, VTG, TKA, positions)
    """

    @abstractmethod
    def render_grid(
        self, scene: QGraphicsScene, grid_mode: str = "diamond"
    ) -> Optional[QGraphicsSvgItem]:
        """
        Render grid using cached renderer.

        Args:
            scene: Target scene to render into
            grid_mode: Grid type ("diamond" or "box")

        Returns:
            Created grid item or None if rendering failed
        """

    @abstractmethod
    def render_prop(
        self,
        scene: QGraphicsScene,
        color: str,
        motion_data: MotionData,
        pictograph_data=None,
    ) -> Optional[QGraphicsSvgItem]:
        """
        Render prop using cached, colored renderer.

        Args:
            scene: Target scene to render into
            color: Prop color ("blue" or "red")
            motion_data: Motion data for positioning

        Returns:
            Created prop item or None if rendering failed
        """

    @abstractmethod
    def render_glyph(
        self, scene: QGraphicsScene, glyph_type: str, glyph_data: Any
    ) -> Optional[QGraphicsSvgItem]:
        """
        Render glyph using cached renderer.

        Args:
            scene: Target scene to render into
            glyph_type: Type of glyph ("letter", "elemental", "vtg", "tka", "position")
            glyph_data: Glyph-specific data for rendering

        Returns:
            Created glyph item or None if rendering failed
        """

    @abstractmethod
    def get_cache_stats(self) -> dict[str, Any]:
        """
        Get cache performance statistics.

        Returns:
            Dictionary containing cache hit rates, renderer counts, etc.
        """

    @abstractmethod
    def clear_cache(self) -> None:
        """Clear all caches to free memory."""

    @abstractmethod
    def get_cache_info(self) -> str:
        """
        Get detailed cache information for debugging.

        Returns:
            Human-readable string with cache statistics
        """


class IArrowRenderingService(ABC):
    """
    Interface for arrow rendering service.

    Note: This interface is kept separate as arrows have more complex
    positioning and motion-based rendering requirements.
    """

    @abstractmethod
    def render_arrow(
        self,
        scene: QGraphicsScene,
        color: str,
        motion_data: MotionData,
        pictograph_data: Optional[PictographData] = None,
    ) -> Optional[QGraphicsSvgItem]:
        """
        Render arrow using cached renderer.

        Args:
            scene: Target scene to render into
            color: Arrow color ("blue" or "red")
            motion_data: Motion data for arrow type and positioning
            pictograph_data: Full pictograph data for context

        Returns:
            Created arrow item or None if rendering failed
        """

    @abstractmethod
    def clear_arrows(self, scene: QGraphicsScene) -> None:
        """Clear all arrows from the specified scene."""


class IPictographAssetManager(ABC):
    """
    Interface for pictograph asset management.

    Handles loading, caching, and color transformation of SVG assets.
    """

    @abstractmethod
    def get_grid_svg_path(self, grid_mode: str) -> str:
        """Get file path for grid SVG."""

    @abstractmethod
    def get_prop_svg_path(self, prop_type: str) -> str:
        """Get file path for prop SVG."""

    @abstractmethod
    def get_arrow_svg_path(self, motion_data: MotionData, color: str) -> str:
        """Get file path for arrow SVG."""

    @abstractmethod
    def get_glyph_svg_path(self, glyph_type: str, glyph_data: Any) -> str:
        """Get file path for glyph SVG."""

    @abstractmethod
    def load_svg_data(self, svg_path: str) -> Optional[str]:
        """Load SVG data from file with caching."""

    @abstractmethod
    def apply_color_transformation(self, svg_data: str, color: str) -> str:
        """Apply color transformation to SVG data."""

    @abstractmethod
    def svg_path_exists(self, svg_path: str) -> bool:
        """Check if SVG file exists."""


class IPictographCacheManager(ABC):
    """
    Interface for pictograph cache management.

    Provides advanced caching strategies with memory management.
    """

    @abstractmethod
    def get_renderer(self, cache_key: str) -> Optional[Any]:
        """Get cached renderer by key."""

    @abstractmethod
    def store_renderer(self, cache_key: str, renderer: Any) -> None:
        """Store renderer in cache."""

    @abstractmethod
    def get_svg_data(self, cache_key: str) -> Optional[str]:
        """Get cached SVG data by key."""

    @abstractmethod
    def store_svg_data(self, cache_key: str, svg_data: str) -> None:
        """Store SVG data in cache."""

    @abstractmethod
    def evict_least_used(self) -> None:
        """Evict least recently used items from cache."""

    @abstractmethod
    def get_memory_usage(self) -> int:
        """Get estimated memory usage in bytes."""

    @abstractmethod
    def clear_all_caches(self) -> None:
        """Clear all caches."""


class IPictographPerformanceMonitor(ABC):
    """
    Interface for pictograph performance monitoring.

    Tracks rendering performance and provides optimization insights.
    """

    @abstractmethod
    def start_render_timer(self, operation: str) -> str:
        """Start timing a render operation. Returns timer ID."""

    @abstractmethod
    def end_render_timer(self, timer_id: str) -> float:
        """End timing and return duration in milliseconds."""

    @abstractmethod
    def record_cache_hit(self, cache_type: str) -> None:
        """Record a cache hit."""

    @abstractmethod
    def record_cache_miss(self, cache_type: str) -> None:
        """Record a cache miss."""

    @abstractmethod
    def get_performance_report(self) -> dict[str, Any]:
        """Get comprehensive performance report."""

    @abstractmethod
    def reset_statistics(self) -> None:
        """Reset all performance statistics."""
