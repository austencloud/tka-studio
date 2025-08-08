"""
Qt Adapter for Pictograph Rendering Service

This adapter bridges the framework-agnostic core orchestration service
with Qt-specific presentation, maintaining backward compatibility while
enabling framework independence.
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsScene

# Import the framework-agnostic services
from shared.application.services.core.pictograph_orchestration_service import (
    CorePictographOrchestrationService,
)
from shared.application.services.core.pictograph_rendering.real_asset_provider import (
    create_real_asset_provider,
)
from shared.application.services.core.types import Point, Size

# Import the Qt render engine from existing adapter
from desktop.modern.application.adapters.qt_pictograph_adapter import (
    QtRenderEngine,
    QtTypeConverter,
)
from desktop.modern.domain.models import MotionData, PictographData


logger = logging.getLogger(__name__)


class QtPictographRenderingServiceAdapter:
    """
    Qt adapter that maintains the same interface as the original Qt-dependent service
    but uses the framework-agnostic core service internally.

    This enables a drop-in replacement that removes Qt dependencies from business logic
    while maintaining backward compatibility for existing Qt code.
    """

    _instance = None
    _creation_logged = False

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is created (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if not cls._creation_logged:
                logger.info(
                    "🎭 [QT_ADAPTER] Created Qt Pictograph Rendering Service Adapter"
                )
                cls._creation_logged = True
        return cls._instance

    def __init__(self):
        """Initialize the adapter with core services."""
        # Prevent re-initialization of singleton
        if hasattr(self, "_initialized"):
            return

        # Initialize core services (framework-agnostic)
        self._asset_provider = create_real_asset_provider()
        self._core_service = CorePictographOrchestrationService(self._asset_provider)

        # Initialize Qt render engine
        self._qt_render_engine = QtRenderEngine()

        # Performance tracking
        self._render_count = 0

        # Mark as initialized
        self._initialized = True

        logger.debug("🎭 [QT_ADAPTER] Initialized Qt adapter with core services")

    # ========================================================================
    # LEGACY INTERFACE COMPATIBILITY (Qt-dependent signatures)
    # ========================================================================

    def render_grid(
        self, scene: QGraphicsScene, grid_mode: str = "diamond"
    ) -> QGraphicsSvgItem | None:
        """
        Render grid using core service + Qt execution (legacy interface).

        This maintains the exact same signature as the original service
        but uses framework-agnostic logic internally.
        """
        try:
            # Convert Qt scene to framework-agnostic size
            scene_rect = scene.sceneRect()
            target_size = Size(
                width=int(scene_rect.width()) if scene_rect.width() > 0 else 950,
                height=int(scene_rect.height()) if scene_rect.height() > 0 else 950,
            )

            # Use core service to create render command
            grid_command = self._core_service.create_grid_command(
                grid_mode, target_size, Point(0, 0)
            )

            # Execute command with Qt render engine
            target = QtTypeConverter.create_render_target_from_scene(scene)
            success = self._qt_render_engine.execute_command(grid_command, target)

            if success:
                # Return the created Qt item for legacy compatibility
                return self._qt_render_engine._created_items.get(
                    grid_command.command_id
                )

            return None

        except Exception as e:
            logger.error(f"❌ [QT_ADAPTER] Failed to render grid: {e}")
            return None

    def render_prop(
        self,
        scene: QGraphicsScene,
        color: str,
        motion_data: MotionData,
        pictograph_data: PictographData | None = None,
    ) -> QGraphicsSvgItem | None:
        """
        Render prop using core service + Qt execution (legacy interface).

        This maintains the exact same signature as the original service
        but uses framework-agnostic logic internally.
        """
        try:
            logger.info(
                f"🎭 [QT_ADAPTER] Rendering {color} prop with motion_type: {motion_data.motion_type}"
            )

            # Use positioning services to calculate proper position
            prop_position = self._calculate_prop_position_from_motion(
                motion_data, color
            )

            # Convert motion data to dict for core service
            motion_dict = {
                "motion_type": (
                    motion_data.motion_type.value if motion_data.motion_type else "pro"
                ),
                "start_loc": str(getattr(motion_data, "start_loc", "s")),
                "end_loc": str(getattr(motion_data, "end_loc", "s")),
                "start_ori": str(getattr(motion_data, "start_ori", "in")),
                "end_ori": str(getattr(motion_data, "end_ori", "in")),
                "turns": getattr(motion_data, "turns", 0),
                "prop_type": "staff",  # Default prop type
            }

            # Use core service to create render command
            prop_command = self._core_service.create_prop_command(
                color,
                motion_dict,
                prop_position,
                (
                    self._convert_pictograph_data_to_dict(pictograph_data)
                    if pictograph_data
                    else None
                ),
            )

            # Execute command with Qt render engine
            target = QtTypeConverter.create_render_target_from_scene(scene)
            success = self._qt_render_engine.execute_command(prop_command, target)

            if success:
                self._render_count += 1
                logger.info(
                    f"✅ [QT_ADAPTER] Successfully rendered {color} prop at ({prop_position.x}, {prop_position.y})"
                )
                return self._qt_render_engine._created_items.get(
                    prop_command.command_id
                )

            logger.warning(
                f"❌ [QT_ADAPTER] Failed to execute render command for {color} prop"
            )
            return None

        except Exception as e:
            logger.error(f"❌ [QT_ADAPTER] Failed to render prop: {e}")
            return None

    def render_glyph(
        self, scene: QGraphicsScene, glyph_type: str, glyph_data: Any
    ) -> QGraphicsSvgItem | None:
        """
        Render glyph using core service + Qt execution (legacy interface).

        This maintains the exact same signature as the original service
        but uses framework-agnostic logic internally.
        """
        try:
            # Convert glyph data to dict format
            if isinstance(glyph_data, dict):
                glyph_dict = glyph_data
            else:
                # Handle other glyph data types (convert to dict)
                glyph_dict = {"id": str(glyph_data), "type": glyph_type}

            # Default position and size
            position = Point(glyph_dict.get("x", 100), glyph_dict.get("y", 100))
            size = Size(glyph_dict.get("width", 50), glyph_dict.get("height", 50))

            # Use core service to create render command
            glyph_command = self._core_service.create_glyph_command(
                glyph_type, glyph_dict, position, size
            )

            # Execute command with Qt render engine
            target = QtTypeConverter.create_render_target_from_scene(scene)
            success = self._qt_render_engine.execute_command(glyph_command, target)

            if success:
                return self._qt_render_engine._created_items.get(
                    glyph_command.command_id
                )

            return None

        except Exception as e:
            logger.error(f"❌ [QT_ADAPTER] Failed to render glyph: {e}")
            return None

    # ========================================================================
    # NEW CAPABILITIES (Framework-agnostic)
    # ========================================================================

    def render_complete_pictograph(
        self,
        scene: QGraphicsScene,
        pictograph_data: PictographData,
        options: dict | None = None,
    ) -> bool:
        """
        Render complete pictograph using core service.

        This is a new capability that leverages the framework-agnostic
        orchestration service.
        """
        try:
            # Clear previous items
            self._qt_render_engine.clear_created_items(scene)

            # Convert to dict format
            pictograph_dict = self._convert_pictograph_data_to_dict(pictograph_data)

            # Get scene size
            scene_rect = scene.sceneRect()
            target_size = Size(
                width=int(scene_rect.width()) if scene_rect.width() > 0 else 950,
                height=int(scene_rect.height()) if scene_rect.height() > 0 else 950,
            )

            # Generate all render commands
            commands = self._core_service.create_pictograph_commands(
                pictograph_dict, target_size, options
            )

            # Execute all commands
            target = QtTypeConverter.create_render_target_from_scene(scene)
            success_count = 0
            for command in commands:
                if self._qt_render_engine.execute_command(command, target):
                    success_count += 1

            logger.info(
                f"🎭 [QT_ADAPTER] Rendered {success_count}/{len(commands)} pictograph elements"
            )
            return success_count > 0

        except Exception as e:
            logger.error(f"❌ [QT_ADAPTER] Failed to render complete pictograph: {e}")
            return False

    def get_performance_stats(self) -> dict[str, Any]:
        """Get performance statistics."""
        core_stats = self._core_service.get_performance_stats()
        return {
            **core_stats,
            "qt_renders": self._render_count,
            "qt_cache_items": len(self._qt_render_engine._created_items),
        }

    def clear_scene_items(self, scene: QGraphicsScene) -> None:
        """Clear all items created by this adapter."""
        self._qt_render_engine.clear_created_items(scene)

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def _convert_pictograph_data_to_dict(
        self, pictograph_data: PictographData
    ) -> dict[str, Any]:
        """Convert PictographData to dictionary format for core service."""
        try:
            result = {
                "grid_mode": "diamond",
                "motions": {},
                "props": [],
                "glyphs": [],
            }  # Default

            # Extract motion data
            if hasattr(pictograph_data, "motions") and pictograph_data.motions:
                for color, motion_data in pictograph_data.motions.items():
                    result["motions"][color] = {
                        "motion_type": (
                            motion_data.motion_type.value
                            if motion_data.motion_type
                            else "pro"
                        ),
                        "end_x": getattr(motion_data, "end_x", 475),
                        "end_y": getattr(motion_data, "end_y", 475),
                        "prop_type": "staff",
                    }

            # Generate props from motion data using positioning services
            if hasattr(pictograph_data, "motions") and pictograph_data.motions:
                result["props"] = self._generate_props_from_motions(pictograph_data)
                logger.info(
                    f"Generated {len(result['props'])} props from {len(pictograph_data.motions)} motions"
                )

            # Extract glyph data (if any)
            if hasattr(pictograph_data, "letter") and pictograph_data.letter:
                result["glyphs"].append(
                    {
                        "type": "letter",
                        "id": pictograph_data.letter,
                        "x": 450,  # Default position
                        "y": 50,
                        "width": 50,
                        "height": 50,
                    }
                )

            return result

        except Exception as e:
            logger.error(f"Failed to convert pictograph data: {e}")
            return {"grid_mode": "diamond", "motions": {}, "props": [], "glyphs": []}

    def _generate_props_from_motions(
        self, pictograph_data: PictographData
    ) -> list[dict[str, Any]]:
        """Generate props from motion data using positioning services."""
        props = []

        try:
            # Import positioning services
            from shared.application.services.positioning.arrows.calculation import (
                ArrowLocationCalculatorService,
            )

            # Create positioning service instance
            positioning_service = ArrowLocationCalculatorService()

            # Generate props for each motion
            for color, motion_data in pictograph_data.motions.items():
                try:
                    # Calculate prop position using positioning services
                    # Use motion data to determine location and orientation
                    start_loc = getattr(motion_data, "start_loc", None)
                    end_loc = getattr(motion_data, "end_loc", None)
                    start_ori = getattr(motion_data, "start_ori", "in")
                    end_ori = getattr(motion_data, "end_ori", "in")

                    # Calculate position based on end location (where prop should be)
                    if end_loc:
                        # Use the positioning service to calculate coordinates
                        # Default to center if positioning fails
                        prop_x = 475.0  # Center X
                        prop_y = 475.0  # Center Y

                        # Try to get better positioning from location
                        location_positions = {
                            "n": (475, 200),  # North
                            "ne": (650, 200),  # Northeast
                            "e": (750, 475),  # East
                            "se": (650, 750),  # Southeast
                            "s": (475, 750),  # South
                            "sw": (300, 750),  # Southwest
                            "w": (200, 475),  # West
                            "nw": (300, 200),  # Northwest
                        }

                        if hasattr(end_loc, "value"):
                            loc_str = end_loc.value
                        else:
                            loc_str = str(end_loc).lower()

                        if loc_str in location_positions:
                            prop_x, prop_y = location_positions[loc_str]

                    # Create prop data dictionary
                    prop_dict = {
                        "type": "staff",
                        "color": color,
                        "x": prop_x,
                        "y": prop_y,
                        "motion_data": {
                            "motion_type": (
                                motion_data.motion_type.value
                                if hasattr(motion_data.motion_type, "value")
                                else str(motion_data.motion_type)
                            ),
                            "start_loc": str(start_loc),
                            "end_loc": str(end_loc),
                            "start_ori": str(start_ori),
                            "end_ori": str(end_ori),
                            "turns": getattr(motion_data, "turns", 0),
                        },
                    }

                    props.append(prop_dict)
                    logger.info(
                        f"✅ Generated prop for {color} at ({prop_x}, {prop_y}) with motion_type: {motion_data.motion_type}"
                    )

                except Exception as e:
                    logger.error(f"Failed to generate prop for {color}: {e}")
                    # Add fallback prop
                    props.append(
                        {
                            "type": "staff",
                            "color": color,
                            "x": 475,
                            "y": 475,
                            "motion_data": {},
                        }
                    )

        except Exception as e:
            logger.error(f"Failed to generate props from motions: {e}")

        return props

    def _calculate_prop_position_from_motion(
        self, motion_data: MotionData, color: str
    ) -> Point:
        """Calculate prop position from motion data using positioning services."""
        try:
            from desktop.modern.core.types.geometry import Point

            # Extract location and orientation data
            end_loc = getattr(motion_data, "end_loc", None)
            end_ori = getattr(motion_data, "end_ori", "in")

            # Default to center
            prop_x = 475.0  # Center X
            prop_y = 475.0  # Center Y

            # Calculate position based on end location (where prop should be)
            if end_loc:
                # Use the positioning service to calculate coordinates
                location_positions = {
                    "n": (475, 200),  # North
                    "ne": (650, 200),  # Northeast
                    "e": (750, 475),  # East
                    "se": (650, 750),  # Southeast
                    "s": (475, 750),  # South
                    "sw": (300, 750),  # Southwest
                    "w": (200, 475),  # West
                    "nw": (300, 200),  # Northwest
                }

                if hasattr(end_loc, "value"):
                    loc_str = end_loc.value
                else:
                    loc_str = str(end_loc).lower()

                if loc_str in location_positions:
                    prop_x, prop_y = location_positions[loc_str]

                # Apply orientation-based offsets
                if end_ori == "in":
                    prop_y -= 20  # Move up slightly for "in" orientation
                elif end_ori == "out":
                    prop_y += 20  # Move down slightly for "out" orientation
                elif end_ori == "clock":
                    prop_x += 20  # Move right for clockwise
                elif end_ori == "counter":
                    prop_x -= 20  # Move left for counter-clockwise

            logger.debug(
                f"Calculated {color} prop position: ({prop_x}, {prop_y}) from end_loc: {end_loc}, end_ori: {end_ori}"
            )
            return Point(prop_x, prop_y)

        except Exception as e:
            logger.error(f"Failed to calculate prop position: {e}")
            return Point(475.0, 475.0)  # Fallback to center
