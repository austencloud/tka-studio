"""
Asset Manager Service

Manages SVG assets, file paths, and color transformations for pictograph rendering.
Framework-agnostic service that handles asset loading, caching, and color transformations.
"""

import logging
import os
import re
from functools import lru_cache

from desktop.modern.core.interfaces.core_services import IAssetManager
from desktop.modern.domain.models import MotionData, MotionType
from shared.application.services.assets.image_asset_utils import get_image_path

logger = logging.getLogger(__name__)


class AssetManager(IAssetManager):
    """
    Manages SVG assets, file paths, and color transformations.

    Provides centralized asset management for pictograph rendering components,
    including SVG file path generation, color transformations, and caching.
    """

    # Class-level cache statistics for monitoring
    _cache_stats: dict[str, int] = {"hits": 0, "misses": 0, "total_files_cached": 0}

    # Track cached files for cache management
    _cached_files: set[str] = set()

    # Color mapping for SVG transformations
    COLOR_MAP = {
        "blue": "#2E3192",  # Reference blue color
        "red": "#ED1C24",  # Reference red color
    }

    def __init__(self):
        """Initialize the asset manager and warm the cache."""
        self._preload_common_assets()

    def get_arrow_svg_path(self, motion_data: MotionData, color: str) -> str:
        """
        Generate SVG file path for arrow assets based on motion type and color.

        Args:
            motion_data: Motion data containing type and turns information
            color: Arrow color ("blue" or "red")

        Returns:
            String path to the appropriate SVG asset file
        """
        turns_str = f"{motion_data.turns:.1f}"

        if motion_data.motion_type == MotionType.STATIC:
            return get_image_path(
                f"arrows_colored/static/{color}/from_radial/static_{turns_str}.svg"
            )
        elif motion_data.motion_type == MotionType.PRO:
            return get_image_path(
                f"arrows_colored/pro/{color}/from_radial/pro_{turns_str}.svg"
            )
        elif motion_data.motion_type == MotionType.ANTI:
            return get_image_path(
                f"arrows_colored/anti/{color}/from_radial/anti_{turns_str}.svg"
            )
        elif motion_data.motion_type == MotionType.DASH:
            return get_image_path(
                f"arrows_colored/dash/{color}/from_radial/dash_{turns_str}.svg"
            )
        elif motion_data.motion_type == MotionType.FLOAT:
            return get_image_path(f"arrows_colored/{color}/float.svg")
        else:
            # Fallback to static for unknown motion types
            logger.warning(
                f"Unknown motion type: {motion_data.motion_type}, using static fallback"
            )
            return get_image_path(
                f"arrows_colored/static/{color}/from_radial/static_{turns_str}.svg"
            )

    def get_fallback_arrow_svg_path(self, motion_data: MotionData) -> str:
        """
        Generate fallback SVG file path for original (non-colored) arrow assets.

        Args:
            motion_data: Motion data containing type and turns information

        Returns:
            String path to the fallback SVG asset file
        """
        turns_str = f"{motion_data.turns:.1f}"

        if motion_data.motion_type == MotionType.STATIC:
            return get_image_path(f"arrows/static/from_radial/static_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.PRO:
            return get_image_path(f"arrows/pro/from_radial/pro_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.ANTI:
            return get_image_path(f"arrows/anti/from_radial/anti_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.DASH:
            return get_image_path(f"arrows/dash/from_radial/dash_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.FLOAT:
            return get_image_path("arrows/float.svg")
        else:
            # Fallback to static for unknown motion types
            logger.warning(
                f"Unknown motion type: {motion_data.motion_type}, using static fallback"
            )
            return get_image_path(f"arrows/static/from_radial/static_{turns_str}.svg")

    def get_prop_asset_path(self, prop_type: str, color: str | None = None) -> str:
        """
        Generate prop asset file path.

        Args:
            prop_type: Type of prop (e.g., "staff")
            color: Optional color specification

        Returns:
            String path to the prop asset file
        """
        # For now, only staff props are supported
        if prop_type == "staff":
            return get_image_path("props/staff.svg")
        else:
            logger.warning(f"Unknown prop type: {prop_type}, using staff fallback")
            return get_image_path("props/staff.svg")

    def svg_path_exists(self, path: str) -> bool:
        """Check if SVG file exists at the given path."""
        return os.path.exists(path)

    def apply_color_transformation(self, svg_data: str, color: str) -> str:
        """
        Apply color transformation to SVG content using regex patterns.

        Args:
            svg_data: Original SVG content as string
            color: Target color ("blue" or "red")

        Returns:
            Transformed SVG content with applied color
        """
        if not svg_data:
            return svg_data

        target_color = self.COLOR_MAP.get(color.lower(), "#2E3192")  # Default to blue

        # Pattern to match CSS fill properties in SVG
        # This matches both fill attributes and CSS style properties
        patterns = [
            # CSS fill property: fill="#color"
            re.compile(r'(fill=")([^"]*)(")'),
            # CSS style attribute: fill: #color;
            re.compile(r"(fill:\s*)([^;]*)(;)"),
            # Class definition: .st0 { fill: #color; } or .cls-1 { fill: #color; }
            re.compile(r"(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)([^;}]*)([^}]*?\})"),
        ]

        # Apply color transformation using all patterns
        for pattern in patterns:
            svg_data = pattern.sub(
                lambda m: m.group(1) + target_color + m.group(len(m.groups())), svg_data
            )

        return svg_data

    def load_and_cache_asset(self, path: str) -> str:
        """
        Load SVG file with LRU caching for performance.

        Args:
            path: File path to the SVG asset

        Returns:
            SVG content as string
        """
        # Check if file is already cached
        if path in self._cached_files:
            self._cache_stats["hits"] += 1
            logger.debug(f"Cache hit for SVG file: {path}")
        else:
            self._cache_stats["misses"] += 1
            logger.debug(f"Cache miss for SVG file: {path}")

        # Use cached version
        return self._load_svg_file_cached(path)

    @lru_cache(maxsize=128)
    def _load_svg_file_cached(self, file_path: str) -> str:
        """Cached SVG file loader with LRU eviction."""
        try:
            with open(file_path, encoding="utf-8") as file:
                content = file.read()

                # Track this file as cached
                self._cached_files.add(file_path)
                self._cache_stats["total_files_cached"] = len(self._cached_files)

                # Extract dimensions from SVG content for debugging
                width_match = re.search(r'width="([^"]*)"', content)
                height_match = re.search(r'height="([^"]*)"', content)
                viewbox_match = re.search(r'viewBox="([^"]*)"', content)

                # Store for potential debugging use
                _ = width_match.group(1) if width_match else "not found"
                _ = height_match.group(1) if height_match else "not found"
                _ = viewbox_match.group(1) if viewbox_match else "not found"

                logger.debug(
                    f"Loaded and cached SVG file: {file_path} ({len(content)} bytes)"
                )
                return content
        except Exception as e:
            logger.warning(f"Failed to load SVG file {file_path}: {e}")
            return ""

    def _preload_common_assets(self) -> None:
        """Warm cache with frequently used assets."""
        try:
            # Pre-load common arrow types for both colors
            common_patterns = [
                "arrows_colored/pro/{color}/from_radial/pro_0.0.svg",
                "arrows_colored/pro/{color}/from_radial/pro_0.5.svg",
                "arrows_colored/pro/{color}/from_radial/pro_1.0.svg",
                "arrows_colored/anti/{color}/from_radial/anti_0.0.svg",
                "arrows_colored/anti/{color}/from_radial/anti_0.5.svg",
                "arrows_colored/anti/{color}/from_radial/anti_1.0.svg",
                "arrows_colored/static/{color}/from_radial/static_0.0.svg",
                "arrows_colored/dash/{color}/from_radial/dash_0.0.svg",
                "arrows_colored/{color}/float.svg",
            ]

            preloaded_count = 0
            for color in ["blue", "red"]:
                for pattern in common_patterns:
                    relative_path = pattern.format(color=color)
                    full_path = get_image_path(relative_path)
                    if (
                        full_path
                        and isinstance(full_path, str)
                        and os.path.exists(full_path)
                    ):
                        # Pre-load into cache
                        self._load_svg_file_cached(full_path)
                        preloaded_count += 1

            logger.debug(f"Preloaded {preloaded_count} common SVG assets")

        except Exception as e:
            logger.warning(f"Failed to pre-load common SVG files: {e}")

    @classmethod
    def get_cache_stats(cls) -> dict[str, int]:
        """Get current cache statistics for monitoring."""
        return cls._cache_stats.copy()

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the SVG file cache and reset statistics."""
        # Find and clear the LRU cache
        for obj in cls.__dict__.values():
            if hasattr(obj, "cache_clear"):
                obj.cache_clear()

        # Reset tracking
        cls._cached_files.clear()
        cls._cache_stats = {"hits": 0, "misses": 0, "total_files_cached": 0}

        logger.info("SVG cache cleared and statistics reset")

    @classmethod
    def get_cache_info(cls) -> str:
        """Get detailed cache information for debugging."""
        try:
            # Get cache info from the LRU cache
            cache_method = getattr(cls, "_load_svg_file_cached", None)
            if cache_method and hasattr(cache_method, "cache_info"):
                cache_info = cache_method.cache_info()
                hit_rate = (
                    cls._cache_stats["hits"]
                    / (cls._cache_stats["hits"] + cls._cache_stats["misses"])
                    * 100
                    if (cls._cache_stats["hits"] + cls._cache_stats["misses"]) > 0
                    else 0
                )

                return (
                    f"SVG Cache Info: {cache_info.hits} hits, {cache_info.misses} misses, "
                    f"cache size: {cache_info.currsize}/{cache_info.maxsize}, "
                    f"hit rate: {hit_rate:.1f}%, files tracked: {len(cls._cached_files)}"
                )
            else:
                return f"Cache info: files tracked: {len(cls._cached_files)}"
        except Exception as e:
            return f"Cache info unavailable: {e}"
