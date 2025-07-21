"""
Simplified Pictograph Widget - Clean 2-layer architecture
"""

from typing import Optional

from domain.models.beat_data import BeatData
from domain.models.pictograph_data import PictographData
from presentation.components.pictograph.pictograph_scene import PictographScene
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QResizeEvent
from PyQt6.QtWidgets import QGraphicsView, QVBoxLayout, QWidget


class PictographWidget(QWidget):
    """
    Simplified pictograph widget that wraps PictographScene with QGraphicsView.

    This is the ONLY pictograph widget class you need.
    Architecture: Widget -> View -> Scene
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create scene (rendering engine) and view (display)
        self._scene = PictographScene()
        self._view = QGraphicsView(self)
        self._view.setScene(self._scene)

        # Store scaling context for start position pickers
        self._scaling_context = None
        self._scaling_params = {}

        # Simple layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._view)

        # Configure view
        self._setup_view()

    def _setup_view(self):
        """Configure view for optimal pictograph display."""
        self._view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self._view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self._view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._view.setFrameStyle(0)
        self._view.setContentsMargins(0, 0, 0, 0)

        viewport = self._view.viewport()
        if viewport:
            viewport.setContentsMargins(0, 0, 0, 0)
        self._view.setViewportMargins(0, 0, 0, 0)
        self._view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    # === PUBLIC INTERFACE ===

    def update_from_pictograph_data(self, pictograph_data: PictographData) -> None:
        """Update display from PictographData."""
        self._scene.render_pictograph(pictograph_data)
        self._fit_view()

    def update_from_beat(self, beat_data: BeatData) -> None:
        """Update display from BeatData."""
        self._scene.render_pictograph(beat_data.pictograph_data)
        self._fit_view()

    def clear_pictograph(self) -> None:
        """Clear the display."""
        self._scene.clear()

    def clear(self) -> None:
        """Alias for clear_pictograph (compatibility)."""
        self.clear_pictograph()

    def cleanup(self) -> None:
        """Clean up resources."""
        self._scene.clear()

    # === SCALING (simplified) ===

    def rescale_for_window_size(self, _window_width: int) -> None:
        """Re-scale for window resize. Implements IPictographRescalable."""
        self._fit_view()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle widget resize."""
        super().resizeEvent(event)
        self._fit_view()

    def _fit_view(self):
        """Fit view to scene content using legacy-style direct scaling."""
        if self._scene and self._view:
            try:
                # Always use items bounding rect for accurate content sizing
                items_rect = self._scene.itemsBoundingRect()

                if items_rect.isEmpty():
                    # No content to scale
                    return

                # LEGACY-STYLE SCALING: Direct calculation like legacy system
                self._apply_legacy_style_scaling(items_rect)

            except RuntimeError:
                pass  # Handle deleted objects gracefully

    def _apply_legacy_style_scaling(self, items_rect):
        """Apply legacy-style direct scaling exactly like the original system."""
        try:
            # CRITICAL: Use Qt's built-in fitInView like legacy system
            # This automatically handles scene-to-view scaling without hardcoded dimensions
            self._view.fitInView(items_rect, Qt.AspectRatioMode.KeepAspectRatio)

            # Apply context-specific scale adjustments if needed (like legacy margin adjustments)
            if self._scaling_context:
                current_transform = self._view.transform()
                current_scale = current_transform.m11()  # Get current scale factor

                # Apply simple adjustment factor
                adjustment_factor = self._get_context_adjustment_factor()
                new_scale = current_scale * adjustment_factor

                # Apply the adjusted scaling
                self._view.resetTransform()
                self._view.scale(new_scale, new_scale)
                self._view.centerOn(items_rect.center())

        except Exception:
            # Final fallback
            self._view.fitInView(
                self._scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio
            )

    def _get_context_adjustment_factor(self):
        """Get simple context-specific adjustment factor for legacy-style scaling."""
        if not self._scaling_context:
            return 0.95  # Small margin for default

        from core.interfaces.pictograph_services import ScalingContext

        # Simple adjustment factors (like legacy margin calculations)
        if self._scaling_context == ScalingContext.LEARN_QUESTION:
            return 0.85  # Slightly smaller for questions
        elif self._scaling_context == ScalingContext.LEARN_ANSWER:
            return 0.80  # Smaller for answer options
        elif self._scaling_context in [
            ScalingContext.START_POS_PICKER,
            ScalingContext.ADVANCED_START_POS,
        ]:
            return 0.90  # Slight margin for start positions
        elif self._scaling_context == ScalingContext.OPTION_VIEW:
            return 0.95  # Small margin for option picker
        else:
            return 0.95  # Default margin

    def ensure_square_widget(self, size: int):
        """
        Ensure the pictograph widget is square like legacy system.

        This is the key to fixing display issues - legacy system always
        sets pictograph widgets to be square with setFixedSize(size, size).

        Args:
            size: The size for both width and height
        """
        self.setFixedSize(size, size)

        # After setting widget size, trigger a re-fit of the view
        if self._scene and self._view:
            self._fit_view()

    # === COMPATIBILITY METHODS ===

    def disable_borders(self) -> None:
        """Compatibility method for legacy code."""
        pass

    def set_scaling_context(self, context, **params) -> None:
        """Set scaling context for start position pickers."""
        self._scaling_context = context
        self._scaling_params = params

        # Also delegate to scene if it supports it
        if hasattr(self._scene, "set_scaling_context"):
            self._scene.set_scaling_context(context, **params)

        # CRITICAL FIX: Trigger view fitting after scaling context is set
        # This ensures start position scaling is applied immediately
        self._fit_view()

    def setFixedSize(self, width, height=None) -> None:
        """Override setFixedSize to ensure proper view fitting."""
        if height is None:
            super().setFixedSize(width)
        else:
            super().setFixedSize(width, height)
        self._fit_view()

    def set_square_size(self, size: int) -> None:
        """Set widget to a square size for perfect pictograph display."""
        self.setFixedSize(size, size)

    def fit_to_container(
        self, container_width: int, container_height: int, maintain_square: bool = True
    ) -> None:
        """
        Fit the pictograph widget to its container while maintaining aspect ratio.

        Args:
            container_width: Available container width
            container_height: Available container height
            maintain_square: Whether to maintain square aspect ratio (default: True)
        """
        if maintain_square:
            # Use smaller dimension to ensure square fits in container
            size = min(container_width, container_height)
            self.set_square_size(size)
        else:
            self.setFixedSize(container_width, container_height)

    # === PROPERTY ACCESS ===

    @property
    def scene(self) -> PictographScene:
        """Access scene for advanced operations."""
        return self._scene

    @property
    def view(self) -> QGraphicsView:
        """Access view for advanced operations."""
        return self._view

    # Renderer access (delegate to scene)
    @property
    def tka_glyph_renderer(self):
        return getattr(self._scene, "tka_glyph_renderer", None)

    @property
    def vtg_glyph_renderer(self):
        return getattr(self._scene, "vtg_glyph_renderer", None)

    @property
    def elemental_glyph_renderer(self):
        return getattr(self._scene, "elemental_glyph_renderer", None)

    @property
    def letter_renderer(self):
        return getattr(self._scene, "letter_renderer", None)

    @property
    def position_glyph_renderer(self):
        return getattr(self._scene, "position_glyph_renderer", None)


# === FACTORY FUNCTION ===


def create_pictograph_widget() -> PictographWidget:
    """Factory function to create a pictograph widget."""
    return PictographWidget()


# === COMPATIBILITY ALIASES ===
create_simplified_pictograph_widget = create_pictograph_widget
