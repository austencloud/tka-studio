"""
Beat pictograph view - Direct view for beat frame contexts.

This provides direct QGraphicsView placement for beat pictographs,
eliminating widget wrapper complexity and ensuring proper scaling
and positioning like the legacy system.
"""

from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QSizePolicy

from .base_pictograph_view import BasePictographView


class BeatPictographView(BasePictographView):
    """
    Direct pictograph view for beat frame contexts.

    Features:
    - Direct QGraphicsView placement like legacy system
    - Fills entire beat frame container
    - Maintains aspect ratio
    - No widget wrapper complexity
    - Immediate scaling on first display
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set size policy to expand and fill available space
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Apply beat frame specific styling
        self._setup_beat_styling()

    def _setup_beat_styling(self):
        """Apply beat frame specific styling."""
        # Clean styling for beat frame display - no borders, transparent background
        self.setStyleSheet(
            """
            BeatPictographView {
                border: none;
                background: transparent;
            }
        """
        )

    def _apply_view_specific_scaling(self):
        """Apply beat frame specific scaling to fill container."""
        # Get current widget size (this is our container)
        widget_size = self.size()

        if widget_size.width() <= 0 or widget_size.height() <= 0:
            return

        # Use the smaller dimension to maintain aspect ratio
        target_size = min(widget_size.width(), widget_size.height())

        # Apply margin factor for beat frames (slightly smaller than container)
        margin_factor = 0.95  # 95% of container size for beat frames
        target_size = int(target_size * margin_factor)

        # Apply legacy-style view scaling
        self._apply_legacy_view_scaling(target_size)

    def _apply_legacy_view_scaling(self, target_size: int):
        """Apply legacy-style view scaling for beat frames."""
        if not self._scene:
            return

        # Get scene content bounds
        items_rect = self._scene.itemsBoundingRect()

        if items_rect.isEmpty():
            # Use scene rect as fallback
            items_rect = self._scene.sceneRect()

        if items_rect.isEmpty():
            return

        # Calculate scale to fit target size while maintaining aspect ratio
        scene_width = items_rect.width()
        scene_height = items_rect.height()

        if scene_width > 0 and scene_height > 0:
            # Calculate scale factors for both dimensions
            scale_x = target_size / scene_width
            scale_y = target_size / scene_height

            # Use minimum scale to ensure content fits
            scale_factor = min(scale_x, scale_y)

            # Apply the scaling
            self.resetTransform()
            self.scale(scale_factor, scale_factor)

            # Center the content
            self.centerOn(items_rect.center())

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize with beat frame specific logic."""
        super().resizeEvent(event)
        # Apply scaling immediately when container resizes
        self._apply_view_specific_scaling()

    def update_pictograph(self, data) -> None:
        """Update pictograph from either PictographData or BeatData."""
        from domain.models.pictograph_data import PictographData
        from domain.models import BeatData

        if isinstance(data, PictographData):
            # Direct pictograph data
            self.update_from_pictograph_data(data)
        elif isinstance(data, BeatData):
            # Extract pictograph data from beat data
            if hasattr(data, "pictograph_data") and data.pictograph_data:
                self.update_from_pictograph_data(data.pictograph_data)
            else:
                # Clear if no pictograph data in beat
                self.clear_pictograph()
        else:
            # Clear for any other data type
            self.clear_pictograph()
