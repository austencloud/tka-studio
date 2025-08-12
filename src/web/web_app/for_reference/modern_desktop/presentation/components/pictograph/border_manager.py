"""
Pictograph Border Manager - Qt Presentation Layer

Handles Qt-specific border rendering while delegating business logic
to PictographBorderService.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPen

from desktop.modern.core.interfaces.core_services import IPictographBorderManager
from desktop.modern.domain.models import LetterType


class PictographBorderManager:
    """
    Qt presentation manager for pictograph borders.

    Handles Qt-specific rendering while delegating calculations
    to PictographBorderService.
    """

    def __init__(self, border_service: IPictographBorderManager):
        """Initialize with border service."""
        self._border_service = border_service

    # Configuration Methods
    def update_border_colors_for_letter_type(self, letter_type: LetterType) -> None:
        """Update border colors based on letter type."""
        self._border_service.apply_letter_type_colors(letter_type)

    def set_gold_border(self) -> None:
        """Set border colors to gold."""
        self._border_service.apply_gold_colors()

    def reset_border_colors(self) -> None:
        """Reset border colors to their original values."""
        self._border_service.reset_to_original_colors()

    def set_custom_border_colors(self, primary: str, secondary: str) -> None:
        """Set custom border colors."""
        self._border_service.apply_custom_colors(primary, secondary)

    def enable_borders(self) -> None:
        """Enable border rendering."""
        self._border_service.enable_borders()

    def disable_borders(self) -> None:
        """Disable border rendering."""
        self._border_service.disable_borders()

    def set_border_width_percentage(self, percentage: float) -> None:
        """Set the border width percentage."""
        self._border_service.set_border_width_percentage(percentage)

    def set_minimum_border_width(self, width: int) -> None:
        """Set the minimum border width."""
        self._border_service.set_minimum_border_width(width)

    # Calculation Methods (delegate to service)
    def calculate_border_width(self, size: int) -> int:
        """Calculate border width based on size."""
        return self._border_service.calculate_border_width(size)

    def get_border_adjusted_size(self, target_size: int) -> int:
        """Get size adjusted for border width."""
        return self._border_service.get_border_adjusted_size(target_size)

    def get_border_dimensions(self, view_width: int) -> tuple[float, float]:
        """Get border dimensions for drawing."""
        dimensions = self._border_service.calculate_floating_dimensions(view_width)
        return (dimensions.outer_width, dimensions.inner_width)

    # Qt Rendering Methods
    def draw_borders(self, painter: QPainter, viewport_rect, view_width: int) -> None:
        """
        Draw borders on the viewport using Qt.

        Args:
            painter: QPainter instance for drawing
            viewport_rect: The viewport rectangle to draw borders on
            view_width: Width of the view for border calculations
        """
        config = self._border_service.get_current_configuration()

        if not config.enabled:
            return

        # Get dimensions from service
        dimensions = self._border_service.calculate_floating_dimensions(view_width)

        # Calculate half pen widths for proper positioning
        half_outer_pen = dimensions.outer_width / 2.0
        half_inner_pen = dimensions.inner_width / 2.0

        # Draw outer border
        pen = QPen()
        pen.setColor(QColor(config.primary_color))
        pen.setWidthF(dimensions.outer_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        # Convert viewport rect to QRectF
        outer_rect = QRectF(viewport_rect)
        outer_rect = outer_rect.adjusted(
            +half_outer_pen,
            +half_outer_pen,
            -half_outer_pen,
            -half_outer_pen,
        )
        painter.drawRect(outer_rect)

        # Draw inner border
        pen.setColor(QColor(config.secondary_color))
        pen.setWidthF(dimensions.inner_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        inner_rect = outer_rect.adjusted(
            +half_inner_pen,
            +half_inner_pen,
            -half_inner_pen,
            -half_inner_pen,
        )
        painter.drawRect(inner_rect)

    # State Access Methods
    def is_borders_enabled(self) -> bool:
        """Check if borders are enabled."""
        return self._border_service.is_borders_enabled()

    def get_current_colors(self) -> tuple[str, str]:
        """Get current border colors."""
        return self._border_service.get_current_colors()


class BorderedPictographMixin:
    """
    Mixin class to add border functionality to pictograph components.

    Updated to use the border service through the manager.
    """

    def __init__(self, border_service: IPictographBorderManager):
        self._border_manager = PictographBorderManager(border_service)

    def update_border_colors_for_letter_type(self, letter_type: LetterType) -> None:
        """Update border colors based on letter type."""
        self._border_manager.update_border_colors_for_letter_type(letter_type)
        if hasattr(self, "update"):
            self.update()  # Trigger repaint if this is a widget

    def set_gold_border(self) -> None:
        """Set border to gold color."""
        self._border_manager.set_gold_border()
        if hasattr(self, "update"):
            self.update()

    def reset_border_colors(self) -> None:
        """Reset border colors to original values."""
        self._border_manager.reset_border_colors()
        if hasattr(self, "update"):
            self.update()

    def enable_borders(self) -> None:
        """Enable border rendering."""
        self._border_manager.enable_borders()
        if hasattr(self, "update"):
            self.update()

    def disable_borders(self) -> None:
        """Disable border rendering."""
        self._border_manager.disable_borders()
        if hasattr(self, "update"):
            self.update()

    def get_border_adjusted_size(self, target_size: int) -> int:
        """Get size adjusted for border width."""
        return self._border_manager.get_border_adjusted_size(target_size)

    def calculate_border_width(self, size: int) -> int:
        """Calculate border width for given size."""
        return self._border_manager.calculate_border_width(size)

    def draw_pictograph_borders(
        self, painter: QPainter, viewport_rect, view_width: int
    ) -> None:
        """Draw borders on the pictograph viewport."""
        self._border_manager.draw_borders(painter, viewport_rect, view_width)
