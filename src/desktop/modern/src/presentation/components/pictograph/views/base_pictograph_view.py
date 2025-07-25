"""
Base pictograph view - Direct view approach like legacy system.

This eliminates the widget wrapper complexity and provides direct
QGraphicsView-based pictograph display like the legacy system.
"""

from typing import Optional

from domain.models.pictograph_data import PictographData
from presentation.components.pictograph.pictograph_scene import PictographScene
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QGraphicsView


class BasePictographView(QGraphicsView):
    """
    Base pictograph view that directly inherits from QGraphicsView.

    This eliminates the widget wrapper complexity and provides the same
    direct approach as the legacy system's BasePictographView.

    Architecture: View -> Scene (no intermediary widget)
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create scene directly
        self._scene = PictographScene()
        self.setScene(self._scene)

        # Configure view for optimal pictograph display
        self._setup_view()

        # Store current pictograph data
        self._current_pictograph_data: Optional[PictographData] = None

    def _setup_view(self):
        """Configure view settings for optimal pictograph display."""
        # Disable scrollbars - pictographs should fit exactly
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # FIXED: Set alignment to center content like legacy
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Enable antialiasing for smooth graphics
        from PyQt6.QtGui import QPainter

        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        # Set view update mode for better performance
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        # Disable drag mode - pictographs are display-only
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

        # FIXED: Set frame style and background like legacy
        from PyQt6.QtWidgets import QFrame

        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet("background: transparent; border: none;")

        # FIXED: Set margins to 0 like legacy
        self.setContentsMargins(0, 0, 0, 0)
        self.viewport().setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)

    # === PUBLIC INTERFACE ===

    def update_from_pictograph_data(self, pictograph_data: PictographData) -> None:
        """Update display from PictographData."""
        self._current_pictograph_data = pictograph_data
        self._scene.render_pictograph(pictograph_data)
        self._fit_view_to_content()

    def clear_pictograph(self) -> None:
        """Clear the display."""
        self._current_pictograph_data = None
        self._scene.clear()

    def refresh_display(self) -> None:
        """Refresh the current display."""
        if self._current_pictograph_data:
            self.update_from_pictograph_data(self._current_pictograph_data)

    # === SCALING (Legacy-style direct approach) ===

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize events with direct scaling like legacy system."""
        super().resizeEvent(event)
        self._fit_view_to_content()

    def _fit_view_to_content(self):
        """Fit view to content using legacy-style direct scaling."""
        if not self._scene:
            return

        # Get items bounding rect for actual content
        items_rect = self._scene.itemsBoundingRect()

        if items_rect.isEmpty():
            # No content to scale
            return

        # LEGACY APPROACH: Use Qt's built-in fitInView
        # This automatically handles scene-to-view scaling
        self.fitInView(items_rect, Qt.AspectRatioMode.KeepAspectRatio)

        # Apply view-specific scaling adjustments
        self._apply_view_specific_scaling()

    def _apply_view_specific_scaling(self):
        """Apply view-specific scaling adjustments. Override in subclasses."""
        # Base implementation applies no additional scaling
        # Subclasses can override for specific scaling behavior

    # === PROPERTIES ===

    @property
    def scene(self) -> PictographScene:
        """Access the pictograph scene."""
        return self._scene

    @property
    def current_pictograph_data(self) -> Optional[PictographData]:
        """Get the current pictograph data."""
        return self._current_pictograph_data

    # === COMPATIBILITY METHODS ===

    def clear(self) -> None:
        """Alias for clear_pictograph (compatibility)."""
        self.clear_pictograph()

    def cleanup(self) -> None:
        """Clean up resources."""
        self.clear_pictograph()
