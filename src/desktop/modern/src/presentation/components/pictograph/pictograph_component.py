"""
Direct pictograph view for Kinetic Constructor - matches legacy container hierarchy.
"""

from typing import Any, Optional

from application.services.pictograph.scaling_service import (
    RenderingContext,
    ScalingContext,
)
from core.dependency_injection import get_container
from core.interfaces.core_services import IPictographBorderManager
from domain.models import BeatData
from domain.models.pictograph_data import PictographData
from presentation.components.pictograph.border_manager import BorderedPictographMixin
from presentation.components.pictograph.pictograph_scene import PictographScene
from PyQt6.QtCore import QEvent, Qt, QTimer
from PyQt6.QtGui import QEnterEvent, QKeyEvent, QPainter, QResizeEvent
from PyQt6.QtWidgets import QGraphicsView, QVBoxLayout, QWidget


class PictographComponent(PictographScene):

    def __init__(
        self,
        border_service: IPictographBorderManager,
        parent: Optional[QGraphicsView] = None,
    ):
        # Initialize scene first
        super().__init__(parent)

        # Store border service and view management
        self._border_service = border_service
        self._current_view: Optional[QGraphicsView] = None
        self._scaling_context = ScalingContext.DEFAULT
        self._context_params = {}

        # Debug functionality
        self.debug_enabled = False
        self.debug_timer = QTimer()
        self.debug_timer.timeout.connect(self._print_debug_dimensions)
        self.debug_timer.setSingleShot(True)

    def attach_view(self, view: QGraphicsView) -> None:
        """
        Attach this scene to a view for display.

        This is called when the component needs to be displayed.
        The view is managed by the PictographViewPool.
        """
        if self._current_view:
            self.detach_view()

        self._current_view = view
        view.setScene(self)

        # Apply view configuration
        self._setup_view_properties(view)

        # Fit view to scene
        self._fit_view_to_scene(view)

    def detach_view(self) -> None:
        """Detach the current view, allowing it to be reused."""
        if self._current_view:
            self._current_view.setScene(None)
            self._current_view = None

    def _setup_view_properties(self, view: QGraphicsView) -> None:
        """Configure view properties for optimal pictograph display."""
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        view.setDragMode(QGraphicsView.DragMode.NoDrag)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setFrameStyle(0)
        view.setContentsMargins(0, 0, 0, 0)

        viewport = view.viewport()
        if viewport:
            viewport.setContentsMargins(0, 0, 0, 0)
        view.setViewportMargins(0, 0, 0, 0)
        view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def _fit_view_to_scene(self, view: QGraphicsView) -> None:
        """Fit the view to display the scene optimally."""
        if view and view.scene():
            try:
                view.setSceneRect(self.itemsBoundingRect())
                view.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            except RuntimeError:
                pass

    def update_from_beat(self, beat_data: BeatData) -> None:
        """Update the pictograph display with beat data."""
        self.render_pictograph(beat_data.pictograph_data)

        # Update view if attached
        if self._current_view:
            self._fit_view_to_scene(self._current_view)

    def update_from_pictograph_data(self, pictograph_data: PictographData) -> None:
        """Update component from PictographData."""
        self.render_pictograph(pictograph_data)

        # Update view if attached
        if self._current_view:
            self._fit_view_to_scene(self._current_view)

    def get_current_beat(self) -> Optional[BeatData]:
        """Get current beat - component is stateless."""
        return None

    def clear_pictograph(self) -> None:
        """Clear the pictograph display."""
        self.clear()

    def cleanup(self) -> None:
        """Clean up the component."""
        if self._current_view:
            self.detach_view()
        self.clear()

    def get_current_view(self) -> Optional[QGraphicsView]:
        """Get the currently attached view."""
        return self._current_view

    def set_scaling_context(
        self, context: ScalingContext, **context_params: Any
    ) -> None:
        """Set the scaling context and parameters."""
        self._scaling_context = context
        self._context_params = context_params

        # Re-apply scaling with new context
        if self._current_view:
            self._fit_view_to_scene(self._current_view)

    def get_scaling_context(self) -> ScalingContext:
        """Get the current scaling context."""
        return self._scaling_context

    def toggle_dimension_debugging(self) -> None:
        """Toggle dimension debugging on/off."""
        self.debug_enabled = not self.debug_enabled
        if self.debug_enabled:
            print(
                "🔍 Optimized Dimension debugging ENABLED - Press Ctrl+D again to disable"
            )
            self._trigger_debug_print()
        else:
            print("🔍 Optimized Dimension debugging DISABLED")

    def _trigger_debug_print(self) -> None:
        """Trigger debug print after a short delay."""
        if self.debug_enabled:
            self.debug_timer.start(100)

    def _print_debug_dimensions(self) -> None:
        """Print detailed dimension information for debugging."""
        if not self.debug_enabled:
            return

        print("\n" + "=" * 80)
        print("🔍 OPTIMIZED PICTOGRAPH DIMENSION DEBUG")
        print("=" * 80)

        # Scene dimensions
        scene_rect = self.sceneRect()
        print(
            f"📐 Scene Rect: {scene_rect.width()}x{scene_rect.height()} at ({scene_rect.x()}, {scene_rect.y()})"
        )

        # View dimensions (if attached)
        if self._current_view:
            view_size = self._current_view.size()
            viewport_size = self._current_view.viewport().size()
            print(f"📐 View Size: {view_size.width()}x{view_size.height()}")
            print(f"📐 Viewport Size: {viewport_size.width()}x{viewport_size.height()}")

            # View scaling
            transform = self._current_view.transform()
            scale_x = transform.m11()
            scale_y = transform.m22()
            print(f"📐 View Scale: {scale_x:.4f}x{scale_y:.4f}")

            # Effective pictograph size
            effective_width = scene_rect.width() * scale_x
            effective_height = scene_rect.height() * scale_y
            print(
                f"📐 Effective Pictograph Size: {effective_width:.1f}x{effective_height:.1f}"
            )
        else:
            print("📐 No view currently attached")

        print("=" * 80)
        print()


def create_pictograph_component(
    parent: Optional[QGraphicsView] = None,
    container=None,
) -> PictographComponent:
    """
    Factory function to create a PictographComponent with injected dependencies.

    This function resolves the border service from the provided or global DI container
    and creates a properly configured PictographComponent instance.

    Args:
        parent: Optional parent widget (for scene hierarchy)
        container: Optional DI container (uses global if not provided)

    Returns:
        PictographComponent: Configured component instance (scene-only)
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


class PictographWidget(QWidget):
    """Widget wrapper for PictographComponent to provide widget interface for UI layouts."""

    def __init__(self, pictograph_component: PictographComponent, parent=None):
        super().__init__(parent)
        self._pictograph_component = pictograph_component
        self._view = QGraphicsView(self)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Connect scene to view
        self._view.setScene(pictograph_component)
        layout.addWidget(self._view)

        # Configure view for optimal pictograph display
        self._view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self._view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._view.setFrameStyle(0)  # Remove frame

        # Attach view to component
        pictograph_component.attach_view(self._view)

    def update_from_pictograph_data(self, pictograph_data: PictographData) -> None:
        """Delegate to the wrapped component."""
        self._pictograph_component.update_from_pictograph_data(pictograph_data)

    def update_from_beat(self, beat_data: BeatData) -> None:
        """Delegate to the wrapped component."""
        self._pictograph_component.update_from_beat(beat_data)

    def clear_pictograph(self) -> None:
        """Delegate to the wrapped component."""
        self._pictograph_component.clear_pictograph()

    def disable_borders(self) -> None:
        """Disable borders - compatibility method."""
        # This method exists for compatibility with legacy code
        pass

    def set_scaling_context(self, context, **context_params) -> None:
        """Set scaling context - delegate to wrapped component."""
        self._pictograph_component.set_scaling_context(context, **context_params)

    def get_pictograph_component(self) -> PictographComponent:
        """Get the wrapped pictograph component."""
        return self._pictograph_component

    def cleanup(self) -> None:
        """Clean up the widget and component."""
        self._pictograph_component.cleanup()


def create_pictograph_widget() -> PictographWidget:
    """Factory function to create a PictographWidget with proper DI."""
    component = create_pictograph_component()
    return PictographWidget(component)
