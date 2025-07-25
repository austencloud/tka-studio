"""
QT Pictograph Rendering Adapter

Bridges between the framework-agnostic core pictograph renderer and QT-specific
presentation layer. Converts render commands to QT graphics items.
"""

import logging
import os

# Import the framework-agnostic core services
import sys
from typing import Dict, List, Optional

from PyQt6.QtCore import QPointF, QRectF, QSizeF
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsScene

from application.services.core.pictograph_renderer import (
    CorePictographRenderer,
    IPictographAssetProvider,
)
from application.services.core.types import (
    Point,
    RenderCommand,
    RenderTarget,
    RenderTargetType,
    Size,
    SvgAsset,
)

logger = logging.getLogger(__name__)


# ============================================================================
# QT-SPECIFIC TYPES CONVERSION
# ============================================================================


class QtTypeConverter:
    """Converts between framework-agnostic types and QT types."""

    @staticmethod
    def size_to_qt(size: Size) -> QSizeF:
        """Convert Size to QSizeF."""
        return QSizeF(size.width, size.height)

    @staticmethod
    def qt_to_size(qt_size: QSizeF) -> Size:
        """Convert QSizeF to Size."""
        return Size(int(qt_size.width()), int(qt_size.height()))

    @staticmethod
    def point_to_qt(point: Point) -> QPointF:
        """Convert Point to QPointF."""
        return QPointF(point.x, point.y)

    @staticmethod
    def qt_to_point(qt_point: QPointF) -> Point:
        """Convert QPointF to Point."""
        return Point(int(qt_point.x()), int(qt_point.y()))

    @staticmethod
    def create_render_target_from_scene(scene: QGraphicsScene) -> RenderTarget:
        """Create RenderTarget from QGraphicsScene."""
        scene_rect = scene.sceneRect()
        return RenderTarget(
            target_id=f"qt_scene_{id(scene)}",
            target_type=RenderTargetType.GRAPHICS_SCENE,
            size=Size(int(scene_rect.width()), int(scene_rect.height())),
            properties={},
            native_handle=scene,
        )


# ============================================================================
# QT RENDER ENGINE
# ============================================================================


class QtRenderEngine:
    """QT-specific render engine that executes render commands."""

    def __init__(self):
        """Initialize QT render engine."""
        self._created_items: Dict[str, QGraphicsItem] = {}
        logger.info("QT render engine initialized")

    def execute_command(self, command: RenderCommand, target: RenderTarget) -> bool:
        """Execute a render command on QT graphics scene."""
        try:
            scene = target.native_handle
            if not isinstance(scene, QGraphicsScene):
                logger.error("Target is not a QGraphicsScene")
                return False

            if command.render_type == "svg":
                return self._render_svg_command(command, scene)
            elif command.render_type == "error":
                return self._render_error_command(command, scene)
            else:
                logger.warning(f"Unknown render type: {command.render_type}")
                return False

        except Exception as e:
            logger.error(f"Failed to execute render command {command.command_id}: {e}")
            return False

    def _render_svg_command(
        self, command: RenderCommand, scene: QGraphicsScene
    ) -> bool:
        """Render SVG command to QT scene."""
        try:
            svg_content = command.properties.get("svg_content")
            if not svg_content:
                logger.error("No SVG content in command")
                return False

            # Create QGraphicsSvgItem
            svg_item = QGraphicsSvgItem()

            # Load SVG content
            svg_renderer = QSvgRenderer()
            svg_content_bytes = svg_content.encode("utf-8")
            if not svg_renderer.load(svg_content_bytes):
                logger.error("Failed to load SVG content")
                return False

            svg_item.setSharedRenderer(svg_renderer)

            # Set position and size
            qt_pos = QtTypeConverter.point_to_qt(command.position)
            qt_size = QtTypeConverter.size_to_qt(command.size)

            svg_item.setPos(qt_pos)

            # Scale to desired size
            current_size = svg_item.boundingRect().size()
            if current_size.width() > 0 and current_size.height() > 0:
                scale_x = qt_size.width() / current_size.width()
                scale_y = qt_size.height() / current_size.height()
                svg_item.setScale(min(scale_x, scale_y))  # Maintain aspect ratio

            # Set Z-order
            z_index = command.properties.get("z_index", 0)
            svg_item.setZValue(z_index)

            # Add to scene
            scene.addItem(svg_item)

            # Track created item
            self._created_items[command.command_id] = svg_item

            logger.debug(f"Successfully rendered SVG command: {command.command_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to render SVG command: {e}")
            return False

    def _render_error_command(
        self, command: RenderCommand, scene: QGraphicsScene
    ) -> bool:
        """Render error placeholder."""
        try:
            # Create a simple red rectangle as error indicator
            from PyQt6.QtGui import QBrush, QPen
            from PyQt6.QtWidgets import QGraphicsRectItem

            qt_pos = QtTypeConverter.point_to_qt(command.position)
            qt_size = QtTypeConverter.size_to_qt(command.size)

            error_rect = QGraphicsRectItem(0, 0, qt_size.width(), qt_size.height())
            error_rect.setPos(qt_pos)
            error_rect.setBrush(QBrush(QColor(255, 0, 0, 100)))  # Semi-transparent red
            error_rect.setPen(QPen(QColor(255, 0, 0)))

            scene.addItem(error_rect)
            self._created_items[command.command_id] = error_rect

            logger.debug(f"Rendered error placeholder: {command.command_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to render error command: {e}")
            return False

    def clear_created_items(self, scene: QGraphicsScene) -> None:
        """Clear all items created by this engine."""
        try:
            for item in self._created_items.values():
                if item.scene() == scene:
                    scene.removeItem(item)
            self._created_items.clear()
            logger.debug("Cleared all created items")
        except Exception as e:
            logger.error(f"Failed to clear items: {e}")


# ============================================================================
# QT ASSET PROVIDER
# ============================================================================


class QtAssetProvider(IPictographAssetProvider):
    """QT-specific asset provider that integrates with existing asset management."""

    def __init__(self, legacy_asset_manager=None):
        """Initialize with existing asset manager."""
        self.legacy_asset_manager = legacy_asset_manager
        if not self.legacy_asset_manager:
            logger.warning("No legacy asset manager provided to QT asset provider")
        logger.info("QT asset provider initialized")

    def get_grid_asset(self, grid_mode: str) -> Optional["SvgAsset"]:
        """Get grid asset from existing QT asset management."""
        try:
            from application.services.core.types import Size, SvgAsset

            if not self.legacy_asset_manager:
                logger.error("No asset manager available for grid assets")
                return None

            # Integrate with your existing grid asset loading
            # This should call your existing grid asset methods
            grid_svg_content = self._load_grid_from_existing_system(grid_mode)
            if not grid_svg_content:
                return None

            return SvgAsset(
                asset_id=f"grid_{grid_mode}",
                svg_content=grid_svg_content,
                original_size=Size(400, 400),  # Get from your existing metadata
                color_properties=self._extract_color_properties(grid_svg_content),
            )

        except Exception as e:
            logger.error(f"Failed to get grid asset: {e}")
            return None

    def get_prop_asset(self, prop_type: str, color: str) -> Optional["SvgAsset"]:
        """Get prop asset from existing QT asset management."""
        try:
            from application.services.core.types import Size, SvgAsset

            if not self.legacy_asset_manager:
                logger.error("No asset manager available for prop assets")
                return None

            # Integrate with your existing prop asset loading
            prop_svg_content = self._load_prop_from_existing_system(prop_type)
            if not prop_svg_content:
                return None

            return SvgAsset(
                asset_id=f"prop_{prop_type}",
                svg_content=prop_svg_content,
                original_size=Size(50, 200),  # Get from your existing metadata
                color_properties=self._extract_color_properties(prop_svg_content),
            )

        except Exception as e:
            logger.error(f"Failed to get prop asset: {e}")
            return None

    def get_glyph_asset(self, glyph_type: str, glyph_id: str) -> Optional["SvgAsset"]:
        """Get glyph asset from existing QT asset management."""
        try:
            from application.services.core.types import Size, SvgAsset

            if not self.legacy_asset_manager:
                logger.error("No asset manager available for glyph assets")
                return None

            # Integrate with your existing glyph asset loading
            glyph_svg_content = self._load_glyph_from_existing_system(
                glyph_type, glyph_id
            )
            if not glyph_svg_content:
                return None

            return SvgAsset(
                asset_id=f"glyph_{glyph_type}_{glyph_id}",
                svg_content=glyph_svg_content,
                original_size=Size(50, 50),  # Get from your existing metadata
                color_properties=self._extract_color_properties(glyph_svg_content),
            )

        except Exception as e:
            logger.error(f"Failed to get glyph asset: {e}")
            return None

    def get_arrow_asset(self, arrow_type: str) -> Optional["SvgAsset"]:
        """Get arrow asset from existing QT asset management."""
        try:
            from application.services.core.types import Size, SvgAsset

            if not self.legacy_asset_manager:
                logger.error("No asset manager available for arrow assets")
                return None

            # Integrate with your existing arrow asset loading
            arrow_svg_content = self._load_arrow_from_existing_system(arrow_type)
            if not arrow_svg_content:
                return None

            return SvgAsset(
                asset_id=f"arrow_{arrow_type}",
                svg_content=arrow_svg_content,
                original_size=Size(100, 20),  # Get from your existing metadata
                color_properties=self._extract_color_properties(arrow_svg_content),
            )

        except Exception as e:
            logger.error(f"Failed to get arrow asset: {e}")
            return None

    def _load_grid_from_existing_system(self, grid_mode: str) -> Optional[str]:
        """Load grid SVG from your existing asset system."""
        try:
            # TODO: Replace with your actual grid loading logic
            # This should call your existing grid asset loading methods
            if hasattr(self.legacy_asset_manager, "get_grid_svg"):
                return self.legacy_asset_manager.get_grid_svg(grid_mode)
            elif hasattr(self.legacy_asset_manager, "load_asset"):
                return self.legacy_asset_manager.load_asset(f"grid_{grid_mode}.svg")
            else:
                logger.error(
                    "Legacy asset manager doesn't have expected grid loading methods"
                )
                return None
        except Exception as e:
            logger.error(f"Failed to load grid from existing system: {e}")
            return None

    def _load_prop_from_existing_system(self, prop_type: str) -> Optional[str]:
        """Load prop SVG from your existing asset system."""
        try:
            # TODO: Replace with your actual prop loading logic
            if hasattr(self.legacy_asset_manager, "get_prop_svg"):
                return self.legacy_asset_manager.get_prop_svg(prop_type)
            elif hasattr(self.legacy_asset_manager, "load_asset"):
                return self.legacy_asset_manager.load_asset(f"prop_{prop_type}.svg")
            else:
                logger.error(
                    "Legacy asset manager doesn't have expected prop loading methods"
                )
                return None
        except Exception as e:
            logger.error(f"Failed to load prop from existing system: {e}")
            return None

    def _load_glyph_from_existing_system(
        self, glyph_type: str, glyph_id: str
    ) -> Optional[str]:
        """Load glyph SVG from your existing asset system."""
        try:
            # TODO: Replace with your actual glyph loading logic
            if hasattr(self.legacy_asset_manager, "get_glyph_svg"):
                return self.legacy_asset_manager.get_glyph_svg(glyph_type, glyph_id)
            elif hasattr(self.legacy_asset_manager, "load_asset"):
                return self.legacy_asset_manager.load_asset(
                    f"glyph_{glyph_type}_{glyph_id}.svg"
                )
            else:
                logger.error(
                    "Legacy asset manager doesn't have expected glyph loading methods"
                )
                return None
        except Exception as e:
            logger.error(f"Failed to load glyph from existing system: {e}")
            return None

    def _load_arrow_from_existing_system(self, arrow_type: str) -> Optional[str]:
        """Load arrow SVG from your existing asset system."""
        try:
            # TODO: Replace with your actual arrow loading logic
            if hasattr(self.legacy_asset_manager, "get_arrow_svg"):
                return self.legacy_asset_manager.get_arrow_svg(arrow_type)
            elif hasattr(self.legacy_asset_manager, "load_asset"):
                return self.legacy_asset_manager.load_asset(f"arrow_{arrow_type}.svg")
            else:
                logger.error(
                    "Legacy asset manager doesn't have expected arrow loading methods"
                )
                return None
        except Exception as e:
            logger.error(f"Failed to load arrow from existing system: {e}")
            return None

    def _extract_color_properties(self, svg_content: str) -> Dict[str, str]:
        """Extract color properties from SVG content."""
        # Simple extraction - you might want to use proper XML parsing
        color_properties = {}

        if "fill=" in svg_content:
            # Extract fill colors
            import re

            fills = re.findall(r'fill=["\']([^"\']*)["\'"]', svg_content)
            if fills:
                color_properties["fill"] = fills[0]

        if "stroke=" in svg_content:
            # Extract stroke colors
            import re

            strokes = re.findall(r'stroke=["\']([^"\']*)["\'"]', svg_content)
            if strokes:
                color_properties["stroke"] = strokes[0]

        return color_properties


# ============================================================================
# MAIN ADAPTER CLASS
# ============================================================================


class QtPictographRenderingAdapter:
    """
    Main adapter that bridges core pictograph renderer with QT presentation.

    This adapter:
    1. Uses the framework-agnostic core renderer to generate render commands
    2. Executes those commands using QT-specific rendering
    3. Provides the same interface as the original QT service for easy migration
    """

    def __init__(
        self,
        core_renderer: Optional[CorePictographRenderer] = None,
        asset_provider: Optional[QtAssetProvider] = None,
    ):
        """Initialize the adapter."""
        self.asset_provider = asset_provider or QtAssetProvider()
        self.core_renderer = core_renderer or CorePictographRenderer(
            self.asset_provider
        )
        self.qt_engine = QtRenderEngine()

        logger.info("QT pictograph rendering adapter initialized")

    # ========================================================================
    # LEGACY INTERFACE COMPATIBILITY
    # ========================================================================

    def render_grid(
        self, scene: QGraphicsScene, grid_mode: str = "diamond"
    ) -> Optional[QGraphicsItem]:
        """Render grid using core service + QT execution (legacy interface)."""
        try:
            # Convert QT scene to render target
            target = QtTypeConverter.create_render_target_from_scene(scene)

            # Use core renderer to create command
            grid_command = self.core_renderer.render_grid(
                grid_mode, target.size, Point(0, 0)
            )

            # Execute command with QT engine
            success = self.qt_engine.execute_command(grid_command, target)

            if success:
                # Return the created item for legacy compatibility
                return self.qt_engine._created_items.get(grid_command.command_id)

            return None

        except Exception as e:
            logger.error(f"Failed to render grid: {e}")
            return None

    def render_prop(
        self,
        scene: QGraphicsScene,
        color: str,
        motion_data: Dict,
        pictograph_data: Optional[Dict] = None,
    ) -> Optional[QGraphicsItem]:
        """Render prop using core service + QT execution (legacy interface)."""
        try:
            target = QtTypeConverter.create_render_target_from_scene(scene)

            # Extract position from motion data
            position = Point(
                motion_data.get("x", 200), motion_data.get("y", 200)  # Default center
            )

            # Use core renderer to create command
            prop_command = self.core_renderer.render_prop(
                "staff", color, position, motion_data  # Default prop type
            )

            # Execute command
            success = self.qt_engine.execute_command(prop_command, target)

            if success:
                return self.qt_engine._created_items.get(prop_command.command_id)

            return None

        except Exception as e:
            logger.error(f"Failed to render prop: {e}")
            return None

    def render_glyph(
        self, scene: QGraphicsScene, glyph_type: str, glyph_data: Dict
    ) -> Optional[QGraphicsItem]:
        """Render glyph using core service + QT execution (legacy interface)."""
        try:
            target = QtTypeConverter.create_render_target_from_scene(scene)

            position = Point(glyph_data.get("x", 100), glyph_data.get("y", 100))

            size = Size(glyph_data.get("width", 50), glyph_data.get("height", 50))

            glyph_command = self.core_renderer.render_glyph(
                glyph_type, glyph_data.get("id", ""), position, size
            )

            success = self.qt_engine.execute_command(glyph_command, target)

            if success:
                return self.qt_engine._created_items.get(glyph_command.command_id)

            return None

        except Exception as e:
            logger.error(f"Failed to render glyph: {e}")
            return None

    # ========================================================================
    # NEW CAPABILITIES
    # ========================================================================

    def render_complete_pictograph(
        self,
        scene: QGraphicsScene,
        pictograph_data: Dict,
        options: Optional[Dict] = None,
    ) -> bool:
        """Render complete pictograph using core service."""
        try:
            # Clear previous items
            self.qt_engine.clear_created_items(scene)

            # Convert scene to render target
            target = QtTypeConverter.create_render_target_from_scene(scene)

            # Generate all render commands
            commands = self.core_renderer.create_render_commands(
                pictograph_data, target.size, options
            )

            # Execute all commands
            success_count = 0
            for command in commands:
                if self.qt_engine.execute_command(command, target):
                    success_count += 1

            logger.info(f"Rendered {success_count}/{len(commands)} pictograph elements")
            return success_count > 0

        except Exception as e:
            logger.error(f"Failed to render complete pictograph: {e}")
            return False

    def clear_rendered_items(self, scene: QGraphicsScene) -> None:
        """Clear all items rendered by this adapter."""
        self.qt_engine.clear_created_items(scene)

    def get_render_statistics(self) -> Dict:
        """Get rendering statistics."""
        return {
            "items_created": len(self.qt_engine._created_items),
            "core_renderer_active": self.core_renderer is not None,
            "asset_provider_active": self.asset_provider is not None,
        }


# ============================================================================
# FACTORY FUNCTION FOR EASY INTEGRATION
# ============================================================================


def create_qt_pictograph_adapter(
    legacy_asset_manager=None,
) -> QtPictographRenderingAdapter:
    """
    Factory function to create QT pictograph adapter.

    Args:
        legacy_asset_manager: Existing asset manager to integrate with

    Returns:
        Configured QT adapter ready for use
    """
    asset_provider = QtAssetProvider(legacy_asset_manager)
    core_renderer = CorePictographRenderer(asset_provider)

    adapter = QtPictographRenderingAdapter(core_renderer, asset_provider)

    logger.info("Created QT pictograph adapter with real asset integration")
    return adapter
