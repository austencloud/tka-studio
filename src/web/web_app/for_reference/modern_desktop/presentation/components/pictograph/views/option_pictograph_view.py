"""
Option pictograph view - Direct view for option picker like legacy system.

This provides the same direct scaling approach as the legacy OptionView
without widget wrapper complexity.
"""

from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import QRectF, QSize, Qt
from PyQt6.QtGui import QColor, QPainter, QPen, QResizeEvent

from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)

from .base_pictograph_view import BasePictographView


class OptionPictographView(BasePictographView):
    """
    Direct pictograph view for option picker.

    Replicates the legacy OptionView scaling behavior:
    - Calculates size based on main window width and option picker width
    - Applies border width calculations
    - Scales view directly without widget wrapper
    - Applies letter type specific border colors
    """

    # Letter type to color mapping (matching border manager - primary, secondary)
    LETTER_TYPE_COLORS = {
        LetterType.TYPE1: ("#36c3ff", "#6F2DA8"),  # Cyan, Purple
        LetterType.TYPE2: ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
        LetterType.TYPE3: ("#26e600", "#6F2DA8"),  # Green, Purple
        LetterType.TYPE4: ("#26e600", "#26e600"),  # Green, Green
        LetterType.TYPE5: ("#00b3ff", "#26e600"),  # Blue, Green
        LetterType.TYPE6: ("#eb7d00", "#eb7d00"),  # Orange, Orange
    }

    def __init__(
        self,
        parent=None,
        main_window_size_provider: Callable[[], QSize] | None = None,
    ):
        super().__init__(parent)

        # Store size provider for legacy-style calculations
        self._main_window_size_provider = main_window_size_provider

        # Store option picker reference for width calculations
        self._option_picker_width = 800  # Default, will be updated

        # Store letter type for border coloring
        self._letter_type = None

        # Apply option-specific styling
        self._setup_option_styling()

    def _setup_option_styling(self):
        """Apply option picker specific styling with letter type border color."""
        self._update_border_styling()

    def _update_border_styling(self):
        """Update border styling based on current letter type with dual-border effect."""
        # Set basic styling - borders will be drawn in paintEvent
        self.setStyleSheet(
            """
            OptionPictographView {
                background-color: white;
                border: none;
            }
        """
        )
        # Trigger repaint to show new border colors
        self.update()

    def paintEvent(self, event):
        """Custom paint event to draw dual borders like legacy system."""
        # Call parent paintEvent first to draw the graphics view content
        super().paintEvent(event)

        # Draw custom borders on top using legacy border manager approach
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get colors for current letter type
        primary_color = "#ccc"
        secondary_color = "#999"
        if self._letter_type and self._letter_type in self.LETTER_TYPE_COLORS:
            primary_color, secondary_color = self.LETTER_TYPE_COLORS[self._letter_type]

        # Get viewport rect
        viewport_rect = self.viewport().rect()

        # Define border dimensions (matching legacy system with slightly thicker outer)
        outer_width = 4.0  # Increased from 3.0 to make outer border more visible
        inner_width = 2.0

        # Calculate half pen widths for proper positioning (legacy approach)
        half_outer_pen = outer_width / 2.0
        half_inner_pen = inner_width / 2.0

        # Draw outer border (primary color)
        pen = QPen()
        pen.setColor(QColor(primary_color))
        pen.setWidthF(outer_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        # Position outer rect with half pen width adjustment (legacy method)
        outer_rect = QRectF(viewport_rect)
        outer_rect = outer_rect.adjusted(
            +half_outer_pen,
            +half_outer_pen,
            -half_outer_pen,
            -half_outer_pen,
        )
        painter.drawRect(outer_rect)

        # Draw inner border (secondary color) - positioned directly inside outer border
        pen.setColor(QColor(secondary_color))
        pen.setWidthF(inner_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        # Position inner rect directly adjacent to outer border (legacy method)
        inner_rect = outer_rect.adjusted(
            +half_inner_pen,
            +half_inner_pen,
            -half_inner_pen,
            -half_inner_pen,
        )
        painter.drawRect(inner_rect)

    def set_option_picker_width(self, width: int):
        """Set the option picker width for size calculations."""
        self._option_picker_width = width
        self._recalculate_size()

    def set_letter_type(self, letter_type: str):
        """Set the letter type for border coloring."""
        self._letter_type = letter_type
        self._update_border_styling()

    def _apply_view_specific_scaling(self):
        """Apply option picker specific scaling like legacy system."""
        # Calculate size using legacy formula
        size = self._calculate_legacy_option_size()

        # Apply the calculated size
        self.setFixedSize(size, size)

        # Apply legacy-style view scaling
        self._apply_legacy_view_scaling(size)

    def _calculate_legacy_option_size(self) -> int:
        """Calculate option size using exact legacy formula."""
        try:
            # Get main window width
            if self._main_window_size_provider:
                main_window_size = self._main_window_size_provider()
                main_window_width = main_window_size.width()
            else:
                # Fallback to parent window
                parent_window = self.window()
                main_window_width = parent_window.width() if parent_window else 1000

            # LEGACY FORMULA: max(mw_width // 16, option_picker_width // 8)
            size_option_1 = main_window_width // 16
            size_option_2 = self._option_picker_width // 8
            size = max(size_option_1, size_option_2)

            # Apply border width calculation like legacy
            border_width = max(1, int(size * 0.015))
            spacing = 3  # Grid spacing
            size = size - (2 * border_width) - spacing

            # Ensure minimum size
            size = max(size, 80)

            return size

        except Exception:
            # Safe fallback
            return 100

    def _apply_legacy_view_scaling(self, target_size: int):
        """Apply legacy-style view scaling."""
        if not self._scene:
            return

        # Get scene dimensions
        scene_rect = self._scene.sceneRect()
        if scene_rect.isEmpty():
            return

        # Calculate scale factor like legacy system
        # view_scale = size / pictograph.width()
        view_scale = target_size / scene_rect.width()

        # Apply the scaling
        self.resetTransform()
        self.scale(view_scale, view_scale)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize with option picker specific logic."""
        super().resizeEvent(event)
        # Recalculate size when parent changes
        self._recalculate_size()

    def _recalculate_size(self):
        """Recalculate and apply size based on current conditions."""
        if self.isVisible():
            self._apply_view_specific_scaling()

    # === COMPATIBILITY METHODS ===

    def resize_option_view(self):
        """Legacy compatibility method."""
        self._recalculate_size()

    def update_border_widths(self):
        """Legacy compatibility method."""
        # Border styling is handled in CSS
