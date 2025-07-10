"""
Arrow renderer for pictograph components.

Handles rendering of arrow elements with positioning, rotation, and mirroring.
"""

import os
import re
import logging
from functools import lru_cache
from typing import Optional, TYPE_CHECKING, Dict, Set
from PyQt6.QtSvg import QSvgRenderer

from presentation.components.pictograph.asset_utils import (
    get_image_path,
)
from application.services.assets.asset_manager import AssetManager
from domain.models import (
    MotionData,
    Location,
    MotionType,
)
from domain.models.pictograph_models import ArrowData, PictographData
from core.interfaces.positioning_services import IArrowPositioningOrchestrator, IArrowCoordinateSystemService
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

        # Initialize asset manager service
        self.asset_manager = AssetManager()

        # Get positioning services from DI container with error handling
        try:
            container = get_container()
            self.positioning_orchestrator = container.resolve(
                IArrowPositioningOrchestrator
            )
            # Get coordinate system service to replace duplicate mappings
            self.coordinate_system = container.resolve(IArrowCoordinateSystemService)
        except Exception as e:
            logger.warning(f"Failed to resolve positioning services: {e}")
            self.positioning_orchestrator = None
            self.coordinate_system = None

        # Initialize cache monitoring
        logger.debug("ArrowRenderer initialized with asset management service")
        
        # Fallback coordinates for when coordinate system service is not available
        self._fallback_location_coordinates = {
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

        # Use asset manager to get SVG path
        arrow_svg_path = self.asset_manager.get_arrow_asset_path(motion_data, color)
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
            original_svg_path = self.asset_manager.get_fallback_arrow_asset_path(motion_data)
            if os.path.exists(original_svg_path):
                # Apply color transformation to SVG data (fallback method)
                svg_data = self.asset_manager.load_and_cache_asset(original_svg_path)
                colored_svg_data = self.asset_manager.apply_color_transformation(svg_data, color)

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
        """Get the coordinate position for a location using the coordinate system service."""
        if self.coordinate_system:
            # Use the coordinate system service to get proper coordinates
            # Since we don't have motion data context, create a dummy static motion
            # for coordinate calculation
            from domain.models import MotionData, MotionType
            dummy_motion = MotionData(
                motion_type=MotionType.STATIC,
                turns=0.0,
                start_loc=location,
                end_loc=location
            )
            point = self.coordinate_system.get_initial_position(dummy_motion, location)
            return (point.x(), point.y())
        else:
            # Fallback to manual calculation if service is not available
            return self._fallback_location_coordinates.get(location.value, (0, 0))

    @classmethod
    def get_cache_stats(cls) -> Dict[str, int]:
        """Get current cache statistics for monitoring."""
        return AssetManager.get_cache_stats()

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the SVG file cache and reset statistics."""
        AssetManager.clear_cache()
        logger.info("SVG cache cleared and statistics reset")

    @classmethod
    def get_cache_info(cls) -> str:
        """Get detailed cache information for debugging."""
        return AssetManager.get_cache_info()
