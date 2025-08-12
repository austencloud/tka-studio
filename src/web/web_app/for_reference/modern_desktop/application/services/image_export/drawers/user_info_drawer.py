"""
User Info Drawer - Legacy-Compatible User Information Rendering
==============================================================

Renders user information (name, date, notes) onto exported images using
exact legacy positioning and font scaling logic.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontMetrics, QImage, QPainter, QPen

from desktop.modern.core.interfaces.image_export_services import (
    ImageExportOptions,
    IUserInfoDrawer,
)


if TYPE_CHECKING:
    from .font_margin_helper import FontMarginHelper

logger = logging.getLogger(__name__)


class UserInfoDrawer(IUserInfoDrawer):
    """
    Drawer for rendering user information with legacy-compatible positioning.

    This drawer replicates the exact user info rendering logic from the Legacy system,
    including font scaling and positioning for user name, date, and notes.
    """

    def __init__(self, font_margin_helper: FontMarginHelper):
        """
        Initialize the user info drawer.

        Args:
            font_margin_helper: Helper for font and margin calculations
        """
        self.font_margin_helper = font_margin_helper

        # Legacy-compatible base font settings
        self.user_info_font_bold = QFont("Georgia", 50, QFont.Weight.Bold)
        self.user_info_font_normal = QFont("Georgia", 50, QFont.Weight.Normal)
        self.base_margin = 50
        self.border_width = 3

        logger.debug("UserInfoDrawer initialized with legacy-compatible settings")

    def draw_user_info(
        self,
        image: QImage,
        options: ImageExportOptions,
        num_filled_beats: int,
    ) -> None:
        """
        Draw user information onto the image using legacy scaling and positioning.

        Args:
            image: Target image
            options: Export options containing user info
            num_filled_beats: Number of beats in sequence (affects font size)
        """
        logger.debug("Drawing user info")

        # Calculate beat scale based on beat size
        beat_size = getattr(options, "beat_size", 280)
        beat_scale = self.font_margin_helper.calculate_beat_scale(beat_size)

        # Apply legacy font and margin adjustment for both fonts
        font_bold, margin = self.font_margin_helper.adjust_font_and_margin(
            self.user_info_font_bold, num_filled_beats, self.base_margin, beat_scale
        )
        font_normal, _ = self.font_margin_helper.adjust_font_and_margin(
            self.user_info_font_normal, num_filled_beats, self.base_margin, beat_scale
        )

        # Set up painter
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        # Format export date (legacy format)
        export_date = self._format_export_date(options.export_date)

        # Calculate text widths with adjusted fonts
        metrics_normal = QFontMetrics(font_normal)
        date_width = metrics_normal.horizontalAdvance(export_date)
        notes_width = metrics_normal.horizontalAdvance(options.notes)

        # Draw user name (bottom-left)
        self._draw_text_at_position(
            painter, image, options.user_name, font_bold, margin, "bottom-left"
        )

        # Draw notes (bottom-center)
        self._draw_text_at_position(
            painter,
            image,
            options.notes,
            font_normal,
            margin,
            "bottom-center",
            notes_width,
        )

        # Draw export date (bottom-right)
        self._draw_text_at_position(
            painter, image, export_date, font_normal, margin, "bottom-right", date_width
        )

        painter.end()
        logger.debug("User info drawn successfully")

    def _format_export_date(self, date_str: str) -> str:
        """
        Format export date in legacy format.

        Args:
            date_str: Date string to format

        Returns:
            Formatted date string
        """
        if not date_str:
            from datetime import datetime

            date_str = datetime.now().strftime("%m-%d-%Y")

        # Legacy format: remove leading zeros
        try:
            return "-".join([str(int(part)) for part in date_str.split("-")])
        except (ValueError, AttributeError):
            logger.warning(f"Invalid date format: {date_str}, using current date")
            from datetime import datetime

            return datetime.now().strftime("%-m-%-d-%Y")

    def _draw_text_at_position(
        self,
        painter: QPainter,
        image: QImage,
        text: str,
        font: QFont,
        margin: int,
        position: str,
        text_width: int = None,
    ) -> None:
        """
        Draw text at the specified position using exact legacy positioning.

        Args:
            painter: QPainter to draw with
            image: Target image
            text: Text to draw
            font: Font to use
            margin: Margin value
            position: Position identifier ("bottom-left", "bottom-center", "bottom-right")
            text_width: Pre-calculated text width (optional)
        """
        if not text:
            return

        painter.setFont(font)

        if text_width is None:
            metrics = QFontMetrics(font)
            text_width = metrics.horizontalAdvance(text)

        # EXACT LEGACY POSITIONING - use original margin calculation
        if position == "bottom-left":
            x = margin + self.border_width
            y = image.height() - margin - self.border_width
        elif position == "bottom-center":
            x = (image.width() - text_width) // 2
            y = image.height() - margin - self.border_width
        elif position == "bottom-right":
            x = image.width() - text_width - margin - self.border_width
            y = image.height() - margin - self.border_width
        else:
            logger.warning(f"Unknown position: {position}")
            return

        painter.setPen(QPen(Qt.GlobalColor.black))
        painter.drawText(x, y, text)

    def _calculate_text_dimensions(self, text: str, font: QFont) -> tuple[int, int]:
        """
        Calculate text dimensions for the given font.

        Args:
            text: Text to measure
            font: Font to use for measurement

        Returns:
            Tuple of (width, height)
        """
        metrics = QFontMetrics(font)
        width = metrics.horizontalAdvance(text)
        height = metrics.height()
        return width, height
