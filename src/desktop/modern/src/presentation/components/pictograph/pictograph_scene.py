"""
Simplified pictograph scene using modular renderers.

This scene coordinates multiple specialized renderers to create the complete pictograph.
"""

import logging
import uuid
from typing import Optional

from domain.models import BeatData
from domain.models.arrow_data import ArrowData
from domain.models.enums import LetterType
from domain.models.letter_type_classifier import LetterTypeClassifier
from domain.models.pictograph_data import PictographData
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QGraphicsScene

logger = logging.getLogger(__name__)

from presentation.components.pictograph.renderers.arrow_renderer import ArrowRenderer
from presentation.components.pictograph.renderers.elemental_glyph_renderer import (
    ElementalGlyphRenderer,
)
from presentation.components.pictograph.renderers.grid_renderer import GridRenderer
from presentation.components.pictograph.renderers.letter_renderer import LetterRenderer
from presentation.components.pictograph.renderers.position_glyph_renderer import (
    PositionGlyphRenderer,
)
from presentation.components.pictograph.renderers.prop_renderer import PropRenderer
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
        # Removed beat_data storage - scene is now stateless

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
            from application.services.pictograph.global_visibility_service import (
                PictographVisibilityManager,
            )
            from application.services.pictograph.global_visibility_service_singleton import (
                get_global_visibility_service,
            )

            # Get or create global service instance
            try:
                from core.application.application_factory import get_container

                container = get_container()
                if container:
                    # Try to resolve from container (if registered)
                    global_service = container.resolve(PictographVisibilityManager)
                else:
                    # Fallback to singleton pattern
                    global_service = get_global_visibility_service()
            except Exception:
                # Fallback to singleton pattern
                global_service = get_global_visibility_service()

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

    def _determine_component_type(self) -> str:
        """
        Determine component type using the robust context service.

        This method is deprecated and maintained for backward compatibility.
        New code should use the context service directly.
        """
        try:
            # Try to get context service from DI container
            from application.services.pictograph.scaling_service import RenderingContext
            from core.application.application_factory import ApplicationFactory
            from core.interfaces.core_services import IPictographContextDetector

            # Use proper application factory method
            container = ApplicationFactory.create_app_from_args()
            if container:
                context_service = container.resolve(IPictographContextDetector)
                # Removed repetitive log statement
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
                # Removed repetitive log statement
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

            # Note: Scene no longer auto-renders on visibility changes
            # Parent component should call update_beat() to re-render with new visibility

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

    def render_pictograph(self, pictograph_data: "PictographData") -> None:
        """Render a complete pictograph from pictograph data."""
        self.clear()
        # Clear prop renderer cache for new pictograph
        self.prop_renderer.clear_rendered_props()
        self._render_pictograph_data(pictograph_data)

    def update_beat(self, beat_data: BeatData) -> None:
        """Legacy method: Convert beat data to pictograph data and render."""
        # Convert BeatData to PictographData for rendering
        pictograph_data = self._beat_data_to_pictograph_data(beat_data)
        self.render_pictograph(pictograph_data)

    def _beat_data_to_pictograph_data(self, beat_data: BeatData) -> PictographData:
        """Convert BeatData to PictographData for rendering."""
        # Use pictograph_data if available, otherwise create from legacy fields
        if beat_data.pictograph_data:
            return beat_data.pictograph_data

        # Fallback: create from legacy fields (deprecated)
        arrows = {}
        motions = {}

        # Check for legacy motion fields (deprecated)
        if hasattr(beat_data, "blue_motion") and beat_data.blue_motion:
            arrows["blue"] = ArrowData(color="blue", is_visible=True)
            motions["blue"] = beat_data.blue_motion

        if hasattr(beat_data, "red_motion") and beat_data.red_motion:
            arrows["red"] = ArrowData(color="red", is_visible=True)
            motions["red"] = beat_data.red_motion

        # Extract position data from glyph_data if available
        start_position = None
        end_position = None
        if beat_data.glyph_data:
            start_position = beat_data.glyph_data.start_position
            end_position = beat_data.glyph_data.end_position

        return PictographData(
            arrows=arrows,
            motions=motions,  # NEW: Include motions dictionary
            letter=beat_data.letter or "",
            start_position=start_position,
            end_position=end_position,
            glyph_data=beat_data.glyph_data,
            is_blank=beat_data.is_blank,
            metadata=beat_data.metadata or {},
        )

    def _render_pictograph_data(self, pictograph_data: PictographData) -> None:
        """Render the pictograph elements using specialized renderers."""
        if not pictograph_data:
            return

        # Render grid (if visible)
        if self._renderer_visibility.get("grid", True):
            self.grid_renderer.render_grid()

        # Extract motion data from arrows
        blue_motion = None
        red_motion = None
        if "blue" in pictograph_data.arrows and "blue" in pictograph_data.motions:
            blue_motion = pictograph_data.motions["blue"]
        if "red" in pictograph_data.arrows and "red" in pictograph_data.motions:
            red_motion = pictograph_data.motions["red"]

        # Render props for blue and red motions (if visible)
        if self._renderer_visibility.get("props", True):
            if blue_motion and self._renderer_visibility.get("blue_motion", True):
                self.prop_renderer.render_prop("blue", blue_motion)
            if red_motion and self._renderer_visibility.get("red_motion", True):
                self.prop_renderer.render_prop("red", red_motion)

        # Apply beta prop positioning after both props are rendered
        # Note: This requires converting back to BeatData temporarily for legacy compatibility
        if blue_motion and red_motion:
            # Create temporary BeatData for beta positioning
            from domain.models import BeatData

            # Create temporary pictograph data with motions
            temp_pictograph = PictographData(
                motions=(
                    {"blue": blue_motion, "red": red_motion}
                    if blue_motion or red_motion
                    else {}
                ),
                letter=pictograph_data.letter,
                glyph_data=pictograph_data.glyph_data,
            )

            temp_beat = BeatData(
                beat_number=0,
                letter=pictograph_data.letter,
                pictograph_data=temp_pictograph,  # NEW: Use pictograph data with motions
                glyph_data=pictograph_data.glyph_data,
            )
            self.prop_renderer.apply_beta_positioning(temp_beat)

        # Use the existing pictograph data for arrow rendering
        # Ensure both blue and red arrows exist for special placement service
        full_pictograph_data = PictographData(
            arrows={
                "blue": pictograph_data.arrows.get("blue", ArrowData(color="blue")),
                "red": pictograph_data.arrows.get("red", ArrowData(color="red")),
            },
            motions=pictograph_data.motions,  # CRITICAL: Include motions for arrow positioning
            letter=pictograph_data.letter,  # Essential for special placement lookup
            glyph_data=pictograph_data.glyph_data,
        )

        # Render arrows using the full pictograph data (if visible)
        if self._renderer_visibility.get("arrows", True):
            if blue_motion and self._renderer_visibility.get("blue_motion", True):
                self.arrow_renderer.render_arrow(
                    "blue", blue_motion, full_pictograph_data
                )
            if red_motion and self._renderer_visibility.get("red_motion", True):
                self.arrow_renderer.render_arrow(
                    "red", red_motion, full_pictograph_data
                )

        # Render glyphs if glyph data is available and visibility allows
        # Note: Letters are rendered via TKA glyph, not simple letter renderer
        if pictograph_data.glyph_data:
            glyph_data = pictograph_data.glyph_data

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
                and pictograph_data.letter
                and self._renderer_visibility.get("tka", True)
            ):
                # Determine the correct letter type from the actual letter
                letter_type_str = LetterTypeClassifier.get_letter_type(
                    pictograph_data.letter
                )
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
                and self._renderer_visibility.get("positions", True)
            ):
                self.position_glyph_renderer.render_position_glyph(
                    glyph_data.start_position,
                    glyph_data.end_position,
                    pictograph_data.letter,
                )
