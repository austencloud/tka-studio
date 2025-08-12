"""
Simplified pictograph scene using modular renderers.

This scene coordinates multiple specialized renderers to create the complete pictograph.
"""

from __future__ import annotations

import logging
import uuid

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QGraphicsScene
from shared.application.services.pictograph.pictograph_visibility_manager import (
    get_pictograph_visibility_manager,
)

from desktop.modern.domain.models import BeatData
from desktop.modern.domain.models.arrow_data import ArrowData
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.pictograph_utils import (
    compute_vtg_mode,
    should_show_elemental,
    should_show_positions,
    should_show_tka,
    should_show_vtg,
)


logger = logging.getLogger(__name__)

from desktop.modern.presentation.components.pictograph.renderers.elemental_glyph_renderer import (
    ElementalGlyphRenderer,
)
from desktop.modern.presentation.components.pictograph.renderers.letter_renderer import (
    LetterRenderer,
)
from desktop.modern.presentation.components.pictograph.renderers.position_glyph_renderer import (
    PositionGlyphRenderer,
)
from desktop.modern.presentation.components.pictograph.renderers.tka_glyph_renderer import (
    TKAGlyphRenderer,
)
from desktop.modern.presentation.components.pictograph.renderers.vtg_glyph_renderer import (
    VTGGlyphRenderer,
)


class PictographScene(QGraphicsScene):
    """Graphics scene for rendering pictographs using modular renderers."""

    arrow_selected = pyqtSignal(str)  # Signal for arrow selection
    visibility_changed = pyqtSignal()  # Signal when visibility settings change

    def __init__(self, parent=None):
        super().__init__(parent)

        # Generate unique ID for this scene instance
        self.scene_id = f"pictograph_scene_{uuid.uuid4().hex[:8]}"

        # Get simple visibility service
        from shared.application.services.pictograph.simple_visibility_service import (
            get_visibility_service,
        )

        self._visibility_service = get_visibility_service()

        self.SCENE_SIZE = 950
        self.CENTER_X = 475
        self.CENTER_Y = 475

        self.setSceneRect(0, 0, self.SCENE_SIZE, self.SCENE_SIZE)
        self.setBackgroundBrush(QBrush(QColor(255, 255, 255)))

        # Get shared positioning services for efficient arrow rendering
        self._positioning_orchestrator = None
        self._coordinate_system = None
        self._arrow_rendering_service = None
        self._services_initialized = False

        # Store the last rendered data for refresh capability
        self._last_pictograph_data: PictographData | None = None

        # Store the last rendered data for refresh capability
        self._last_pictograph_data: PictographData | None = None

        # Use shared rendering service instead of per-scene renderers
        self._shared_rendering_service = None

        # Defer glyph renderer initialization until first render
        self._glyph_renderers_initialized = False

    @property
    def rendering_service(self):
        """Get shared rendering service for optimal performance with retry logic."""
        if self._shared_rendering_service is None:
            try:
                self._shared_rendering_service = self._get_shared_rendering_service()
                if self._shared_rendering_service is None:
                    # Service not available yet, will retry on next access
                    logger.debug(
                        "[SCENE] Rendering service not available yet, will retry later"
                    )
            except Exception as e:
                logger.debug(
                    f"[SCENE] Deferred rendering service resolution failed: {e}"
                )
                return None
        return self._shared_rendering_service

    def _get_shared_rendering_service(self):
        """Get shared rendering service from DI container with retry logic."""
        try:
            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
            )
            from desktop.modern.core.interfaces.pictograph_rendering_services import (
                IPictographRenderingService,
            )

            container = get_container()

            # Check if container has services registered (avoid empty container)
            service_count = len(getattr(container, "_services", {}))
            if (
                service_count < 50
            ):  # Expect at least 50 services for full initialization
                logger.debug(
                    f"[SCENE] Container not fully initialized yet ({service_count} services), deferring rendering service resolution"
                )
                return None

            service = container.resolve(IPictographRenderingService)
            logger.debug(
                f"[SCENE] Successfully resolved rendering service: {type(service)} from container with {service_count} services"
            )
            return service

        except Exception as e:
            logger.debug(f"[SCENE] Failed to get shared rendering service: {e}")
            return None

    def _create_arrow_directly(self, color: str, motion_data, full_pictograph_data):
        """Create arrow directly without any renderer (legacy approach)."""
        from desktop.modern.presentation.components.pictograph.graphics_items.arrow_item import (
            ArrowItem,
        )

        arrow_item = ArrowItem()
        arrow_item.arrow_color = color

        arrow_item.update_arrow(
            color=color, motion_data=motion_data, pictograph_data=full_pictograph_data
        )

        self.addItem(arrow_item)

    def _initialize_glyph_renderers(self):
        """Initialize glyph renderers (lazy-loaded)."""
        if self._glyph_renderers_initialized:
            return

        self.letter_renderer = LetterRenderer(self)
        self.elemental_glyph_renderer = ElementalGlyphRenderer(self)
        self.vtg_glyph_renderer = VTGGlyphRenderer(self)
        self.tka_glyph_renderer = TKAGlyphRenderer(self)
        self.position_glyph_renderer = PositionGlyphRenderer(self)

        self._glyph_renderers_initialized = True

    def _initialize_shared_services(self):
        """Initialize shared services that will be injected into renderers."""
        if self._services_initialized:
            return

        try:
            from shared.application.services.pictograph.arrow_rendering_service import (
                ArrowRenderingService,
            )

            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
            )
            from desktop.modern.core.interfaces.positioning_services import (
                IArrowCoordinateSystemService,
                IArrowPositioningOrchestrator,
            )

            container = get_container()

            self._positioning_orchestrator = container.resolve(
                IArrowPositioningOrchestrator
            )
            self._coordinate_system = container.resolve(IArrowCoordinateSystemService)
            self._arrow_rendering_service = ArrowRenderingService()

            self._services_initialized = True

        except Exception as e:
            logger.debug(
                f"Scene {self.scene_id}: Deferred shared services initialization: {e}"
            )

    def update_visibility(self, element_type: str, element_name: str, visible: bool):
        """
        Update visibility of specific elements in this scene using targeted visibility updates.

        This method is called by external visibility controls to update what should be rendered.
        """
        try:
            # Update the simple visibility service
            self._visibility_service.set_element_visibility(
                element_type, element_name, visible
            )

            # Apply targeted visibility update to specific rendered elements
            self._update_element_visibility(element_type, element_name, visible)

            # Emit signal that visibility changed
            self.visibility_changed.emit()

        except Exception as e:
            logger.error(
                f"Error updating visibility in PictographScene {self.scene_id}: {e}"
            )
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")

    def _update_element_visibility(
        self, element_type: str, element_name: str, visible: bool
    ):
        """
        Update visibility of specific rendered elements without full re-rendering.
        """
        try:
            if element_type == "motion":
                # Handle motion visibility (affects both props and arrows)
                color = element_name.replace("_motion", "")
                updated_items = 0

                # Find and update arrow items
                for item in self.items():
                    if hasattr(item, "arrow_color") and item.arrow_color == color:
                        item.setVisible(visible)
                        updated_items += 1

                # Force immediate view update for targeted changes
                if updated_items > 0:
                    self._force_view_update()

                # For props and other elements, we need to check if dependency handling is needed
                # For now, fall back to refresh for complex cases
                if updated_items == 0:
                    self.refresh_with_current_visibility()
                    return

            elif element_type == "glyph" or element_type == "other":
                # For glyphs and other elements, use the full refresh approach
                # since identifying specific glyph items is complex
                self.refresh_with_current_visibility()
                return

        except Exception as e:
            logger.error(f"Error in targeted visibility update: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            # Fallback to full refresh if targeted update fails
            try:
                self.refresh_with_current_visibility()
            except Exception as refresh_error:
                logger.error(f"Even refresh failed: {refresh_error}")

    def render_pictograph(self, pictograph_data: PictographData) -> None:
        """Render a complete pictograph from pictograph data."""
        self._initialize_shared_services()
        self._initialize_glyph_renderers()

        # Store the data for potential refresh operations
        self._last_pictograph_data = pictograph_data

        # Force retry of rendering service if not available (critical for Learn tab)
        if not self.rendering_service:
            logger.debug(
                "[SCENE] Forcing rendering service retry for pictograph rendering"
            )
            self._shared_rendering_service = None  # Reset to force retry

        self.clear()
        if self.rendering_service and hasattr(
            self.rendering_service, "clear_rendered_props"
        ):
            self.rendering_service.clear_rendered_props()

        self._render_pictograph_data(pictograph_data)

    def refresh_with_current_visibility(self) -> None:
        """Re-render the pictograph with current visibility settings."""
        if self._last_pictograph_data:
            # Re-render with the same data but current visibility settings
            self.render_pictograph(self._last_pictograph_data)
            # Force immediate graphics view update
            self._force_view_update()

    def _force_view_update(self) -> None:
        """Force all views of this scene to immediately update their display."""
        try:
            views = self.views()
            if not views:
                logger.debug(f"No views found for scene {self.scene_id}")
                return

            for view in views:
                if view and hasattr(view, "viewport") and hasattr(view, "update"):
                    try:
                        view.viewport().update()
                        view.update()
                    except Exception as view_error:
                        logger.debug(f"Error updating individual view: {view_error}")
        except Exception as e:
            logger.debug(f"Error forcing view update for scene {self.scene_id}: {e}")

    def update_beat(self, beat_data: BeatData) -> None:
        """Legacy method: Convert beat data to pictograph data and render."""
        self.render_pictograph(beat_data.pictograph_data)

    def _render_pictograph_data(self, pictograph_data: PictographData) -> None:
        """Render the pictograph elements using specialized renderers."""
        if not pictograph_data:
            return

        # Render grid using shared service (if visible)
        grid_visible = self._visibility_service.get_element_visibility("other", "grid")

        if grid_visible:
            # Force retry of rendering service if not available
            if not self.rendering_service:
                self._shared_rendering_service = None  # Reset to force retry

            if self.rendering_service:
                grid_mode = (
                    pictograph_data.grid_data.grid_mode.value
                    if pictograph_data.grid_data
                    else "diamond"
                )
                self.rendering_service.render_grid(self, grid_mode)
            else:
                logger.warning(
                    f"[SCENE] No rendering service available for grid: {self.scene_id}"
                )

        # Extract motion data
        blue_motion = pictograph_data.motions.get("blue")
        red_motion = pictograph_data.motions.get("red")

        # Render props using shared service (if visible)
        if self._visibility_service.get_element_visibility("other", "props"):
            if blue_motion and self._visibility_service.get_motion_visibility("blue"):
                if self.rendering_service:
                    self.rendering_service.render_prop(
                        self, "blue", blue_motion, pictograph_data
                    )
                else:
                    logger.warning(
                        f"[SCENE] No rendering service available for blue prop: {self.scene_id}"
                    )

            if red_motion and self._visibility_service.get_motion_visibility("red"):
                if self.rendering_service:
                    self.rendering_service.render_prop(
                        self, "red", red_motion, pictograph_data
                    )
                else:
                    logger.warning(
                        f"[SCENE] No rendering service available for red prop: {self.scene_id}"
                    )
        else:
            logger.info(f"🚫 [SCENE] Props are not visible in scene {self.scene_id}")

        # Create full pictograph data for arrow rendering
        full_pictograph_data = PictographData(
            arrows={
                "blue": pictograph_data.arrows.get("blue", ArrowData(color="blue")),
                "red": pictograph_data.arrows.get("red", ArrowData(color="red")),
            },
            motions=pictograph_data.motions,
            letter=pictograph_data.letter,
        )

        # Render arrows directly (if visible)
        if self._visibility_service.get_element_visibility("other", "arrows"):
            if blue_motion and self._visibility_service.get_motion_visibility("blue"):
                self._create_arrow_directly("blue", blue_motion, full_pictograph_data)
            if red_motion and self._visibility_service.get_motion_visibility("red"):
                self._create_arrow_directly("red", red_motion, full_pictograph_data)

        # Render glyphs using computed data from PictographData
        if pictograph_data.letter:
            visibility_manager = get_pictograph_visibility_manager()
            pictograph_id = pictograph_data.id

            # Compute derived data from PictographData
            vtg_mode = compute_vtg_mode(pictograph_data)
            letter_type = pictograph_data.letter_type

            # Initialize visibility if not already set
            if pictograph_id not in visibility_manager._pictograph_visibility:
                visibility_manager.initialize_pictograph_visibility(
                    pictograph_id, letter_type
                )

            # Render elemental glyph (if visible)
            if (
                should_show_elemental(letter_type)
                and visibility_manager.get_pictograph_visibility(
                    pictograph_id, "elemental"
                )
                and vtg_mode
                and self._visibility_service.get_glyph_visibility("Elemental")
            ):
                self.elemental_glyph_renderer.render_elemental_glyph(
                    vtg_mode,
                    letter_type.value if letter_type else None,
                )

            # Render VTG glyph (if visible)
            if (
                should_show_vtg(letter_type)
                and visibility_manager.get_pictograph_visibility(pictograph_id, "vtg")
                and vtg_mode
                and self._visibility_service.get_glyph_visibility("VTG")
            ):
                self.vtg_glyph_renderer.render_vtg_glyph(
                    vtg_mode,
                    letter_type.value if letter_type else None,
                )

            # Render TKA glyph (if visible)
            should_show = should_show_tka(letter_type)
            pictograph_visible = visibility_manager.get_pictograph_visibility(
                pictograph_id, "tka"
            )
            glyph_visible = self._visibility_service.get_glyph_visibility("TKA")

            if should_show and pictograph_visible and glyph_visible:
                from desktop.modern.domain.models.pictograph_utils import (
                    get_turns_from_motions,
                    has_dash_from_pictograph,
                )

                has_dash = has_dash_from_pictograph(pictograph_data)
                turns_data = get_turns_from_motions(pictograph_data)

                self.tka_glyph_renderer.render_tka_glyph(
                    pictograph_data.letter,
                    letter_type,
                    has_dash,
                    turns_data,
                )

            # Render position glyph (if visible)
            if (
                should_show_positions(letter_type)
                and visibility_manager.get_pictograph_visibility(
                    pictograph_id, "positions"
                )
                and pictograph_data.start_position
                and pictograph_data.end_position
                and self._visibility_service.get_glyph_visibility("Positions")
            ):
                self.position_glyph_renderer.render_position_glyph(
                    pictograph_data.start_position,
                    pictograph_data.end_position,
                    pictograph_data.letter,
                )
