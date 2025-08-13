"""
Qt Adapter for Prop Rendering Service

This adapter maintains the Qt-dependent interface of the original PropRenderingService
while using the framework-agnostic core service internally.
"""

from __future__ import annotations

import logging

from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene

# Import Qt render engine from existing adapter
from desktop.modern.application.adapters.qt_pictograph_adapter import (
    QtRenderEngine,
    QtTypeConverter,
)
from desktop.modern.application.services.core.pictograph_rendering.real_asset_provider import (
    create_real_asset_provider,
)
from desktop.modern.application.services.core.prop_rendering_service import (
    create_prop_rendering_service,
)
from desktop.modern.application.services.core.types import Size
from desktop.modern.domain.models import MotionData, PictographData


logger = logging.getLogger(__name__)


class QtPropRenderingServiceAdapter:
    """
    Qt adapter for prop rendering service.

    Maintains the same interface as the original Qt-dependent PropRenderingService
    but uses the framework-agnostic core service internally.
    """

    def __init__(self):
        """Initialize the adapter with core services."""
        # Initialize core services (framework-agnostic)
        self._asset_provider = create_real_asset_provider()
        self._core_service = create_prop_rendering_service(self._asset_provider)

        # Initialize Qt render engine
        self._qt_render_engine = QtRenderEngine()

        # Performance tracking
        self._render_count = 0

        logger.debug("🎭 [QT_PROP_ADAPTER] Initialized Qt prop rendering adapter")

    def render_prop(
        self,
        scene: QGraphicsScene,
        color: str,
        motion_data: MotionData,
        pictograph_data: PictographData | None = None,
    ) -> QGraphicsSvgItem | None:
        """
        Render prop using core service + Qt execution (legacy interface).

        This maintains the exact same signature as the original service
        but uses framework-agnostic logic internally.
        """
        try:
            # Get target size from scene
            scene_rect = scene.sceneRect()
            target_size = Size(
                width=int(scene_rect.width()) if scene_rect.width() > 0 else 950,
                height=int(scene_rect.height()) if scene_rect.height() > 0 else 950,
            )

            # Use core service to create render command
            prop_command = self._core_service.create_prop_render_command(
                color, motion_data, target_size, pictograph_data
            )

            # Execute command with Qt render engine
            target = QtTypeConverter.create_render_target_from_scene(scene)
            success = self._qt_render_engine.execute_command(prop_command, target)

            if success:
                self._render_count += 1
                logger.debug(f"🎭 [QT_PROP_ADAPTER] Rendered {color} prop")
                return self._qt_render_engine._created_items.get(
                    prop_command.command_id
                )
            logger.error(
                f"❌ [QT_PROP_ADAPTER] Failed to execute prop command for {color}"
            )
            return None

        except Exception as e:
            logger.exception(f"❌ [QT_PROP_ADAPTER] Prop rendering failed: {e}")
            return None

    def get_performance_stats(self):
        """Get performance statistics."""
        core_stats = self._core_service.get_performance_stats()
        return {**core_stats, "qt_renders": self._render_count}

    def clear_scene_items(self, scene: QGraphicsScene):
        """Clear all items created by this adapter."""
        self._qt_render_engine.clear_created_items(scene)
