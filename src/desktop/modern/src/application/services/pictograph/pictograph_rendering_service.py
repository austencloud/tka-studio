"""
Shared rendering service for all pictograph scenes.

This service provides centralized, cached rendering for grids, props, arrows, and glyphs
to eliminate the performance overhead of creating multiple renderer instances per scene.

REFACTORING NOTE: This service is being broken down into smaller microservices:
- PictographAssetManager: SVG loading and color transformations
- PictographCacheManager: Caching and memory management
- GridRenderingService: Grid-specific rendering
- PropRenderingService: Prop-specific rendering
- GlyphRenderingService: Glyph-specific rendering
- PictographPerformanceMonitor: Performance tracking
"""

import logging
from typing import Any, Dict, Optional

from application.services.pictograph.glyph_rendering.glyph_rendering_service import (
    GlyphRenderingService,
)
from application.services.pictograph.grid_rendering.grid_rendering_service import (
    GridRenderingService,
)
from application.services.pictograph.prop_rendering.prop_rendering_service import (
    PropRenderingService,
)
from domain.models import MotionData, PictographData
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene

from application.services.pictograph.asset_management.pictograph_asset_manager import (
    PictographAssetManager,
)
from application.services.pictograph.cache_management.pictograph_cache_manager import (
    PictographCacheManager,
)
from application.services.pictograph.performance_monitoring.pictograph_performance_monitor import (
    PictographPerformanceMonitor,
)

logger = logging.getLogger(__name__)


class PictographRenderingService:
    """
    Orchestrator service for pictograph rendering.

    This service coordinates specialized microservices to provide:
    - Grids (diamond, box modes) via GridRenderingService
    - Props (staff in various colors) via PropRenderingService
    - Arrows (via existing arrow rendering service)
    - Glyphs (letters, elemental, VTG, TKA, positions) via GlyphRenderingService

    Benefits:
    - Modular architecture with focused microservices
    - Dependency injection for better testability
    - Centralized coordination with distributed responsibilities
    - Maintained compatibility with existing interface
    """

    _instance = None
    _creation_logged = False

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is created (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if not cls._creation_logged:

                cls._creation_logged = True
        return cls._instance

    def __init__(
        self,
        asset_manager: PictographAssetManager = None,
        cache_manager: PictographCacheManager = None,
        performance_monitor: PictographPerformanceMonitor = None,
        grid_renderer: GridRenderingService = None,
        prop_renderer: PropRenderingService = None,
        glyph_renderer: GlyphRenderingService = None,
    ):
        """Initialize the orchestrator with injected microservices."""
        # Prevent re-initialization of singleton
        if hasattr(self, "_initialized"):
            return

        # Initialize microservices (create defaults if not injected)
        self._asset_manager = asset_manager or PictographAssetManager()
        self._cache_manager = cache_manager or PictographCacheManager()
        self._performance_monitor = (
            performance_monitor or PictographPerformanceMonitor()
        )

        # Initialize rendering services with dependencies
        self._grid_renderer = grid_renderer or GridRenderingService(
            self._asset_manager, self._cache_manager, self._performance_monitor
        )
        self._prop_renderer = prop_renderer or PropRenderingService(
            self._asset_manager, self._cache_manager, self._performance_monitor
        )
        self._glyph_renderer = glyph_renderer or GlyphRenderingService(
            self._asset_manager, self._cache_manager, self._performance_monitor
        )

        # Pre-initialize common renderers for better startup performance
        self._preload_common_renderers()

        # Mark as initialized
        self._initialized = True

    def _preload_common_renderers(self):
        """Pre-create commonly used renderers during startup."""
        try:
            # Pre-load grid renderers
            self._grid_renderer.preload_common_grids()

            # Pre-load prop renderers for common colors
            self._prop_renderer.preload_common_props()

            # Pre-load glyph renderers
            self._glyph_renderer.preload_common_glyphs()

        except Exception as e:
            logger.warning(
                f"⚠️ [RENDERING_SERVICE] Failed to pre-load some renderers: {e}"
            )

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
        return self._grid_renderer.render_grid(scene, grid_mode)

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
            pictograph_data: Full pictograph data for beta positioning

        Returns:
            Created prop item or None if rendering failed
        """
        return self._prop_renderer.render_prop(
            scene, color, motion_data, pictograph_data
        )

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
        return self._glyph_renderer.render_glyph(scene, glyph_type, glyph_data)

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics from all microservices."""
        # Aggregate stats from all microservices
        cache_stats = self._cache_manager.get_cache_stats()
        asset_stats = self._asset_manager.get_asset_stats()
        performance_report = self._performance_monitor.get_performance_report()

        # Combine stats from all services
        combined_stats = {
            **cache_stats,
            **asset_stats,
            "performance": performance_report,
            "grid_stats": self._grid_renderer.get_grid_stats(),
            "prop_stats": self._prop_renderer.get_prop_stats(),
            "glyph_stats": self._glyph_renderer.get_glyph_stats(),
        }

        return combined_stats

    def clear_rendered_props(self):
        """Clear rendered props from all scenes (compatibility method)."""
        # This is a compatibility method for the transition
        logger.debug(
            "🧹 [RENDERING_SERVICE] Clear rendered props called (compatibility)"
        )

    def clear_cache(self):
        """Clear all caches to free memory."""
        self._cache_manager.clear_all_caches()
        self._asset_manager.clear_color_cache()
        self._performance_monitor.reset_statistics()

        logger.info("🧹 [RENDERING_SERVICE] Cleared all caches across microservices")

    def get_cache_info(self) -> str:
        """Get detailed cache information for debugging."""
        cache_stats = self.get_cache_stats()
        cache_info = self._cache_manager.get_cache_info()
        performance_report = self._performance_monitor.get_performance_report()

        return (
            f"PictographRenderingService Orchestrator Stats:\n"
            f"{cache_info}\n"
            f"Performance Summary:\n"
            f"  Total Operations: {performance_report.get('system_health', {}).get('total_operations', 0)}\n"
            f"  Slow Operations: {performance_report.get('system_health', {}).get('slow_operations', 0)}\n"
            f"  Error Count: {performance_report.get('system_health', {}).get('error_count', 0)}\n"
            f"Microservices Status:\n"
            f"  Grid Renderer: {cache_stats.get('grid_stats', {}).get('service_status', 'unknown')}\n"
            f"  Prop Renderer: {cache_stats.get('prop_stats', {}).get('service_status', 'unknown')}\n"
            f"  Glyph Renderer: {cache_stats.get('glyph_stats', {}).get('service_status', 'unknown')}"
        )

    # ============================================================================
    # MICROSERVICE ACCESS METHODS
    # ============================================================================

    def get_asset_manager(self) -> PictographAssetManager:
        """Get the asset manager microservice."""
        return self._asset_manager

    def get_cache_manager(self) -> PictographCacheManager:
        """Get the cache manager microservice."""
        return self._cache_manager

    def get_performance_monitor(self) -> PictographPerformanceMonitor:
        """Get the performance monitor microservice."""
        return self._performance_monitor

    def get_grid_renderer(self) -> GridRenderingService:
        """Get the grid rendering microservice."""
        return self._grid_renderer

    def get_prop_renderer(self) -> PropRenderingService:
        """Get the prop rendering microservice."""
        return self._prop_renderer

    def get_glyph_renderer(self) -> GlyphRenderingService:
        """Get the glyph rendering microservice."""
        return self._glyph_renderer
