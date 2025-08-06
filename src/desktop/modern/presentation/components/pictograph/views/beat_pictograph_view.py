"""
Beat pictograph view - Direct view for beat frame contexts.

This provides direct QGraphicsView placement for beat pictographs,
eliminating widget wrapper complexity and ensuring proper scaling
and positioning like the legacy system.
"""

from __future__ import annotations

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
        # Use unified scaling with standard margin factor
        self._apply_unified_scaling(margin_factor=0.95)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize with beat frame specific logic."""
        super().resizeEvent(event)
        # NOTE: _apply_view_specific_scaling() is already called by base class _fit_view_to_content()
        # Removing duplicate call to fix double scaling issue

    def update_pictograph(self, data) -> None:
        """Update pictograph from either PictographData or BeatData."""
        from desktop.modern.domain.models import BeatData
        from desktop.modern.domain.models.pictograph_data import PictographData

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
