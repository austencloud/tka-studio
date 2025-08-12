"""
Codex Pictograph View

Specialized pictograph view for codex display with appropriate sizing
and styling for the codex grid layout.
"""

from __future__ import annotations

import logging

from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QSizePolicy

from desktop.modern.presentation.components.pictograph.views.base_pictograph_view import (
    BasePictographView,
)


logger = logging.getLogger(__name__)


class CodexPictographView(BasePictographView):
    """
    Specialized pictograph view for codex display.

    Features:
    - Fixed size based on codex grid requirements
    - Border styling to match legacy codex
    - Proper scaling for small grid display
    - Maintains aspect ratio
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set object name for styling
        self.setObjectName("codex_pictograph_view")

        # Configure size policy for grid layout
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Apply codex-specific styling
        self._setup_codex_styling()

        # Set initial size
        self._codex_size = 80  # Default size, will be updated based on parent
        self._update_size()

        logger.debug("CodexPictographView initialized")

    def _setup_codex_styling(self) -> None:
        """Setup styling specific to codex display."""
        # Apply border styling like legacy codex
        self.setStyleSheet("""
            CodexPictographView {
                border: 1px solid black;
                background-color: white;
            }
        """)

        # Set frame style for better appearance
        self.setFrameStyle(self.Shape.Box)

    def _update_size(self) -> None:
        """Update the view size based on codex requirements."""
        # Set fixed size for grid display
        self.setFixedSize(self._codex_size, self._codex_size)

        # Don't manually set scene rect - let the scene manage its own rect
        # The base class scaling methods will handle proper centering

    def set_codex_size(self, size: int) -> None:
        """
        Set the size for this codex pictograph view.

        Args:
            size: The size in pixels (width and height)
        """
        self._codex_size = size
        self._update_size()
        # Use base class method for proper scaling and centering
        self._fit_view_to_content()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize events with codex-specific logic."""
        super().resizeEvent(event)

        # Ensure we maintain the fixed size
        if hasattr(self, "_codex_size"):
            self._update_size()

    def _apply_view_specific_scaling(self):
        """Apply codex-specific scaling using base class methods."""
        # Calculate target size with margin for codex display
        margin_factor = 1  # Leave 15% margin
        target_size = int(self._codex_size * margin_factor)

        # Use base class legacy scaling method for proper centering
        self._apply_legacy_view_scaling(target_size)

    def calculate_optimal_size(self, container_width: int, grid_columns: int) -> int:
        """
        Calculate optimal size based on container width and grid layout.

        Args:
            container_width: Width of the container
            grid_columns: Number of columns in the grid

        Returns:
            Optimal size for pictograph views
        """
        # Calculate size based on container width and grid layout
        # Leave space for margins and spacing
        available_width = container_width  # Account for margins
        spacing = 10 * (grid_columns - 1)  # Space between items

        size = (available_width - spacing) // grid_columns

        # Ensure minimum and maximum sizes
        size = max(60, min(size, 120))

        return size

    def update_from_pictograph_data(self, pictograph_data) -> None:
        """Update display from pictograph data with codex-specific handling."""
        super().update_from_pictograph_data(pictograph_data)

        # Apply codex-specific scaling after update
        self._apply_view_specific_scaling()

    def get_size(self) -> int:
        """Get the current codex size."""
        return self._codex_size
