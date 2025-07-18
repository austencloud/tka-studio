"""
Simplified Pictograph Architecture

This module provides a clean 2-layer pictograph system:
1. PictographScene - The rendering engine (already exists)
2. SimplifiedPictographWidget - The UI interface

This eliminates the unnecessary PictographComponent layer while maintaining
all functionality and performance optimizations.
"""

from typing import Optional

from domain.models.beat_data import BeatData
from domain.models.pictograph_data import PictographData
from presentation.components.pictograph.pictograph_scene import PictographScene
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsView, QVBoxLayout, QWidget


class SimplifiedPictographWidget(QWidget):
    """
    Simplified pictograph widget that provides a clean UI interface.

    This widget wraps a PictographScene with a QGraphicsView to provide
    a widget that can be used in layouts while maintaining all pictograph
    functionality.

    Architecture:
    - QWidget (this class) - UI interface for layouts
    - QGraphicsView - Display component
    - PictographScene - Rendering engine (existing)
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the scene (rendering engine)
        self._scene = PictographScene()

        # Create the view (display component)
        self._view = QGraphicsView(self)
        self._view.setScene(self._scene)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._view)

        # Configure view for optimal display
        self._configure_view()

    def _configure_view(self):
        """Configure the view for optimal pictograph display."""
        self._view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self._view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self._view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._view.setFrameStyle(0)
        self._view.setContentsMargins(0, 0, 0, 0)

        # Configure viewport
        viewport = self._view.viewport()
        if viewport:
            viewport.setContentsMargins(0, 0, 0, 0)
        self._view.setViewportMargins(0, 0, 0, 0)
        self._view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    # MAIN INTERFACE METHODS
    def update_from_pictograph_data(self, pictograph_data: PictographData) -> None:
        """Update pictograph display from PictographData."""
        self._scene.render_pictograph(pictograph_data)
        self._fit_view()

    def update_from_beat(self, beat_data: BeatData) -> None:
        """Update pictograph display from BeatData."""
        self._scene.render_pictograph(beat_data.pictograph_data)
        self._fit_view()

    def clear_pictograph(self) -> None:
        """Clear the pictograph display."""
        self._scene.clear()

    def clear(self) -> None:
        """Clear the pictograph display (compatibility method for pool management)."""
        self._scene.clear()

    def cleanup(self) -> None:
        """Clean up widget resources."""
        self._scene.cleanup()

    # COMPATIBILITY METHODS (for existing code)
    def disable_borders(self) -> None:
        """Compatibility method for legacy code."""
        pass

    def set_scaling_context(self, context, **params) -> None:
        """Set scaling context - delegate to scene."""
        if hasattr(self._scene, "set_scaling_context"):
            self._scene.set_scaling_context(context, **params)

    def setFixedSize(self, width, height=None) -> None:
        """Override setFixedSize to ensure proper sizing."""
        if height is None:
            # Handle QSize parameter
            super().setFixedSize(width)
        else:
            super().setFixedSize(width, height)
        self._fit_view()

    # INTERNAL METHODS
    def _fit_view(self):
        """Fit view to scene content."""
        if self._scene and self._view:
            try:
                scene_rect = self._scene.sceneRect()
                if not scene_rect.isEmpty():
                    self._view.fitInView(scene_rect, Qt.AspectRatioMode.KeepAspectRatio)
            except RuntimeError:
                # Handle case where scene/view might be deleted
                pass

    # PROPERTIES for accessing internals if needed
    @property
    def scene(self) -> PictographScene:
        """Access to the scene for advanced operations."""
        return self._scene

    @property
    def view(self) -> QGraphicsView:
        """Access to the view for advanced operations."""
        return self._view

    # RENDERER ACCESS (for compatibility)
    @property
    def tka_glyph_renderer(self):
        """Access TKA glyph renderer through scene."""
        return getattr(self._scene, "tka_glyph_renderer", None)

    @property
    def vtg_glyph_renderer(self):
        """Access VTG glyph renderer through scene."""
        return getattr(self._scene, "vtg_glyph_renderer", None)

    @property
    def elemental_glyph_renderer(self):
        """Access elemental glyph renderer through scene."""
        return getattr(self._scene, "elemental_glyph_renderer", None)

    @property
    def letter_renderer(self):
        """Access letter renderer through scene."""
        return getattr(self._scene, "letter_renderer", None)

    @property
    def position_glyph_renderer(self):
        """Access position glyph renderer through scene."""
        return getattr(self._scene, "position_glyph_renderer", None)


# FACTORY FUNCTIONS
def create_simplified_pictograph_widget() -> SimplifiedPictographWidget:
    """Factory function to create a simplified pictograph widget."""
    return SimplifiedPictographWidget()


# COMPATIBILITY ALIASES (for gradual migration)
PictographWidget = SimplifiedPictographWidget
create_pictograph_widget = create_simplified_pictograph_widget
