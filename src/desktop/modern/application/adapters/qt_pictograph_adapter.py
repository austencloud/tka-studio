"""
QT Pictograph Rendering Adapter

Bridges between the framework-agnostic core pictograph renderer and QT-specific
presentation layer. Converts render commands to QT graphics items.
"""

from __future__ import annotations

import logging
from pathlib import Path

# Add project root to path for core services
import sys

# Import the framework-agnostic core services
from PyQt6.QtCore import QPointF, QSizeF
from PyQt6.QtGui import QColor
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsScene


def _get_project_root() -> Path:
    """Find the TKA project root by looking for pyproject.toml."""
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    # Fallback: assume TKA is 6 levels up from this file
    return current_path.parents[5]


_project_root = _get_project_root()
sys.path.insert(0, str(_project_root / "src"))

from desktop.modern.application.services.core.pictograph_renderer import (
    CorePictographRenderer,
    IPictographAssetProvider,
)
from desktop.modern.application.services.core.types import (
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
        self._created_items: dict[str, QGraphicsItem] = {}

    def execute_command(self, command: RenderCommand, target: RenderTarget) -> bool:
        """Execute a render command on QT graphics scene."""
        try:
            scene = target.native_handle
            if not isinstance(scene, QGraphicsScene):
                logger.error("Target is not a QGraphicsScene")
                return False

            if command.render_type == "svg":
                return self._render_svg_command(command, scene)
            if command.render_type == "error":
                return self._render_error_command(command, scene)
            logger.warning(f"Unknown render type: {command.render_type}")
            return False

        except Exception as e:
            logger.exception(f"Failed to execute render command {command.command_id}: {e}")
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

            # Set position and size with LAYER-SPECIFIC POSITIONING
            qt_pos = QtTypeConverter.point_to_qt(command.position)
            QtTypeConverter.size_to_qt(command.size)

            # Different positioning logic based on layer type
            layer = command.properties.get("layer", "unknown")

            if layer == "props":
                # PROPS: Center-based positioning (legacy behavior)
                # This matches legacy behavior: place_prop_at_hand_point centers the prop
                svg_bounds = svg_item.boundingRect()
                svg_center = svg_bounds.center()

                # Calculate position so the prop's center appears at the target point
                centered_x = qt_pos.x() - svg_center.x()
                centered_y = qt_pos.y() - svg_center.y()
                svg_item.setPos(centered_x, centered_y)

            else:
                # GRIDS/OTHER: Top-left positioning (standard Qt behavior)
                # Grids should fill the scene from (0,0)
                svg_item.setPos(qt_pos)

            # Legacy approach: Don't scale props - use natural SVG size
            # Legacy props use their natural SVG dimensions without scaling
            # The SVG renderer handles the sizing based on the viewBox

            # Apply rotation if specified
            rotation = command.properties.get("rotation", 0.0)
            if rotation != 0.0:
                # Set rotation around the center of the item
                svg_item.setTransformOriginPoint(svg_item.boundingRect().center())
                svg_item.setRotation(rotation)

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
            logger.exception(f"Failed to render SVG command: {e}")
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
            logger.exception(f"Failed to render error command: {e}")
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
            logger.exception(f"Failed to clear items: {e}")


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

    def get_grid_asset(self, grid_mode: str) -> SvgAsset | None:
        """Get grid asset from existing QT asset management."""
        try:
            from desktop.modern.application.services.core.types import Size, SvgAsset

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
            logger.exception(f"Failed to get grid asset: {e}")
            return None

    def get_prop_asset(
        self, prop_type: str, color: str, pictograph_data: dict | None = None
    ) -> SvgAsset | None:
        """Get prop asset from existing QT asset management with color transformation and beta positioning support."""
        try:
            from desktop.modern.application.services.core.types import Size, SvgAsset

            if not self.legacy_asset_manager:
                logger.error("No asset manager available for prop assets")
                return None

            # Integrate with your existing prop asset loading
            prop_svg_content = self._load_prop_from_existing_system(prop_type)
            if not prop_svg_content:
                return None

            # Apply color transformation (same logic as RealAssetProvider)
            colored_svg_content = self._apply_color_transformation(
                prop_svg_content, color
            )

            # Create asset ID that includes beta positioning info if applicable
            asset_id = f"prop_{prop_type}_{color}"
            if pictograph_data and self._should_apply_beta_positioning(pictograph_data):
                asset_id += "_beta"

            return SvgAsset(
                asset_id=asset_id,
                svg_content=colored_svg_content,
                original_size=Size(50, 200),  # Get from your existing metadata
                color_properties=self._extract_color_properties(colored_svg_content),
            )

        except Exception as e:
            logger.exception(f"Failed to get prop asset: {e}")
            return None

    def get_glyph_asset(self, glyph_type: str, glyph_id: str) -> SvgAsset | None:
        """Get glyph asset from existing QT asset management."""
        try:
            from desktop.modern.application.services.core.types import Size, SvgAsset

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
            logger.exception(f"Failed to get glyph asset: {e}")
            return None

    def get_arrow_asset(self, arrow_type: str) -> SvgAsset | None:
        """Get arrow asset from existing QT asset management."""
        try:
            from desktop.modern.application.services.core.types import Size, SvgAsset

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
            logger.exception(f"Failed to get arrow asset: {e}")
            return None

    def _load_grid_from_existing_system(self, grid_mode: str) -> str | None:
        """Load grid SVG from your existing asset system."""
        try:
            # If no legacy asset manager, use direct file loading
            if not self.legacy_asset_manager:
                logger.debug(
                    f"No asset manager provided - loading grid directly: {grid_mode}"
                )
                return self._load_grid_directly(grid_mode)

            # Debug: Check what methods the asset manager has
            logger.debug(f"Asset manager type: {type(self.legacy_asset_manager)}")
            logger.debug(
                f"Has get_grid_svg_path: {hasattr(self.legacy_asset_manager, 'get_grid_svg_path')}"
            )
            logger.debug(
                f"Has load_svg_data: {hasattr(self.legacy_asset_manager, 'load_svg_data')}"
            )

            # Try to call existing grid loading methods
            if hasattr(self.legacy_asset_manager, "get_grid_svg_path") and hasattr(
                self.legacy_asset_manager, "load_svg_data"
            ):
                # Use PictographAssetManager methods
                logger.debug(
                    f"Using PictographAssetManager methods for grid: {grid_mode}"
                )
                grid_path = self.legacy_asset_manager.get_grid_svg_path(grid_mode)
                logger.debug(f"Grid path resolved: {grid_path}")
                result = self.legacy_asset_manager.load_svg_data(grid_path)
                if result:
                    logger.debug(
                        f"Successfully loaded grid SVG: {len(result)} characters"
                    )
                    return result
                logger.warning(f"Grid SVG loading returned None for path: {grid_path}")
            elif hasattr(self.legacy_asset_manager, "get_grid_svg"):
                return self.legacy_asset_manager.get_grid_svg(grid_mode)
            elif hasattr(self.legacy_asset_manager, "load_asset"):
                return self.legacy_asset_manager.load_asset(f"grid_{grid_mode}.svg")
            else:
                logger.debug(
                    "Asset manager doesn't have expected grid loading methods, using direct loading"
                )
                return self._load_grid_directly(grid_mode)
        except Exception as e:
            logger.exception(f"Failed to load grid from existing system: {e}")
            return self._load_grid_directly(grid_mode)

    def _load_prop_from_existing_system(self, prop_type: str) -> str | None:
        """Load prop SVG from your existing asset system."""
        try:
            # If no legacy asset manager, use direct file loading
            if not self.legacy_asset_manager:
                logger.debug(
                    f"No asset manager provided - loading prop directly: {prop_type}"
                )
                return self._load_prop_directly(prop_type)

            # Try to call existing prop loading methods
            if hasattr(self.legacy_asset_manager, "get_prop_svg_path") and hasattr(
                self.legacy_asset_manager, "load_svg_data"
            ):
                # Use PictographAssetManager methods
                prop_path = self.legacy_asset_manager.get_prop_svg_path(prop_type)
                return self.legacy_asset_manager.load_svg_data(prop_path)
            if hasattr(self.legacy_asset_manager, "get_prop_svg"):
                return self.legacy_asset_manager.get_prop_svg(prop_type)
            if hasattr(self.legacy_asset_manager, "load_asset"):
                return self.legacy_asset_manager.load_asset(f"prop_{prop_type}.svg")
            logger.debug(
                "Asset manager doesn't have expected prop loading methods, using direct loading"
            )
            return self._load_prop_directly(prop_type)
        except Exception as e:
            logger.exception(f"Failed to load prop from existing system: {e}")
            return self._load_prop_directly(prop_type)

    def _load_glyph_from_existing_system(
        self, glyph_type: str, glyph_id: str
    ) -> str | None:
        """Load glyph SVG from your existing asset system."""
        try:
            # If no legacy asset manager, use direct file loading
            if not self.legacy_asset_manager:
                logger.debug(
                    f"No asset manager provided - loading glyph directly: {glyph_type}_{glyph_id}"
                )
                return self._load_glyph_directly(glyph_type, glyph_id)

            # Try to call existing glyph loading methods
            if hasattr(self.legacy_asset_manager, "get_glyph_svg_path") and hasattr(
                self.legacy_asset_manager, "load_svg_data"
            ):
                # Use PictographAssetManager methods
                glyph_path = self.legacy_asset_manager.get_glyph_svg_path(
                    glyph_type, glyph_id
                )
                return self.legacy_asset_manager.load_svg_data(glyph_path)
            if hasattr(self.legacy_asset_manager, "get_glyph_svg"):
                return self.legacy_asset_manager.get_glyph_svg(glyph_type, glyph_id)
            if hasattr(self.legacy_asset_manager, "load_asset"):
                return self.legacy_asset_manager.load_asset(
                    f"glyph_{glyph_type}_{glyph_id}.svg"
                )
            logger.debug(
                "Asset manager doesn't have expected glyph loading methods, using direct loading"
            )
            return self._load_glyph_directly(glyph_type, glyph_id)
        except Exception as e:
            logger.exception(f"Failed to load glyph from existing system: {e}")
            return self._load_glyph_directly(glyph_type, glyph_id)

    def _load_arrow_from_existing_system(self, arrow_type: str) -> str | None:
        """Load arrow SVG from your existing asset system."""
        try:
            # TODO: Replace with your actual arrow loading logic
            if hasattr(self.legacy_asset_manager, "get_arrow_svg"):
                return self.legacy_asset_manager.get_arrow_svg(arrow_type)
            if hasattr(self.legacy_asset_manager, "load_asset"):
                return self.legacy_asset_manager.load_asset(f"arrow_{arrow_type}.svg")
            logger.error(
                "Legacy asset manager doesn't have expected arrow loading methods"
            )
            return None
        except Exception as e:
            logger.exception(f"Failed to load arrow from existing system: {e}")
            return None

    def _load_grid_directly(self, grid_mode: str) -> str | None:
        """Load grid SVG directly from file system."""
        try:
            from desktop.modern.application.services.assets.image_asset_utils import (
                get_image_path,
            )

            grid_path = get_image_path(f"grid/{grid_mode}_grid.svg")
            with open(grid_path, encoding="utf-8") as file:
                content = file.read()
                logger.debug(f"Loaded grid directly: {grid_path}")
                return content
        except Exception as e:
            logger.exception(f"Failed to load grid directly: {e}")
            return None

    def _load_prop_directly(self, prop_type: str) -> str | None:
        """Load prop SVG directly from file system."""
        try:
            from desktop.modern.application.services.assets.image_asset_utils import (
                get_image_path,
            )

            prop_path = get_image_path(f"props/{prop_type}.svg")
            with open(prop_path, encoding="utf-8") as file:
                content = file.read()
                logger.debug(f"Loaded prop directly: {prop_path}")
                return content
        except Exception as e:
            logger.exception(f"Failed to load prop directly: {e}")
            return None

    def _load_glyph_directly(self, glyph_type: str, glyph_id: str) -> str | None:
        """Load glyph SVG directly from file system."""
        try:
            from desktop.modern.application.services.assets.image_asset_utils import (
                get_image_path,
            )

            # Handle different glyph types
            if glyph_type == "letter":
                glyph_path = get_image_path(f"letters_trimmed/Type1/{glyph_id}.svg")
            elif glyph_type == "vtg":
                glyph_path = get_image_path(f"vtg_glyphs/{glyph_id}.svg")
            elif glyph_type == "element":
                glyph_path = get_image_path(f"elements/{glyph_id}.svg")
            else:
                logger.warning(f"Unknown glyph type: {glyph_type}")
                return None

            with open(glyph_path, encoding="utf-8") as file:
                content = file.read()
                logger.debug(f"Loaded glyph directly: {glyph_path}")
                return content
        except Exception as e:
            logger.exception(f"Failed to load glyph directly: {e}")
            return None

    def _apply_color_transformation(self, svg_content: str, color: str) -> str:
        """
        Apply color transformation to SVG content.

        Uses the same logic as RealAssetProvider to ensure consistent colors.
        """
        try:
            # Import constants from desktop data directory
            from data.constants import BLUE, HEX_BLUE, HEX_RED, RED

            # Define color mappings using the same constants as legacy system
            COLOR_MAP = {RED: HEX_RED, BLUE: HEX_BLUE}

            # Handle both string color names and direct hex values
            if color and color.startswith("#"):
                new_hex_color = color
            else:
                # Map color names to hex values (case insensitive)
                color_lower = color.lower()
                if color_lower == "red":
                    new_hex_color = COLOR_MAP.get(RED)
                elif color_lower == "blue":
                    new_hex_color = COLOR_MAP.get(BLUE)
                else:
                    new_hex_color = COLOR_MAP.get(color)

            if not new_hex_color:
                # If we still don't have a color, nothing to replace
                return svg_content

            # Use the same regex patterns as the legacy system for consistency
            import re

            # Pattern for CSS class definitions: .st0 { fill: #color; } or .cls-1 { fill: #color; }
            class_color_pattern = re.compile(
                r"(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)(#[a-fA-F0-9]{6})([^}]*?\})"
            )

            # Pattern for direct fill attributes: fill="#color"
            fill_pattern = re.compile(r'(fill=")(#[a-fA-F0-9]{6})(")')

            def replace_class_color(match):
                return match.group(1) + new_hex_color + match.group(4)

            def replace_fill_color(match):
                return match.group(1) + new_hex_color + match.group(3)

            # Apply transformations using the same logic as legacy system
            result = class_color_pattern.sub(replace_class_color, svg_content)
            result = fill_pattern.sub(replace_fill_color, result)

            return result

        except Exception as e:
            logger.exception(f"Failed to apply color transformation for {color}: {e}")
            return svg_content

    def _should_apply_beta_positioning(self, pictograph_data) -> bool:
        """
        Determine if beta positioning should be applied.

        Uses the same logic as BetaPositioningDetector.
        Handles both dictionary and PictographData object formats.
        """
        try:
            # Handle both dictionary and PictographData object formats
            if hasattr(pictograph_data, "letter"):
                # PictographData object
                letter = pictograph_data.letter
            elif hasattr(pictograph_data, "get"):
                # Dictionary format
                letter = pictograph_data.get("letter")
            else:
                logger.warning(
                    f"Unknown pictograph_data format: {type(pictograph_data)}"
                )
                return False

            if not letter:
                return False

            # Letters that end at beta positions (same as BetaPositioningDetector)
            beta_ending_letters = [
                "G",
                "H",
                "I",
                "J",
                "K",
                "L",
                "Y",
                "Z",
                "Y-",
                "Z-",
                "Ψ",
                "Ψ-",
                "β",
            ]

            return letter in beta_ending_letters

        except Exception as e:
            logger.warning(f"Failed to check beta positioning: {e}")
            return False

    def _extract_color_properties(self, svg_content: str) -> dict[str, str]:
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
        core_renderer: CorePictographRenderer | None = None,
        asset_provider: QtAssetProvider | None = None,
    ):
        """Initialize the adapter."""
        self.asset_provider = asset_provider or QtAssetProvider()
        self.core_renderer = core_renderer or CorePictographRenderer(
            self.asset_provider
        )
        self.qt_engine = QtRenderEngine()

    # ========================================================================
    # LEGACY INTERFACE COMPATIBILITY
    # ========================================================================

    def render_grid(
        self, scene: QGraphicsScene, grid_mode: str = "diamond"
    ) -> QGraphicsItem | None:
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
            logger.exception(f"Failed to render grid: {e}")
            return None

    def render_prop(
        self,
        scene: QGraphicsScene,
        color: str,
        motion_data: dict,
        pictograph_data: dict | None = None,
    ) -> QGraphicsItem | None:
        """Render prop using core service + QT execution (legacy interface)."""
        try:
            target = QtTypeConverter.create_render_target_from_scene(scene)

            # Extract position from motion data
            position = Point(
                motion_data.get("x", 200),
                motion_data.get("y", 200),  # Default center
            )

            # Use core renderer to create command with beta positioning support
            prop_command = self.core_renderer.render_prop(
                "staff", color, position, motion_data, pictograph_data
            )

            # Execute command
            success = self.qt_engine.execute_command(prop_command, target)

            if success:
                return self.qt_engine._created_items.get(prop_command.command_id)

            return None

        except Exception as e:
            logger.exception(f"Failed to render prop: {e}")
            return None

    def render_glyph(
        self, scene: QGraphicsScene, glyph_type: str, glyph_data: dict
    ) -> QGraphicsItem | None:
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
            logger.exception(f"Failed to render glyph: {e}")
            return None

    # ========================================================================
    # NEW CAPABILITIES
    # ========================================================================

    def render_complete_pictograph(
        self,
        scene: QGraphicsScene,
        pictograph_data: dict,
        options: dict | None = None,
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
            logger.exception(f"Failed to render complete pictograph: {e}")
            return False

    def clear_rendered_items(self, scene: QGraphicsScene) -> None:
        """Clear all items rendered by this adapter."""
        self.qt_engine.clear_created_items(scene)

    def get_render_statistics(self) -> dict:
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
    # Use QtAssetProvider with legacy asset manager for full asset support,
    # but we need to add color transformation to it
    asset_provider = QtAssetProvider(legacy_asset_manager)
    core_renderer = CorePictographRenderer(asset_provider)

    adapter = QtPictographRenderingAdapter(core_renderer, asset_provider)

    return adapter
