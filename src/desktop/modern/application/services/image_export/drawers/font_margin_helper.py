"""
Font Margin Helper - Legacy-Compatible Font and Margin Calculations
==================================================================

Provides exact legacy font and margin calculations to prevent "humongous" text issues
and ensure consistent sizing across different sequence lengths.
"""

from __future__ import annotations

import logging

from PyQt6.QtGui import QFont

from desktop.modern.core.interfaces.image_export_services import IFontMarginHelper


logger = logging.getLogger(__name__)


class FontMarginHelper(IFontMarginHelper):
    """
    Helper class for font and margin calculations using exact legacy logic.

    This class replicates the exact font scaling logic from the Legacy system
    to prevent font sizing regressions and ensure consistent visual output.
    """

    def __init__(self):
        """Initialize the font margin helper."""
        logger.debug("FontMarginHelper initialized")

    def adjust_font_and_margin(
        self,
        base_font: QFont,
        num_filled_beats: int,
        base_margin: int,
        beat_scale: float = 1.0,
    ) -> tuple[QFont, int]:
        """
        Adjust font and margin based on number of beats - EXACT LEGACY LOGIC.

        This method replicates the exact calculations from the Legacy system
        to prevent "humongous" text issues for small sequences.

        Args:
            base_font: Base font to adjust
            num_filled_beats: Number of beats in sequence
            base_margin: Base margin to adjust
            beat_scale: Scale factor to apply

        Returns:
            Tuple of (adjusted_font, adjusted_margin)
        """
        # Get the base font size, ensuring it's at least 1
        base_font_size = max(1, base_font.pointSize())

        # EXACT LEGACY LOGIC - do not modify these calculations
        if num_filled_beats <= 1:
            font_size = max(1, int(base_font_size / 2.3))
            margin = max(1, base_margin // 3)
        elif num_filled_beats == 2:
            font_size = max(1, int(base_font_size / 1.5))
            margin = max(1, base_margin // 2)
        else:
            font_size = base_font_size
            margin = base_margin

        # Ensure the scaled font size is at least 1
        scaled_font_size = max(1, int(font_size * beat_scale))

        # Create adjusted font with same properties as base font
        adjusted_font = QFont(
            base_font.family(),
            scaled_font_size,
            base_font.weight(),
            base_font.italic(),
        )

        # Scale margin with beat scale
        scaled_margin = max(1, int(margin * beat_scale))

        logger.debug(
            f"Font adjusted: {base_font_size} -> {scaled_font_size} "
            f"(beats: {num_filled_beats}, scale: {beat_scale})"
        )
        logger.debug(
            f"Margin adjusted: {base_margin} -> {scaled_margin} "
            f"(beats: {num_filled_beats}, scale: {beat_scale})"
        )

        return adjusted_font, scaled_margin

    def calculate_beat_scale(self, beat_size: int, reference_size: int = 280) -> float:
        """
        Calculate beat scale factor based on beat size.

        Args:
            beat_size: Actual beat size in pixels
            reference_size: Reference beat size for scaling (default: 280)

        Returns:
            Scale factor for fonts and elements
        """
        if reference_size <= 0:
            logger.warning(
                f"Invalid reference size: {reference_size}, using default 280"
            )
            reference_size = 280

        beat_scale = beat_size / reference_size

        logger.debug(
            f"Beat scale calculated: {beat_scale} (size: {beat_size}, ref: {reference_size})"
        )

        return beat_scale

    @staticmethod
    def get_legacy_font_sizes() -> dict:
        """
        Get the standard legacy font sizes for different text elements.

        Returns:
            Dictionary of font sizes for different elements
        """
        return {
            "word": 175,  # Base word font size
            "user_info_bold": 50,  # User info bold font size
            "user_info_normal": 50,  # User info normal font size
            "beat_number": 12,  # Beat number overlay font size
            "difficulty": None,  # Difficulty font size is calculated dynamically
        }

    @staticmethod
    def get_legacy_margins() -> dict:
        """
        Get the standard legacy margin values.

        Returns:
            Dictionary of margin values for different elements
        """
        return {
            "base": 50,  # Base margin
            "border": 3,  # Border width
            "kerning": 20,  # Letter spacing for word text
        }
