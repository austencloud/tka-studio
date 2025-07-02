"""
Simplified pictograph scene using modular renderers.

This scene coordinates multiple specialized renderers to create the complete pictograph.
"""

from typing import Optional
import logging
import uuid
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtCore import pyqtSignal

from domain.models.core_models import BeatData, LetterType
from domain.models.letter_type_classifier import LetterTypeClassifier

logger = logging.getLogger(__name__)

from presentation.components.pictograph.renderers.grid_renderer import (
    GridRenderer,
)
from presentation.components.pictograph.renderers.prop_renderer import (
    PropRenderer,
)
from presentation.components.pictograph.renderers.arrow_renderer import (
    ArrowRenderer,
)
from presentation.components.pictograph.renderers.letter_renderer import (
    LetterRenderer,
)
from presentation.components.pictograph.renderers.elemental_glyph_renderer import (
    ElementalGlyphRenderer,
)
from presentation.components.pictograph.renderers.vtg_glyph_renderer import (
    VTGGlyphRenderer,
)
from presentation.components.pictograph.renderers.tka_glyph_renderer import (
    TKAGlyphRenderer,
)
from presentation.components.pictograph.renderers.position_glyph_renderer import (
    PositionGlyphRenderer,
)


class PictographScene(QGraphicsScene):
    """Graphics scene for rendering pictographs using modular renderers."""

    arrow_selected = pyqtSignal(str)  # Signal for arrow selection

    def __init__(self, parent=None):
        super().__init__(parent)
        self.beat_data: Optional[BeatData] = None

        # Generate unique ID for this scene instance
        self.scene_id = f"pictograph_scene_{uuid.uuid4().hex[:8]}"

        # Track visibility states for each renderer
        self._renderer_visibility = {
            "grid": True,
            "props": True,
            "arrows": True,
            "tka": True,
            "vtg": True,
            "elemental": True,
            "positions": True,
            "reversals": True,
            "non_radial": True,
        }

        self.SCENE_SIZE = 950
        self.CENTER_X = 475
        self.CENTER_Y = 475

        self.setSceneRect(0, 0, self.SCENE_SIZE, self.SCENE_SIZE)
        self.setBackgroundBrush(QBrush(QColor(255, 255, 255)))

        # Initialize renderers
        self.grid_renderer = GridRenderer(self)
        self.prop_renderer = PropRenderer(self)
        self.arrow_renderer = ArrowRenderer(self)
        self.letter_renderer = LetterRenderer(self)  # Initialize glyph renderers
        self.elemental_glyph_renderer = ElementalGlyphRenderer(self)
        self.vtg_glyph_renderer = VTGGlyphRenderer(self)
        self.tka_glyph_renderer = TKAGlyphRenderer(self)
        self.position_glyph_renderer = PositionGlyphRenderer(self)

        # Register with global visibility service
        self._register_with_global_service()

    def _register_with_global_service(self):
        """Register this scene with the global visibility service."""
        try:
            # Try to get the global visibility service from the DI container
            from core.application.application_factory import ApplicationFactory
            from application.services.pictograph.global_visibility_service import (
                GlobalVisibilityService,
            )

            # Get or create global service instance
            try:
                from core.application.application_factory import get_container

                container = get_container()
                if container:
                    # Try to resolve from container (if registered)
                    global_service = container.resolve(GlobalVisibilityService)
                else:
                    # Fallback to singleton pattern
                    global_service = self._get_global_service_singleton()
            except Exception:
                # Fallback to singleton pattern
                global_service = self._get_global_service_singleton()

            if global_service:
                # Determine component type from parent hierarchy
                component_type = self._determine_component_type()

                # Register this scene
                success = global_service.register_pictograph(
                    pictograph_id=self.scene_id,
                    pictograph_instance=self,
                    component_type=component_type,
                    update_method="update_visibility",
                    metadata={
                        "scene_size": self.SCENE_SIZE,
                        "has_renderers": True,
                        "created_at": str(uuid.uuid4()),
                    },
                )

                if success:
                    logger.debug(
                        f"Registered PictographScene {self.scene_id} with GlobalVisibilityService"
                    )
                else:
                    logger.warning(
                        f"Failed to register PictographScene {self.scene_id}"
                    )

        except Exception as e:
            logger.warning(f"Could not register with GlobalVisibilityService: {e}")

    def _get_global_service_singleton(self):
        """Get or create global service singleton."""
        if not hasattr(PictographScene, "_global_service"):
            from application.services.pictograph.global_visibility_service import (
                GlobalVisibilityService,
            )

            PictographScene._global_service = GlobalVisibilityService()
        return PictographScene._global_service

    def _determine_component_type(self) -> str:
        """
        Determine component type using the robust context service.

        This method is deprecated and maintained for backward compatibility.
        New code should use the context service directly.
        """
        try:
            # Try to get context service from DI container
            from core.application.application_factory import ApplicationFactory
            from core.interfaces.core_services import IPictographContextService
            from application.services.ui.context_aware_scaling_service import (
                RenderingContext,
            )

            # Use proper application factory method
            container = ApplicationFactory.create_app_from_args()
            if container:
                context_service = container.resolve(IPictographContextService)
                print(
                    f"✅ [PICTOGRAPH_SCENE] Successfully resolved IPictographContextService: {type(context_service).__name__}"
                )
                context = context_service.determine_context_from_scene(self)

                # Convert enum to string for backward compatibility
                context_map = {
                    RenderingContext.GRAPH_EDITOR: "graph_editor",
                    RenderingContext.BEAT_FRAME: "beat_frame",
                    RenderingContext.OPTION_PICKER: "option_picker",
                    RenderingContext.PREVIEW: "preview",
                    RenderingContext.SEQUENCE_VIEWER: "sequence_viewer",
                    RenderingContext.UNKNOWN: "unknown",
                }

                result = context_map.get(context, "unknown")
                print(f"✅ [SCENE_CONTEXT] Context service determined: {result}")
                return result

        except Exception as e:
            print(f"⚠️ [SCENE_CONTEXT] Context service failed, using fallback: {e}")

        # Fallback to original logic for backward compatibility
        return self._legacy_determine_component_type()

    def _legacy_determine_component_type(self) -> str:
        """Legacy context detection method (deprecated)."""
        parent = self.parent()
        hierarchy = []
        while parent:
            class_name = parent.__class__.__name__.lower()
            hierarchy.append(class_name)
            print(f"🔍 [SCENE_CONTEXT] Checking parent: {class_name}")

            if "grapheditor" in class_name:
                print(f"✅ [SCENE_CONTEXT] Found graph_editor context!")
                return "graph_editor"
            elif "beat" in class_name:
                print(f"✅ [SCENE_CONTEXT] Found beat_frame context!")
                return "beat_frame"
            elif "option" in class_name or "clickable" in class_name:
                print(f"✅ [SCENE_CONTEXT] Found option_picker context!")
                return "option_picker"
            elif "preview" in class_name:
                print(f"✅ [SCENE_CONTEXT] Found preview context!")
                return "preview"
            elif "sequence" in class_name:
                print(f"✅ [SCENE_CONTEXT] Found sequence_viewer context!")
                return "sequence_viewer"
            parent = parent.parent() if hasattr(parent, "parent") else None

        print(f"⚠️ [SCENE_CONTEXT] Unknown context! Hierarchy: {' -> '.join(hierarchy)}")
        return "unknown"

    def is_in_graph_editor_context(self) -> bool:
        """Check if this scene is being used in a graph editor context."""
        return self._determine_component_type() == "graph_editor"

    def update_visibility(self, element_type: str, element_name: str, visible: bool):
        """Update visibility of specific elements in this scene."""
        try:
            logger.debug(
                f"PictographScene {self.scene_id}: Updating {element_name} visibility to {visible}"
            )

            # Update internal visibility tracking
            if element_name in self._renderer_visibility:
                self._renderer_visibility[element_name] = visible

            # Apply visibility changes to renderers
            if element_name == "TKA":
                self._set_renderer_visibility("tka", visible)
            elif element_name == "VTG":
                self._set_renderer_visibility("vtg", visible)
            elif element_name == "Elemental":
                self._set_renderer_visibility("elemental", visible)
            elif element_name == "Positions":
                self._set_renderer_visibility("positions", visible)
            elif element_name == "Reversals":
                self._set_renderer_visibility("reversals", visible)
            elif element_name == "Non-radial_points":
                self._set_renderer_visibility("non_radial", visible)
            elif element_name in ["red_motion", "blue_motion"]:
                # Motion visibility affects props and arrows
                self._set_motion_visibility(element_name, visible)

            # Re-render the scene with updated visibility
            if self.beat_data:
                self._render_pictograph()

        except Exception as e:
            logger.error(
                f"Error updating visibility in PictographScene {self.scene_id}: {e}"
            )

    def _set_renderer_visibility(self, renderer_type: str, visible: bool):
        """Set visibility for a specific renderer type."""
        self._renderer_visibility[renderer_type] = visible

        # Note: Individual renderers don't have setVisible() methods
        # Visibility is controlled by whether they render or not during _render_pictograph()

    def _set_motion_visibility(self, motion_type: str, visible: bool):
        """Set visibility for motion-related renderers."""
        if motion_type == "red_motion":
            self._renderer_visibility["props"] = (
                visible or self._renderer_visibility.get("blue_motion", True)
            )
            self._renderer_visibility["arrows"] = (
                visible or self._renderer_visibility.get("blue_motion", True)
            )
        elif motion_type == "blue_motion":
            self._renderer_visibility["props"] = (
                visible or self._renderer_visibility.get("red_motion", True)
            )
            self._renderer_visibility["arrows"] = (
                visible or self._renderer_visibility.get("red_motion", True)
            )

    def update_beat(self, beat_data: BeatData) -> None:
        """Update the scene with new beat data."""
        self.beat_data = beat_data
        self.clear()
        # Clear prop renderer cache for new beat
        self.prop_renderer.clear_rendered_props()
        self._render_pictograph()

    def _render_pictograph(self) -> None:
        """Render the pictograph elements using specialized renderers."""
        if not self.beat_data:
            return

        # Render grid (if visible)
        if self._renderer_visibility.get("grid", True):
            self.grid_renderer.render_grid()

        # Render props for blue and red motions (if visible)
        if self._renderer_visibility.get("props", True):
            if self.beat_data.blue_motion and self._renderer_visibility.get(
                "blue_motion", True
            ):
                self.prop_renderer.render_prop("blue", self.beat_data.blue_motion)
            if self.beat_data.red_motion and self._renderer_visibility.get(
                "red_motion", True
            ):
                self.prop_renderer.render_prop("red", self.beat_data.red_motion)

        # Apply beta prop positioning after both props are rendered
        if self.beat_data.blue_motion and self.beat_data.red_motion:
            self.prop_renderer.apply_beta_positioning(self.beat_data)

        # CRITICAL FIX: Always create full pictograph data for special placement service
        # The special placement service requires both blue and red arrow data to generate
        # orientation keys and turns tuples, even when only one arrow is being rendered
        from domain.models.pictograph_models import PictographData, ArrowData

        # Create arrow data for both colors, using None motion_data if not available
        blue_arrow = (
            ArrowData(motion_data=self.beat_data.blue_motion, color="blue")
            if self.beat_data.blue_motion
            else ArrowData(color="blue")
        )

        red_arrow = (
            ArrowData(motion_data=self.beat_data.red_motion, color="red")
            if self.beat_data.red_motion
            else ArrowData(color="red")
        )

        # Always create full pictograph data with both arrows and letter
        full_pictograph_data = PictographData(
            arrows={"blue": blue_arrow, "red": red_arrow},
            letter=self.beat_data.letter,  # Essential for special placement lookup
        )

        # Render arrows using the full pictograph data (if visible)
        if self._renderer_visibility.get("arrows", True):
            if self.beat_data.blue_motion and self._renderer_visibility.get(
                "blue_motion", True
            ):
                self.arrow_renderer.render_arrow(
                    "blue", self.beat_data.blue_motion, full_pictograph_data
                )
            if self.beat_data.red_motion and self._renderer_visibility.get(
                "red_motion", True
            ):
                self.arrow_renderer.render_arrow(
                    "red", self.beat_data.red_motion, full_pictograph_data
                )

        # Render glyphs if glyph data is available and visibility allows
        # Note: Letters are rendered via TKA glyph, not simple letter renderer
        if self.beat_data.glyph_data:
            glyph_data = self.beat_data.glyph_data

            # Render elemental glyph (if visible)
            if (
                glyph_data.show_elemental
                and glyph_data.vtg_mode
                and self._renderer_visibility.get("elemental", True)
            ):
                self.elemental_glyph_renderer.render_elemental_glyph(
                    glyph_data.vtg_mode,
                    glyph_data.letter_type.value if glyph_data.letter_type else None,
                )

            # Render VTG glyph (if visible)
            if (
                glyph_data.show_vtg
                and glyph_data.vtg_mode
                and self._renderer_visibility.get("vtg", True)
            ):
                self.vtg_glyph_renderer.render_vtg_glyph(
                    glyph_data.vtg_mode,
                    glyph_data.letter_type.value if glyph_data.letter_type else None,
                )

            # Render TKA glyph (if visible)
            if (
                glyph_data.show_tka
                and self.beat_data.letter
                and self._renderer_visibility.get("tka", True)
            ):
                # Determine the correct letter type from the actual letter
                letter_type_str = LetterTypeClassifier.get_letter_type(
                    self.beat_data.letter
                )
                letter_type = LetterType(letter_type_str)

                self.tka_glyph_renderer.render_tka_glyph(
                    self.beat_data.letter,
                    letter_type,
                    glyph_data.has_dash,
                    glyph_data.turns_data,
                )

            # Render position glyph (if visible)
            if (
                glyph_data.show_positions
                and glyph_data.start_position
                and glyph_data.end_position
                and self._renderer_visibility.get("positions", True)
            ):
                self.position_glyph_renderer.render_position_glyph(
                    glyph_data.start_position,
                    glyph_data.end_position,
                    self.beat_data.letter,
                )
