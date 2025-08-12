"""
Shared rendering service for all pictograph scenes - REFACTORED VERSION

This service now acts as a Qt adapter that delegates to the framework-agnostic
core pictograph rendering service. This eliminates Qt dependencies from the
business logic while maintaining backward compatibility.

ARCHITECTURE:
- Delegates to CorePictographRenderingService for business logic
- Uses Qt adapters to convert render commands to Qt graphics items
- Maintains same public interface for existing code compatibility
- Enables web service reuse of the same core logic
"""

from __future__ import annotations

import logging
from pathlib import Path

# Import framework-agnostic core services
import sys
from typing import Any


# Add project root to path using pathlib (standardized approach)
def _get_project_root() -> Path:
    """Find the TKA project root by looking for pyproject.toml."""
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    # Fallback: assume TKA is 6 levels up from this file
    return current_path.parents[5]


# Add project paths for imports
_project_root = _get_project_root()
sys.path.insert(0, str(_project_root))
sys.path.insert(0, str(_project_root / "src"))

from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene

# Import Qt adapter for render command execution
from desktop.modern.application.adapters.qt_pictograph_adapter import (
    QtPictographRenderingAdapter,
    create_qt_pictograph_adapter,
)
from desktop.modern.domain.models import MotionData


# Import from shared application services
sys.path.insert(0, str(_project_root / "src"))
from shared.application.services.core.pictograph_renderer import (
    CorePictographRenderer,
    create_pictograph_renderer,
)
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


class PictographRenderingService:
    """
    Qt-specific pictograph rendering service - REFACTORED VERSION

    This service now acts as a Qt adapter that delegates rendering to the
    framework-agnostic CorePictographRenderingService. This provides:

    - Same public interface for existing Qt code compatibility
    - Framework-agnostic business logic for web service reuse
    - Clean separation between Qt presentation and core logic
    - Better testability and maintainability

    Architecture:
    1. Receives Qt rendering requests (same interface as before)
    2. Converts Qt data to framework-agnostic format
    3. Delegates to CorePictographRenderingService for business logic
    4. Uses QtPictographRenderingAdapter to execute render commands on Qt scenes
    """

    _instance = None
    _creation_logged = False

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is created (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if not cls._creation_logged:
                logger.info(
                    "🎨 [RENDERING_SERVICE] Creating shared pictograph rendering service"
                )
                cls._creation_logged = True
        return cls._instance

    def __init__(
        self,
        asset_manager: PictographAssetManager = None,
        cache_manager: PictographCacheManager = None,
        performance_monitor: PictographPerformanceMonitor = None,
        # New framework-agnostic dependencies
        core_service: CorePictographRenderer = None,
        qt_adapter: QtPictographRenderingAdapter = None,
    ):
        """Initialize the service with framework-agnostic core and Qt adapter."""
        # Prevent re-initialization of singleton
        if hasattr(self, "_initialized"):
            return

        # Legacy dependencies (still used for compatibility)
        self._asset_manager = asset_manager or PictographAssetManager()
        self._cache_manager = cache_manager or PictographCacheManager()
        self._performance_monitor = (
            performance_monitor or PictographPerformanceMonitor()
        )

        # Core framework-agnostic service
        if core_service is None:
            # Create asset provider that integrates with existing asset management
            asset_provider = None  # Will use default asset provider
            self._core_service = create_pictograph_renderer(asset_provider)
        else:
            self._core_service = core_service

        # Qt adapter for executing render commands
        self._qt_adapter = qt_adapter or create_qt_pictograph_adapter(
            self._asset_manager
        )

        # Qt adapter for executing render commands
        self._qt_adapter = qt_adapter or create_qt_pictograph_adapter(
            self._asset_manager
        )

        # Mark as initialized
        self._initialized = True

        # Pre-load common renderers for performance
        self._preload_common_renderers()

        logger.info(
            "✅ [RENDERING_SERVICE] Service initialized with framework-agnostic core"
        )

    def _preload_common_renderers(self):
        """Pre-create commonly used renderers during startup."""
        try:
            # Let the Qt adapter handle pre-loading since it manages Qt-specific rendering
            logger.info("🚀 [RENDERING_SERVICE] Pre-loading delegated to Qt adapter")

        except Exception as e:
            logger.warning(
                f"⚠️ [RENDERING_SERVICE] Failed to pre-load some renderers: {e}"
            )

    def render_grid(
        self, scene: QGraphicsScene, grid_mode: str = "diamond"
    ) -> QGraphicsSvgItem | None:
        """
        Render grid using framework-agnostic core service + Qt adapter.

        Args:
            scene: Target scene to render into
            grid_mode: Grid type ("diamond" or "box")

        Returns:
            Created grid item or None if rendering failed
        """
        try:
            # Delegate to Qt adapter which uses the core service
            return self._qt_adapter.render_grid(scene, grid_mode)
        except Exception as e:
            logger.error(f"❌ [RENDERING_SERVICE] Grid rendering failed: {e}")
            return None

    def render_prop(
        self,
        scene: QGraphicsScene,
        color: str,
        motion_data: MotionData,
        pictograph_data=None,
    ) -> QGraphicsSvgItem | None:
        """
        Render prop using framework-agnostic core service + Qt adapter.

        Args:
            scene: Target scene to render into
            color: Prop color ("blue" or "red")
            motion_data: Motion data for positioning
            pictograph_data: Full pictograph data for beta positioning

        Returns:
            Created prop item or None if rendering failed
        """
        try:
            # Convert motion data to dictionary format for adapter
            motion_dict = {
                "motion_type": motion_data.motion_type.value,
                "start_loc": motion_data.start_loc.value,
                "end_loc": motion_data.end_loc.value,
                "start_ori": motion_data.start_ori.value,
                "end_ori": motion_data.end_ori.value,
                "turns": motion_data.turns,
            }

            # Delegate to Qt adapter which uses the core service
            return self._qt_adapter.render_prop(
                scene, color, motion_dict, pictograph_data
            )
        except Exception as e:
            logger.error(f"❌ [RENDERING_SERVICE] Prop rendering failed: {e}")
            return None

    def render_glyph(
        self, scene: QGraphicsScene, glyph_type: str, glyph_data: Any
    ) -> QGraphicsSvgItem | None:
        """
        Render glyph using framework-agnostic core service + Qt adapter.

        Args:
            scene: Target scene to render into
            glyph_type: Type of glyph ("letter", "elemental", "vtg", "tka", "position")
            glyph_data: Glyph-specific data for rendering

        Returns:
            Created glyph item or None if rendering failed
        """
        try:
            # Delegate to Qt adapter which uses the core service
            return self._qt_adapter.render_glyph(scene, glyph_type, glyph_data)
        except Exception as e:
            logger.error(f"❌ [RENDERING_SERVICE] Glyph rendering failed: {e}")
            return None

    def get_cache_stats(self) -> dict[str, Any]:
        """Get cache performance statistics from core and adapter services."""
        try:
            # Get stats from legacy services (for compatibility)
            cache_stats = self._cache_manager.get_cache_stats()
            asset_stats = self._asset_manager.get_asset_stats()
            performance_report = self._performance_monitor.get_performance_report()

            # Get stats from Qt adapter
            adapter_stats = self._qt_adapter.get_render_statistics()

            # Combine stats from all services
            combined_stats = {
                **cache_stats,
                **asset_stats,
                "performance": performance_report,
                "adapter_stats": adapter_stats,
                "architecture": "framework_agnostic_core_with_qt_adapter",
            }

            return combined_stats
        except Exception as e:
            logger.error(f"❌ [RENDERING_SERVICE] Failed to get cache stats: {e}")
            return {"error": str(e)}

    def clear_rendered_props(self):
        """Clear rendered props from all scenes (compatibility method)."""
        # This is a compatibility method for the transition
        logger.debug(
            "🧹 [RENDERING_SERVICE] Clear rendered props called (compatibility)"
        )

    def clear_cache(self):
        """Clear all caches to free memory."""
        try:
            self._cache_manager.clear_all_caches()
            self._asset_manager.clear_color_cache()
            self._performance_monitor.reset_statistics()

            logger.info("🧹 [RENDERING_SERVICE] Cleared all caches across services")
        except Exception as e:
            logger.error(f"❌ [RENDERING_SERVICE] Failed to clear caches: {e}")

    def get_cache_info(self) -> str:
        """Get detailed cache information for debugging."""
        try:
            cache_stats = self.get_cache_stats()
            cache_info = self._cache_manager.get_cache_info()
            performance_report = self._performance_monitor.get_performance_report()

            return (
                f"PictographRenderingService (Framework-Agnostic) Stats:\n"
                f"{cache_info}\n"
                f"Performance Summary:\n"
                f"  Total Operations: {performance_report.get('system_health', {}).get('total_operations', 0)}\n"
                f"  Slow Operations: {performance_report.get('system_health', {}).get('slow_operations', 0)}\n"
                f"  Error Count: {performance_report.get('system_health', {}).get('error_count', 0)}\n"
                f"Architecture: Framework-agnostic core with Qt adapter\n"
                f"Adapter Stats: {cache_stats.get('adapter_stats', 'unavailable')}"
            )
        except Exception as e:
            logger.error(f"❌ [RENDERING_SERVICE] Failed to get cache info: {e}")
            return f"Error getting cache info: {e}"

    # ============================================================================
    # SERVICE ACCESS METHODS (UPDATED FOR NEW ARCHITECTURE)
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

    def get_core_service(self) -> CorePictographRenderer:
        """Get the framework-agnostic core service."""
        return self._core_service

    def get_qt_adapter(self) -> QtPictographRenderingAdapter:
        """Get the Qt adapter service."""
        return self._qt_adapter

    # Legacy compatibility methods (deprecated but maintained for transition)
    def get_grid_renderer(self):
        """DEPRECATED: Use get_qt_adapter() instead."""
        logger.warning(
            "get_grid_renderer() is deprecated - use get_qt_adapter() instead"
        )
        return self._qt_adapter

    def get_prop_renderer(self):
        """DEPRECATED: Use get_qt_adapter() instead."""
        logger.warning(
            "get_prop_renderer() is deprecated - use get_qt_adapter() instead"
        )
        return self._qt_adapter

    def get_glyph_renderer(self):
        """DEPRECATED: Use get_qt_adapter() instead."""
        logger.warning(
            "get_glyph_renderer() is deprecated - use get_qt_adapter() instead"
        )
        return self._qt_adapter
