"""
Prop rendering microservice for pictograph rendering.

This service handles:
- Staff prop rendering with color transformations
- Prop positioning and rotation calculations
- Beta positioning integration for prop overlap handling
- Prop-specific caching and performance optimization
"""

import logging
from typing import Optional

from application.services.pictograph.asset_management.pictograph_asset_manager import (
    PictographAssetManager,
)
from application.services.pictograph.cache_management.pictograph_cache_manager import (
    PictographCacheManager,
)
from application.services.pictograph.performance_monitoring.pictograph_performance_monitor import (
    PictographPerformanceMonitor,
)
from domain.models import MotionData, PictographData
from PyQt6.QtCore import QByteArray, QPointF
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene

logger = logging.getLogger(__name__)


class PropRenderingService:
    """
    Microservice for rendering pictograph props.

    Provides:
    - Staff prop rendering with color transformations
    - Sophisticated prop positioning and rotation
    - Beta positioning integration for overlap handling
    - Performance-optimized prop caching
    """

    def __init__(
        self,
        asset_manager: PictographAssetManager,
        cache_manager: PictographCacheManager,
        performance_monitor: PictographPerformanceMonitor,
    ):
        """Initialize the prop rendering service with injected dependencies."""
        self._asset_manager = asset_manager
        self._cache_manager = cache_manager
        self._performance_monitor = performance_monitor

        logger.info("🎭 [PROP_RENDERER] Initialized prop rendering service")

    def render_prop(
        self,
        scene: QGraphicsScene,
        color: str,
        motion_data: MotionData,
        pictograph_data: Optional[PictographData] = None,
    ) -> Optional[QGraphicsSvgItem]:
        """
        Render prop using cached, colored renderer with performance monitoring.

        Args:
            scene: Target scene to render into
            color: Prop color ("blue" or "red")
            motion_data: Motion data for positioning
            pictograph_data: Full pictograph data for beta positioning

        Returns:
            Created prop item or None if rendering failed
        """
        timer_id = self._performance_monitor.start_render_timer("prop_render")

        try:
            renderer = self._get_prop_renderer(color)
            if not renderer or not renderer.isValid():
                logger.error(
                    f"❌ [PROP_RENDERER] Invalid prop renderer for color: {color}"
                )
                self._performance_monitor.record_error(
                    "prop_render", f"Invalid renderer for {color}"
                )
                return None

            prop_item = QGraphicsSvgItem()
            prop_item.setSharedRenderer(renderer)

            # Position prop using motion data with beta positioning support
            self._position_prop(prop_item, motion_data, color, pictograph_data)

            scene.addItem(prop_item)

            logger.debug(f"🎭 [PROP_RENDERER] Rendered {color} prop")
            return prop_item

        except Exception as e:
            logger.error(f"❌ [PROP_RENDERER] Prop rendering failed: {e}")
            self._performance_monitor.record_error("prop_render", str(e))
            return None
        finally:
            self._performance_monitor.end_render_timer(timer_id)

    def _get_prop_renderer(self, color: str) -> Optional[QSvgRenderer]:
        """Get cached prop renderer or create new one."""
        cache_key = f"staff_{color}"

        # Try to get from cache first
        renderer = self._cache_manager.get_renderer(cache_key)
        if renderer:
            self._performance_monitor.record_cache_hit("prop")
            return renderer

        self._performance_monitor.record_cache_miss("prop")

        # Create new renderer
        renderer = self._create_prop_renderer(color)
        if renderer:
            self._cache_manager.store_renderer(cache_key, renderer)

        return renderer

    def _create_prop_renderer(self, color: str) -> Optional[QSvgRenderer]:
        """Create new prop renderer with actual SVG loading and color transformation."""
        timer_id = self._performance_monitor.start_render_timer("svg_load")

        try:
            # Get prop SVG path (currently only staff props supported)
            prop_svg_path = self._asset_manager.get_prop_svg_path("staff")

            if not self._asset_manager.svg_path_exists(prop_svg_path):
                logger.warning(f"⚠️ [PROP_RENDERER] Prop SVG not found: {prop_svg_path}")
                return self._create_fallback_prop_renderer(color)

            # Load SVG data from file
            svg_data = self._asset_manager.load_svg_data(prop_svg_path)
            if not svg_data:
                logger.error(
                    f"❌ [PROP_RENDERER] Failed to load prop SVG: {prop_svg_path}"
                )
                return self._create_fallback_prop_renderer(color)

            # Apply color transformation
            color_timer_id = self._performance_monitor.start_render_timer(
                "color_transform"
            )
            try:
                colored_svg_data = self._asset_manager.apply_color_transformation(
                    svg_data, color
                )
            finally:
                self._performance_monitor.end_render_timer(color_timer_id)

            # Create renderer from colored SVG data
            renderer = QSvgRenderer(QByteArray(colored_svg_data.encode("utf-8")))
            if renderer.isValid():
                logger.debug(
                    f"🎭 [PROP_RENDERER] Created {color} prop renderer from {prop_svg_path}"
                )
                return renderer
            else:
                logger.error(f"❌ [PROP_RENDERER] Invalid SVG for {color} prop")
                return self._create_fallback_prop_renderer(color)

        except Exception as e:
            logger.error(
                f"❌ [PROP_RENDERER] Failed to create {color} prop renderer: {e}"
            )
            self._performance_monitor.record_error("prop_create", str(e))
            return self._create_fallback_prop_renderer(color)
        finally:
            self._performance_monitor.end_render_timer(timer_id)

    def _create_fallback_prop_renderer(self, color: str) -> Optional[QSvgRenderer]:
        """Create fallback prop renderer when SVG loading fails."""
        try:
            fallback_svg = self._asset_manager.create_fallback_prop_svg(color)

            renderer = QSvgRenderer(QByteArray(fallback_svg.encode("utf-8")))
            if renderer.isValid():
                logger.debug(
                    f"🔧 [PROP_RENDERER] Created fallback {color} prop renderer"
                )
                return renderer
            else:
                logger.error(
                    f"❌ [PROP_RENDERER] Failed to create fallback prop renderer"
                )
                return None

        except Exception as e:
            logger.error(
                f"❌ [PROP_RENDERER] Failed to create fallback prop renderer: {e}"
            )
            return None

    def _position_prop(
        self,
        prop_item: QGraphicsSvgItem,
        motion_data: MotionData,
        color: str,
        pictograph_data: Optional[PictographData] = None,
    ) -> None:
        """Position prop item using motion data with proper hand point positioning and beta positioning."""
        try:
            # Get base hand point coordinates
            hand_point = self._get_hand_point_coordinates(motion_data.end_loc)

            if hand_point is None:
                logger.warning(
                    f"⚠️ [PROP_RENDERER] Could not get hand point for location {motion_data.end_loc}"
                )
                # Fallback to center
                hand_point = QPointF(475.0, 475.0)

            # Apply beta positioning if needed
            if pictograph_data and color:
                logger.debug(
                    f"🎯 [PROP_RENDERER] Checking beta positioning for {color} prop"
                )
                beta_offset = self._calculate_beta_offset(pictograph_data, color)
                if beta_offset:
                    hand_point = QPointF(
                        hand_point.x() + beta_offset.x(),
                        hand_point.y() + beta_offset.y(),
                    )
                    logger.debug(
                        f"🎯 [PROP_RENDERER] Applied beta offset to {color} prop: ({beta_offset.x()}, {beta_offset.y()})"
                    )

            # Calculate prop rotation
            prop_rotation = self._calculate_prop_rotation(motion_data)

            # Set rotation with proper transform origin
            bounds = prop_item.boundingRect()
            prop_item.setTransformOriginPoint(bounds.center())
            prop_item.setRotation(prop_rotation)

            # Place prop at hand point (with beta offset if applied)
            self._place_prop_at_hand_point(prop_item, hand_point.x(), hand_point.y())

        except Exception as e:
            logger.error(f"❌ [PROP_RENDERER] Failed to position prop: {e}")
            # Fallback positioning
            prop_item.setPos(475.0, 475.0)  # Center position

    def _get_hand_point_coordinates(self, location) -> Optional[QPointF]:
        """Get hand point coordinates for a location using grid data."""
        # Convert location to string if it's an enum
        if hasattr(location, "value"):
            location_str = location.value
        else:
            location_str = str(location)

        # Use absolute coordinates that match the legacy pictograph positioning
        # These coordinates are based on a 950x950 scene with center at (475, 475)
        CENTER_X = 475.0
        CENTER_Y = 475.0
        HAND_RADIUS = 143.1

        location_coordinates = {
            "n": QPointF(CENTER_X, CENTER_Y - HAND_RADIUS),  # (475.0, 331.9)
            "e": QPointF(CENTER_X + HAND_RADIUS, CENTER_Y),  # (618.1, 475.0)
            "s": QPointF(CENTER_X, CENTER_Y + HAND_RADIUS),  # (475.0, 618.1)
            "w": QPointF(CENTER_X - HAND_RADIUS, CENTER_Y),  # (331.9, 475.0)
            "ne": QPointF(
                CENTER_X + HAND_RADIUS * 0.707, CENTER_Y - HAND_RADIUS * 0.707
            ),
            "se": QPointF(
                CENTER_X + HAND_RADIUS * 0.707, CENTER_Y + HAND_RADIUS * 0.707
            ),
            "sw": QPointF(
                CENTER_X - HAND_RADIUS * 0.707, CENTER_Y + HAND_RADIUS * 0.707
            ),
            "nw": QPointF(
                CENTER_X - HAND_RADIUS * 0.707, CENTER_Y - HAND_RADIUS * 0.707
            ),
        }

        hand_point = location_coordinates.get(location_str)
        if hand_point is None:
            logger.warning(
                f"⚠️ [PROP_RENDERER] Unknown location {location_str}, using north fallback"
            )
            hand_point = location_coordinates["n"]

        return hand_point

    def _calculate_beta_offset(
        self, pictograph_data: PictographData, color: str
    ) -> Optional[QPointF]:
        """Calculate beta positioning offset for a prop if beta positioning should be applied."""
        try:
            from application.services.positioning.props.orchestration.prop_orchestrator import (
                PropOrchestrator,
            )
            from domain.models.beat_data import BeatData

            # Create a BeatData object from pictograph_data for beta positioning
            beat_data = BeatData(
                beat_number=1,  # Default beat number
                pictograph_data=pictograph_data,
                is_blank=False,
            )

            # Create prop orchestrator to handle beta positioning
            prop_orchestrator = PropOrchestrator()

            # Check if beta positioning should be applied
            if not prop_orchestrator.should_apply_beta_positioning(beat_data):
                return None

            # Check if props actually overlap
            if not prop_orchestrator.detect_prop_overlap(beat_data):
                return None

            # Calculate separation offsets
            blue_offset, red_offset = prop_orchestrator.calculate_separation_offsets(
                beat_data
            )

            # Return the appropriate offset for this color
            if color == "blue":
                if hasattr(blue_offset, "x") and callable(
                    getattr(blue_offset, "x", None)
                ):
                    return QPointF(blue_offset.x(), blue_offset.y())
                elif hasattr(blue_offset, "x"):
                    return QPointF(blue_offset.x, blue_offset.y)
                else:
                    return blue_offset
            elif color == "red":
                if hasattr(red_offset, "x") and callable(
                    getattr(red_offset, "x", None)
                ):
                    return QPointF(red_offset.x(), red_offset.y())
                elif hasattr(red_offset, "x"):
                    return QPointF(red_offset.x, red_offset.y)
                else:
                    return red_offset

            return None

        except Exception as e:
            logger.debug(f"🎯 [PROP_RENDERER] Beta positioning calculation failed: {e}")
            return None

    def _calculate_prop_rotation(self, motion_data: MotionData) -> float:
        """Calculate prop rotation based on motion data using the sophisticated positioning logic."""
        try:
            from application.services.positioning.props.calculation.prop_classification_service import (
                PropClassificationService,
            )
            from domain.models.enums import Orientation

            # Create classification service to use its rotation calculation
            classification_service = PropClassificationService()

            # Calculate rotation using the sophisticated logic
            rotation_angle = classification_service.calculate_prop_rotation_angle(
                motion_data, start_orientation=Orientation.IN
            )

            return rotation_angle

        except Exception as e:
            logger.warning(
                f"⚠️ [PROP_RENDERER] Failed to calculate sophisticated prop rotation, using fallback: {e}"
            )
            return self._calculate_basic_prop_rotation(motion_data)

    def _calculate_basic_prop_rotation(self, motion_data: MotionData) -> float:
        """Basic fallback prop rotation calculation."""
        from domain.models.enums import MotionType, Orientation, RotationDirection

        if motion_data.motion_type == MotionType.STATIC:
            return 0.0

        base_rotation = 0.0

        # Orientation-based rotation
        if motion_data.end_ori == Orientation.OUT:
            base_rotation += 180.0

        # Rotation direction adjustment
        if motion_data.prop_rot_dir == RotationDirection.CLOCKWISE:
            base_rotation += 90.0
        elif motion_data.prop_rot_dir == RotationDirection.COUNTER_CLOCKWISE:
            base_rotation -= 90.0

        return base_rotation % 360.0

    def _place_prop_at_hand_point(
        self, prop_item: QGraphicsSvgItem, target_x: float, target_y: float
    ) -> None:
        """Place prop at specific hand point coordinates."""
        bounds = prop_item.boundingRect()
        center_point_in_local_coords = bounds.center()
        center_point_in_scene = prop_item.mapToScene(center_point_in_local_coords)
        target_hand_point = QPointF(target_x, target_y)
        offset = target_hand_point - center_point_in_scene
        new_position = prop_item.pos() + offset
        prop_item.setPos(new_position)

    def preload_common_props(self) -> None:
        """Pre-load commonly used prop renderers for better performance."""
        try:
            logger.info("🚀 [PROP_RENDERER] Pre-loading common prop renderers...")

            # Pre-load prop renderers for common colors
            for color in self._asset_manager.get_supported_colors():
                self._get_prop_renderer(color)

            logger.info("✅ [PROP_RENDERER] Pre-loaded common prop renderers")

        except Exception as e:
            logger.warning(
                f"⚠️ [PROP_RENDERER] Failed to pre-load some prop renderers: {e}"
            )

    def get_supported_colors(self) -> list[str]:
        """Get list of supported prop colors."""
        return self._asset_manager.get_supported_colors()

    def validate_color(self, color: str) -> bool:
        """Validate if the color is supported."""
        return color in self.get_supported_colors()

    def get_prop_stats(self) -> dict:
        """Get prop rendering statistics."""
        return {
            "supported_colors": self.get_supported_colors(),
            "service_status": "active",
        }
