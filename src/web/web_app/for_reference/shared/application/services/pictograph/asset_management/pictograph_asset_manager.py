"""
SVG asset management microservice for pictograph rendering.

This service handles:
- SVG file loading with caching
- Color transformations for props and other elements
- Asset path resolution
- File existence validation
"""

import logging
import os
import re
from functools import lru_cache

from desktop.modern.core.interfaces.pictograph_rendering_services import (
    IPictographAssetManager,
)
from desktop.modern.domain.models import MotionData
from shared.application.services.assets.image_asset_utils import get_image_path
from shared.application.services.core.types import Size, SvgAsset

logger = logging.getLogger(__name__)


class PictographAssetManager(IPictographAssetManager):
    """
    Microservice for managing pictograph SVG assets.

    Provides:
    - Cached SVG file loading
    - Color transformations for props
    - Asset path resolution for all pictograph elements
    - File existence validation
    """

    def __init__(self):
        """Initialize the asset manager with color mappings."""
        # Color mapping for SVG transformations
        self._color_map = {
            "blue": "#2E3192",  # Reference blue color
            "red": "#ED1C24",  # Reference red color
        }

        # Cached colored SVG data to avoid repeated transformations
        self._colored_svg_cache: dict[str, str] = {}

        # Performance statistics
        self._stats = {
            "svg_files_loaded": 0,
            "color_transformations": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }

    def get_grid_svg_path(self, grid_mode: str) -> str:
        """Get file path for grid SVG based on mode."""
        if grid_mode == "box":
            return get_image_path("grid/box_grid.svg")
        else:  # Default to diamond
            return get_image_path("grid/diamond_grid.svg")

    def get_prop_svg_path(self, prop_type: str) -> str:
        """Get file path for prop SVG based on type."""
        # Currently only staff props are supported
        return get_image_path("props/staff.svg")

    def get_arrow_svg_path(self, motion_data: MotionData, color: str) -> str:
        """Get file path for arrow SVG based on motion data and color."""
        # TODO: Implement arrow SVG path resolution
        # This will need to integrate with the existing arrow rendering service
        logger.debug(
            f"🏹 [ASSET_MANAGER] Arrow SVG path requested for {motion_data.motion_type} {color}"
        )
        return ""

    def get_glyph_svg_path(self, glyph_type: str, glyph_data) -> str:
        """Get file path for glyph SVG based on type and data."""
        if glyph_type == "letter":
            # Handle letter glyphs - they are organized by type
            letter = glyph_data if isinstance(glyph_data, str) else str(glyph_data)

            # Try different type folders for the letter
            type_folders = [
                "Type1",
                "Type2",
                "Type3",
                "Type4",
                "Type5",
                "Type6",
                "Type7",
                "Type8",
                "Type9",
            ]
            for type_folder in type_folders:
                path = get_image_path(f"letters_trimmed/{type_folder}/{letter}.svg")
                if self.svg_path_exists(path):
                    return path

            # Fallback to direct path
            return get_image_path(f"letters_trimmed/{letter}.svg")
        elif glyph_type == "vtg":
            return get_image_path("vtg_glyphs/vtg.svg")
        elif glyph_type == "tka":
            return get_image_path("letters_trimmed/TKA.svg")
        else:
            logger.warning(f"🔤 [ASSET_MANAGER] Unknown glyph type: {glyph_type}")
            return ""

    @lru_cache(maxsize=64)
    def load_svg_data(self, svg_path: str) -> str | None:
        """Load SVG file with LRU caching for performance."""
        try:
            with open(svg_path, encoding="utf-8") as file:
                content = file.read()
                self._stats["svg_files_loaded"] += 1
                logger.debug(f"📁 [ASSET_MANAGER] Loaded SVG file: {svg_path}")
                return content
        except Exception as e:
            logger.error(f"❌ [ASSET_MANAGER] Failed to load SVG file {svg_path}: {e}")
            return None

    def apply_color_transformation(self, svg_data: str, color: str) -> str:
        """Apply color transformation to SVG data."""
        if color not in self._color_map:
            logger.warning(
                f"⚠️ [ASSET_MANAGER] Unknown color: {color}, using original SVG"
            )
            return svg_data

        # Cache key for colored SVG
        cache_key = f"{hash(svg_data)}_{color}"
        if cache_key in self._colored_svg_cache:
            self._stats["cache_hits"] += 1
            return self._colored_svg_cache[cache_key]

        self._stats["cache_misses"] += 1

        # Apply EXACT LEGACY color transformation
        # Replicates legacy SvgColorHandler.apply_color_transformations
        target_color = self._color_map[color]
        colored_svg = svg_data

        # Legacy patterns from SvgColorHandler (EXACT COPY)
        class_color_pattern = re.compile(
            r"(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)(#[a-fA-F0-9]{6})([^}]*?\})"
        )
        fill_pattern = re.compile(r'(fill=")(#[a-fA-F0-9]{6})(")')

        def replace_class_color(match):
            # For class patterns: group(1) + new_color + group(4)
            return match.group(1) + target_color + match.group(4)

        def replace_fill_color(match):
            # For fill patterns: group(1) + new_color + group(3)
            return match.group(1) + target_color + match.group(3)

        # Apply legacy transformations (EXACT ORDER)
        colored_svg = class_color_pattern.sub(replace_class_color, colored_svg)
        colored_svg = fill_pattern.sub(replace_fill_color, colored_svg)

        # Cache the result
        self._colored_svg_cache[cache_key] = colored_svg
        self._stats["color_transformations"] += 1

        logger.debug(f"🎨 [ASSET_MANAGER] Applied {color} color transformation")
        return colored_svg

    def svg_path_exists(self, svg_path: str) -> bool:
        """Check if SVG file exists."""
        return os.path.exists(svg_path)

    def get_supported_colors(self) -> list[str]:
        """Get list of supported colors for transformations."""
        return list(self._color_map.keys())

    def add_color_mapping(self, color_name: str, hex_color: str) -> None:
        """Add a new color mapping for transformations."""
        self._color_map[color_name] = hex_color
        logger.info(
            f"🎨 [ASSET_MANAGER] Added color mapping: {color_name} -> {hex_color}"
        )

    def clear_color_cache(self) -> None:
        """Clear the colored SVG cache."""
        self._colored_svg_cache.clear()
        logger.info("🧹 [ASSET_MANAGER] Cleared color transformation cache")

    def get_asset_stats(self) -> dict[str, int]:
        """Get asset management statistics."""
        return {
            "svg_files_loaded": self._stats["svg_files_loaded"],
            "color_transformations": self._stats["color_transformations"],
            "cache_hits": self._stats["cache_hits"],
            "cache_misses": self._stats["cache_misses"],
            "colored_svg_cache_size": len(self._colored_svg_cache),
            "supported_colors": len(self._color_map),
        }

    def create_fallback_grid_svg(self, grid_mode: str) -> str:
        """Create fallback grid SVG when file loading fails."""
        fallback_svg = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
            <rect x="10" y="10" width="180" height="180" fill="none" stroke="black" stroke-width="2"/>
            <line x1="100" y1="10" x2="100" y2="190" stroke="black" stroke-width="1"/>
            <line x1="10" y1="100" x2="190" y2="100" stroke="black" stroke-width="1"/>
            <text x="100" y="100" text-anchor="middle" font-size="12" fill="gray">Grid</text>
        </svg>
        """
        logger.debug(f"🔧 [ASSET_MANAGER] Created fallback {grid_mode} grid SVG")
        return fallback_svg.strip()

    def create_fallback_prop_svg(self, color: str) -> str:
        """Create fallback prop SVG when file loading fails."""
        prop_color = self._color_map.get(color, "#000000")
        fallback_svg = f"""
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="30" fill="{prop_color}" stroke="black" stroke-width="2"/>
            <text x="50" y="55" text-anchor="middle" font-size="10" fill="white">Prop</text>
        </svg>
        """
        logger.debug(f"🔧 [ASSET_MANAGER] Created fallback {color} prop SVG")
        return fallback_svg.strip()

    # Additional methods expected by QtAssetProvider
    def get_grid_svg_path(self, grid_mode: str) -> str:
        """Get file path for grid SVG based on mode."""
        if grid_mode == "diamond":
            return get_image_path("grid/diamond_grid.svg")
        elif grid_mode == "box":
            return get_image_path("grid/box_grid.svg")
        else:
            logger.warning(f"🔲 [ASSET_MANAGER] Unknown grid mode: {grid_mode}")
            return ""

    def get_prop_svg(self, prop_type: str) -> str | None:
        """Get prop SVG content directly."""
        svg_path = self.get_prop_svg_path(prop_type)
        if svg_path and self.svg_path_exists(svg_path):
            return self.load_svg_data(svg_path)
        else:
            # Return fallback SVG for props
            logger.debug(f"🔧 [ASSET_MANAGER] Using fallback for prop: {prop_type}")
            return self.create_fallback_prop_svg("blue")  # Default color

    def get_glyph_svg(self, glyph_type: str, glyph_id: str) -> str | None:
        """Get glyph SVG content directly."""
        svg_path = self.get_glyph_svg_path(glyph_type, glyph_id)
        if svg_path and self.svg_path_exists(svg_path):
            return self.load_svg_data(svg_path)
        else:
            logger.debug(
                f"🔧 [ASSET_MANAGER] No glyph found for: {glyph_type}:{glyph_id}"
            )
            return None

    def get_grid_svg(self, grid_mode: str) -> str | None:
        """Get grid SVG content directly."""
        svg_path = self.get_grid_svg_path(grid_mode)
        if svg_path and self.svg_path_exists(svg_path):
            return self.load_svg_data(svg_path)
        else:
            # Return fallback SVG for grids
            logger.debug(f"🔧 [ASSET_MANAGER] Using fallback for grid: {grid_mode}")
            return self.create_fallback_grid_svg(grid_mode)

    def get_prop_asset(self, prop_type: str, color: str) -> SvgAsset | None:
        """Get prop asset as SvgAsset object for framework-agnostic renderer."""
        try:
            # Get SVG content
            svg_content = self.get_prop_svg(prop_type)
            if not svg_content:
                logger.debug(f"🔧 [ASSET_MANAGER] No prop SVG found for: {prop_type}")
                return None

            # Apply color transformation if needed
            if color and color != "default":
                svg_content = self.apply_color_transformation(svg_content, color)

            # Create SvgAsset object
            return SvgAsset(
                asset_id=f"prop_{prop_type}_{color}",
                svg_content=svg_content,
                original_size=Size(253, 78),  # Natural staff.svg dimensions
                color_properties={"fill": self._color_map.get(color, "#000000")},
            )

        except Exception as e:
            logger.error(
                f"❌ [ASSET_MANAGER] Failed to get prop asset {prop_type}/{color}: {e}"
            )
            return None

    def get_grid_asset(self, grid_mode: str) -> SvgAsset | None:
        """Get grid asset as SvgAsset object for framework-agnostic renderer."""
        try:
            svg_content = self.get_grid_svg(grid_mode)
            if not svg_content:
                return None

            return SvgAsset(
                asset_id=f"grid_{grid_mode}",
                svg_content=svg_content,
                original_size=Size(950, 950),  # Standard grid size
                color_properties={},
            )

        except Exception as e:
            logger.error(
                f"❌ [ASSET_MANAGER] Failed to get grid asset {grid_mode}: {e}"
            )
            return None

    def get_glyph_asset(self, glyph_type: str, glyph_id: str) -> SvgAsset | None:
        """Get glyph asset as SvgAsset object for framework-agnostic renderer."""
        try:
            svg_content = self.get_glyph_svg(glyph_type, glyph_id)
            if not svg_content:
                return None

            return SvgAsset(
                asset_id=f"glyph_{glyph_type}_{glyph_id}",
                svg_content=svg_content,
                original_size=Size(50, 50),  # Standard glyph size
                color_properties={},
            )

        except Exception as e:
            logger.error(
                f"❌ [ASSET_MANAGER] Failed to get glyph asset {glyph_type}/{glyph_id}: {e}"
            )
            return None
