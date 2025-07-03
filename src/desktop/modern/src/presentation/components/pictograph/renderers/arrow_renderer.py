"""
Arrow renderer for pictograph components.

Handles rendering of arrow elements with positioning, rotation, and mirroring.
"""

import os
import re
import logging
from functools import lru_cache
from typing import Optional, TYPE_CHECKING, Dict, Set
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from presentation.components.pictograph.asset_utils import (
    get_image_path,
)
from domain.models.core_models import (
    MotionData,
    Location,
    MotionType,
)
from domain.models.pictograph_models import ArrowData, PictographData
from core.interfaces.positioning_services import IArrowPositioningOrchestrator
from core.dependency_injection.di_container import get_container
from presentation.components.pictograph.graphics_items.arrow_item import (
    ArrowItem,
)


if TYPE_CHECKING:
    from presentation.components.pictograph.pictograph_scene import PictographScene

# Module-level logger for performance monitoring
logger = logging.getLogger(__name__)


class ArrowRenderer:
    """Handles arrow rendering for pictographs with optimized SVG caching."""

    # Class-level cache statistics for monitoring
    _cache_stats: Dict[str, int] = {"hits": 0, "misses": 0, "total_files_cached": 0}

    # Track cached files for cache management
    _cached_files: Set[str] = set()

    def __init__(self, scene: "PictographScene"):
        self.scene = scene
        self.CENTER_X = 475
        self.CENTER_Y = 475
        self.HAND_RADIUS = 143.1

        # Get orchestrator from DI container with error handling
        try:
            container = get_container()
            self.positioning_orchestrator = container.resolve(
                IArrowPositioningOrchestrator
            )
        except Exception as e:
            logger.warning(f"Failed to resolve IArrowPositioningOrchestrator: {e}")
            self.positioning_orchestrator = None

        # Initialize cache monitoring
        logger.debug("ArrowRenderer initialized with SVG caching enabled")

        # Pre-warm cache with common SVG files if needed
        self._preload_common_svgs()

        self.location_coordinates = {
            Location.NORTH.value: (0, -self.HAND_RADIUS),
            Location.EAST.value: (self.HAND_RADIUS, 0),
            Location.SOUTH.value: (0, self.HAND_RADIUS),
            Location.WEST.value: (-self.HAND_RADIUS, 0),
            Location.NORTHEAST.value: (
                self.HAND_RADIUS * 0.707,
                -self.HAND_RADIUS * 0.707,
            ),
            Location.SOUTHEAST.value: (
                self.HAND_RADIUS * 0.707,
                self.HAND_RADIUS * 0.707,
            ),
            Location.SOUTHWEST.value: (
                -self.HAND_RADIUS * 0.707,
                self.HAND_RADIUS * 0.707,
            ),
            Location.NORTHWEST.value: (
                -self.HAND_RADIUS * 0.707,
                -self.HAND_RADIUS * 0.707,
            ),
        }

    def render_arrow(
        self,
        color: str,
        motion_data: MotionData,
        full_pictograph_data: Optional[PictographData] = None,
    ) -> None:
        """Render an arrow using SVG files."""
        # Note: Static motions with 0 turns should still show arrows in TKA
        # Only filter out if explicitly marked as invisible
        if hasattr(motion_data, "is_visible") and not motion_data.is_visible:
            return

        arrow_svg_path = self._get_arrow_svg_file(motion_data, color)
        # component_type = self.scene._determine_component_type()
        arrow_item = self._create_arrow_item_for_context(color)
        renderer = None

        if os.path.exists(arrow_svg_path):
            # Load pre-colored SVG directly (no color transformation needed)
            renderer = QSvgRenderer(arrow_svg_path)
            logger.debug(f"Using pre-colored SVG: {arrow_svg_path}")
        else:
            # Fallback to original method if pre-colored SVG doesn't exist
            logger.warning(
                f"Pre-colored SVG not found: {arrow_svg_path}, falling back to original method"
            )
            original_svg_path = self._get_original_arrow_svg_file(motion_data)
            if os.path.exists(original_svg_path):
                # Apply color transformation to SVG data (fallback method)
                svg_data = self._load_svg_file(original_svg_path)
                colored_svg_data = self._apply_color_transformation(svg_data, color)

                renderer = QSvgRenderer(bytearray(colored_svg_data, encoding="utf-8"))
                logger.debug(
                    f"Using original SVG with color transformation: {original_svg_path}"
                )
            else:
                logger.error(
                    f"Neither pre-colored nor original SVG found for motion: {motion_data}"
                )
                return

        # Validate renderer and proceed with arrow rendering
        if renderer and renderer.isValid():
            arrow_item.setSharedRenderer(renderer)

            (
                position_x,
                position_y,
                rotation,
            ) = self._calculate_arrow_position_with_service(
                color, motion_data, full_pictograph_data
            )

            # CRITICAL: Set transform origin to arrow's visual center BEFORE rotation
            bounds = arrow_item.boundingRect()
            arrow_item.setTransformOriginPoint(bounds.center())

            # Now apply rotation around the visual center
            arrow_item.setRotation(rotation)

            arrow_data = ArrowData(
                motion_data=motion_data,
                color=color,
                turns=motion_data.turns,
                position_x=position_x,
                position_y=position_y,
                rotation_angle=rotation,
            )
            # Apply mirror transform if positioning orchestrator is available
            if self.positioning_orchestrator:
                self.positioning_orchestrator.apply_mirror_transform(
                    arrow_item,
                    self.positioning_orchestrator.should_mirror_arrow(arrow_data),
                )

            # POSITIONING FORMULA:
            # Get bounding rect AFTER all transformations (scaling + rotation)
            # This ensures we have the correct bounds for positioning calculation
            final_bounds = (
                arrow_item.boundingRect()
            )  # final_pos = calculated_pos - bounding_rect_center
            # This ensures the arrow's visual center appears exactly at the calculated position
            # regardless of rotation angle, achieving pixel-perfect positioning accuracy
            final_x = position_x - final_bounds.center().x()
            final_y = position_y - final_bounds.center().y()

            arrow_item.setPos(final_x, final_y)
            arrow_item.setZValue(100)  # Bring arrows to front

            self.scene.addItem(arrow_item)
        else:
            logger.error(f"Invalid SVG renderer for motion: {motion_data}")

    def _create_arrow_item_for_context(self, color: str):
        """Create appropriate arrow item type based on scene context."""
        # Always create an ArrowItem - context detection will configure behavior
        arrow_item = ArrowItem()
        arrow_item.arrow_color = color  # Set color for all contexts

        # Also debug the parent hierarchy
        parent = self.scene.parent()
        hierarchy = []
        while parent and len(hierarchy) < 5:  # Limit to avoid infinite loops
            hierarchy.append(parent.__class__.__name__)
            parent = parent.parent() if hasattr(parent, "parent") else None

        # Return the arrow item - it will configure its own behavior based on context
        return arrow_item

    def _get_arrow_svg_file(self, motion_data: MotionData, color: str) -> str:
        """Get the correct pre-colored arrow SVG file path with proper motion type mapping."""
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
            return get_image_path(
                f"arrows_colored/static/{color}/from_radial/static_{turns_str}.svg"
            )

    def _get_original_arrow_svg_file(self, motion_data: MotionData) -> str:
        """Get the original (non-colored) arrow SVG file path for fallback."""
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
            return get_image_path(f"arrows/static/from_radial/static_{turns_str}.svg")

    def _calculate_arrow_position_with_service(
        self,
        color: str,
        motion_data: MotionData,
        full_pictograph_data: Optional[PictographData] = None,
    ) -> tuple[float, float, float]:
        """Calculate arrow position using the complete positioning service."""
        arrow_data = ArrowData(
            motion_data=motion_data,
            color=color,
            turns=motion_data.turns,
        )

        # Use full pictograph data if available for Type 3 detection
        if full_pictograph_data:
            pictograph_data = full_pictograph_data
        else:
            pictograph_data = PictographData(arrows={color: arrow_data})

        # Use positioning orchestrator if available, otherwise use fallback positioning
        if self.positioning_orchestrator:
            return self.positioning_orchestrator.calculate_arrow_position(
                arrow_data, pictograph_data
            )
        else:
            # Fallback positioning - center of scene
            logger.warning(
                "No positioning orchestrator available, using fallback positioning"
            )
            return (self.CENTER_X, self.CENTER_Y, 0.0)

    def _get_location_position(self, location: Location) -> tuple[float, float]:
        """Get the coordinate position for a location."""
        return self.location_coordinates.get(location.value, (0, 0))

    def _load_svg_file(self, file_path: str) -> str:
        """Load SVG file content as string with caching."""
        # Check if file is already cached
        if file_path in self._cached_files:
            self._cache_stats["hits"] += 1
            logger.debug(f"Cache hit for SVG file: {file_path}")
        else:
            self._cache_stats["misses"] += 1
            logger.debug(f"Cache miss for SVG file: {file_path}")

        # Use cached version
        return self._load_svg_file_cached(file_path)

    @lru_cache(maxsize=128)
    def _load_svg_file_cached(self, file_path: str) -> str:
        """Cached SVG file loader with LRU eviction."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
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

    def _apply_color_transformation(self, svg_data: str, color: str) -> str:
        """Apply color transformation to SVG data based on arrow color."""
        if not svg_data:
            return svg_data

        # Color mapping based on reference implementation
        COLOR_MAP = {
            "blue": "#2E3192",  # Reference blue color
            "red": "#ED1C24",  # Reference red color
        }

        target_color = COLOR_MAP.get(color.lower(), "#2E3192")  # Default to blue

        # Pattern to match CSS fill properties in SVG
        # This matches both fill attributes and CSS style properties
        patterns = [
            # CSS fill property: fill="#color"
            re.compile(r'(fill=")([^"]*)(")'),
            # CSS style attribute: fill: #color;
            re.compile(r"(fill:\s*)([^;]*)(;)"),
            # Class definition: .st0 { fill: #color; }
            re.compile(r"(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)([^;}]*)([^}]*?\})"),
        ]

        # Apply color transformation using all patterns
        for pattern in patterns:
            svg_data = pattern.sub(
                lambda m: m.group(1) + target_color + m.group(len(m.groups())), svg_data
            )

        return svg_data

    def _preload_common_svgs(self) -> None:
        """Pre-load commonly used pre-colored SVG files to warm the cache."""
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
                    if os.path.exists(full_path):
                        # Pre-load into cache
                        self._load_svg_file_cached(full_path)
                        preloaded_count += 1

        except Exception as e:
            logger.warning(f"Failed to pre-load common SVG files: {e}")

    @classmethod
    def get_cache_stats(cls) -> Dict[str, int]:
        """Get current cache statistics for monitoring."""
        return cls._cache_stats.copy()

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the SVG file cache and reset statistics."""
        # Clear the LRU cache
        if hasattr(cls, "_load_svg_file_cached"):
            cls._load_svg_file_cached.cache_clear()

        # Reset tracking
        cls._cached_files.clear()
        cls._cache_stats = {"hits": 0, "misses": 0, "total_files_cached": 0}

        logger.info("SVG cache cleared and statistics reset")

    @classmethod
    def get_cache_info(cls) -> str:
        """Get detailed cache information for debugging."""
        try:
            cache_info = cls._load_svg_file_cached.cache_info(cls._load_svg_file_cached)
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
        except Exception as e:
            return f"Cache info unavailable: {e}"
