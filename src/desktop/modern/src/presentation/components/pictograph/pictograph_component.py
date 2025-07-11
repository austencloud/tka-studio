"""
Direct pictograph view for Kinetic Constructor - matches legacy container hierarchy.
"""

from typing import Any, Optional

from application.services.pictograph.scaling_service import ScalingContext
from core.dependency_injection import get_container
from core.interfaces.core_services import IPictographBorderManager
from domain.models import BeatData
from domain.models.pictograph_data import PictographData
from presentation.components.pictograph.border_manager import BorderedPictographMixin
from presentation.components.pictograph.pictograph_scene import PictographScene
from PyQt6.QtCore import QEvent, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QEnterEvent, QKeyEvent, QPainter, QResizeEvent
from PyQt6.QtWidgets import QGraphicsView


class PictographComponent(BorderedPictographMixin, QGraphicsView):

    def __init__(
        self,
        border_service: IPictographBorderManager,
        parent: Optional[QGraphicsView] = None,
    ):
        if parent is not None:
            try:
                _ = parent.isVisible()
            except RuntimeError as exc:
                print("❌ Parent widget deleted, cannot create PictographComponent")
                raise RuntimeError("Parent widget has been deleted") from exc

        BorderedPictographMixin.__init__(self, border_service)
        QGraphicsView.__init__(self, parent)

        # Removed current_beat storage - component is now stateless
        self.scene: Optional[PictographScene] = None  # Dimension debugging
        self.debug_enabled = False
        self.debug_timer = QTimer()
        self.debug_timer.timeout.connect(self._print_debug_dimensions)
        self.debug_timer.setSingleShot(True)

        # WINDOW MANAGEMENT FIX: Hide during creation to prevent flashing
        self.hide()

        self._setup_ui()

    def _setup_ui(self) -> None:
        try:
            self.scene = PictographScene(parent=self)
            self.setScene(self.scene)

            self.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setFrameStyle(0)

            self.setContentsMargins(0, 0, 0, 0)
            viewport = self.viewport()
            if viewport:
                viewport.setContentsMargins(0, 0, 0, 0)
            self.setViewportMargins(0, 0, 0, 0)
            self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

            self._fit_view()
        except RuntimeError as e:
            print(f"❌ Failed to setup PictographComponent UI: {e}")

    def update_from_beat(self, beat_data: BeatData) -> None:
        """Update the pictograph display with beat data (stateless rendering)."""
        if self.scene:
            self.scene.update_beat(beat_data)
            self._fit_view()

        # Update border colors based on letter type if available
        if beat_data.glyph_data and beat_data.glyph_data.letter_type:
            self.update_border_colors_for_letter_type(beat_data.glyph_data.letter_type)

        # VISIBILITY FIX: Show component when updated with data
        if not self.isVisible():
            self.show()

    def update_from_pictograph_data(self, pictograph_data: "PictographData") -> None:
        """
        Update component from PictographData (for pickers and non-sequence contexts).

        This is the preferred method for pickers since they work with pictographs,
        not beats. Only sequence beat frames should use update_from_beat().
        """
        # FIXED: Use scene's direct pictograph rendering method
        # No more unnecessary BeatData conversion!
        if self.scene:
            self.scene.render_pictograph(pictograph_data)
            self._fit_view()

        # VISIBILITY FIX: Show component when updated with data
        if not self.isVisible():
            self.show()

        # Emit the actual data we're working with - no unnecessary conversion!

    def get_current_beat(self) -> Optional[BeatData]:
        """Get current beat - component is now stateless, returns None."""
        return None  # Component no longer stores beat data

    def clear_pictograph(self) -> None:
        """Clear the pictograph display."""
        if self.scene:
            self.scene.clear()

    def cleanup(self) -> None:
        try:
            if self.scene:
                self.scene.clear()
                self.scene.setParent(None)
                self.scene = None
        except RuntimeError:
            pass

    def _fit_view(self) -> None:
        """Fit the pictograph scene to the view, exactly like Legacy."""
        if self.scene:
            try:
                # Simple Legacy-style fitting: just use fitInView to automatically scale
                self.setSceneRect(self.scene.itemsBoundingRect())
                self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            except RuntimeError:
                pass

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._fit_view()

    def showEvent(self, event: Any) -> None:
        super().showEvent(event)
        self._fit_view()

    def paintEvent(self, event: Any) -> None:
        """Handle paint events and draw borders if enabled."""
        super().paintEvent(event)

        # Draw borders using the border manager
        painter = QPainter(self.viewport())
        try:
            self.draw_pictograph_borders(
                painter, self.viewport().rect(), self.viewport().size().width()
            )
        finally:
            painter.end()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle key press events for debugging."""
        if (
            event.key() == Qt.Key.Key_D
            and event.modifiers() == Qt.KeyboardModifier.ControlModifier
        ):
            self.toggle_dimension_debugging()
        else:
            super().keyPressEvent(event)

    def enterEvent(self, event: QEnterEvent) -> None:
        """Handle mouse enter events for hover effects."""
        super().enterEvent(event)
        # Default hover behavior - can be overridden by context configurator
        if hasattr(self, "_hover_enter_func"):
            self._hover_enter_func()

    def leaveEvent(self, event: QEvent) -> None:
        """Handle mouse leave events for hover effects."""
        super().leaveEvent(event)
        # Default hover behavior - can be overridden by context configurator
        if hasattr(self, "_hover_leave_func"):
            self._hover_leave_func()

    def toggle_dimension_debugging(self) -> None:
        """Toggle dimension debugging on/off."""
        self.debug_enabled = not self.debug_enabled
        if self.debug_enabled:
            print(
                "🔍 Modern Dimension debugging ENABLED - Press Ctrl+D again to disable"
            )
            self._trigger_debug_print()
        else:
            print("🔍 Modern Dimension debugging DISABLED")

    def _trigger_debug_print(self) -> None:
        """Trigger debug print after a short delay to ensure rendering is complete."""
        if self.debug_enabled:
            self.debug_timer.start(100)  # 100ms delay

    def _print_debug_dimensions(self) -> None:
        """Print detailed dimension information for debugging."""
        if not self.debug_enabled or not self.scene:
            return

        print("\n" + "=" * 80)
        print("🔍 Modern PICTOGRAPH DIMENSION DEBUG")
        print("=" * 80)

        # Component dimensions
        component_size = self.size()
        viewport_size = self.viewport().size()
        print(f"📐 Component Size: {component_size.width()}x{component_size.height()}")
        print(f"📐 Viewport Size: {viewport_size.width()}x{viewport_size.height()}")

        # Scene dimensions
        scene_rect = self.scene.sceneRect()
        print(
            f"📐 Scene Rect: {scene_rect.width()}x{scene_rect.height()} at ({scene_rect.x()}, {scene_rect.y()})"
        )

        # View scaling
        transform = self.transform()
        scale_x = transform.m11()
        scale_y = transform.m22()
        print(f"📐 View Scale: {scale_x:.4f}x{scale_y:.4f}")

        # Calculate effective pictograph size
        effective_width = scene_rect.width() * scale_x
        effective_height = scene_rect.height() * scale_y
        print(
            f"📐 Effective Pictograph Size: {effective_width:.1f}x{effective_height:.1f}"
        )

        # TKA glyph analysis
        self._debug_tka_glyph_dimensions()

        print("=" * 80)
        print()

    def _debug_tka_glyph_dimensions(self) -> None:
        """Debug TKA glyph specific dimensions."""
        if not self.scene:
            return

        print("\n🔤 TKA GLYPH ANALYSIS:")

        # Find TKA glyph items in the scene
        tka_items = []
        for item in self.scene.items():
            if hasattr(item, "childItems") and item.childItems():
                # Check if this looks like a TKA group
                children = item.childItems()
                if len(children) > 0:
                    first_child = children[0]
                    if hasattr(first_child, "boundingRect"):
                        tka_items.append((item, first_child))

        if not tka_items:
            print("   No TKA glyph items found")
            return

        for i, (group_item, letter_item) in enumerate(tka_items):
            print(f"   TKA Group {i+1}:")

            # Group dimensions
            group_rect = group_item.boundingRect()
            group_pos = group_item.pos()
            print(
                f"     Group Rect: {group_rect.width():.1f}x{group_rect.height():.1f}"
            )
            print(f"     Group Pos: ({group_pos.x():.1f}, {group_pos.y():.1f})")

            # Letter dimensions
            letter_rect = letter_item.boundingRect()
            letter_pos = letter_item.pos()
            print(
                f"     Letter Rect: {letter_rect.width():.1f}x{letter_rect.height():.1f}"
            )
            print(f"     Letter Pos: ({letter_pos.x():.1f}, {letter_pos.y():.1f})")

            # Scene coordinates
            scene_rect = group_item.sceneBoundingRect()
            print(
                f"     Scene Rect: {scene_rect.width():.1f}x{scene_rect.height():.1f} at ({scene_rect.x():.1f}, {scene_rect.y():.1f})"
            )

            # Effective size after view scaling
            transform = self.transform()
            effective_width = scene_rect.width() * transform.m11()
            effective_height = scene_rect.height() * transform.m22()
            print(f"     Effective Size: {effective_width:.1f}x{effective_height:.1f}")

    def set_scaling_context(
        self, context: ScalingContext, **context_params: Any
    ) -> None:
        """Set the scaling context and parameters for context-aware scaling."""
        self.scaling_context = context
        self.context_params = context_params
        # Re-apply scaling with new context
        self._fit_view()

    def get_scaling_context(self) -> ScalingContext:
        """Get the current scaling context."""
        return self.scaling_context


def create_pictograph_component(
    parent: Optional[QGraphicsView] = None,
    container=None,
) -> PictographComponent:
    """
    Factory function to create a PictographComponent with injected dependencies.

    This function resolves the border service from the provided or global DI container
    and creates a properly configured PictographComponent instance.

    Args:
        parent: Optional parent widget
        container: Optional DI container (uses global if not provided)

    Returns:
        PictographComponent: Configured component instance
    """
    if container is None:
        container = get_container()

    try:
        border_service = container.resolve(IPictographBorderManager)
    except Exception as e:
        # Fallback: create service directly if DI fails
        print(f"⚠️ DI resolution failed, creating border service directly: {e}")
        from application.services.pictograph.border_manager import (
            PictographBorderManager,
        )

        border_service = PictographBorderManager()

    return PictographComponent(border_service, parent)
