"""
Start position pictograph view - Direct view for start position picker.

This provides direct scaling like the legacy StartPosPickerPictographView
without widget wrapper complexity.
"""

from __future__ import annotations

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
        # Use unified scaling with mode-specific margin factor
        margin_factor = 0.90 if self._is_advanced else 0.95
        self._apply_unified_scaling(margin_factor)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize with start position specific logic."""
        super().resizeEvent(event)
        # NOTE: _apply_view_specific_scaling() is already called by base class _fit_view_to_content()
        # Removing duplicate call to fix double scaling issue

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
