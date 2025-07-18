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
        """Fit view to scene content."""
        if self._scene and self._view:
            try:
                # Check if we have a start position scaling context
                if self._scaling_context and self._is_start_position_context():
                    self._apply_start_position_scaling()
                else:
                    # Use standard fitInView for other contexts
                    # CRITICAL FIX: Use items bounding rect like legacy system
                    # This ensures we fit to actual content, not the full 950x950 scene
                    items_rect = self._scene.itemsBoundingRect()
                    if not items_rect.isEmpty():
                        # Update scene rect to match items bounds (like legacy)
                        self._scene.setSceneRect(items_rect)
                        self._view.fitInView(
                            items_rect, Qt.AspectRatioMode.KeepAspectRatio
                        )
                    else:
                        # Fallback to scene rect if no items
                        scene_rect = self._scene.sceneRect()
                        if not scene_rect.isEmpty():
                            self._view.fitInView(
                                scene_rect, Qt.AspectRatioMode.KeepAspectRatio
                            )
            except RuntimeError:
                pass  # Handle deleted objects gracefully

    def _is_start_position_context(self) -> bool:
        """Check if current scaling context is for start position picker."""
        from application.services.pictograph.scaling_service import ScalingContext

        return self._scaling_context in [
            ScalingContext.START_POS_PICKER,
            ScalingContext.ADVANCED_START_POS,
        ]

    def _apply_start_position_scaling(self):
        """Apply manual scaling for start position pickers like legacy system."""
        try:
            # Get scene dimensions
            scene_rect = self._scene.sceneRect()
            if scene_rect.width() <= 0 or scene_rect.height() <= 0:
                return

            # Get main window width for calculation
            main_window = self.window()
            main_window_width = main_window.width() if main_window else 1200

            # Calculate target size based on context (like legacy)
            from application.services.pictograph.scaling_service import ScalingContext

            if self._scaling_context == ScalingContext.ADVANCED_START_POS:
                # Advanced mode: main_window_width // 12
                target_size = main_window_width // 12
                min_size = 70
            else:
                # Basic mode: main_window_width // 10
                target_size = main_window_width // 10
                min_size = 80

            # Apply border calculation like legacy
            border_width = max(1, int(target_size * 0.015))
            target_size = target_size - (2 * border_width)
            target_size = max(target_size, min_size)

            # Calculate scale factor like legacy
            scale_factor = target_size / max(scene_rect.width(), scene_rect.height())

            # Apply manual scaling like legacy
            self._view.resetTransform()
            self._view.scale(scale_factor, scale_factor)

        except Exception as e:
            # Fallback to fitInView if manual scaling fails
            items_rect = self._scene.itemsBoundingRect()
            if not items_rect.isEmpty():
                self._view.fitInView(items_rect, Qt.AspectRatioMode.KeepAspectRatio)

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

    def setFixedSize(self, width, height=None) -> None:
        """Override setFixedSize to ensure proper view fitting."""
        if height is None:
            super().setFixedSize(width)
        else:
            super().setFixedSize(width, height)
        self._fit_view()

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
