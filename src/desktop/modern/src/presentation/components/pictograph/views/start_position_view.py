"""
Start position pictograph view - Direct view for start position picker.

This provides direct scaling like the legacy StartPosPickerPictographView
without widget wrapper complexity.
"""

from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent

from .base_pictograph_view import BasePictographView


class StartPositionView(BasePictographView):
    """
    Direct pictograph view for start position picker.

    Replicates the legacy start position view scaling behavior:
    - Scales to fit container exactly
    - Maintains square aspect ratio
    - Applies appropriate margins for advanced vs basic modes
    """

    def __init__(self, parent=None, is_advanced: bool = False):
        # Initialize _is_advanced BEFORE calling super().__init__
        # because resizeEvent may be called during initialization
        self._is_advanced = is_advanced

        super().__init__(parent)

        # Apply start position specific styling
        self._setup_start_position_styling()

    def _setup_start_position_styling(self):
        """Apply start position picker specific styling."""
        # Clean styling for start position display
        self.setStyleSheet(
            """
            StartPositionView {
                border: 2px solid #4a90e2;
                border-radius: 8px;
                background-color: white;
            }
            StartPositionView:hover {
                border-color: #357abd;
                background-color: #f8f9fa;
            }
        """
        )

    def set_advanced_mode(self, is_advanced: bool):
        """Set whether this is an advanced start position."""
        self._is_advanced = is_advanced
        self._apply_view_specific_scaling()

    def _apply_view_specific_scaling(self):
        """Apply start position specific scaling."""
        # Get current widget size
        widget_size = self.size()

        if widget_size.width() <= 0 or widget_size.height() <= 0:
            return

        # Use the smaller dimension to maintain square aspect ratio
        size = min(widget_size.width(), widget_size.height())

        # Apply margin based on mode (like legacy system)
        margin_factor = 0.90 if self._is_advanced else 0.95
        effective_size = int(size * margin_factor)

        # Apply legacy-style view scaling
        self._apply_legacy_view_scaling(effective_size)

    def _apply_legacy_view_scaling(self, target_size: int):
        """Apply legacy-style view scaling for start positions."""
        if not self._scene:
            return

        # Get scene content bounds
        items_rect = self._scene.itemsBoundingRect()

        if items_rect.isEmpty():
            # Use scene rect as fallback
            items_rect = self._scene.sceneRect()

        if items_rect.isEmpty():
            return

        # Calculate scale to fit target size
        scene_size = max(items_rect.width(), items_rect.height())
        if scene_size > 0:
            scale_factor = target_size / scene_size

            # Apply the scaling
            self.resetTransform()
            self.scale(scale_factor, scale_factor)

            # Center the content
            self.centerOn(items_rect.center())

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize with start position specific logic."""
        super().resizeEvent(event)
        # Apply scaling immediately when resized
        self._apply_view_specific_scaling()

    def setFixedSize(self, width, height=None) -> None:
        """Override setFixedSize to trigger scaling."""
        if height is None:
            super().setFixedSize(width)
        else:
            super().setFixedSize(width, height)

        # Apply scaling after size change
        self._apply_view_specific_scaling()

    # === COMPATIBILITY METHODS ===

    def update_pictograph_size(self, size: int, is_advanced: bool):
        """Legacy compatibility method for size updates."""
        self._is_advanced = is_advanced
        self.setFixedSize(size, size)
