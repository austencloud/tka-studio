"""
Arrow renderer for pictograph components.

Handles Qt-specific arrow rendering while delegating business logic
to ArrowRenderingService.
"""

import logging
from typing import TYPE_CHECKING, Dict, Optional

from application.services.pictograph.arrow_rendering_service import (
    ArrowRenderingService,
)
from core.dependency_injection.di_container import get_container
from core.interfaces.positioning_services import (
    IArrowCoordinateSystemService,
    IArrowPositioningOrchestrator,
)
from domain.models import MotionData
from domain.models.arrow_data import ArrowData
from domain.models.pictograph_data import PictographData
from presentation.components.pictograph.graphics_items.arrow_item import ArrowItem
from PyQt6.QtSvg import QSvgRenderer

if TYPE_CHECKING:
    from presentation.components.pictograph.pictograph_scene import PictographScene

# Module-level logger for performance monitoring
logger = logging.getLogger(__name__)


class QtArrowRenderer:
    """
    Qt presentation layer for arrow rendering.

    Handles Qt-specific operations (QSvgRenderer, QPainter, QGraphicsItems)
    while delegating business logic to ArrowRenderingService.
    """

    def __init__(
        self,
        scene: "PictographScene",
        positioning_orchestrator: Optional[IArrowPositioningOrchestrator] = None,
        coordinate_system: Optional[IArrowCoordinateSystemService] = None,
        rendering_service: Optional[ArrowRenderingService] = None,
    ):
        """
        Initialize the Qt arrow renderer with dependency injection.

        Args:
            scene: The pictograph scene this renderer belongs to
            positioning_orchestrator: Service for calculating arrow positions
            coordinate_system: Service for coordinate system management
            rendering_service: Service for arrow rendering operations
        """
        self.scene = scene
        self.CENTER_X = 475
        self.CENTER_Y = 475

        # Use injected services or create/resolve as fallback
        self.positioning_orchestrator = positioning_orchestrator
        self.coordinate_system = coordinate_system
        self._rendering_service = rendering_service or ArrowRenderingService()

        # Use local arrow item pool for performance (small pool size)
        self._arrow_item_pool = {"blue": [], "red": []}
        self._active_arrow_items = {"blue": [], "red": []}
        self._pool_size = 2  # Small pool: only 2 items per color per scene
        self._scene_id = getattr(scene, "scene_id", "unknown")
        self._initialize_arrow_item_pool()

        # Only resolve from container if services weren't injected
        if self.positioning_orchestrator is None or self.coordinate_system is None:
            self._resolve_missing_services()

    def _initialize_arrow_item_pool(self):
        """Initialize the local arrow item pool with small size for performance."""
        try:
            for color in ["blue", "red"]:
                for _ in range(self._pool_size):
                    arrow_item = ArrowItem()
                    arrow_item.arrow_color = color
                    arrow_item.setVisible(False)  # Hide initially
                    self._arrow_item_pool[color].append(arrow_item)

            logger.debug(
                f"✅ [ARROW_POOL] Scene {self._scene_id}: Initialized with {self._pool_size} items per color"
            )
        except Exception as e:
            logger.warning(
                f"⚠️ [ARROW_POOL] Scene {self._scene_id}: Failed to initialize pool: {e}"
            )

    def _checkout_arrow_item(self, color: str) -> ArrowItem:
        """Get an arrow item from the local pool or create new if pool is empty."""
        if self._arrow_item_pool[color]:
            arrow_item = self._arrow_item_pool[color].pop()
            self._active_arrow_items[color].append(arrow_item)
            arrow_item.setVisible(True)
            logger.debug(
                f"🔄 [ARROW_POOL] Scene {self._scene_id}: Checked out {color} arrow (pool: {len(self._arrow_item_pool[color])})"
            )
            return arrow_item
        else:
            # Pool exhausted, create new item
            logger.debug(
                f"⚠️ [ARROW_POOL] Scene {self._scene_id}: Pool exhausted for {color}, creating new item"
            )
            arrow_item = ArrowItem()
            arrow_item.arrow_color = color
            self._active_arrow_items[color].append(arrow_item)
            return arrow_item

    def _return_arrow_items_to_pool(self):
        """Return all active arrow items to the local pool and clear from scene."""
        for color in ["blue", "red"]:
            items_to_return = []

            for arrow_item in self._active_arrow_items[color]:
                try:
                    # Check if the item is still valid before accessing it
                    if hasattr(arrow_item, "scene") and arrow_item.scene():
                        arrow_item.scene().removeItem(arrow_item)

                    # Reset item state only if item is still valid
                    arrow_item.setVisible(False)
                    arrow_item.setPos(0, 0)
                    arrow_item.setRotation(0)
                    arrow_item.setScale(1.0)

                    # Return to pool if there's space and item is valid
                    if len(self._arrow_item_pool[color]) < self._pool_size:
                        items_to_return.append(arrow_item)

                except RuntimeError:
                    # Item has been deleted by Qt, skip it
                    logger.debug(
                        f"🗑️ [ARROW_POOL] Scene {self._scene_id}: {color} arrow item was deleted by Qt"
                    )
                    continue
                except Exception as e:
                    logger.warning(
                        f"⚠️ [ARROW_POOL] Scene {self._scene_id}: Error returning {color} arrow: {e}"
                    )
                    continue

            # Add valid items back to pool
            self._arrow_item_pool[color].extend(items_to_return)

            # Clear active items list
            self._active_arrow_items[color].clear()

        logger.debug(
            f"🔄 [ARROW_POOL] Scene {self._scene_id}: Returned arrow items to pool"
        )

    def _resolve_missing_services(self):
        """Resolve missing services from DI container as fallback."""
        try:
            from core.dependency_injection.container_utils import (
                ensure_container_initialized,
            )

            # Ensure container is properly initialized with all services
            if not ensure_container_initialized():
                raise RuntimeError("Failed to initialize DI container with services")

            container = get_container()

            if self.positioning_orchestrator is None:
                self.positioning_orchestrator = container.resolve(
                    IArrowPositioningOrchestrator
                )

            if self.coordinate_system is None:
                self.coordinate_system = container.resolve(
                    IArrowCoordinateSystemService
                )

            logger.debug(
                "Successfully resolved missing positioning services from DI container"
            )
        except Exception as e:
            logger.error(f"Failed to resolve positioning services: {e}")
            logger.warning("Falling back to center positioning for all arrows")
            self.positioning_orchestrator = None
            self.coordinate_system = None

    def render_arrow(
        self,
        color: str,
        motion_data: MotionData,
        full_pictograph_data: Optional[PictographData] = None,
    ) -> None:
        """Render an arrow using SVG files with service delegation."""
        # Validate motion visibility using service
        if not self._rendering_service.validate_motion_visibility(motion_data):
            return

        # Get SVG path using service
        arrow_svg_path = self._rendering_service.asset_manager.get_arrow_svg_path(
            motion_data, color
        )
        arrow_item = self._create_arrow_item_for_context(color)
        renderer = None

        if self._rendering_service.asset_manager.svg_path_exists(arrow_svg_path):
            # Load pre-colored SVG directly (no color transformation needed)
            renderer = QSvgRenderer(arrow_svg_path)
        else:
            # Fallback to original method if pre-colored SVG doesn't exist
            original_svg_path = (
                self._rendering_service.asset_manager.get_fallback_arrow_svg_path(
                    motion_data
                )
            )
            if self._rendering_service.asset_manager.svg_path_exists(original_svg_path):
                # Apply color transformation to SVG data using service
                svg_data = self._rendering_service.load_cached_svg_data(
                    original_svg_path
                )
                if svg_data:
                    colored_svg_data = self._rendering_service.asset_manager.apply_color_transformation(
                        svg_data, color
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

            # Delegate position calculation to the positioning orchestrator directly
            if self.positioning_orchestrator and full_pictograph_data:
                try:
                    motion_data = None
                    if (
                        hasattr(full_pictograph_data, "motions")
                        and full_pictograph_data.motions
                    ):
                        motion_data = full_pictograph_data.motions.get(color)

                    position_x, position_y, rotation = (
                        self.positioning_orchestrator.calculate_arrow_position(
                            ArrowData(
                                color=color,
                                turns=motion_data.turns if motion_data else 0,
                                is_visible=True,
                            ),
                            full_pictograph_data,
                            motion_data,
                        )
                    )
                except Exception as e:
                    logger.error(f"Positioning orchestrator failed: {e}")
                    position_x, position_y, rotation = self.CENTER_X, self.CENTER_Y, 0.0
            else:
                logger.warning("Using fallback arrow positioning (center)")
                position_x, position_y, rotation = self.CENTER_X, self.CENTER_Y, 0.0

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
        """Get arrow item from pool for optimal performance."""
        # Use pooled arrow item instead of creating new one
        return self._checkout_arrow_item(color)

    # Cache Management (delegate to service)
    @classmethod
    def get_cache_stats(cls) -> Dict[str, int]:
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
