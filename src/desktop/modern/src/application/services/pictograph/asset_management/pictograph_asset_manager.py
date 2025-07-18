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
from typing import Dict, Optional

from application.services.assets.image_asset_utils import get_image_path
from core.interfaces.pictograph_rendering_services import IPictographAssetManager
from domain.models import MotionData

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
            "red": "#ED1C24",   # Reference red color
        }
        
        # Cached colored SVG data to avoid repeated transformations
        self._colored_svg_cache: Dict[str, str] = {}
        
        # Performance statistics
        self._stats = {
            "svg_files_loaded": 0,
            "color_transformations": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }
        
        logger.info("🎨 [ASSET_MANAGER] Initialized pictograph asset manager")

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
        logger.debug(f"🏹 [ASSET_MANAGER] Arrow SVG path requested for {motion_data.motion_type} {color}")
        return ""

    def get_glyph_svg_path(self, glyph_type: str, glyph_data) -> str:
        """Get file path for glyph SVG based on type and data."""
        # TODO: Implement glyph SVG path resolution
        logger.debug(f"🔤 [ASSET_MANAGER] Glyph SVG path requested for {glyph_type}")
        return ""

    @lru_cache(maxsize=64)
    def load_svg_data(self, svg_path: str) -> Optional[str]:
        """Load SVG file with LRU caching for performance."""
        try:
            with open(svg_path, "r", encoding="utf-8") as file:
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
            logger.warning(f"⚠️ [ASSET_MANAGER] Unknown color: {color}, using original SVG")
            return svg_data

        # Cache key for colored SVG
        cache_key = f"{hash(svg_data)}_{color}"
        if cache_key in self._colored_svg_cache:
            self._stats["cache_hits"] += 1
            return self._colored_svg_cache[cache_key]

        self._stats["cache_misses"] += 1

        # Apply color transformation (simple replacement for now)
        target_color = self._color_map[color]
        colored_svg = svg_data

        # Replace fill colors
        colored_svg = re.sub(r'fill="[^"]*"', f'fill="{target_color}"', colored_svg)
        colored_svg = re.sub(r"fill:[^;]*;", f"fill:{target_color};", colored_svg)

        # Replace stroke colors
        colored_svg = re.sub(r'stroke="[^"]*"', f'stroke="{target_color}"', colored_svg)
        colored_svg = re.sub(r"stroke:[^;]*;", f"stroke:{target_color};", colored_svg)

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
        logger.info(f"🎨 [ASSET_MANAGER] Added color mapping: {color_name} -> {hex_color}")

    def clear_color_cache(self) -> None:
        """Clear the colored SVG cache."""
        self._colored_svg_cache.clear()
        logger.info("🧹 [ASSET_MANAGER] Cleared color transformation cache")

    def get_asset_stats(self) -> Dict[str, int]:
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
