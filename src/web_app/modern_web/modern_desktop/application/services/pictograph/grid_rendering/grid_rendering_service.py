"""
Grid rendering microservice for pictograph rendering.

This service handles:
- Diamond and box grid rendering
- Grid positioning within scenes
- Fallback grid creation when assets fail to load
- Grid-specific caching and performance optimization
"""

from __future__ import annotations

import logging
from typing import Optional

from PyQt6.QtCore import QByteArray
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene
from shared.application.services.pictograph.asset_management.pictograph_asset_manager import (
    PictographAssetManager,
)
from shared.application.services.pictograph.performance_monitoring.pictograph_performance_monitor import (
    PictographPerformanceMonitor,
)

from desktop.modern.application.services.pictograph.cache_management.pictograph_cache_manager import (
    PictographCacheManager,
)


logger = logging.getLogger(__name__)


class GridRenderingService:
    """
    Microservice for rendering pictograph grids.

    Provides:
    - Diamond and box grid rendering
    - Grid positioning and centering
    - Fallback grid creation
    - Performance-optimized grid caching
    """

    def __init__(
        self,
        asset_manager: PictographAssetManager,
        cache_manager: PictographCacheManager,
        performance_monitor: PictographPerformanceMonitor,
    ):
        """Initialize the grid rendering service with injected dependencies."""
        self._asset_manager = asset_manager
        self._cache_manager = cache_manager
        self._performance_monitor = performance_monitor

    def render_grid(
        self, scene: QGraphicsScene, grid_mode: str = "diamond"
    ) -> Optional[QGraphicsSvgItem]:
        """
        Render grid using cached renderer with performance monitoring.

        Args:
            scene: Target scene to render into
            grid_mode: Grid type ("diamond" or "box")

        Returns:
            Created grid item or None if rendering failed
        """
        timer_id = self._performance_monitor.start_render_timer("grid_render")

        try:
            renderer = self._get_grid_renderer(grid_mode)
            if not renderer or not renderer.isValid():
                logger.error(
                    f"❌ [GRID_RENDERER] Invalid grid renderer for mode: {grid_mode}"
                )
                self._performance_monitor.record_error(
                    "grid_render", f"Invalid renderer for {grid_mode}"
                )
                return None

            grid_item = QGraphicsSvgItem()
            grid_item.setSharedRenderer(renderer)

            # Position grid at scene center
            self._position_grid_in_scene(grid_item, scene)

            scene.addItem(grid_item)

            logger.debug(f"🔲 [GRID_RENDERER] Rendered {grid_mode} grid")
            return grid_item

        except Exception as e:
            logger.error(f"❌ [GRID_RENDERER] Grid rendering failed: {e}")
            self._performance_monitor.record_error("grid_render", str(e))
            return None
        finally:
            self._performance_monitor.end_render_timer(timer_id)

    def _get_grid_renderer(self, grid_mode: str) -> Optional[QSvgRenderer]:
        """Get cached grid renderer or create new one."""
        cache_key = f"grid_{grid_mode}"

        # Try to get from cache first
        renderer = self._cache_manager.get_renderer(cache_key)
        if renderer:
            self._performance_monitor.record_cache_hit("grid")
            return renderer

        self._performance_monitor.record_cache_miss("grid")

        # Create new renderer
        renderer = self._create_grid_renderer(grid_mode)
        if renderer:
            self._cache_manager.store_renderer(cache_key, renderer)

        return renderer

    def _create_grid_renderer(self, grid_mode: str) -> Optional[QSvgRenderer]:
        """Create new grid renderer with actual SVG loading."""
        timer_id = self._performance_monitor.start_render_timer("svg_load")

        try:
            # Get grid SVG path based on mode
            grid_svg_path = self._asset_manager.get_grid_svg_path(grid_mode)

            if not self._asset_manager.svg_path_exists(grid_svg_path):
                logger.warning(f"⚠️ [GRID_RENDERER] Grid SVG not found: {grid_svg_path}")
                return self._create_fallback_grid_renderer(grid_mode)

            # Load SVG data from file
            svg_data = self._asset_manager.load_svg_data(grid_svg_path)
            if not svg_data:
                logger.error(
                    f"❌ [GRID_RENDERER] Failed to load grid SVG: {grid_svg_path}"
                )
                return self._create_fallback_grid_renderer(grid_mode)

            # Create renderer from SVG data
            renderer = QSvgRenderer(QByteArray(svg_data.encode("utf-8")))
            if renderer.isValid():
                logger.debug(
                    f"🔲 [GRID_RENDERER] Created {grid_mode} grid renderer from {grid_svg_path}"
                )
                return renderer
            logger.error(f"❌ [GRID_RENDERER] Invalid SVG for {grid_mode} grid")
            return self._create_fallback_grid_renderer(grid_mode)

        except Exception as e:
            logger.error(
                f"❌ [GRID_RENDERER] Failed to create {grid_mode} grid renderer: {e}"
            )
            self._performance_monitor.record_error("grid_create", str(e))
            return self._create_fallback_grid_renderer(grid_mode)
        finally:
            self._performance_monitor.end_render_timer(timer_id)

    def _create_fallback_grid_renderer(self, grid_mode: str) -> Optional[QSvgRenderer]:
        """Create fallback grid renderer when SVG loading fails."""
        try:
            fallback_svg = self._asset_manager.create_fallback_grid_svg(grid_mode)

            renderer = QSvgRenderer(QByteArray(fallback_svg.encode("utf-8")))
            if renderer.isValid():
                logger.debug(
                    f"🔧 [GRID_RENDERER] Created fallback {grid_mode} grid renderer"
                )
                return renderer
            logger.error("❌ [GRID_RENDERER] Failed to create fallback grid renderer")
            return None

        except Exception as e:
            logger.error(
                f"❌ [GRID_RENDERER] Failed to create fallback grid renderer: {e}"
            )
            return None

    def _position_grid_in_scene(
        self, grid_item: QGraphicsSvgItem, scene: QGraphicsScene
    ) -> None:
        """Position grid at the center of the scene."""
        try:
            scene_rect = scene.sceneRect()
            grid_bounds = grid_item.boundingRect()

            # Calculate center position
            center_x = scene_rect.center().x() - grid_bounds.width() / 2
            center_y = scene_rect.center().y() - grid_bounds.height() / 2

            grid_item.setPos(center_x, center_y)

            logger.debug(
                f"🎯 [GRID_RENDERER] Positioned grid at ({center_x:.1f}, {center_y:.1f})"
            )

        except Exception as e:
            logger.warning(f"⚠️ [GRID_RENDERER] Failed to position grid: {e}")
            # Fallback to origin if positioning fails
            grid_item.setPos(0, 0)

    def preload_common_grids(self) -> None:
        """Pre-load commonly used grid renderers for better performance."""
        try:
            # Pre-load diamond and box grids
            self._get_grid_renderer("diamond")
            self._get_grid_renderer("box")

        except Exception as e:
            logger.warning(
                f"⚠️ [GRID_RENDERER] Failed to pre-load some grid renderers: {e}"
            )

    def clear_grid_cache(self) -> None:
        """Clear grid-specific cache entries."""
        # This would need to be implemented in the cache manager
        # For now, we'll log the request
        logger.info("🧹 [GRID_RENDERER] Grid cache clear requested")

    def get_supported_grid_modes(self) -> list[str]:
        """Get list of supported grid modes."""
        return ["diamond", "box"]

    def validate_grid_mode(self, grid_mode: str) -> bool:
        """Validate if the grid mode is supported."""
        return grid_mode in self.get_supported_grid_modes()

    def get_grid_stats(self) -> dict:
        """Get grid rendering statistics."""
        # This would integrate with the performance monitor
        # For now, return basic info
        return {
            "supported_modes": self.get_supported_grid_modes(),
            "service_status": "active",
        }
