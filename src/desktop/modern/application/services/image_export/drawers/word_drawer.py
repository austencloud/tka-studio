"""
Word Drawer - Legacy-Compatible Word Text Rendering
==================================================

Renders word text onto exported images using exact legacy font scaling logic
to prevent "humongous" text issues and ensure consistent visual output.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontMetrics, QImage, QPainter, QPen

from desktop.modern.core.interfaces.image_export_services import (
    ImageExportOptions,
    IWordDrawer,
)


if TYPE_CHECKING:
    from .font_margin_helper import FontMarginHelper

logger = logging.getLogger(__name__)


class WordDrawer(IWordDrawer):
    """
    Drawer for rendering word text with legacy-compatible font scaling.

    This drawer replicates the exact word rendering logic from the Legacy system,
    including font scaling based on sequence length and kerning adjustments.
    """

    def __init__(self, font_margin_helper: FontMarginHelper):
        """
        Initialize the word drawer.

        Args:
            font_margin_helper: Helper for font and margin calculations
        """
        self.font_margin_helper = font_margin_helper

        # Legacy-compatible base font settings
        self.base_font = QFont("Georgia", 175, QFont.Weight.DemiBold, False)
        self.base_margin = 50
        self.border_width = 3

        logger.debug("WordDrawer initialized with legacy-compatible settings")

    def draw_word(
        self,
        image: QImage,
        word: str,
        num_filled_beats: int,
        options: ImageExportOptions,
    ) -> None:
        """
        Draw word text onto the image using legacy scaling logic.

        Args:
            image: Target image
            word: Word to draw
            num_filled_beats: Number of beats in sequence (affects font size)
            options: Export options
        """
        if not word:
            logger.debug("No word to draw")
            return

        logger.debug(f"Drawing word: '{word}' for {num_filled_beats} beats")

        # Calculate beat scale based on beat size
        beat_size = getattr(options, "beat_size", 280)
        beat_scale = self.font_margin_helper.calculate_beat_scale(beat_size)

        # Apply legacy font and margin adjustment
        font, margin = self.font_margin_helper.adjust_font_and_margin(
            self.base_font, num_filled_beats, self.base_margin, beat_scale
        )

        # Adjust kerning with beat scale
        kerning = int(20 * beat_scale)

        # Set up painter
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setFont(font)

        # Calculate text dimensions
        metrics = QFontMetrics(font)
        text_width = metrics.horizontalAdvance(word)
        text_height = metrics.ascent()

        # Adjust font size if text is too wide (legacy behavior)
        while text_width + 2 * margin > image.width() - (image.width() // 4):
            font_size = font.pointSize() - 1
            if font_size <= 10:
                logger.warning(f"Word '{word}' font size reduced to minimum (10)")
                break
            font = QFont(font.family(), font_size, font.weight(), font.italic())
            painter.setFont(font)
            metrics = QFontMetrics(font)
            text_width = metrics.horizontalAdvance(word)
            text_height = metrics.ascent()

        # Calculate position using legacy positioning logic
        y = (
            (options.additional_height_top // 2 + text_height // 2)
            - (text_height // 10)
            + self.border_width
        )
        x = (image.width() - text_width - kerning * (len(word) - 1)) // 2

        # Draw each letter with kerning (legacy behavior)
        painter.setPen(QPen(Qt.GlobalColor.black))
        for letter in word:
            painter.drawText(x, y, letter)
            x += metrics.horizontalAdvance(letter) + kerning

        painter.end()
        logger.debug(f"Word '{word}' drawn successfully")

    def _calculate_text_position(
        self,
        image: QImage,
        text_width: int,
        text_height: int,
        margin: int,
        kerning: int,
        word_length: int,
        additional_height_top: int,
    ) -> tuple[int, int]:
        """
        Calculate text position using legacy logic.

        Args:
            image: Target image
            text_width: Width of the text
            text_height: Height of the text
            margin: Margin value
            kerning: Kerning value
            word_length: Length of the word
            additional_height_top: Additional height at top

        Returns:
            Tuple of (x, y) position
        """
        # Legacy Y positioning
        y = (
            (additional_height_top // 2 + text_height // 2)
            - (text_height // 10)
            + self.border_width
        )

        # Legacy X positioning (centered with kerning)
        x = (image.width() - text_width - kerning * (word_length - 1)) // 2

        return x, y

    def _draw_text_with_kerning(
        self,
        painter: QPainter,
        word: str,
        start_x: int,
        y: int,
        metrics: QFontMetrics,
        kerning: int,
    ) -> None:
        """
        Draw text with legacy kerning behavior.

        Args:
            painter: QPainter to draw with
            word: Word to draw
            start_x: Starting X position
            y: Y position
            metrics: Font metrics for character width calculation
            kerning: Kerning value between characters
        """
        x = start_x
        painter.setPen(QPen(Qt.GlobalColor.black))

        for letter in word:
            painter.drawText(x, y, letter)
            x += metrics.horizontalAdvance(letter) + kerning
