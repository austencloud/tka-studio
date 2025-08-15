"""
Arrow renderer for pictograph components.

Handles Qt-specific arrow rendering while delegating business logic
to ArrowRenderingService.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PyQt6.QtSvg import QSvgRenderer

from desktop.modern.src.application.services.pictograph.arrow_rendering_service import (
    ArrowRenderingService,
)
from desktop.modern.src.core.dependency_injection import get_container
from desktop.modern.src.core.interfaces.positioning_services import (
    IArrowCoordinateSystemService,
    IArrowPositioningOrchestrator,
)
from desktop.modern.src.domain.models.arrow_data import ArrowData
from desktop.modern.src.domain.models.pictograph_data import PictographData
from desktop.modern.src.presentation.components.pictograph.graphics_items.arrow_item import (
    ArrowItem,
)
from domain.models import MotionData


if TYPE_CHECKING:
    from desktop.modern.src.presentation.components.pictograph.pictograph_scene import (
        PictographScene,
    )

# Module-level logger for performance monitoring
logger = logging.getLogger(__name__)


class ArrowRenderer:
    """
    Qt presentation layer for arrow rendering.

    Handles Qt-specific operations (QSvgRenderer, QPainter, QGraphicsItems)
    while delegating business logic to ArrowRenderingService.
    """

    def __init__(self, scene: PictographScene):
        self.scene = scene
        self.CENTER_X = 475
        self.CENTER_Y = 475

        # Initialize business service
        self._rendering_service = ArrowRenderingService()

        # Get positioning services from DI container with error handling
        try:
            container = get_container()
            self.positioning_orchestrator = container.resolve(
                IArrowPositioningOrchestrator
            )
            self.coordinate_system = container.resolve(IArrowCoordinateSystemService)
        except Exception as e:
            logger.exception(f"Failed to resolve positioning services: {e}")
            self.positioning_orchestrator = None
            self.coordinate_system = None

    def render_arrow(
        self,
        color: str,
        motion_data: MotionData,
        full_pictograph_data: PictographData | None = None,
    ) -> None:
        """Render an arrow using SVG files with service delegation."""
        # Validate motion visibility using service
        if not self._rendering_service.validate_motion_visibility(motion_data):
            return

        # Get SVG path using service
        arrow_svg_path = self._rendering_service.get_arrow_svg_path(motion_data, color)
        arrow_item = self._create_arrow_item_for_context(color)
        renderer = None

        if self._rendering_service.svg_path_exists(arrow_svg_path):
            # Load pre-colored SVG directly (no color transformation needed)
            renderer = QSvgRenderer(arrow_svg_path)
        else:
            # Fallback to original method if pre-colored SVG doesn't exist
            original_svg_path = self._rendering_service.get_fallback_arrow_svg_path(
                motion_data
            )
            if self._rendering_service.svg_path_exists(original_svg_path):
                # Apply color transformation to SVG data using service
                svg_data = self._rendering_service.load_cached_svg_data(
                    original_svg_path
                )
                if svg_data:
                    colored_svg_data = (
                        self._rendering_service.apply_color_transformation(
                            svg_data, color
                        )
                    )
                    renderer = QSvgRenderer(
                        bytearray(colored_svg_data, encoding="utf-8")
                    )
            else:
                logger.error(
                    f"Neither pre-colored nor original SVG found for motion: {motion_data}"
                )
                return

        # Validate renderer and proceed with arrow rendering
        if renderer and renderer.isValid():
            arrow_item.setSharedRenderer(renderer)

            # Calculate position using service
            arrow_data = ArrowData(
                color=color,
                turns=motion_data.turns,
                is_visible=True,
            )

            (
                position_x,
                position_y,
                rotation,
            ) = self._rendering_service.calculate_arrow_position(
                arrow_data,
                full_pictograph_data,
                self.positioning_orchestrator,
                self.coordinate_system,
            )

            # Qt-specific rendering operations
            self._apply_arrow_transforms(arrow_item, position_x, position_y, rotation)

            # Apply mirror transform if positioning orchestrator is available
            if self.positioning_orchestrator:
                arrow_data_with_position = ArrowData(
                    color=color,
                    turns=motion_data.turns,
                    position_x=position_x,
                    position_y=position_y,
                    rotation_angle=rotation,
                    is_visible=True,
                )
                self.positioning_orchestrator.apply_mirror_transform(
                    arrow_item,
                    self.positioning_orchestrator.should_mirror_arrow(
                        arrow_data_with_position, full_pictograph_data
                    ),
                )

            # Final positioning and scene addition
            self._finalize_arrow_positioning(arrow_item, position_x, position_y)
            self.scene.addItem(arrow_item)
        else:
            logger.error(f"Invalid SVG renderer for motion: {motion_data}")

    def _apply_arrow_transforms(
        self,
        arrow_item: ArrowItem,
        position_x: float,
        position_y: float,
        rotation: float,
    ) -> None:
        """Apply Qt-specific transforms to arrow item."""
        # CRITICAL: Set transform origin to arrow's visual center BEFORE rotation
        bounds = arrow_item.boundingRect()
        arrow_item.setTransformOriginPoint(bounds.center())

        # Now apply rotation around the visual center
        arrow_item.setRotation(rotation)

    def _finalize_arrow_positioning(
        self, arrow_item: ArrowItem, position_x: float, position_y: float
    ) -> None:
        """Finalize arrow positioning in Qt scene."""
        # POSITIONING FORMULA:
        # Get bounding rect AFTER all transformations (scaling + rotation)
        # This ensures we have the correct bounds for positioning calculation
        final_bounds = arrow_item.boundingRect()
        # final_pos = calculated_pos - bounding_rect_center
        # This ensures the arrow's visual center appears exactly at the calculated position
        # regardless of rotation angle, achieving pixel-perfect positioning accuracy
        final_x = position_x - final_bounds.center().x()
        final_y = position_y - final_bounds.center().y()

        arrow_item.setPos(final_x, final_y)
        arrow_item.setZValue(100)  # Bring arrows to front

    def _create_arrow_item_for_context(self, color: str) -> ArrowItem:
        """Create appropriate arrow item type based on scene context."""
        # Always create an ArrowItem - context detection will configure behavior
        arrow_item = ArrowItem()
        arrow_item.arrow_color = color  # Set color for all contexts

        # Debug the parent hierarchy for context detection
        parent = self.scene.parent()
        hierarchy = []
        while parent and len(hierarchy) < 5:  # Limit to avoid infinite loops
            hierarchy.append(parent.__class__.__name__)
            parent = parent.parent() if hasattr(parent, "parent") else None

        # Return the arrow item - it will configure its own behavior based on context
        return arrow_item

    # Cache Management (delegate to service)
    @classmethod
    def get_cache_stats(cls) -> dict[str, int]:
        """Get current cache statistics for monitoring."""
        return ArrowRenderingService.get_cache_statistics()

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the SVG file cache and reset statistics."""
        ArrowRenderingService.clear_cache()

    @classmethod
    def get_cache_info(cls) -> str:
        """Get detailed cache information for debugging."""
        return ArrowRenderingService.get_cache_info()
