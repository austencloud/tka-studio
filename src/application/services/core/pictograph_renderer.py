"""
Core Pictograph Rendering Service

Framework-agnostic pictograph rendering service that generates render commands
instead of directly manipulating UI frameworks. Can be used by both desktop (QT)
and web services.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Protocol

from .types import (
    AssetHandle,
    Color,
    Colors,
    ImageData,
    ImageFormat,
    Point,
    RenderCommand,
    RenderTarget,
    Size,
    SvgAsset,
)

logger = logging.getLogger(__name__)


# ============================================================================
# INTERFACES
# ============================================================================


class IPictographAssetProvider(Protocol):
    """Protocol for providing pictograph assets."""

    def get_grid_asset(self, grid_mode: str) -> Optional[SvgAsset]:
        """Get grid SVG asset."""
        ...

    def get_prop_asset(self, prop_type: str, color: str) -> Optional[SvgAsset]:
        """Get prop SVG asset."""
        ...

    def get_glyph_asset(self, glyph_type: str, glyph_id: str) -> Optional[SvgAsset]:
        """Get glyph SVG asset."""
        ...

    def get_arrow_asset(self, arrow_type: str) -> Optional[SvgAsset]:
        """Get arrow SVG asset."""
        ...


class IPictographRenderer(ABC):
    """Interface for pictograph rendering operations."""

    @abstractmethod
    def create_render_commands(
        self, pictograph_data: Dict, target_size: Size, options: Optional[Dict] = None
    ) -> List[RenderCommand]:
        """Create list of render commands for pictograph."""
        pass

    @abstractmethod
    def render_grid(
        self, grid_mode: str, target_size: Size, position: Point = Point(0, 0)
    ) -> RenderCommand:
        """Create render command for grid."""
        pass

    @abstractmethod
    def render_prop(
        self,
        prop_type: str,
        color: str,
        position: Point,
        motion_data: Optional[Dict] = None,
    ) -> RenderCommand:
        """Create render command for prop."""
        pass

    @abstractmethod
    def render_glyph(
        self, glyph_type: str, glyph_id: str, position: Point, size: Size
    ) -> RenderCommand:
        """Create render command for glyph."""
        pass


# ============================================================================
# CORE SERVICE IMPLEMENTATION
# ============================================================================


class CorePictographRenderer(IPictographRenderer):
    """
    Framework-agnostic core pictograph renderer.

    Generates render commands instead of directly manipulating UI frameworks.
    Can be used by both QT desktop applications and web services.
    """

    def __init__(self, asset_provider: IPictographAssetProvider):
        """Initialize with asset provider."""
        self.asset_provider = asset_provider
        self._command_counter = 0
        logger.info("Core pictograph renderer initialized")

    def create_render_commands(
        self, pictograph_data: Dict, target_size: Size, options: Optional[Dict] = None
    ) -> List[RenderCommand]:
        """
        Create complete list of render commands for pictograph.

        Args:
            pictograph_data: Pictograph data dictionary
            target_size: Target rendering size
            options: Optional rendering options

        Returns:
            List of render commands to execute
        """
        commands = []
        options = options or {}

        try:
            # 1. Render grid (background)
            grid_mode = pictograph_data.get("grid_mode", "diamond")
            if options.get("show_grid", True):
                grid_command = self.render_grid(grid_mode, target_size)
                commands.append(grid_command)

            # 2. Render props
            props_data = pictograph_data.get("props", [])
            for prop_data in props_data:
                prop_command = self.render_prop(
                    prop_data.get("type", "staff"),
                    prop_data.get("color", "blue"),
                    Point(prop_data.get("x", 0), prop_data.get("y", 0)),
                    prop_data.get("motion_data"),
                )
                commands.append(prop_command)

            # 3. Render glyphs
            glyphs_data = pictograph_data.get("glyphs", [])
            for glyph_data in glyphs_data:
                glyph_command = self.render_glyph(
                    glyph_data.get("type", "letter"),
                    glyph_data.get("id", ""),
                    Point(glyph_data.get("x", 0), glyph_data.get("y", 0)),
                    Size(glyph_data.get("width", 50), glyph_data.get("height", 50)),
                )
                commands.append(glyph_command)

            # 4. Render arrows
            arrows_data = pictograph_data.get("arrows", [])
            for arrow_data in arrows_data:
                arrow_command = self._render_arrow(
                    arrow_data.get("type", "motion"),
                    Point(arrow_data.get("start_x", 0), arrow_data.get("start_y", 0)),
                    Point(arrow_data.get("end_x", 100), arrow_data.get("end_y", 100)),
                    arrow_data.get("color", "black"),
                )
                commands.append(arrow_command)

            logger.info(f"Created {len(commands)} render commands for pictograph")
            return commands

        except Exception as e:
            logger.error(f"Failed to create render commands: {e}")
            return []

    def render_grid(
        self, grid_mode: str, target_size: Size, position: Point = Point(0, 0)
    ) -> RenderCommand:
        """Create render command for grid background."""
        try:
            grid_asset = self.asset_provider.get_grid_asset(grid_mode)
            if not grid_asset:
                logger.warning(f"Grid asset not found for mode: {grid_mode}")
                return self._create_error_command("grid", position, target_size)

            return RenderCommand(
                command_id=self._next_command_id(),
                target_id="background",
                render_type="svg",
                position=position,
                size=target_size,
                properties={
                    "asset_id": grid_asset.asset_id,
                    "svg_content": grid_asset.svg_content,
                    "layer": "background",
                    "z_index": 0,
                },
            )

        except Exception as e:
            logger.error(f"Failed to create grid render command: {e}")
            return self._create_error_command("grid", position, target_size)

    def render_prop(
        self,
        prop_type: str,
        color: str,
        position: Point,
        motion_data: Optional[Dict] = None,
    ) -> RenderCommand:
        """Create render command for prop."""
        try:
            prop_asset = self.asset_provider.get_prop_asset(prop_type, "default")
            if not prop_asset:
                logger.warning(f"Prop asset not found: {prop_type}")
                return self._create_error_command("prop", position, Size(50, 200))

            # Apply color transformation
            color_obj = self._parse_color(color)
            colored_svg = prop_asset.get_colored_svg({"fill": color_obj})

            # Calculate size and final position based on motion data
            prop_size = self._calculate_prop_size(motion_data)
            final_position = self._calculate_prop_position(position, motion_data)

            return RenderCommand(
                command_id=self._next_command_id(),
                target_id=f"prop_{self._command_counter}",
                render_type="svg",
                position=final_position,
                size=prop_size,
                properties={
                    "asset_id": prop_asset.asset_id,
                    "svg_content": colored_svg,
                    "layer": "props",
                    "z_index": 10,
                    "prop_type": prop_type,
                    "color": color,
                    "motion_data": motion_data or {},
                },
            )

        except Exception as e:
            logger.error(f"Failed to create prop render command: {e}")
            return self._create_error_command("prop", position, Size(50, 200))

    def render_glyph(
        self, glyph_type: str, glyph_id: str, position: Point, size: Size
    ) -> RenderCommand:
        """Create render command for glyph."""
        try:
            glyph_asset = self.asset_provider.get_glyph_asset(glyph_type, glyph_id)
            if not glyph_asset:
                logger.warning(f"Glyph asset not found: {glyph_type}:{glyph_id}")
                return self._create_error_command("glyph", position, size)

            return RenderCommand(
                command_id=self._next_command_id(),
                target_id=f"glyph_{self._command_counter}",
                render_type="svg",
                position=position,
                size=size,
                properties={
                    "asset_id": glyph_asset.asset_id,
                    "svg_content": glyph_asset.svg_content,
                    "layer": "glyphs",
                    "z_index": 20,
                    "glyph_type": glyph_type,
                    "glyph_id": glyph_id,
                },
            )

        except Exception as e:
            logger.error(f"Failed to create glyph render command: {e}")
            return self._create_error_command("glyph", position, size)

    def _render_arrow(
        self, arrow_type: str, start_pos: Point, end_pos: Point, color: str
    ) -> RenderCommand:
        """Create render command for arrow."""
        try:
            arrow_asset = self.asset_provider.get_arrow_asset(arrow_type)
            if not arrow_asset:
                logger.warning(f"Arrow asset not found: {arrow_type}")
                return self._create_error_command("arrow", start_pos, Size(100, 20))

            # Calculate arrow size and rotation
            arrow_size, rotation = self._calculate_arrow_transform(start_pos, end_pos)
            color_obj = self._parse_color(color)
            colored_svg = arrow_asset.get_colored_svg(
                {"stroke": color_obj, "fill": color_obj}
            )

            return RenderCommand(
                command_id=self._next_command_id(),
                target_id=f"arrow_{self._command_counter}",
                render_type="svg",
                position=start_pos,
                size=arrow_size,
                properties={
                    "asset_id": arrow_asset.asset_id,
                    "svg_content": colored_svg,
                    "layer": "arrows",
                    "z_index": 15,
                    "arrow_type": arrow_type,
                    "rotation": rotation,
                    "start_pos": start_pos,
                    "end_pos": end_pos,
                },
            )

        except Exception as e:
            logger.error(f"Failed to create arrow render command: {e}")
            return self._create_error_command("arrow", start_pos, Size(100, 20))

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def _next_command_id(self) -> str:
        """Generate next command ID."""
        self._command_counter += 1
        return f"cmd_{self._command_counter:04d}"

    def _create_error_command(
        self, item_type: str, position: Point, size: Size
    ) -> RenderCommand:
        """Create error placeholder command."""
        return RenderCommand(
            command_id=self._next_command_id(),
            target_id=f"error_{self._command_counter}",
            render_type="error",
            position=position,
            size=size,
            properties={
                "error": True,
                "item_type": item_type,
                "error_message": f"Failed to render {item_type}",
            },
        )

    def _parse_color(self, color_str: str) -> Color:
        """Parse color string to Color object."""
        try:
            if color_str.startswith("#"):
                return Color.from_hex(color_str)
            elif color_str == "red":
                return Colors.RED
            elif color_str == "blue":
                return Colors.BLUE
            elif color_str == "green":
                return Colors.GREEN
            elif color_str == "black":
                return Colors.BLACK
            else:
                logger.warning(f"Unknown color: {color_str}, using black")
                return Colors.BLACK
        except Exception as e:
            logger.error(f"Failed to parse color {color_str}: {e}")
            return Colors.BLACK

    def _calculate_prop_size(self, motion_data: Optional[Dict]) -> Size:
        """Calculate prop size based on motion data."""
        if not motion_data:
            return Size(50, 200)  # Default staff size

        # Add logic based on motion type, rotation, etc.
        base_width = motion_data.get("width", 50)
        base_height = motion_data.get("height", 200)

        return Size(base_width, base_height)

    def _calculate_prop_position(
        self, base_position: Point, motion_data: Optional[Dict]
    ) -> Point:
        """Calculate final prop position based on motion data."""
        if not motion_data:
            return base_position

        # Add logic for prop positioning based on motion attributes
        offset_x = motion_data.get("offset_x", 0)
        offset_y = motion_data.get("offset_y", 0)

        return base_position.translate(offset_x, offset_y)

    def _calculate_arrow_transform(
        self, start: Point, end: Point
    ) -> tuple[Size, float]:
        """Calculate arrow size and rotation."""
        import math

        # Calculate distance and angle
        dx = end.x - start.x
        dy = end.y - start.y
        length = int(math.sqrt(dx * dx + dy * dy))
        rotation = math.degrees(math.atan2(dy, dx))

        return Size(length, 20), rotation  # 20px height for arrow


# ============================================================================
# REAL ASSET PROVIDER INTEGRATION
# ============================================================================


class RealAssetProvider(IPictographAssetProvider):
    """Real asset provider that integrates with existing TKA asset management."""

    def __init__(self, asset_manager=None):
        """Initialize with existing asset manager."""
        self.asset_manager = asset_manager
        if not self.asset_manager:
            logger.warning("No asset manager provided - assets may not load")

    def get_grid_asset(self, grid_mode: str) -> Optional[SvgAsset]:
        """Get grid asset from real asset system."""
        try:
            if not self.asset_manager:
                logger.error("No asset manager available for grid assets")
                return None

            # Integrate with your existing grid asset loading
            # This should call your real asset loading methods
            asset_path = self._get_grid_asset_path(grid_mode)
            if not asset_path:
                return None

            svg_content = self.asset_manager.load_svg_asset(asset_path)
            if not svg_content:
                return None

            return SvgAsset(
                asset_id=f"grid_{grid_mode}",
                svg_content=svg_content,
                original_size=Size(400, 400),  # Get from your asset metadata
                color_properties=self._extract_color_properties(svg_content),
            )

        except Exception as e:
            logger.error(f"Failed to load grid asset {grid_mode}: {e}")
            return None

    def get_prop_asset(self, prop_type: str, color: str) -> Optional[SvgAsset]:
        """Get prop asset from real asset system."""
        try:
            if not self.asset_manager:
                logger.error("No asset manager available for prop assets")
                return None

            # Integrate with your existing prop asset loading
            asset_path = self._get_prop_asset_path(prop_type)
            if not asset_path:
                return None

            svg_content = self.asset_manager.load_svg_asset(asset_path)
            if not svg_content:
                return None

            return SvgAsset(
                asset_id=f"prop_{prop_type}",
                svg_content=svg_content,
                original_size=Size(50, 200),  # Get from your asset metadata
                color_properties=self._extract_color_properties(svg_content),
            )

        except Exception as e:
            logger.error(f"Failed to load prop asset {prop_type}: {e}")
            return None

    def get_glyph_asset(self, glyph_type: str, glyph_id: str) -> Optional[SvgAsset]:
        """Get glyph asset from real asset system."""
        try:
            if not self.asset_manager:
                logger.error("No asset manager available for glyph assets")
                return None

            # Integrate with your existing glyph asset loading
            asset_path = self._get_glyph_asset_path(glyph_type, glyph_id)
            if not asset_path:
                return None

            svg_content = self.asset_manager.load_svg_asset(asset_path)
            if not svg_content:
                return None

            return SvgAsset(
                asset_id=f"glyph_{glyph_type}_{glyph_id}",
                svg_content=svg_content,
                original_size=Size(50, 50),  # Get from your asset metadata
                color_properties=self._extract_color_properties(svg_content),
            )

        except Exception as e:
            logger.error(f"Failed to load glyph asset {glyph_type}:{glyph_id}: {e}")
            return None

    def get_arrow_asset(self, arrow_type: str) -> Optional[SvgAsset]:
        """Get arrow asset from real asset system."""
        try:
            if not self.asset_manager:
                logger.error("No asset manager available for arrow assets")
                return None

            # Integrate with your existing arrow asset loading
            asset_path = self._get_arrow_asset_path(arrow_type)
            if not asset_path:
                return None

            svg_content = self.asset_manager.load_svg_asset(asset_path)
            if not svg_content:
                return None

            return SvgAsset(
                asset_id=f"arrow_{arrow_type}",
                svg_content=svg_content,
                original_size=Size(100, 20),  # Get from your asset metadata
                color_properties=self._extract_color_properties(svg_content),
            )

        except Exception as e:
            logger.error(f"Failed to load arrow asset {arrow_type}: {e}")
            return None

    def _get_grid_asset_path(self, grid_mode: str) -> Optional[str]:
        """Get path to grid asset - integrate with your asset path logic."""
        # TODO: Replace with your actual grid asset path logic
        grid_paths = {
            "diamond": "assets/grids/diamond_grid.svg",
            "box": "assets/grids/box_grid.svg",
        }
        return grid_paths.get(grid_mode)

    def _get_prop_asset_path(self, prop_type: str) -> Optional[str]:
        """Get path to prop asset - integrate with your asset path logic."""
        # TODO: Replace with your actual prop asset path logic
        prop_paths = {
            "staff": "assets/props/staff.svg",
            "club": "assets/props/club.svg",
            "fan": "assets/props/fan.svg",
        }
        return prop_paths.get(prop_type.lower())

    def _get_glyph_asset_path(self, glyph_type: str, glyph_id: str) -> Optional[str]:
        """Get path to glyph asset - integrate with your asset path logic."""
        # TODO: Replace with your actual glyph asset path logic
        return f"assets/glyphs/{glyph_type}/{glyph_id}.svg"

    def _get_arrow_asset_path(self, arrow_type: str) -> Optional[str]:
        """Get path to arrow asset - integrate with your asset path logic."""
        # TODO: Replace with your actual arrow asset path logic
        arrow_paths = {
            "motion": "assets/arrows/motion_arrow.svg",
            "static": "assets/arrows/static_arrow.svg",
        }
        return arrow_paths.get(arrow_type)

    def _extract_color_properties(self, svg_content: str) -> Dict[str, str]:
        """Extract color properties from SVG content."""
        # Simple extraction - you might want to use proper XML parsing
        color_properties = {}

        if "fill=" in svg_content:
            # Extract fill colors
            import re

            fills = re.findall(r'fill=["\']([^"\']*)["\']', svg_content)
            if fills:
                color_properties["fill"] = fills[0]

        if "stroke=" in svg_content:
            # Extract stroke colors
            import re

            strokes = re.findall(r'stroke=["\']([^"\']*)["\']', svg_content)
            if strokes:
                color_properties["stroke"] = strokes[0]

        return color_properties


# ============================================================================
# FACTORY FUNCTION
# ============================================================================


def create_pictograph_renderer(
    asset_provider: Optional[IPictographAssetProvider] = None, asset_manager=None
) -> CorePictographRenderer:
    """
    Factory function to create pictograph renderer.

    Args:
        asset_provider: Asset provider implementation (creates real provider if None)
        asset_manager: Existing asset manager to integrate with

    Returns:
        Configured pictograph renderer
    """
    if asset_provider is None:
        asset_provider = RealAssetProvider(asset_manager)
        logger.info("Created real asset provider for pictograph renderer")

    return CorePictographRenderer(asset_provider)
