"""
Simplified pictograph scene using modular renderers.

This scene coordinates multiple specialized renderers to create the complete pictograph.
"""

import logging
import uuid

from domain.models import BeatData
from domain.models.arrow_data import ArrowData
from domain.models.enums import LetterType
from domain.models.letter_type_classifier import LetterTypeClassifier
from domain.models.pictograph_data import PictographData
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QGraphicsScene

logger = logging.getLogger(__name__)

from presentation.components.pictograph.renderers.elemental_glyph_renderer import (
    ElementalGlyphRenderer,
)
from presentation.components.pictograph.renderers.letter_renderer import LetterRenderer
from presentation.components.pictograph.renderers.position_glyph_renderer import (
    PositionGlyphRenderer,
)
from presentation.components.pictograph.renderers.tka_glyph_renderer import (
    TKAGlyphRenderer,
)
from presentation.components.pictograph.renderers.vtg_glyph_renderer import (
    VTGGlyphRenderer,
)


class PictographScene(QGraphicsScene):
    """Graphics scene for rendering pictographs using modular renderers."""

    arrow_selected = pyqtSignal(str)  # Signal for arrow selection

    def __init__(self, parent=None):
        super().__init__(parent)

        # Generate unique ID for this scene instance
        self.scene_id = f"pictograph_scene_{uuid.uuid4().hex[:8]}"

        # Get simple visibility service
        from application.services.pictograph.simple_visibility_service import get_visibility_service
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

        # Use shared rendering service instead of per-scene renderers
        self._shared_rendering_service = None

        # Defer glyph renderer initialization until first render
        self._glyph_renderers_initialized = False

    @property
    def rendering_service(self):
        """Get shared rendering service for optimal performance."""
        if self._shared_rendering_service is None:
            try:
                self._shared_rendering_service = self._get_shared_rendering_service()
            except Exception as e:
                logger.debug(f"[SCENE] Deferred rendering service resolution failed: {e}")
                return None
        return self._shared_rendering_service

    def _get_shared_rendering_service(self):
        """Get shared rendering service from DI container."""
        try:
            from core.dependency_injection.di_container import get_container
            from core.interfaces.pictograph_rendering_services import (
                IPictographRenderingService,
            )

            container = get_container()
            service = container.resolve(IPictographRenderingService)
            logger.debug(f"[SCENE] Connected to shared rendering service: {self.scene_id}")
            return service

        except Exception as e:
            logger.error(f"[SCENE] Failed to get shared rendering service: {e}")
            return None

    def _create_arrow_directly(self, color: str, motion_data, full_pictograph_data):
        """Create arrow directly without any renderer (legacy approach)."""
        from presentation.components.pictograph.graphics_items.arrow_item import (
            ArrowItem,
        )

        arrow_item = ArrowItem()
        arrow_item.arrow_color = color

        arrow_item.update_arrow(
            color=color, motion_data=motion_data, pictograph_data=full_pictograph_data
        )

        self.addItem(arrow_item)
        logger.debug(f"[SCENE] Created {color} arrow directly for scene {self.scene_id}")

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
            from application.services.pictograph.arrow_rendering_service import (
                ArrowRenderingService,
            )
            from core.dependency_injection.di_container import get_container
            from core.interfaces.positioning_services import (
                IArrowCoordinateSystemService,
                IArrowPositioningOrchestrator,
            )

            container = get_container()

            self._positioning_orchestrator = container.resolve(IArrowPositioningOrchestrator)
            self._coordinate_system = container.resolve(IArrowCoordinateSystemService)
            self._arrow_rendering_service = ArrowRenderingService()

            logger.debug(f"Scene {self.scene_id}: Successfully initialized shared services")
            self._services_initialized = True

        except Exception as e:
            logger.debug(f"Scene {self.scene_id}: Deferred shared services initialization: {e}")

    def update_visibility(self, element_type: str, element_name: str, visible: bool):
        """
        Update visibility of specific elements in this scene.
        
        This method is called by external visibility controls to update what should be rendered.
        """
        try:
            logger.debug(f"PictographScene {self.scene_id}: Updating {element_name} visibility to {visible}")
            
            # Update the simple visibility service
            self._visibility_service.set_element_visibility(element_type, element_name, visible)
            
            # No need to re-render here - parent component should call render_pictograph() when needed

        except Exception as e:
            logger.error(f"Error updating visibility in PictographScene {self.scene_id}: {e}")

    def render_pictograph(self, pictograph_data: "PictographData") -> None:
        """Render a complete pictograph from pictograph data."""
        self._initialize_shared_services()
        self._initialize_glyph_renderers()

        self.clear()
        if self.rendering_service and hasattr(self.rendering_service, "clear_rendered_props"):
            self.rendering_service.clear_rendered_props()
            
        self._render_pictograph_data(pictograph_data)

    def update_beat(self, beat_data: BeatData) -> None:
        """Legacy method: Convert beat data to pictograph data and render."""
        self.render_pictograph(beat_data.pictograph_data)

    def _render_pictograph_data(self, pictograph_data: PictographData) -> None:
        """Render the pictograph elements using specialized renderers."""
        if not pictograph_data:
            return

        # Render grid using shared service (if visible)
        if self._visibility_service.get_element_visibility("other", "grid"):
            if self.rendering_service:
                grid_mode = (
                    pictograph_data.grid_data.grid_mode.value
                    if pictograph_data.grid_data
                    else "diamond"
                )
                self.rendering_service.render_grid(self, grid_mode)
            else:
                logger.warning(f"[SCENE] No rendering service available for grid: {self.scene_id}")

        # Extract motion data
        blue_motion = pictograph_data.motions.get("blue")
        red_motion = pictograph_data.motions.get("red")

        # Render props using shared service (if visible)
        if self._visibility_service.get_element_visibility("other", "props"):
            if blue_motion and self._visibility_service.get_motion_visibility("blue"):
                if self.rendering_service:
                    self.rendering_service.render_prop(self, "blue", blue_motion, pictograph_data)
                else:
                    logger.warning(f"[SCENE] No rendering service available for blue prop: {self.scene_id}")
                    
            if red_motion and self._visibility_service.get_motion_visibility("red"):
                if self.rendering_service:
                    self.rendering_service.render_prop(self, "red", red_motion, pictograph_data)
                else:
                    logger.warning(f"[SCENE] No rendering service available for red prop: {self.scene_id}")

        # Create full pictograph data for arrow rendering
        full_pictograph_data = PictographData(
            arrows={
                "blue": pictograph_data.arrows.get("blue", ArrowData(color="blue")),
                "red": pictograph_data.arrows.get("red", ArrowData(color="red")),
            },
            motions=pictograph_data.motions,
            letter=pictograph_data.letter,
            glyph_data=pictograph_data.glyph_data,
        )

        # Render arrows directly (if visible)
        if self._visibility_service.get_element_visibility("other", "arrows"):
            if blue_motion and self._visibility_service.get_motion_visibility("blue"):
                self._create_arrow_directly("blue", blue_motion, full_pictograph_data)
            if red_motion and self._visibility_service.get_motion_visibility("red"):
                self._create_arrow_directly("red", red_motion, full_pictograph_data)

        # Render glyphs if glyph data is available and visibility allows
        if pictograph_data.glyph_data:
            glyph_data = pictograph_data.glyph_data

            # Render elemental glyph (if visible)
            if (
                glyph_data.show_elemental
                and glyph_data.vtg_mode
                and self._visibility_service.get_glyph_visibility("Elemental")
            ):
                self.elemental_glyph_renderer.render_elemental_glyph(
                    glyph_data.vtg_mode,
                    glyph_data.letter_type.value if glyph_data.letter_type else None,
                )

            # Render VTG glyph (if visible)
            if (
                glyph_data.show_vtg
                and glyph_data.vtg_mode
                and self._visibility_service.get_glyph_visibility("VTG")
            ):
                self.vtg_glyph_renderer.render_vtg_glyph(
                    glyph_data.vtg_mode,
                    glyph_data.letter_type.value if glyph_data.letter_type else None,
                )

            # Render TKA glyph (if visible)
            if (
                glyph_data.show_tka
                and pictograph_data.letter
                and self._visibility_service.get_glyph_visibility("TKA")
            ):
                letter_type_str = LetterTypeClassifier.get_letter_type(pictograph_data.letter)
                letter_type = LetterType(letter_type_str)

                self.tka_glyph_renderer.render_tka_glyph(
                    pictograph_data.letter,
                    letter_type,
                    glyph_data.has_dash,
                    glyph_data.turns_data,
                )

            # Render position glyph (if visible)
            if (
                glyph_data.show_positions
                and glyph_data.start_position
                and glyph_data.end_position
                and self._visibility_service.get_glyph_visibility("Positions")
            ):
                self.position_glyph_renderer.render_position_glyph(
                    glyph_data.start_position,
                    glyph_data.end_position,
                    pictograph_data.letter,
                )
