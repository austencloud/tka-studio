"""
Real Asset Provider - Framework Agnostic

Integrates with TKA's existing asset management system to provide SVG content
without Qt dependencies. This bridges the core rendering service with your
existing asset infrastructure.
"""

import logging
from pathlib import Path
from typing import Any

from desktop.modern.application.services.core.types import Size, SvgAsset

from .core_pictograph_rendering_service import IAssetProvider

logger = logging.getLogger(__name__)


class RealAssetProvider(IAssetProvider):
    """
    Real asset provider that integrates with existing TKA asset management.

    This provider loads actual SVG files and applies color transformations
    without any Qt dependencies, making it usable in web services and
    headless environments.
    """

    def __init__(self, assets_base_path: str | None = None):
        """Initialize with base path to assets."""
        self._assets_base_path = (
            Path(assets_base_path)
            if assets_base_path
            else self._get_default_assets_path()
        )
        self._svg_cache: dict[str, str] = {}

    def get_grid_svg(self, grid_mode: str) -> str | None:
        """Get grid SVG content."""
        try:
            cache_key = f"grid_{grid_mode}"
            if cache_key in self._svg_cache:
                return self._svg_cache[cache_key]

            # Construct path to grid SVG
            grid_path = (
                self._assets_base_path / "images" / "grid" / f"{grid_mode}_grid.svg"
            )

            if not grid_path.exists():
                logger.warning(f"Grid SVG not found: {grid_path}")
                return None

            svg_content = grid_path.read_text(encoding="utf-8")
            self._svg_cache[cache_key] = svg_content
            return svg_content

        except Exception as e:
            logger.error(f"Failed to load grid SVG for {grid_mode}: {e}")
            return None

    def get_prop_svg(self, prop_type: str, color: str) -> str | None:
        """Get prop SVG content with color applied."""
        try:
            cache_key = f"prop_{prop_type}_{color}"
            if cache_key in self._svg_cache:
                return self._svg_cache[cache_key]

            # Load base prop SVG
            prop_path = self._assets_base_path / "images" / "props" / f"{prop_type}.svg"

            if not prop_path.exists():
                logger.warning(f"Prop SVG not found: {prop_path}")
                return None

            base_svg = prop_path.read_text(encoding="utf-8")

            # Apply color transformation
            colored_svg = self._apply_color_transformation(base_svg, color)

            self._svg_cache[cache_key] = colored_svg
            return colored_svg

        except Exception as e:
            logger.error(f"Failed to load prop SVG for {prop_type}/{color}: {e}")
            return None

    def get_arrow_svg(self, arrow_data: dict[str, Any]) -> str | None:
        """Get arrow SVG content."""
        try:
            # Extract arrow properties
            motion_type = arrow_data.get("motion_type", "pro")
            color = arrow_data.get("color", "blue")
            turns = arrow_data.get("turns", 0.0)

            cache_key = f"arrow_{motion_type}_{color}_{turns}"

            if cache_key in self._svg_cache:
                return self._svg_cache[cache_key]

            # Format turns for filename
            turns_str = f"{turns:.1f}"

            # Construct path based on motion type and actual directory structure
            if motion_type == "static":
                arrow_path = (
                    self._assets_base_path
                    / "images"
                    / "arrows_colored"
                    / "static"
                    / color
                    / "from_radial"
                    / f"static_{turns_str}.svg"
                )
            elif motion_type == "pro":
                arrow_path = (
                    self._assets_base_path
                    / "images"
                    / "arrows_colored"
                    / "pro"
                    / color
                    / "from_radial"
                    / f"pro_{turns_str}.svg"
                )
            elif motion_type == "anti":
                arrow_path = (
                    self._assets_base_path
                    / "images"
                    / "arrows_colored"
                    / "anti"
                    / color
                    / "from_radial"
                    / f"anti_{turns_str}.svg"
                )
            elif motion_type == "dash":
                arrow_path = (
                    self._assets_base_path
                    / "images"
                    / "arrows_colored"
                    / "dash"
                    / color
                    / "from_radial"
                    / f"dash_{turns_str}.svg"
                )
            elif motion_type == "float":
                arrow_path = (
                    self._assets_base_path
                    / "images"
                    / "arrows_colored"
                    / color
                    / "float.svg"
                )
            else:
                # Fallback to basic arrows directory
                arrow_path = (
                    self._assets_base_path / "images" / "arrows" / f"{motion_type}.svg"
                )

            if not arrow_path.exists():
                logger.warning(f"Arrow SVG not found: {arrow_path}")
                # Try fallback without color transformation
                fallback_path = (
                    self._assets_base_path
                    / "images"
                    / "arrows"
                    / f"{motion_type}"
                    / "from_radial"
                    / f"{motion_type}_{turns_str}.svg"
                )
                if fallback_path.exists():
                    arrow_path = fallback_path
                else:
                    return None

            base_svg = arrow_path.read_text(encoding="utf-8")

            # For arrows_colored, the SVG should already have the color
            # For fallback arrows, apply color transformation
            if "arrows_colored" in str(arrow_path):
                colored_svg = base_svg  # Already colored
            else:
                colored_svg = self._apply_color_transformation(base_svg, color)

            self._svg_cache[cache_key] = colored_svg
            return colored_svg

        except Exception as e:
            logger.error(f"Failed to load arrow SVG: {e}")
            return None

    def get_glyph_svg(self, glyph_type: str, glyph_data: dict[str, Any]) -> str | None:
        """Get glyph SVG content."""
        try:
            if glyph_type == "letter":
                letter = glyph_data.get("letter", "A")
                cache_key = f"glyph_letter_{letter}"

                if cache_key in self._svg_cache:
                    return self._svg_cache[cache_key]

                # Construct path to letter glyph
                letter_path = (
                    self._assets_base_path
                    / "images"
                    / "glyphs"
                    / "letters"
                    / f"{letter}.svg"
                )

                if not letter_path.exists():
                    logger.warning(f"Letter glyph SVG not found: {letter_path}")
                    return None

                svg_content = letter_path.read_text(encoding="utf-8")
                self._svg_cache[cache_key] = svg_content
                return svg_content

            # Handle other glyph types (elemental, VTG, TKA, etc.)
            # This can be expanded as needed

            return None

        except Exception as e:
            logger.error(f"Failed to load glyph SVG for {glyph_type}: {e}")
            return None

    def _apply_color_transformation(self, svg_content: str, color: str) -> str:
        """
        Apply color transformation to SVG content.

        This replicates the color transformation logic from the legacy system
        to ensure consistent prop colors across legacy and modern applications.
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
            logger.error(f"Failed to apply color transformation for {color}: {e}")
            return svg_content

    def _get_default_assets_path(self) -> Path:
        """Get default path to TKA desktop assets using centralized resolver."""
        try:
            from desktop.modern.infrastructure.path_resolver import path_resolver

            return path_resolver.desktop_root
        except Exception as e:
            logger.warning(f"Could not use centralized path resolver: {e}")
            # Fallback to manual discovery
            current_file = Path(__file__)
            desktop_root = current_file
            while (
                desktop_root.name != "desktop" and desktop_root.parent != desktop_root
            ):
                desktop_root = desktop_root.parent

            if desktop_root.name == "desktop":
                return desktop_root

            return Path.cwd()

    def clear_cache(self):
        """Clear the SVG cache."""
        self._svg_cache.clear()

    def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        return {
            "cached_items": len(self._svg_cache),
            "cache_keys": list(self._svg_cache.keys()),
        }

    # ============================================================================
    # IPictographAssetProvider COMPATIBILITY METHODS
    # ============================================================================

    def get_prop_asset(
        self, prop_type: str, color: str, pictograph_data: dict | None = None
    ) -> SvgAsset | None:
        """Get prop asset as SvgAsset object (IPictographAssetProvider compatibility)."""
        try:
            # Get colored SVG content
            svg_content = self.get_prop_svg(prop_type, color)
            if not svg_content:
                logger.debug(
                    f"🔧 [REAL_ASSET_PROVIDER] No prop SVG found for: {prop_type}/{color}"
                )
                return None

            # Create SvgAsset object
            return SvgAsset(
                asset_id=f"prop_{prop_type}_{color}",
                svg_content=svg_content,
                original_size=Size(253, 78),  # Natural staff.svg dimensions
                color_properties={"fill": self._get_color_hex(color)},
            )

        except Exception as e:
            logger.error(f"Failed to get prop asset for {prop_type}/{color}: {e}")
            return None

    def get_grid_asset(self, grid_mode: str) -> SvgAsset | None:
        """Get grid asset (IPictographAssetProvider compatibility)."""
        try:
            svg_content = self.get_grid_svg(grid_mode)
            if not svg_content:
                return None

            return SvgAsset(
                asset_id=f"grid_{grid_mode}",
                svg_content=svg_content,
                original_size=Size(400, 400),
                color_properties={},
            )
        except Exception as e:
            logger.error(f"Failed to get grid asset for {grid_mode}: {e}")
            return None

    def get_glyph_asset(self, glyph_type: str, glyph_id: str) -> SvgAsset | None:
        """Get glyph asset (IPictographAssetProvider compatibility)."""
        try:
            glyph_data = (
                {"letter": glyph_id} if glyph_type == "letter" else {"id": glyph_id}
            )
            svg_content = self.get_glyph_svg(glyph_type, glyph_data)
            if not svg_content:
                return None

            return SvgAsset(
                asset_id=f"glyph_{glyph_type}_{glyph_id}",
                svg_content=svg_content,
                original_size=Size(50, 50),
                color_properties={},
            )
        except Exception as e:
            logger.error(f"Failed to get glyph asset for {glyph_type}:{glyph_id}: {e}")
            return None

    def get_arrow_asset(self, arrow_type: str) -> SvgAsset | None:
        """Get arrow asset (IPictographAssetProvider compatibility)."""
        try:
            arrow_data = {"motion_type": arrow_type, "color": "blue"}
            svg_content = self.get_arrow_svg(arrow_data)
            if not svg_content:
                return None

            return SvgAsset(
                asset_id=f"arrow_{arrow_type}",
                svg_content=svg_content,
                original_size=Size(100, 20),
                color_properties={},
            )
        except Exception as e:
            logger.error(f"Failed to get arrow asset for {arrow_type}: {e}")
            return None

    def _get_color_hex(self, color: str) -> str:
        """Get hex color value for color name."""
        from data.constants import BLUE, HEX_BLUE, HEX_RED, RED

        COLOR_MAP = {RED: HEX_RED, BLUE: HEX_BLUE}

        if color and color.startswith("#"):
            return color
        else:
            color_lower = color.lower()
            if color_lower == "red":
                return COLOR_MAP.get(RED, "#ED1C24")
            elif color_lower == "blue":
                return COLOR_MAP.get(BLUE, "#2E3192")
            else:
                return COLOR_MAP.get(color, "#000000")


# Factory function for easy creation
def create_real_asset_provider(
    assets_base_path: str | None = None,
) -> RealAssetProvider:
    """Create real asset provider with optional base path."""
    return RealAssetProvider(assets_base_path)
