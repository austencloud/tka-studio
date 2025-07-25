"""
Real Asset Provider - Framework Agnostic

Integrates with TKA's existing asset management system to provide SVG content
without Qt dependencies. This bridges the core rendering service with your
existing asset infrastructure.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from .core_pictograph_rendering_service import IAssetProvider

logger = logging.getLogger(__name__)


class RealAssetProvider(IAssetProvider):
    """
    Real asset provider that integrates with existing TKA asset management.

    This provider loads actual SVG files and applies color transformations
    without any Qt dependencies, making it usable in web services and
    headless environments.
    """

    def __init__(self, assets_base_path: Optional[str] = None):
        """Initialize with base path to assets."""
        self._assets_base_path = (
            Path(assets_base_path)
            if assets_base_path
            else self._get_default_assets_path()
        )
        self._svg_cache: Dict[str, str] = {}

    def get_grid_svg(self, grid_mode: str) -> Optional[str]:
        """Get grid SVG content."""
        try:
            cache_key = f"grid_{grid_mode}"
            if cache_key in self._svg_cache:
                return self._svg_cache[cache_key]

            # Construct path to grid SVG
            grid_path = self._assets_base_path / "images" / "grids" / f"{grid_mode}.svg"

            if not grid_path.exists():
                logger.warning(f"Grid SVG not found: {grid_path}")
                return None

            svg_content = grid_path.read_text(encoding="utf-8")
            self._svg_cache[cache_key] = svg_content
            return svg_content

        except Exception as e:
            logger.error(f"Failed to load grid SVG for {grid_mode}: {e}")
            return None

    def get_prop_svg(self, prop_type: str, color: str) -> Optional[str]:
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

    def get_arrow_svg(self, arrow_data: Dict[str, Any]) -> Optional[str]:
        """Get arrow SVG content."""
        try:
            # Create cache key from arrow data
            motion_type = arrow_data.get("motion_type", "pro")
            color = arrow_data.get("color", "blue")
            cache_key = f"arrow_{motion_type}_{color}"

            if cache_key in self._svg_cache:
                return self._svg_cache[cache_key]

            # Construct path to arrow SVG
            arrow_path = (
                self._assets_base_path / "images" / "arrows" / f"{motion_type}.svg"
            )

            if not arrow_path.exists():
                logger.warning(f"Arrow SVG not found: {arrow_path}")
                return None

            base_svg = arrow_path.read_text(encoding="utf-8")

            # Apply color transformation
            colored_svg = self._apply_color_transformation(base_svg, color)

            self._svg_cache[cache_key] = colored_svg
            return colored_svg

        except Exception as e:
            logger.error(f"Failed to load arrow SVG: {e}")
            return None

    def get_glyph_svg(
        self, glyph_type: str, glyph_data: Dict[str, Any]
    ) -> Optional[str]:
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

        This replicates the color transformation logic from your existing
        asset management without Qt dependencies.
        """
        try:
            # Define color mappings
            color_map = {
                "blue": "#0066ff",
                "red": "#ff0000",
                "green": "#00ff00",
                "purple": "#800080",
                "orange": "#ff8000",
                "yellow": "#ffff00",
            }

            target_color = color_map.get(color.lower(), color)

            # Simple color replacement (can be made more sophisticated)
            # Replace common SVG color attributes
            transformations = [
                ('fill="black"', f'fill="{target_color}"'),
                ('stroke="black"', f'stroke="{target_color}"'),
                ('fill="#000000"', f'fill="{target_color}"'),
                ('stroke="#000000"', f'stroke="{target_color}"'),
                # Add more transformations as needed
            ]

            result = svg_content
            for old, new in transformations:
                result = result.replace(old, new)

            return result

        except Exception as e:
            logger.error(f"Failed to apply color transformation for {color}: {e}")
            return svg_content

    def _get_default_assets_path(self) -> Path:
        """Get default path to TKA assets."""
        # This should point to your actual assets directory
        # Adjust based on your project structure
        try:
            # Try to find assets relative to this file
            current_file = Path(__file__)

            # Navigate up to find the TKA root
            tka_root = current_file
            while tka_root.name != "TKA" and tka_root.parent != tka_root:
                tka_root = tka_root.parent

            if tka_root.name == "TKA":
                return tka_root

            # Fallback to current working directory
            return Path.cwd()

        except Exception as e:
            logger.warning(f"Could not determine assets path: {e}")
            return Path.cwd()

    def clear_cache(self):
        """Clear the SVG cache."""
        self._svg_cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "cached_items": len(self._svg_cache),
            "cache_keys": list(self._svg_cache.keys()),
        }


# Factory function for easy creation
def create_real_asset_provider(
    assets_base_path: Optional[str] = None,
) -> RealAssetProvider:
    """Create real asset provider with optional base path."""
    return RealAssetProvider(assets_base_path)
